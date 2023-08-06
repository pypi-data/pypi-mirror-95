#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Unit tests for :py:mod:`hawat.blueprints.auth_env`.
"""


import unittest

import vial.const
import vial.test
import vial.test.fixtures
import vial.db
from hawat.test import RegistrationHawatTestCase
from hawat.test.runner import TestRunnerMixin


class AuthEnvTestCase(TestRunnerMixin, RegistrationHawatTestCase):
    """
    Class for testing :py:mod:`hawat.blueprints.auth_env` blueprint.
    """

    def test_01_login_user(self):
        """
        Test login/logout with *auth_env* module - user 'user'.
        """
        response = self.login_env(vial.const.ROLE_USER)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'You have been successfully logged in as' in response.data)

        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'You have been successfully logged out' in response.data)

        response = self.login_env(vial.const.ROLE_USER, 'REMOTE_USER')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'You have been successfully logged in as' in response.data)

        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'You have been successfully logged out' in response.data)

    def test_02_login_developer(self):
        """
        Test login/logout with *auth_env* module - user 'developer'.
        """
        response = self.login_env(vial.const.ROLE_DEVELOPER)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'You have been successfully logged in as' in response.data)

        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'You have been successfully logged out' in response.data)

        response = self.login_env(vial.const.ROLE_DEVELOPER, 'REMOTE_USER')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'You have been successfully logged in as' in response.data)

        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'You have been successfully logged out' in response.data)

    def test_03_login_admin(self):
        """
        Test login/logout with *auth_env* module - user 'admin'.
        """
        response = self.login_env(vial.const.ROLE_ADMIN)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'You have been successfully logged in as' in response.data)

        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'You have been successfully logged out' in response.data)

        response = self.login_env(vial.const.ROLE_ADMIN, 'REMOTE_USER')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'You have been successfully logged in as' in response.data)

        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'You have been successfully logged out' in response.data)

    def test_04_register(self):
        """
        Test registration with *auth_env* module - new user 'test'.
        """
        self.assertRegister(
            '/auth_env/register',
            [
                ('submit', 'Register'),
                ('organization', 'TEST, org.'),
                ('justification', 'I really want in.')
            ],
            {
                'txt': [
                    'Dear administrator,\n'
                    '\n'
                    'a new account "test" was just registered in Mentat. Please review the '
                    'following\n'
                    'request and activate or delete the account:\n'
                    '\n'
                    '    Login:           test\n'
                    '    Full name:       Test User\n'
                    '    Email:           test.user@domain.org\n'
                    '    Organization:    TEST, org.\n'
                    '\n'
                    'User has provided following justification to be given access to the system:\n'
                    '\n'
                    '    I really want in.\n'
                    '\n'
                    'Account details can be found here:\n'
                    '\n'
                    '  http://localhost/users/5/show\n'
                    '\n'
                    'Have a nice day\n'
                    '\n'
                    '-- Mentat',
                    'Dear user,\n'
                    '\n'
                    'this email is a confirmation, that you have successfully registered your '
                    'new\n'
                    'user account "test" in Mentat.\n'
                    '\n'
                    'During the registration process you have provided following information:\n'
                    '\n'
                    '    Login:           test\n'
                    '    Full name:       Test User\n'
                    '    Email:           test.user@domain.org\n'
                    '    Organization:    TEST, org.\n'
                    '\n'
                    'You have provided following justification to be given access to the system:\n'
                    '\n'
                    '    I really want in.\n'
                    '\n'
                    'Administrator was informed about registration of a new account. You will\n'
                    'receive email confirmation when your account will be activated.\n'
                    '\n'
                    'After successfull activation you will be able to login and start using the\n'
                    'system:\n'
                    '\n'
                    '\thttp://localhost/auth_pwd/login\n'
                    '\n'
                    'Have a nice day\n'
                    '\n'
                    '-- Mentat'
                ],
                'html': [
                    None,
                    None
                ]
            },
            {
                'eppn': 'test',
                'cn': 'Test User',
                'givenName': 'Test',
                'sn': 'User',
                'perunPreferredMail': 'test.user@domain.org',
                'perunOrganizationName': 'TEST, orgggg.'
            }
        )

    def test_05_register_fail(self):
        """
        Test registration with *auth_env* module - existing user 'user'.
        """
        self.assertRegisterFail(
            '/auth_env/register',
            [
                ('submit', 'Register'),
                ('organization', 'TEST, org.'),
                ('justification', 'I really want in.')
            ],
            {
                'eppn': 'user',
                'cn': 'Test User',
                'perunPreferredMail': 'test.user@domain.org',
                'perunOrganizationName': 'TEST, orgggg.'
            }
        )


#-------------------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main()
