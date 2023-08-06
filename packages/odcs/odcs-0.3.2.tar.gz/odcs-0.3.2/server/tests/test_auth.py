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


import flask
import unittest

from mock import patch, Mock

import odcs.server.auth

from werkzeug.exceptions import Unauthorized
from odcs.server.auth import init_auth
from odcs.server.auth import load_krb_user_from_request
from odcs.server.auth import load_openidc_user
from odcs.server.auth import query_ldap_groups
from odcs.server.auth import require_scopes
from odcs.server.auth import load_krb_or_ssl_user_from_request
from odcs.server.auth import load_ssl_user_from_request
from odcs.server.errors import Forbidden
from odcs.server import app, conf, db
from odcs.server.models import User
from .utils import ModelsBaseTest


class TestLoadSSLUserFromRequest(ModelsBaseTest):
    def setUp(self):
        super(TestLoadSSLUserFromRequest, self).setUp()

        self.user = User(username="CN=tester1,L=prod,DC=example,DC=com")
        db.session.add(self.user)
        db.session.commit()

    def test_create_new_user(self):
        environ_base = {
            "SSL_CLIENT_VERIFY": "SUCCESS",
            "SSL_CLIENT_S_DN": "CN=client,L=prod,DC=example,DC=com",
        }

        with app.test_request_context(environ_base=environ_base):
            load_ssl_user_from_request(flask.request)

            expected_user = db.session.query(User).filter(
                User.username == "CN=client,L=prod,DC=example,DC=com"
            )[0]

            self.assertEqual(expected_user.id, flask.g.user.id)
            self.assertEqual(expected_user.username, flask.g.user.username)

            # Ensure user's groups are set to empty list
            self.assertEqual(0, len(flask.g.groups))

    def test_return_existing_user(self):
        environ_base = {
            "SSL_CLIENT_VERIFY": "SUCCESS",
            "SSL_CLIENT_S_DN": self.user.username,
        }

        with app.test_request_context(environ_base=environ_base):
            load_ssl_user_from_request(flask.request)

            self.assertEqual(self.user.id, flask.g.user.id)
            self.assertEqual(self.user.username, flask.g.user.username)

            # Ensure user's groups are set to empty list
            self.assertEqual(0, len(flask.g.groups))

    def test_401_if_ssl_client_verify_not_success(self):
        environ_base = {
            "SSL_CLIENT_VERIFY": "GENEROUS",
            "SSL_CLIENT_S_DN": self.user.username,
        }

        with app.test_request_context(environ_base=environ_base):
            with self.assertRaises(Unauthorized) as ctx:
                load_ssl_user_from_request(flask.request)
            self.assertIn("Cannot verify client: GENEROUS", ctx.exception.description)

    def test_401_if_cn_not_set(self):
        environ_base = {
            "SSL_CLIENT_VERIFY": "SUCCESS",
        }

        with app.test_request_context(environ_base=environ_base):
            with self.assertRaises(Unauthorized) as ctx:
                load_ssl_user_from_request(flask.request)
            self.assertIn(
                "Unable to get user information (DN) from client certificate",
                ctx.exception.description,
            )


class TestLoadKrbOrSSLUserFromRequest(unittest.TestCase):
    @patch("odcs.server.auth.load_ssl_user_from_request")
    @patch("odcs.server.auth.load_krb_user_from_request")
    def test_load_krb_or_ssl_user_from_request_remote_user(
        self, load_krb_user, load_ssl_user
    ):
        load_krb_user.return_value = "krb_user"
        load_ssl_user.return_value = "ssl_user"

        environ_base = {"REMOTE_USER": "newuser@EXAMPLE.COM"}

        with app.test_request_context(environ_base=environ_base):
            user = load_krb_or_ssl_user_from_request(flask.request)
            self.assertEqual(user, "krb_user")

    @patch("odcs.server.auth.load_ssl_user_from_request")
    @patch("odcs.server.auth.load_krb_user_from_request")
    def test_load_krb_or_ssl_user_from_request_ssl_client(
        self, load_krb_user, load_ssl_user
    ):
        load_krb_user.return_value = "krb_user"
        load_ssl_user.return_value = "ssl_user"

        environ_base = {
            "SSL_CLIENT_VERIFY": "SUCCESS",
            "SSL_CLIENT_S_DN": "ssl_user",
        }

        with app.test_request_context(environ_base=environ_base):
            user = load_krb_or_ssl_user_from_request(flask.request)
            self.assertEqual(user, "ssl_user")


class TestLoadKrbUserFromRequest(ModelsBaseTest):
    def setUp(self):
        super(TestLoadKrbUserFromRequest, self).setUp()

        self.user = User(username="tester1")
        db.session.add(self.user)
        db.session.commit()

    @patch("odcs.server.auth.query_ldap_groups")
    def test_create_new_user(self, query_ldap_groups):
        query_ldap_groups.return_value = ["devel", "admins"]

        environ_base = {"REMOTE_USER": "newuser@EXAMPLE.COM"}

        with app.test_request_context(environ_base=environ_base):
            load_krb_user_from_request(flask.request)

            expected_user = db.session.query(User).filter(User.username == "newuser")[0]

            self.assertEqual(expected_user.id, flask.g.user.id)
            self.assertEqual(expected_user.username, flask.g.user.username)

            # Ensure user's groups are created
            self.assertEqual(2, len(flask.g.groups))
            self.assertEqual(["admins", "devel"], sorted(flask.g.groups))

    @patch("odcs.server.auth.query_ldap_groups")
    def test_return_existing_user(self, query_ldap_groups):
        query_ldap_groups.return_value = ["devel", "admins"]
        original_users_count = db.session.query(User.id).count()

        environ_base = {"REMOTE_USER": "{0}@EXAMPLE.COM".format(self.user.username)}

        with app.test_request_context(environ_base=environ_base):
            load_krb_user_from_request(flask.request)

            self.assertEqual(original_users_count, db.session.query(User.id).count())
            self.assertEqual(self.user.id, flask.g.user.id)
            self.assertEqual(self.user.username, flask.g.user.username)
            self.assertEqual(["admins", "devel"], sorted(flask.g.groups))

    def test_401_if_remote_user_not_present(self):
        with app.test_request_context():
            with self.assertRaises(Unauthorized) as ctx:
                load_krb_user_from_request(flask.request)
            self.assertIn(
                "REMOTE_USER is not present in request.", ctx.exception.description
            )


class TestLoadOpenIDCUserFromRequest(ModelsBaseTest):
    def setUp(self):
        super(TestLoadOpenIDCUserFromRequest, self).setUp()

        self.user = User(username="tester1")
        db.session.add(self.user)
        db.session.commit()

    @patch("odcs.server.auth.requests.get")
    def test_create_new_user(self, get):
        get.return_value.status_code = 200
        get.return_value.json.return_value = {
            "groups": ["tester", "admin"],
            "name": "new_user",
        }

        environ_base = {
            "REMOTE_USER": "new_user",
            "OIDC_access_token": "39283",
            "OIDC_CLAIM_iss": "https://iddev.fedorainfracloud.org/openidc/",
            "OIDC_CLAIM_scope": "openid https://id.fedoraproject.org/scope/groups "
            "https://pagure.io/odcs/new-compose "
            "https://pagure.io/odcs/renew-compose "
            "https://pagure.io/odcs/delete-compose",
        }

        with app.test_request_context(environ_base=environ_base):
            load_openidc_user(flask.request)

            new_user = db.session.query(User).filter(User.username == "new_user")[0]

            self.assertEqual(new_user, flask.g.user)
            self.assertEqual("new_user", flask.g.user.username)
            self.assertEqual(sorted(["admin", "tester"]), sorted(flask.g.groups))

    @patch("odcs.server.auth.requests.get")
    def test_return_existing_user(self, get):
        get.return_value.status_code = 200
        get.return_value.json.return_value = {
            "groups": ["testers", "admins"],
            "name": self.user.username,
        }

        environ_base = {
            "REMOTE_USER": self.user.username,
            "OIDC_access_token": "39283",
            "OIDC_CLAIM_iss": "https://iddev.fedorainfracloud.org/openidc/",
            "OIDC_CLAIM_scope": "openid https://id.fedoraproject.org/scope/groups "
            "https://pagure.io/odcs/new-compose "
            "https://pagure.io/odcs/renew-compose "
            "https://pagure.io/odcs/delete-compose",
        }

        with app.test_request_context(environ_base=environ_base):
            original_users_count = db.session.query(User.id).count()

            load_openidc_user(flask.request)

            users_count = db.session.query(User.id).count()
            self.assertEqual(original_users_count, users_count)

            # Ensure existing user is set in g
            self.assertEqual(self.user.id, flask.g.user.id)
            self.assertEqual(["admins", "testers"], sorted(flask.g.groups))

    @patch("odcs.server.auth.requests.get")
    def test_user_info_failure(self, get):
        # If the user_info endpoint errors out, we continue to authenticate
        # based only on the user (which we have from the token), ignoring groups.
        get.return_value.status_code = 400

        environ_base = {
            "REMOTE_USER": self.user.username,
            "OIDC_access_token": "39283",
            "OIDC_CLAIM_iss": "https://iddev.fedorainfracloud.org/openidc/",
            "OIDC_CLAIM_scope": "openid https://id.fedoraproject.org/scope/groups "
            "https://pagure.io/odcs/new-compose "
            "https://pagure.io/odcs/renew-compose "
            "https://pagure.io/odcs/delete-compose",
        }

        with app.test_request_context(environ_base=environ_base):
            load_openidc_user(flask.request)

            self.assertEqual(self.user.id, flask.g.user.id)
            self.assertEqual([], sorted(flask.g.groups))

    def test_401_if_remote_user_not_present(self):
        environ_base = {
            # Missing REMOTE_USER here
            "OIDC_access_token": "39283",
            "OIDC_CLAIM_iss": "https://iddev.fedorainfracloud.org/openidc/",
            "OIDC_CLAIM_scope": "openid https://id.fedoraproject.org/scope/groups",
        }
        with app.test_request_context(environ_base=environ_base):
            self.assertRaises(Unauthorized, load_openidc_user, flask.request)

    def test_401_if_access_token_not_present(self):
        environ_base = {
            "REMOTE_USER": "tester1",
            # Missing OIDC_access_token here
            "OIDC_CLAIM_iss": "https://iddev.fedorainfracloud.org/openidc/",
            "OIDC_CLAIM_scope": "openid https://id.fedoraproject.org/scope/groups",
        }
        with app.test_request_context(environ_base=environ_base):
            self.assertRaises(Unauthorized, load_openidc_user, flask.request)

    def test_401_if_scope_not_present(self):
        environ_base = {
            "REMOTE_USER": "tester1",
            "OIDC_access_token": "39283",
            "OIDC_CLAIM_iss": "https://iddev.fedorainfracloud.org/openidc/",
            # Missing OIDC_CLAIM_scope here
        }
        with app.test_request_context(environ_base=environ_base):
            self.assertRaises(Unauthorized, load_openidc_user, flask.request)

    def test_401_if_required_scope_not_present_in_token_scope(self):
        environ_base = {
            "REMOTE_USER": "new_user",
            "OIDC_access_token": "39283",
            "OIDC_CLAIM_iss": "https://iddev.fedorainfracloud.org/openidc/",
            "OIDC_CLAIM_scope": "openid https://id.fedoraproject.org/scope/groups",
        }

        with patch.object(
            odcs.server.auth.conf, "auth_openidc_required_scopes", ["new-compose"]
        ):
            with app.test_request_context(environ_base=environ_base):
                with self.assertRaises(Unauthorized) as ctx:
                    load_openidc_user(flask.request)
                self.assertIn(
                    "Required OIDC scope new-compose not present.",
                    ctx.exception.description,
                )


class TestQueryLdapGroups(unittest.TestCase):
    """Test auth.query_ldap_groups"""

    @patch("odcs.server.auth.ldap.initialize")
    def test_get_groups(self, initialize):
        initialize.return_value.search_s.return_value = [
            (
                "cn=odcsdev,ou=Groups,dc=example,dc=com",
                {"gidNumber": ["5523"], "cn": ["odcsdev"]},
            ),
            (
                "cn=freshmakerdev,ou=Groups,dc=example,dc=com",
                {"gidNumber": ["17861"], "cn": ["freshmakerdev"]},
            ),
            (
                "cn=devel,ou=Groups,dc=example,dc=com",
                {"gidNumber": ["5781"], "cn": ["devel"]},
            ),
        ]

        groups = query_ldap_groups("me")
        self.assertEqual(sorted(["odcsdev", "freshmakerdev", "devel"]), sorted(groups))


class TestInitAuth(unittest.TestCase):
    """Test init_auth"""

    def setUp(self):
        self.login_manager = Mock()

    def test_select_kerberos_auth_backend(self):
        init_auth(self.login_manager, "kerberos")
        self.login_manager.request_loader.assert_called_once_with(
            load_krb_user_from_request
        )

    def test_select_openidc_auth_backend(self):
        init_auth(self.login_manager, "openidc")
        self.login_manager.request_loader.assert_called_once_with(load_openidc_user)

    def test_select_ssl_auth_backend(self):
        init_auth(self.login_manager, "ssl")
        self.login_manager.request_loader.assert_called_once_with(
            load_ssl_user_from_request
        )

    def test_select_kerberos_or_ssl_auth_backend(self):
        init_auth(self.login_manager, "kerberos_or_ssl")
        self.login_manager.request_loader.assert_called_once_with(
            load_krb_or_ssl_user_from_request
        )

    def test_not_use_auth_backend(self):
        init_auth(self.login_manager, "noauth")
        self.login_manager.request_loader.assert_not_called()

    def test_error_if_select_an_unknown_backend(self):
        self.assertRaises(ValueError, init_auth, self.login_manager, "xxx")
        self.assertRaises(ValueError, init_auth, self.login_manager, "")
        self.assertRaises(ValueError, init_auth, self.login_manager, None)

    def test_init_auth_no_ldap_server(self):
        with patch.object(odcs.server.auth.conf, "auth_ldap_server", ""):
            self.assertRaises(ValueError, init_auth, self.login_manager, "kerberos")

    def test_init_auths_no_ldap_group_base(self):
        with patch.object(odcs.server.auth.conf, "auth_ldap_group_base", ""):
            self.assertRaises(ValueError, init_auth, self.login_manager, "kerberos")


class TestDecoratorRequireScopes(unittest.TestCase):
    """Test decorator require_scopes"""

    @patch.object(conf, "oidc_base_namespace", new="http://example.com/")
    @patch.object(conf, "auth_backend", new="openidc")
    def test_function_is_called(self):
        with app.test_request_context():
            flask.g.oidc_scopes = ["http://example.com/renew-compose"]

            mock_func = Mock()
            mock_func.__name__ = "real_function"
            decorated_func = require_scopes("renew-compose")(mock_func)
            decorated_func(1, 2, 3)

        mock_func.assert_called_once_with(1, 2, 3)

    @patch.object(conf, "oidc_base_namespace", new="http://example.com/")
    @patch.object(conf, "auth_backend", new="openidc")
    def test_function_is_not_called_if_scope_is_not_present(self):
        with app.test_request_context():
            flask.g.oidc_scopes = [
                "http://example.com/new-compose",
                "http://example.com/renew-compose",
            ]

            mock_func = Mock()
            mock_func.__name__ = "real_function"
            decorated_func = require_scopes("delete-compose")(mock_func)
            self.assertRaises(Forbidden, decorated_func, 1, 2, 3)

    @patch.object(conf, "oidc_base_namespace", new="http://example.com/")
    @patch.object(conf, "auth_backend", new="kerberos")
    def test_function_is_called_for_non_openidc_backend(self):
        with app.test_request_context():
            flask.g.oidc_scopes = [
                "http://example.com/new-compose",
                "http://example.com/renew-compose",
            ]

            mock_func = Mock()
            mock_func.__name__ = "real_function"
            decorated_func = require_scopes("delete-compose")(mock_func)
            decorated_func(1, 2, 3)
            mock_func.assert_called_once_with(1, 2, 3)
