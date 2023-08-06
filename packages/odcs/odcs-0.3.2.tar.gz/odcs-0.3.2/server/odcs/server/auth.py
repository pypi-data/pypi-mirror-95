# -*- coding: utf-8 -*-
# Copyright (c) 2017  Red Hat, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Written by Chenxiong Qi <cqi@redhat.com>


from functools import wraps
import requests
import ldap
import flask

from itertools import chain

from flask import g
from flask_login import login_required as _login_required

from werkzeug.exceptions import Unauthorized
from odcs.server import conf, log
from odcs.server.errors import Forbidden
from odcs.server.models import User
from odcs.server.models import commit_on_success


def _validate_kerberos_config():
    """
    Validates the kerberos configuration and raises ValueError in case of
    error.
    """
    errors = []
    if not conf.auth_ldap_server:
        errors.append(
            "kerberos authentication enabled with no LDAP server configured, "
            "check AUTH_LDAP_SERVER in your config."
        )

    if not conf.auth_ldap_group_base:
        errors.append(
            "kerberos authentication enabled with no LDAP group base configured, "
            "check AUTH_LDAP_GROUP_BASE in your config."
        )

    if errors:
        for error in errors:
            log.exception(error)
        raise ValueError("Invalid configuration for kerberos authentication.")


@commit_on_success
def load_krb_user_from_request(request):
    """Load Kerberos user from current request

    REMOTE_USER needs to be set in environment variable, that is set by
    frontend Apache authentication module.
    """
    remote_user = request.environ.get("REMOTE_USER")
    if not remote_user:
        raise Unauthorized("REMOTE_USER is not present in request.")

    username, realm = remote_user.split("@")

    user = User.find_user_by_name(username)
    if not user:
        user = User.create_user(username=username)

    try:
        groups = query_ldap_groups(username)
    except ldap.SERVER_DOWN as e:
        log.error(
            "Cannot query groups of %s from LDAP. Error: %s",
            username,
            e.args[0]["desc"],
        )
        groups = []

    g.groups = groups
    g.user = user
    return user


@commit_on_success
def load_ssl_user_from_request(request):
    """
    Loads SSL user from current request.

    SSL_CLIENT_VERIFY and SSL_CLIENT_S_DN needs to be set in
    request.environ. This is set by frontend httpd mod_ssl module.
    """
    ssl_client_verify = request.environ.get("SSL_CLIENT_VERIFY")
    if ssl_client_verify != "SUCCESS":
        raise Unauthorized("Cannot verify client: %s" % ssl_client_verify)

    username = request.environ.get("SSL_CLIENT_S_DN")
    if not username:
        raise Unauthorized(
            "Unable to get user information (DN) from client certificate"
        )

    user = User.find_user_by_name(username)
    if not user:
        user = User.create_user(username=username)

    g.groups = []
    g.user = user
    return user


def load_krb_or_ssl_user_from_request(request):
    """
    Loads User using Kerberos or SSL auth.
    """
    if request.environ.get("REMOTE_USER"):
        return load_krb_user_from_request(request)
    else:
        return load_ssl_user_from_request(request)


def query_ldap_groups(uid):
    client = ldap.initialize(conf.auth_ldap_server)
    groups = client.search_s(
        conf.auth_ldap_group_base,
        ldap.SCOPE_ONELEVEL,
        attrlist=["cn", "gidNumber"],
        filterstr="memberUid={0}".format(uid),
    )

    group_names = list(chain(*[info["cn"] for _, info in groups]))
    return group_names


@commit_on_success
def load_openidc_user(request):
    """Load FAS user from current request"""
    username = request.environ.get("REMOTE_USER")
    if not username:
        raise Unauthorized("REMOTE_USER is not present in request.")

    token = request.environ.get("OIDC_access_token")
    if not token:
        raise Unauthorized("Missing token passed to ODCS.")

    scope = request.environ.get("OIDC_CLAIM_scope")
    if not scope:
        raise Unauthorized("Missing OIDC_CLAIM_scope.")
    validate_scopes(scope)

    user_info = get_user_info(token)

    user = User.find_user_by_name(username)
    if not user:
        user = User.create_user(username=username)

    g.groups = user_info.get("groups", [])
    g.user = user
    g.oidc_scopes = scope.split(" ")
    return user


def validate_scopes(scope):
    """Validate if request scopes are all in required scope

    :param str scope: scope passed in from.
    :raises: Unauthorized if any of required scopes is not present.
    """
    scopes = scope.split(" ")
    required_scopes = conf.auth_openidc_required_scopes
    for scope in required_scopes:
        if scope not in scopes:
            raise Unauthorized("Required OIDC scope {0} not present.".format(scope))


def require_oidc_scope(scope):
    """Check if required scopes is in OIDC scopes within request"""
    full_scope = "{0}{1}".format(conf.oidc_base_namespace, scope)
    if conf.auth_backend == "openidc" and full_scope not in g.oidc_scopes:
        message = "Request does not have required scope %s" % scope
        log.error(message)
        raise Forbidden(message)


def require_scopes(*scopes):
    """Check if required scopes is in OIDC scopes within request"""

    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            if conf.auth_backend != "noauth":
                for scope in scopes:
                    require_oidc_scope(scope)
            return f(*args, **kwargs)

        return decorator

    return wrapper


def get_user_info(token):
    """Query FAS groups from Fedora"""
    headers = {"authorization": "Bearer {0}".format(token)}
    r = requests.get(
        conf.auth_openidc_userinfo_uri, headers=headers, timeout=conf.net_timeout
    )
    if r.status_code != 200:
        # In Fedora, the manually created service tokens can't be used with the UserInfo
        # endpoint. We treat this as an empty response - and hence an empty group list. An empty
        # group list only makes our authorization checks more strict, so it should be safe
        # to proceed and check the user.
        log.warning(
            "Failed to query group information - UserInfo endpoint failed with status=%d",
            r.status_code,
        )
        return {}

    return r.json()


def init_auth(login_manager, backend):
    """Initialize authentication backend

    Enable and initialize authentication backend to work with frontend
    authentication module running in Apache.
    """
    if backend == "noauth":
        # Do not enable any authentication backend working with frontend
        # authentication module in Apache.
        log.warning("Authorization is disabled in ODCS configuration.")
        return
    if backend == "kerberos":
        _validate_kerberos_config()
        global load_krb_user_from_request
        load_krb_user_from_request = login_manager.request_loader(
            load_krb_user_from_request
        )
    elif backend == "openidc":
        global load_openidc_user
        load_openidc_user = login_manager.request_loader(load_openidc_user)
    elif backend == "kerberos_or_ssl":
        _validate_kerberos_config()
        global load_krb_or_ssl_user_from_request
        load_krb_or_ssl_user_from_request = login_manager.request_loader(
            load_krb_or_ssl_user_from_request
        )
    elif backend == "ssl":
        global load_ssl_user_from_request
        load_ssl_user_from_request = login_manager.request_loader(
            load_ssl_user_from_request
        )
    else:
        raise ValueError("Unknown backend name {0}.".format(backend))


def has_role(role):
    """Check if current user has given role. With noauth all users have all
    roles.

    :returns: bool
    """
    if conf.auth_backend == "noauth":
        return True

    groups = []
    for group in getattr(conf, role).get("groups", []):
        groups.append(group)

    users = []
    for user in getattr(conf, role).get("users", []):
        users.append(user)

    in_groups = bool(set(flask.g.groups) & set(groups))
    in_users = flask.g.user.username in users
    if in_groups or in_users:
        return True
    return False


def requires_role(role):
    """Check if user is in the configured role.

    :param str role: role name, supported roles: 'allowed_clients', 'admins'.
    """
    valid_roles = ["allowed_clients", "admins"]
    if role not in valid_roles:
        raise ValueError(
            "Unknown role <%s> specified, supported roles: %s."
            % (role, str(valid_roles))
        )

    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if has_role(role):
                return f(*args, **kwargs)

            msg = "User %s is not in role %s." % (flask.g.user.username, role)
            log.error(msg)
            raise Forbidden(msg)

        return wrapped

    return wrapper


def login_required(f):
    """Wrapper of flask_login's login_required to ingore auth check when auth backend is 'noauth'."""

    @wraps(f)
    def wrapped(*args, **kwargs):
        if conf.auth_backend == "noauth":
            return f(*args, **kwargs)
        return _login_required(f)(*args, **kwargs)

    return wrapped
