#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This pluggable module provides access to all currently enabled authentication
and user account registration methods.
"""


import flask
import flask_login
from flask_babel import lazy_gettext

import vial.const
from vial.app import VialBlueprint
from vial.view import SimpleView
from vial.view.mixin import HTMLMixin


BLUEPRINT_NAME = 'auth'
"""Name of the blueprint as module global constant."""


class LoginView(HTMLMixin, SimpleView):
    """
    View enabling access to all currently enabled user login options.
    """
    methods = ['GET']

    @classmethod
    def get_view_name(cls):
        return vial.const.ACTION_USER_LOGIN

    @classmethod
    def get_view_icon(cls):
        return vial.const.ACTION_USER_LOGIN

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('User login')

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Login')

    def do_before_response(self, **kwargs):
        # In case user is already authenticated redirect to endpoint after login.
        if flask_login.current_user.is_authenticated:
            return self.redirect(
                default_url = flask.url_for(
                    flask.current_app.config['ENDPOINT_LOGIN']
                )
            )

        # Otherwise lookup all currently enabled 'SIGN IN' endpoints.
        self.response_context.update(
            signin_endpoints = flask.current_app.get_endpoints(
                lambda name, mod: getattr(mod, 'is_sign_in', False)
            )
        )

        return None


class RegisterView(HTMLMixin, SimpleView):
    """
    View enabling access to all currently enabled user registration options.
    """
    methods = ['GET']

    @classmethod
    def get_view_name(cls):
        return vial.const.ACTION_USER_REGISTER

    @classmethod
    def get_view_icon(cls):
        return vial.const.ACTION_USER_REGISTER

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('User account registration')

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Register')

    def do_before_response(self, **kwargs):
        # Lookup all currently enabled 'SIGN UP' endpoints.
        self.response_context.update(
            signup_endpoints = flask.current_app.get_endpoints(
                lambda name, mod: getattr(mod, 'is_sign_up', False)
            )
        )


#-------------------------------------------------------------------------------


class AuthBlueprint(VialBlueprint):
    """Pluggable module - authentication and registration directional service (*auth*)."""

    @classmethod
    def get_module_title(cls):
        return lazy_gettext('Authentication directional service')

    def register_app(self, app):
        app.menu_anon.add_entry(
            'view',
            'login',
            position = 0,
            view = LoginView,
            hidelegend = True
        )
        app.menu_anon.add_entry(
            'view',
            'register',
            position = 100,
            view = RegisterView,
            hidelegend = True
        )


#-------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface for :py:mod:`vial.Vial` and factory function. This function
    must return a valid instance of :py:class:`vial.app.VialBlueprint` or
    :py:class:`flask.Blueprint`.
    """

    hbp = AuthBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder = 'templates',
        url_prefix = '/{}'.format(BLUEPRINT_NAME)
    )

    hbp.register_view_class(LoginView,    '/login')
    hbp.register_view_class(RegisterView, '/register')

    return hbp
