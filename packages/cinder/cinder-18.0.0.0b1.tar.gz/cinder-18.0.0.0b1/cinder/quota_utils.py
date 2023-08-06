# Copyright 2013 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from keystoneauth1 import identity
from keystoneauth1 import loading as ka_loading
from keystoneclient import client
from oslo_config import cfg
from oslo_log import log as logging

from cinder import exception

CONF = cfg.CONF
CONF.import_group('keystone_authtoken',
                  'keystonemiddleware.auth_token.__init__')

LOG = logging.getLogger(__name__)


class GenericProjectInfo(object):
    """Abstraction layer for Keystone V2 and V3 project objects"""
    def __init__(self, project_id, project_keystone_api_version,
                 project_parent_id=None,
                 project_subtree=None,
                 project_parent_tree=None,
                 is_admin_project=False,
                 domain_id=None):
        self.id = project_id
        self.domain_id = domain_id
        self.keystone_api_version = project_keystone_api_version
        self.parent_id = project_parent_id
        self.subtree = project_subtree
        self.parents = project_parent_tree
        self.is_admin_project = is_admin_project


def get_volume_type_reservation(ctxt, volume, type_id,
                                reserve_vol_type_only=False):
    from cinder import quota
    QUOTAS = quota.QUOTAS
    # Reserve quotas for the given volume type
    try:
        reserve_opts = {'volumes': 1, 'gigabytes': volume['size']}
        QUOTAS.add_volume_type_opts(ctxt,
                                    reserve_opts,
                                    type_id)
        # If reserve_vol_type_only is True, just reserve volume_type quota,
        # not volume quota.
        if reserve_vol_type_only:
            reserve_opts.pop('volumes')
            reserve_opts.pop('gigabytes')
        # Note that usually the project_id on the volume will be the same as
        # the project_id in the context. But, if they are different then the
        # reservations must be recorded against the project_id that owns the
        # volume.
        project_id = volume['project_id']
        reservations = QUOTAS.reserve(ctxt,
                                      project_id=project_id,
                                      **reserve_opts)
    except exception.OverQuota as e:
        process_reserve_over_quota(ctxt, e,
                                   resource='volumes',
                                   size=volume.size)
    return reservations


def _filter_domain_id_from_parents(domain_id, tree):
    """Removes the domain_id from the tree if present"""
    new_tree = None
    if tree:
        parent, children = next(iter(tree.items()))
        # Don't add the domain id to the parents hierarchy
        if parent != domain_id:
            new_tree = {parent: _filter_domain_id_from_parents(domain_id,
                                                               children)}

    return new_tree


def get_project_hierarchy(context, project_id, subtree_as_ids=False,
                          parents_as_ids=False, is_admin_project=False):
    """A Helper method to get the project hierarchy.

    Along with hierarchical multitenancy in keystone API v3, projects can be
    hierarchically organized. Therefore, we need to know the project
    hierarchy, if any, in order to do default volume type operations properly.
    """
    keystone = _keystone_client(context)
    generic_project = GenericProjectInfo(project_id, keystone.version)
    if keystone.version == 'v3':
        project = keystone.projects.get(project_id,
                                        subtree_as_ids=subtree_as_ids,
                                        parents_as_ids=parents_as_ids)

        generic_project.parent_id = None
        generic_project.domain_id = project.domain_id
        if project.parent_id != project.domain_id:
            generic_project.parent_id = project.parent_id

        generic_project.subtree = (
            project.subtree if subtree_as_ids else None)

        generic_project.parents = None
        if parents_as_ids:
            generic_project.parents = _filter_domain_id_from_parents(
                project.domain_id, project.parents)

        generic_project.is_admin_project = is_admin_project

    return generic_project


def _keystone_client(context, version=(3, 0)):
    """Creates and returns an instance of a generic keystone client.

    :param context: The request context
    :param version: version of Keystone to request
    :return: keystoneclient.client.Client object
    """
    if context.system_scope is not None:
        auth_plugin = identity.Token(
            auth_url=CONF.keystone_authtoken.auth_url,
            token=context.auth_token,
            system_scope=context.system_scope
        )
    elif context.domain_id is not None:
        auth_plugin = identity.Token(
            auth_url=CONF.keystone_authtoken.auth_url,
            token=context.auth_token,
            domain_id=context.domain_id
        )
    elif context.project_id is not None:
        auth_plugin = identity.Token(
            auth_url=CONF.keystone_authtoken.auth_url,
            token=context.auth_token,
            project_id=context.project_id
        )
    else:
        # We're dealing with an unscoped token from keystone that doesn't
        # carry any authoritative power outside of the user simplify proving
        # they know their own password. This token isn't associated with any
        # authorization target (e.g., system, domain, or project).
        auth_plugin = context.get_auth_plugin()

    client_session = ka_loading.session.Session().load_from_options(
        auth=auth_plugin,
        insecure=CONF.keystone_authtoken.insecure,
        cacert=CONF.keystone_authtoken.cafile,
        key=CONF.keystone_authtoken.keyfile,
        cert=CONF.keystone_authtoken.certfile,
        split_loggers=CONF.service_user.split_loggers)
    return client.Client(auth_url=CONF.keystone_authtoken.auth_url,
                         session=client_session, version=version)


OVER_QUOTA_RESOURCE_EXCEPTIONS = {'snapshots': exception.SnapshotLimitExceeded,
                                  'backups': exception.BackupLimitExceeded,
                                  'volumes': exception.VolumeLimitExceeded,
                                  'groups': exception.GroupLimitExceeded}


def process_reserve_over_quota(context, over_quota_exception,
                               resource, size=None):
    """Handle OverQuota exception.

    Analyze OverQuota exception, and raise new exception related to
    resource type. If there are unexpected items in overs,
    UnexpectedOverQuota is raised.

    :param context: security context
    :param over_quota_exception: OverQuota exception
    :param resource: can be backups, snapshots, and volumes
    :param size: requested size in reservation
    """
    def _consumed(name):
        return (usages[name]['reserved'] + usages[name]['in_use'])

    overs = over_quota_exception.kwargs['overs']
    usages = over_quota_exception.kwargs['usages']
    quotas = over_quota_exception.kwargs['quotas']
    invalid_overs = []

    for over in overs:
        if 'gigabytes' in over:
            msg = ("Quota exceeded for %(s_pid)s, tried to create "
                   "%(s_size)dG %(s_resource)s (%(d_consumed)dG of "
                   "%(d_quota)dG already consumed).")
            LOG.warning(msg, {'s_pid': context.project_id,
                              's_size': size,
                              's_resource': resource[:-1],
                              'd_consumed': _consumed(over),
                              'd_quota': quotas[over]})
            if resource == 'backups':
                exc = exception.VolumeBackupSizeExceedsAvailableQuota
            else:
                exc = exception.VolumeSizeExceedsAvailableQuota
            raise exc(
                name=over,
                requested=size,
                consumed=_consumed(over),
                quota=quotas[over])
        if (resource in OVER_QUOTA_RESOURCE_EXCEPTIONS.keys() and
                resource in over):
            msg = ("Quota exceeded for %(s_pid)s, tried to create "
                   "%(s_resource)s (%(d_consumed)d %(s_resource)ss "
                   "already consumed).")
            LOG.warning(msg, {'s_pid': context.project_id,
                              'd_consumed': _consumed(over),
                              's_resource': resource[:-1]})
            raise OVER_QUOTA_RESOURCE_EXCEPTIONS[resource](
                allowed=quotas[over],
                name=over)
        invalid_overs.append(over)

    if invalid_overs:
        raise exception.UnexpectedOverQuota(name=', '.join(invalid_overs))
