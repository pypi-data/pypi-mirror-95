#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------

"""
Enricher plugin performing lookup of all Source/IPx addresses within configured
whois service.


.. todo::

    Documentation needs to be finished.

.. warning::

    Still a work in progress and alpha code.

"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import collections
import pprint


#
# Custom libraries
#
from pynspect.jpath import jpath_values, jpath_set
import mentat.const
import mentat.services.whois


class WhoisEnricherPlugin:
    """
    Enricher plugin performing lookup of all Source/IPx addresses within configured
    whois service.
    """
    def setup(self, daemon, config):
        """
        Setup plugin.
        """
        self.whois_service = self._bootstrap_whois_service(daemon, config['whois_modules'])
        daemon.logger.info("Initialized '{}' enricher plugin: {}".format(self.__class__.__name__, pprint.pformat(self.whois_service.status())))

    def _configure_whois_module(self, daemon, name, conf):
        """
        Preprocess configuration for whois module.
        """
        return conf

    def _bootstrap_whois_service(self, daemon, modules):
        """
        Bootstrap whois service and all its modules according to given configuration.
        """
        whois_service = mentat.services.whois.WhoisService()
        for module in modules:
            cfg = self._configure_whois_module(daemon, module['name'], module['config'])

            module_class = getattr(mentat.services.whois, module['name'])
            whois_module = module_class(**cfg)

            whois_service.add_module(whois_module.setup())
            daemon.logger.debug("Initialized '{}' whois module".format(module['name']))
        return whois_service

    def process(self, daemon, message_id, message):
        """
        Process and enrich given message.
        """
        daemon.logger.debug("Whois - message '{}'".format(message_id))

        sources = []
        sources += jpath_values(message, 'Source.IP4')
        sources += jpath_values(message, 'Source.IP6')

        resolved_abuses = collections.defaultdict(int)
        for src in sources:
            result = self.whois_service.lookup_abuse(src)
            if result is None:
                continue

            for res in result:
                resolved_abuses[res] += 1

        changed = False
        resolved_abuses = sorted(resolved_abuses.keys())
        if resolved_abuses:
            jpath_set(message, '_CESNET.ResolvedAbuses', resolved_abuses)
            daemon.logger.debug("Enriched message '{}' with attribute '_CESNET.ResolvedAbuses'".format(message_id))
            changed = True

        return (daemon.FLAG_CONTINUE, changed)
