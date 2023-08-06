#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Unit tests for :py:mod:`vial.blueprints.auth_api`.
"""


import sys
import unittest

import vial.const
import vial.test
import vial.db
from vial.test import VialTestCase
from vial.test.runner import TestRunnerMixin


_IS_NOSE = sys.argv[0].endswith('nosetests')

@unittest.skipIf(_IS_NOSE, "broken under nosetest")
class AuthAPITestCase(TestRunnerMixin, VialTestCase):
    """
    Class for testing :py:mod:`vial.blueprints.auth_api` blueprint.
    """

    def _req_key_generate(self, uid, status_code, confirm = False):
        response = None
        if confirm:
            response = self.client.post(
                '/auth_api/{:d}/key-generate'.format(uid),
                follow_redirects = True,
                data = {'submit': 'Confirm'}
            )
        else:
            response = self.client.get(
                '/auth_api/{:d}/key-generate'.format(uid),
                follow_redirects = True
            )
        self.assertEqual(response.status_code, status_code)
        return response

    def _req_key_delete(self, uid, status_code, confirm = False):
        response = None
        if confirm:
            response = self.client.post(
                '/auth_api/{:d}/key-delete'.format(uid),
                follow_redirects = True,
                data = {'submit': 'Confirm'}
            )
        else:
            response = self.client.get(
                '/auth_api/{:d}/key-delete'.format(uid),
                follow_redirects = True
            )
        self.assertEqual(response.status_code, status_code)
        return response

    def _test_keymng_success(self, uname):
        uobj = self.user_get(uname, with_app_ctx = True)
        uid = uobj.id
        self.assertEqual(uobj.apikey, 'apikey-{}'.format(uname))

        response = self._req_key_generate(uid, 200)
        uobj = self.user_get(uname, with_app_ctx = True)
        self.assertTrue(b'Are you really sure you want to generate new API access key for following user account' in response.data)
        self.assertEqual(uobj.apikey, 'apikey-{}'.format(uname))

        response = self._req_key_generate(uid, 200, True)
        uobj = self.user_get(uname, with_app_ctx = True)
        self.assertTrue(uobj.apikey != 'apikey-{}'.format(uname))
        self.assertTrue(uobj.apikey)

        response = self._req_key_delete(uid, 200)
        uobj = self.user_get(uname, with_app_ctx = True)
        self.assertTrue(b'Are you really sure you want to delete API access key from following user account' in response.data)
        self.assertTrue(uobj.apikey != 'apikey-{}'.format(uname))
        self.assertTrue(uobj.apikey)

        response = self._req_key_delete(uid, 200, True)
        uobj = self.user_get(uname, with_app_ctx = True)
        self.assertEqual(uobj.apikey, None)
        self.assertFalse(uobj.apikey)

    def _test_keymng_failure(self, uname):
        uobj = self.user_get(uname, with_app_ctx = True)
        uid = uobj.id
        self.assertEqual(uobj.apikey, 'apikey-{}'.format(uname))

        self._req_key_generate(uid, 403)
        self._req_key_generate(uid, 403, True)
        self._req_key_delete(uid, 403)
        self._req_key_delete(uid, 403, True)

        uobj = self.user_get(uname, with_app_ctx = True)
        self.assertEqual(uobj.apikey, 'apikey-{}'.format(uname))

    def test_01_login_api(self):
        """
        Test login/logout with *auth_api* module.
        """
        for tcase in (
                {'Authorization': 'apikey-admin'},
                {'Authorization': 'key apikey-admin'},
                {'Authorization': 'token apikey-admin'}
            ):
            response = self.client.get(
                '/',
                follow_redirects = True,
                headers = tcase
            )
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'Welcome!' in response.data)
            self.assertTrue(b'My account' in response.data)
            self.assertTrue(b'data-user-name="admin"' in response.data)


        for tcase in (
                {'api_key': 'apikey-admin'},
                {'api_token': 'apikey-admin'}
            ):
            response = self.client.post(
                '/',
                follow_redirects = True,
                data = tcase
            )
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'Welcome!' in response.data)
            self.assertTrue(b'My account' in response.data)
            self.assertTrue(b'data-user-name="admin"' in response.data)

    @vial.test.do_as_user_decorator(vial.const.ROLE_USER)
    def test_02_keymng_user(self):
        """
        Test, that 'user' can manage only his own API key.
        """
        self._test_keymng_success(vial.const.ROLE_USER)
        self._test_keymng_failure(vial.const.ROLE_DEVELOPER)
        self._test_keymng_failure(vial.const.ROLE_ADMIN)

    @vial.test.do_as_user_decorator(vial.const.ROLE_DEVELOPER)
    def test_03_keymng_developer(self):
        """
        Test, that 'developer' can manage only his own API key.
        """
        self._test_keymng_failure(vial.const.ROLE_USER)
        self._test_keymng_success(vial.const.ROLE_DEVELOPER)
        self._test_keymng_failure(vial.const.ROLE_ADMIN)

    @vial.test.do_as_user_decorator(vial.const.ROLE_ADMIN)
    def test_04_keymng_admin(self):
        """
        Test, that 'admin' user is able to manage all API keys.
        """
        self._test_keymng_success(vial.const.ROLE_USER)
        self._test_keymng_success(vial.const.ROLE_DEVELOPER)
        self._test_keymng_success(vial.const.ROLE_ADMIN)


#-------------------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main()
