#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains custom network record management forms for Hawat.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import wtforms
from wtforms.ext.sqlalchemy.fields import QuerySelectField

#
# Flask related modules.
#
from flask_babel import lazy_gettext

#
# Custom modules.
#
import vial.const
import vial.forms
import vial.db
from vial.forms import get_available_groups

from mentat.datatype.sqldb import NetworkModel


def get_available_sources():
    """
    Query the database for list of network record sources.
    """
    result = vial.db.db_query(NetworkModel)\
        .distinct(NetworkModel.source)\
        .order_by(NetworkModel.source)\
        .all()
    return [x.source for x in result]


class BaseNetworkForm(vial.forms.BaseItemForm):
    """
    Class representing base network record form.
    """
    netname = wtforms.StringField(
        lazy_gettext('Netname:'),
        validators = [
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min = 3, max = 250)
        ]
    )
    source = wtforms.HiddenField(
        default = 'manual',
        validators = [
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min = 3, max = 50)
        ]
    )
    network = wtforms.TextAreaField(
        lazy_gettext('Network:'),
        validators = [
            wtforms.validators.DataRequired(),
            vial.forms.check_network_record
        ]
    )
    description = wtforms.TextAreaField(
        lazy_gettext('Description:')
    )
    submit = wtforms.SubmitField(
        lazy_gettext('Submit')
    )
    cancel = wtforms.SubmitField(
        lazy_gettext('Cancel')
    )


class AdminNetworkForm(BaseNetworkForm):
    """
    Class representing network record create form.
    """
    group = QuerySelectField(
        lazy_gettext('Group:'),
        query_factory = get_available_groups,
        allow_blank = False
    )


class NetworkSearchForm(vial.forms.BaseSearchForm):
    """
    Class representing simple user search form.
    """
    search = wtforms.StringField(
        lazy_gettext('Netname, network, description:'),
        validators = [
            wtforms.validators.Optional(),
            wtforms.validators.Length(min = 3, max = 100)
        ],
        description = lazy_gettext('Network`s name, address or description. Search is performed even in the middle of the strings.')
    )
    dt_from = vial.forms.SmartDateTimeField(
        lazy_gettext('Creation time from:'),
        validators = [
            wtforms.validators.Optional()
        ],
        description = lazy_gettext('Lower time boundary for item creation time. Timestamp is expected to be in the format <code>YYYY-MM-DD hh:mm:ss</code> and in the timezone according to the user`s preferences.')
    )
    dt_to = vial.forms.SmartDateTimeField(
        lazy_gettext('Creation time to:'),
        validators = [
            wtforms.validators.Optional()
        ],
        description = lazy_gettext('Upper time boundary for item creation time. Timestamp is expected to be in the format <code>YYYY-MM-DD hh:mm:ss</code> and in the timezone according to the user`s preferences.')
    )

    group = QuerySelectField(
        lazy_gettext('Group:'),
        query_factory = get_available_groups,
        allow_blank = True
    )
    source = wtforms.SelectField(
        lazy_gettext('Record source:'),
        validators = [
            wtforms.validators.Optional()
        ],
        default = ''
    )

    sortby = wtforms.SelectField(
        lazy_gettext('Sort by:'),
        validators = [
            wtforms.validators.Optional()
        ],
        choices = [
            ('createtime.desc', lazy_gettext('by creation time descending')),
            ('createtime.asc',  lazy_gettext('by creation time ascending')),
            ('netname.desc', lazy_gettext('by netname descending')),
            ('netname.asc',  lazy_gettext('by netname ascending')),
            ('network.desc', lazy_gettext('by network descending')),
            ('network.asc',  lazy_gettext('by network ascending'))
        ],
        default = 'netname.asc'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #
        # Handle additional custom keywords.
        #

        # The list of choices for 'roles' attribute comes from outside of the
        # form to provide as loose tie as possible to the outer application.
        # Another approach would be to load available choices here with:
        #
        #   roles = flask.current_app.config['ROLES']
        #
        # That would mean direct dependency on flask.Flask application.
        source_list = get_available_sources()
        self.source.choices = [('', lazy_gettext('Nothing selected'))] + list(zip(source_list, source_list))

    @staticmethod
    def is_multivalue(field_name):
        """
        Check, if given form field is a multivalue field.

        :param str field_name: Name of the form field.
        :return: ``True``, if the field can contain multiple values, ``False`` otherwise.
        :rtype: bool
        """
        return False
