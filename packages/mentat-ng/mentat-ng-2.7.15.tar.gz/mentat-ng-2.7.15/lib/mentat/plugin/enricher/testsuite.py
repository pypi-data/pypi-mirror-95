#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Base test suite for testing Mentat enricher module plugins implemented on top of
the :py:class:`mentat.plugin.enricher.EnricherPlugin` class.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import os
import unittest
from unittest.mock import Mock
from pprint import pformat

import pyzenkit.jsonconf

class MentatEnricherPluginTestCase(unittest.TestCase):
    """
    Base test case class for testing Mentat enricher module plugins implemented
    on top of the :py:class:`mentat.plugin.enricher.EnricherPlugin` class.
    """

    def setUp(self):
        #
        # Turn on more verbose output, which includes print-out of constructed
        # objects. This will really clutter your console, usable only for test
        # debugging.
        #
        self.verbose = False

        cdir_path = os.path.dirname(os.path.realpath(__file__))
        self.core_config = pyzenkit.jsonconf.config_load_dir(
            os.path.realpath(
                os.path.join(cdir_path, '../../../../conf/core')
            )
        )

    def _verbose_print(self, label, data):
        """
        Helper method, print additional information in verbose mode.
        """
        if self.verbose:
            print("{}\n{}".format(label, pformat(data)))

    def _build_application_mock(self, config_list, core_config_list = None):
        """
        Helper method, build and return daemon mock object.
        """
        daemon = Mock(
            config = self.core_config,
            cid = 'testcomp',
            FLAG_CONTINUE = 1,
            FLAG_STOP = 0,
        )
        daemon.attach_mock(
            Mock(

                # Define required configuration values in order they are required
                # from daemon instance (ussually in setup() method).
                side_effect = config_list

            ), 'c'
        )
        if core_config_list:
            daemon.attach_mock(
                Mock(

                    # Define required configuration values in order they are required
                    # from daemon instance (ussually in setup() method).
                    side_effect = core_config_list

                ), 'cc'
            )
        return daemon
