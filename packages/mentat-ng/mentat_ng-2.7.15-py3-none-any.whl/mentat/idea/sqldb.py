#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module provides class for object representation and conversion
of `IDEA <https://idea.cesnet.cz/en/index>`__  messages into their appropriate
`PostgreSQL <https://www.postgresql.org>`__ records. These records can be then
stored into database using the :py:mod:`mentat.services.eventstorage` event
persistent storage service.

The resulting record is intended to be stored into `PostgreSQL <https://www.postgresql.org>`__
database using **flat** schema. This is a very simple custom schema and it was
designed to tackle performance issues with full relational schema representation
of `IDEA <https://idea.cesnet.cz/en/index>`__ messages. It is basically a single
database table with fixed set of prepared indexed columns for the purposes of
searching and the whole `IDEA <https://idea.cesnet.cz/en/index>`__ message is then
stored as `PostgreSQL's <https://www.postgresql.org>`__ native ``jsonb``
datatype inside the last table column.

The schema currently supports indexing of following `IDEA <https://idea.cesnet.cz/en/index>`__
message attributes:

* ID
* DetectTime
* Category
* Description
* Source.IP (both v4 and v6)
* Source.Port
* Source.Type
* Target.IP (both v4 and v6)
* Target.Port
* Target.Type
* Protocol (both source and target, unique set)
* Node.Name
* Node.Type
* _CESNET.ResolvedAbuses
* _CESNET.StorageTime

As a side-effect of this approach, searching according to other IDEA message attributes
is not possible.


This module is expected to work only with messages based on or compatible with the
:py:class:`mentat.idea.internal.Idea` class.


This module contains following message class:

* :py:class:`mentat.idea.sqldb.Idea`

    Forward conversion into PostgreSQL data format.


Example usage:

.. code-block:: python

    >>> import mentat.idea.internal
    >>> import mentat.idea.sqldb

    # IDEA messages ussually come from regular dicts or JSON.
    >>> idea_raw = {...}

    # Just pass the dict as parameter to constructor to create internal IDEA.
    >>> idea_msg = mentat.idea.internal.Idea(idea_raw)

    # Just pass the IDEA message as parameter to constructor to create SQL record.
    >>> idea_postgresql = mentat.idea.sqldb.Idea(idea_msg)
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Radko Krkoš <radko.krkos@cesnet.cz>, Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import psycopg2
import ipranges


class IPList(list):
    """
    Custom list container for :py:mod:`ipranges` objects. This was implemented
    in order to support custom adaptation of IP objects into SQL query. Please
    see the :py:class:`mentat.services.eventstorage.IPListAdapter` for more
    details. Please see the `psycopg2 documentation <http://initd.org/psycopg/docs/advanced.html#adapting-new-python-types-to-sql-syntax>`__
    for in-depth explanation.
    """

class Idea:    # pylint: disable=locally-disabled,too-many-instance-attributes,too-few-public-methods
    """
    Performs conversion of IDEA messages into flat relational model.
    """
    ident                   = None
    detecttime              = None
    category                = list()
    description             = None
    source_ip               = IPList()
    target_ip               = IPList()
    source_ip_aggr_ip4      = None
    source_ip_aggr_ip6      = None
    target_ip_aggr_ip4      = None
    target_ip_aggr_ip6      = None
    source_port             = list()
    target_port             = list()
    source_type             = set()
    target_type             = set()
    protocol                = set()
    node_name               = list()
    node_type               = set()
    cesnet_resolvedabuses   = list()
    cesnet_storagetime      = None
    cesnet_eventclass       = None
    cesnet_eventseverity    = None
    cesnet_inspectionerrors = list()
    jsonb                   = None

    def __init__(self, idea_event):
        """
        :param mentat.idea.internal.Idea idea_event: IDEA event object.
        """
        # Convert the whole IDEA event object to JSON string and then encode it
        # to bytes. The event will be stored as a BYTEA datatype within the
        # PostgreSQL database istead of JSONB, because PostgreSQL is unable to
        # store JSON objects that contain null characters anywhere in the content.
        self.jsonb       = psycopg2.Binary(idea_event.to_json().encode('utf-8'))
        self.ident       = idea_event.get_id()
        self.detecttime  = idea_event.get_detect_time()
        self.category    = idea_event.get_categories()
        self.description = idea_event.get_description()

        # Source IP (both v4 a v6 in single attribute).
        self.source_ip = IPList()
        self.source_ip.extend([ip for ip in idea_event.get_addresses('Source')])

        # Target IP (both v4 a v6 in single attribute).
        self.target_ip = IPList()
        self.target_ip.extend([ip for ip in idea_event.get_addresses('Target')])

        # Aggregated source and target IP4|6 ranges for search optimizations.
        self.source_ip_aggr_ip4 = self._aggr_iplist(
            idea_event.get_addresses('Source', get_v6 = False),
            ipranges.IP4Range
        )
        self.source_ip_aggr_ip6 = self._aggr_iplist(
            idea_event.get_addresses('Source', get_v4 = False),
            ipranges.IP6Range
        )
        self.target_ip_aggr_ip4 = self._aggr_iplist(
            idea_event.get_addresses('Target', get_v6 = False),
            ipranges.IP4Range
        )
        self.target_ip_aggr_ip6 = self._aggr_iplist(
            idea_event.get_addresses('Target', get_v4 = False),
            ipranges.IP6Range
        )

        # Ports.
        self.source_port = idea_event.get_ports('Source')
        self.target_port = idea_event.get_ports('Target')

        # Types (tags).
        self.source_type = idea_event.get_types('Source')
        self.target_type = idea_event.get_types('Target')

        # Protocol (both source and target in single attribute).
        source_proto = idea_event.get_protocols('Source')
        target_proto = idea_event.get_protocols('Target')
        self.protocol = sorted(list(set(source_proto + target_proto)))

        # Node (detector) name and types (tags).
        self.node_name = idea_event.get_detectors()
        if not self.node_name:
            raise KeyError("Missing Node name")
        self.node_type = idea_event.get_types('Node')

        # CESNET implementation specific metadata.
        self.cesnet_resolvedabuses = idea_event.get_abuses()
        self.cesnet_storagetime    = idea_event.get_storage_time()

        self.cesnet_eventclass = idea_event.get_class()
        if self.cesnet_eventclass:
            self.cesnet_eventclass = self.cesnet_eventclass.lower()

        self.cesnet_eventseverity = idea_event.get_severity()
        if self.cesnet_eventseverity:
            self.cesnet_eventseverity = self.cesnet_eventseverity.lower()

        self.cesnet_inspectionerrors = list(
            idea_event.get('_CESNET', {}).get('InspectionErrors', list())
        )

    @staticmethod
    def _aggr_iplist(ranges, rngcls):
        """
        Helper method for creating aggregated IP range from given list of IP ranges.
        """
        if not ranges:
            return None
        ipmin = None
        ipmax = None
        for rng in ranges:
            if ipmin is None or rng.low() < ipmin:
                ipmin = rng.low()
            if ipmax is None or rng.high() > ipmax:
                ipmax = rng.high()
        return rngcls((ipmin, ipmax))

    @staticmethod
    def _get_subitems(obj, key, subkey):
        """
        Helper method for merging and retrieving lists from complex IDEA message
        substructures (lists within dicts within lists within dict). As an example
        usage this method can be used for obtaining all IP4 addresses within all
        sources in IDEA message.
        """
        result = []
        try:
            for item in obj[key]:
                try:
                    result.extend(item[subkey])
                except KeyError:
                    pass
        except KeyError:
            pass
        return result

    def get_record(self):
        """
        Return tuple containing object attributes in correct order for insertion
        into PostgreSQL database using the :py:mod:`mentat.services.eventstorage`
        service.
        """
        return (
            self.ident,
            self.detecttime,
            self.category,
            self.description,
            self.source_ip,
            self.target_ip,
            self.source_ip_aggr_ip4,
            self.source_ip_aggr_ip6,
            self.target_ip_aggr_ip4,
            self.target_ip_aggr_ip6,
            self.source_port,
            self.target_port,
            self.source_type,
            self.target_type,
            self.protocol,
            self.node_name,
            self.node_type,
            self.cesnet_resolvedabuses,
            self.cesnet_storagetime,
            self.cesnet_eventclass,
            self.cesnet_eventseverity,
            self.cesnet_inspectionerrors,
            self.jsonb
        )
