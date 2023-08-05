# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# CESNET-OpenID-Remote is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""CESNET OIDC Auth backend for OARepo"""
from urllib.parse import urlparse, parse_qs

from flask import current_app
from invenio_accounts.proxies import current_datastore
from werkzeug.local import LocalProxy

CESNET_OPENID_REMOTE_GROUP_PREFIX = 'urn:geant:cesnet.cz:'
"""Default prefix of group attribute URIs."""

CESNET_OPENID_REMOTE_GROUP_AUTHORITY = 'perun.cesnet.cz'
"""Default authority that issues the group attribute URIs."""

gconf = LocalProxy(
    lambda: dict(
        prefix=current_app.config.get(
            "CESNET_OPENID_REMOTE_GROUP_PREFIX",
            CESNET_OPENID_REMOTE_GROUP_PREFIX),
        authority=current_app.config.get(
            "CESNET_OPENID_REMOTE_GROUP_AUTHORITY",
            CESNET_OPENID_REMOTE_GROUP_AUTHORITY)))


def validate_group_uri(group_uri):
    """Checks if group URI is well-formatted and valid.

       @param group_uri: group URI string
       @returns: True if group URI is valid, False otherwise
    """
    if not group_uri.startswith(gconf['prefix']) or not group_uri.endswith(f'#{gconf["authority"]}'):
        return False
    if 'groupAttributes:' not in group_uri:
        return False

    return True


def parse_group_uri(group_uri):
    """Parses UUID and any extra data from the group URI string.

        @param group_uri: group URI string
        @returns Tuple with (UUID, dict(extra_data)) specification of the group
    """
    attrs = group_uri[len(gconf['prefix']) + len('groupAttributes:'):-(len(gconf['authority']) + 1)]
    parsed_url = urlparse(attrs)
    qs = parse_qs(parsed_url.query)
    if 'displayName' in qs:
        qs['displayName'] = qs['displayName'][0]
    return parsed_url.path, qs


def add_user_role_from_group(user, group_uuid, extra_data):
    """Creates role from the external group (when necessary) and adds user to it.

        @param user: e-mail of the user
        @param group_uuid: UUID of the external group
        @param extra_data: any additional data for role creation
        @returns True if user is added to role, False otherwise
    """
    user, role = current_datastore._prepare_role_modify_args(user, group_uuid)
    if user is None:
        current_app.logger.error(f'Cannot assign role {group_uuid} to empty user')
        return False
    if role is None:
        role_kwargs = dict(name=group_uuid)
        if 'displayName' in extra_data:
            role_kwargs['description'] = extra_data.pop('displayName')
        if not current_datastore.create_role(**role_kwargs):
            current_app.logger.error(f'Failed to create role {role_kwargs}')
            return False

    if not current_datastore.add_role_to_user(user, group_uuid):
        current_app.logger.error(f'Failed to add {user} to role {group_uuid}')
        return False

    return True


def disconnect_user_role(user, group_uuid):
    """Remove user from role linked with external group UUID.

        @param user: e-mail of the user
        @param group_uuid: UUID of the external group
        @returns True if user is removed from role, False otherwise
    """
    user, role = current_datastore._prepare_role_modify_args(user, group_uuid)
    if user is None:
        current_app.logger.error(f'Cannot remove role {group_uuid} from empty user')
        return False
    if role is None:
        current_app.logger.error(f'Cannot remove role {group_uuid} from user {user}. Role does not exist')
        return False

    if not current_datastore.remove_role_from_user(user, group_uuid):
        current_app.logger.error(f'Failed to remove {user} from role {group_uuid}')
        return False

    return True
