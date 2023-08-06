#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Library for generating event reports.

The implementation is based on :py:class:`mentat.reports.base.BaseReporter`.
"""


__author__  = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import os
import json
import datetime
import zipfile
import csv
from copy import deepcopy

#
# Custom libraries
#
from pynspect.jpath   import jpath_value, jpath_values
from pynspect.gparser import PynspectFilterParser
from pynspect.filters import DataObjectFilter

from mentat.idea.internal import IDEAFilterCompiler

import mentat.const
import mentat.datatype.internal
import mentat.idea.internal
import mentat.stats.idea
import mentat.services.whois
from mentat.const import tr_
from mentat.reports.utils import StorageThresholdingCache, NoThresholdingCache
from mentat.datatype.sqldb import EventReportModel
from mentat.emails.event import ReportEmail
from mentat.reports.base import BaseReporter
from mentat.services.eventstorage import record_to_idea


REPORT_SUBJECT_SUMMARY = tr_("[{:s}] {:s} - Notice about possible problems in your network")
"""Subject for summary report emails."""

REPORT_SUBJECT_EXTRA = tr_("[{:s}] {:s} - Notice about possible problems regarding host {:s}")
"""Subject for extra report emails."""

REPORT_EMAIL_TEXT_WIDTH = 90
"""Width of the report email text."""


def json_default(val):
    """
    Helper function for JSON serialization of non basic data types.
    """
    if isinstance(val, datetime.datetime):
        return val.isoformat()
    return str(val)

def csv_dict(idea):
    """
    Convert selected attributes of given IDEA message into flat dictionary suitable for CSV dump. This is a legacy feature from old version of Mentat system and due to its shortcomings is planned to be removed in the future. It was implemented only for the purposes of compatibility and transition from old version of Mentat system to new one.
    """
    dump = {}

    dtime = jpath_value(idea, 'DetectTime')
    ctime = jpath_value(idea, 'CreateTime')
    if not ctime:
        ctime = dtime
    anlzr = jpath_value(idea, 'Node[#].SW')
    dtctr = jpath_value(idea, 'Node[#].Name')
    descr = jpath_value(idea, 'Description')
    if not descr:
        descr = jpath_value(idea, 'Note')
    categ = jpath_values(idea, 'Category')

    sip   = jpath_values(idea, 'Source.IP4') + jpath_values(idea, 'Source.IP6')
    sport = jpath_values(idea, 'Source.Port')
    tport = jpath_values(idea, 'Target.Port')
    sproto = jpath_values(idea, 'Source.Proto')
    tproto = jpath_values(idea, 'Target.Proto')

    concnt = jpath_value(idea, 'ConnCount')
    note   = jpath_value(idea, 'Note')
    impact = jpath_value(idea, '_CESNET.Impact')

    #---

    dump['date_gmt']       = str(ctime)
    dump['detected_gmt']   = str(dtime)
    dump['analyzer']       = anlzr or '-'
    dump['detector']       = dtctr or '-'
    dump['classification'] = descr or '-'
    dump['con_cnt']        = concnt or '-'
    dump['date_ts']        = int(ctime.timestamp())
    dump['detected_ts']    = int(dtime.timestamp())
    dump['note']           = note or '-'
    dump['impact']         = impact or '-'
    dump['src_host']       = '-'

    if categ:
        dump['categories'] = ','.join([str(x) for x in categ])
    else:
        dump['categories'] = '-'

    if sip:
        dump['src_ip'] = ','.join([str(x) for x in sip])
    else:
        dump['src_ip'] = '-'

    if sport:
        dump['src_port'] = ','.join([str(x) for x in sport])
    else:
        dump['src_port'] = '-'

    if tport:
        dump['tgt_port'] = ','.join([str(x) for x in tport])
    else:
        dump['tgt_port'] = '-'

    if sproto:
        dump['src_proto'] = ','.join([str(x) for x in sproto])
    else:
        dump['src_proto'] = '-'

    if tproto:
        dump['tgt_proto'] = ','.join([str(x) for x in tproto])
    else:
        dump['tgt_proto'] = '-'

    return dump


class EventReporter(BaseReporter):
    """
    Implementation of reporting class providing Mentat event reports.
    """

    def __init__(self, logger, reports_dir, templates_dir, locale, timezone, eventservice, sqlservice, mailer, event_classes_dir, thresholding = True):
        self.translations_dir = ";".join([os.path.join(event_classes_dir, event_class, "translations")
                                          for event_class in os.listdir(event_classes_dir)
                                          if os.path.isdir(os.path.join(event_classes_dir, event_class))])
        self.translations_dir += ";" + os.path.join(templates_dir, "translations")
        super().__init__(logger, reports_dir, templates_dir + ";" + event_classes_dir, locale, timezone, self.translations_dir)

        self.eventservice    = eventservice
        self.sqlservice      = sqlservice
        self.mailer          = mailer

        self.event_classes_data = {}
        self.event_classes_dir = event_classes_dir

        self.filter_parser   = PynspectFilterParser()
        self.filter_compiler = IDEAFilterCompiler()
        self.filter_worker   = DataObjectFilter()

        self.filter_parser.build()

        if thresholding:
            self.tcache = StorageThresholdingCache(logger, eventservice)
        else:
            self.tcache = NoThresholdingCache()

    def _get_event_class_data(self, event_class):
        if event_class not in self.event_classes_data:
            self.event_classes_data[event_class] = data = {}
            if os.path.isfile(os.path.join(self.event_classes_dir, event_class, "info.json")):
                with open(os.path.join(self.event_classes_dir, event_class, "info.json")) as f:
                    info = json.load(f)
                    [data.__setitem__(key, info[key]) for key in ["label", "reference"] if key in info]
            data["has_macro"] = os.path.isfile(os.path.join(self.event_classes_dir, event_class, "email.j2"))

    def _setup_renderer(self, templates_dir):
        """
        *Interface reimplementation* of :py:func:`mentat.reports.base.BaseReporter._setup_renderer`
        """

        renderer = super()._setup_renderer(templates_dir)

        renderer.globals['idea_path_valueset'] = self.j2t_idea_path_valueset

        return renderer

    @staticmethod
    def j2t_idea_path_valueset(message_s, jpath_s):
        """
        Calculate and return set of all values on all given jpaths in all given
        messages. Messages and jpaths can also be a single values.
        """
        result = {}
        if not isinstance(message_s, list):
            message_s = [message_s]
        if not isinstance(jpath_s, list):
            jpath_s = [jpath_s]
        for item in message_s:
            for jpath in jpath_s:
                values = item.get_jpath_values(jpath)
                for val in values:
                    result[val] = 1
        return list(sorted(result.keys()))


    #---------------------------------------------------------------------------


    def cleanup(self, ttl):
        """
        Cleanup thresholding cache and remove all records with TTL older than given
        value.

        :param datetime.datetime time_h: Upper cleanup time threshold.
        :return: Number of removed records.
        :rtype: int
        """
        return self.tcache.cleanup(ttl)

    def report(self, abuse_group, settings, severity, time_l, time_h, template_vars = None, testdata = False):
        """
        Perform reporting for given abuse group, event severity and time window.

        :param mentat.datatype.internal.GroupModel abuse_group: Abuse group.
        :param mentat.reports.event.ReportingSettings settings: Reporting settings.
        :param str severity: Severity for which to perform reporting.
        :param datetime.datetime time_l: Lower reporting time threshold.
        :param datetime.datetime time_h: Upper reporting time threshold.
        :param dict template_vars: Dictionary containing additional template variables.
        :param bool testdata: Switch to use test data for reporting.
        """
        result = {}
        result['ts_from_s'] = time_l.isoformat()
        result['ts_to_s']   = time_h.isoformat()
        result['ts_from']   = int(time_l.timestamp())
        result['ts_to']     = int(time_h.timestamp())

        events = {}

        while True:
            # A: Fetch events from database.
            events_fetched = self.fetch_severity_events(abuse_group, severity, time_l, time_h, testdata)
            result['evcount_new'] = len(events_fetched)
            result['evcount_all'] = result['evcount_new']
            if not events_fetched:
                break

            # B: Perform event filtering according to custom group filters and aggregate by source.
            events_flt, events_aggr, fltlog = self.filter_events(events_fetched, abuse_group, settings)
            result['evcount_flt'] = len(events_flt)
            result['evcount_flt_blk'] = len(events_fetched) - len(events_flt)
            result['filtering'] = fltlog
            if not events_flt:
                break

            # C: Perform event thresholding.
            events_thr, events_aggr = self.threshold_events(events_aggr, abuse_group, severity, time_h)

            result['evcount_thr'] = len(events_thr)
            result['evcount_thr_blk'] = len(events_flt) - len(events_thr)
            if not events_thr:
                break

            # D: Save aggregated events for further processing.
            events['regular'] = events_thr
            events['regular_aggr'] = events_aggr

            break

        while True:
            # A: Detect possible event relapses.
            events_rel = self.relapse_events(abuse_group, severity, time_h)
            result['evcount_rlp'] = len(events_rel)
            result['evcount_all'] = result['evcount_all'] + result['evcount_rlp']
            if not events_rel:
                break

            # B: Aggregate events by sources for further processing.
            events_rel, events_aggr = self.aggregate_relapsed_events(events_rel)
            events['relapsed'] = events_rel
            events['relapsed_aggr'] = events_aggr

            break

        # Check, that there is anything to report (regular and/or relapsed events).
        if 'regular' not in events and 'relapsed' not in events:
            result['evcount_rep'] = 0
            result['result'] = 'skipped-no-events'
            return result
        result['evcount_rep'] = len(events.get('regular', [])) + len(events.get('relapsed', []))

        # Generate summary report.
        report_summary = self.report_summary(result, events, abuse_group, settings, severity, time_l, time_h, template_vars, testdata)

        # Generate extra reports.
        self.report_extra(report_summary, result, events, abuse_group, settings, severity, time_l, time_h, template_vars, testdata)

        # Update thresholding cache.
        self.update_thresholding_cache(events, settings, severity, time_h)

        result['result'] = 'reported'
        return result

    def report_summary(self, result, events, abuse_group, settings, severity, time_l, time_h, template_vars = None, testdata = False):
        """
        Generate summary report from given events for given abuse group, severity and period.

        :param dict result: Reporting result structure with various usefull metadata.
        :param dict events: Dictionary structure with IDEA events to be reported.
        :param mentat.datatype.internal.GroupModel abuse_group: Abuse group.
        :param mentat.reports.event.ReportingSettings settings: Reporting settings.
        :param str severity: Severity for which to perform reporting.
        :param datetime.datetime time_l: Lower reporting time threshold.
        :param datetime.datetime time_h: Upper reporting time threshold.
        :param dict template_vars: Dictionary containing additional template variables.
        :param bool testdata: Switch to use test data for reporting.
        """
        # Instantinate the report object.
        report = EventReportModel(
            group    = abuse_group,
            severity = severity,
            type     = mentat.const.REPORT_TYPE_SUMMARY,
            dt_from  = time_l,
            dt_to    = time_h,

            evcount_rep     = result.get('evcount_rep', 0),
            evcount_all     = result.get('evcount_all', 0),
            evcount_new     = result.get('evcount_new', 0),
            evcount_flt     = result.get('evcount_flt', 0),
            evcount_flt_blk = result.get('evcount_flt_blk', 0),
            evcount_thr     = result.get('evcount_thr', 0),
            evcount_thr_blk = result.get('evcount_thr_blk', 0),
            evcount_rlp     = result.get('evcount_rlp', 0),

            flag_testdata = testdata,

            filtering = result.get('filtering', {})
        )
        report.generate_label()
        report.calculate_delta()

        events_all = events.get('regular', []) + events.get('relapsed', [])
        report.statistics = mentat.stats.idea.truncate_evaluations(
            mentat.stats.idea.evaluate_events(events_all)
        )

        # Save report data to disk in various formats.
        self._save_to_json_files(
            events_all,
            'security-report-{}.json'.format(report.label)
        )
        self._save_to_csv_files(
            events_all,
            'security-report-{}.csv'.format(report.label)
        )

        # Attachments were moved from emails to web (Redmine issue #6255).
        attachment_files = []
        #attachment_files = self.choose_attachments(
        #    'security-report-{}'.format(report.label),
        #    settings
        #)

        report.structured_data = self.prepare_structured_data(events.get('regular_aggr', {}), events.get('relapsed_aggr', {}), settings)

        # Send report via email.
        if not settings.mute and settings.mode in (mentat.const.REPORTING_MODE_SUMMARY, mentat.const.REPORTING_MODE_BOTH):
            self._mail_report(report, settings, attachment_files, result, template_vars)

        # Commit all changes on report object to database.
        self.sqlservice.session.add(report)
        self.sqlservice.session.commit()

        result['summary_id'] = report.label

        return report

    def report_extra(self, parent_rep, result, events, abuse_group, settings, severity, time_l, time_h, template_vars = None, testdata = False):
        """
        Generate extra reports from given events for given abuse group, severity and period.

        :param mentat.datatype.internal.EventReportModel parent_rep: Parent summary report.
        :param dict result: Reporting result structure with various usefull metadata.
        :param dict events: Dictionary structure with IDEA events to be reported.
        :param mentat.datatype.internal.GroupModel abuse_group: Abuse group.
        :param mentat.reports.event.ReportingSettings settings: Reporting settings.
        :param str severity: Severity for which to perform reporting.
        :param datetime.datetime time_l: Lower reporting time threshold.
        :param datetime.datetime time_h: Upper reporting time threshold.
        :param dict template_vars: Dictionary containing additional template variables.
        :param bool testdata: Switch to use test data for reporting.
        """
        if settings.mode not in (mentat.const.REPORTING_MODE_EXTRA, mentat.const.REPORTING_MODE_BOTH):
            return

        sources = list(
            set(
                list(events.get('regular_aggr', {}).keys()) + list(events.get('relapsed_aggr', {}).keys())
            )
        )

        for src in sorted(sources):

            events_regular_aggr = events.get('regular_aggr', {}).get(src, [])
            events_relapsed_aggr = events.get('relapsed_aggr', {}).get(src, [])
            events_all = events_regular_aggr + events_relapsed_aggr

            # Instantinate the report object.
            report = EventReportModel(
                group    = abuse_group,
                parent   = parent_rep,
                severity = severity,
                type     = mentat.const.REPORT_TYPE_EXTRA,
                dt_from  = time_l,
                dt_to    = time_h,

                evcount_rep = len(events_all),
                evcount_all = result['evcount_rep'],

                flag_testdata = testdata
            )
            report.generate_label()
            report.calculate_delta()

            report.statistics = mentat.stats.idea.truncate_evaluations(
                mentat.stats.idea.evaluate_events(events_all)
            )

            # Save report data to disk in various formats.
            self._save_to_json_files(
                events_all,
                'security-report-{}.json'.format(report.label)
            )
            self._save_to_csv_files(
                events_all,
                'security-report-{}.csv'.format(report.label)
            )

            # Attachments were moved from emails to web (Redmine issue #6255).
            attachment_files = []
            #attachment_files = self.choose_attachments(
            #    'security-report-{}'.format(report.label),
            #    settings
            #)

            report.structured_data = self.prepare_structured_data({src: events_regular_aggr}, {src: events_relapsed_aggr}, settings)

            # Send report via email.
            if not settings.mute:
                self._mail_report(report, settings, attachment_files, result, template_vars, src)

            # Commit all changes on report object to database.
            self.sqlservice.session.add(report)
            self.sqlservice.session.commit()

            result.setdefault('extra_id', []).append(report.label)


    #---------------------------------------------------------------------------

    @staticmethod
    def prepare_structured_data(events_reg_aggr, events_rel_aggr, settings):
        """
        Prepare structured data for report column

        :param list events_reg_aggr: List of events as :py:class:`mentat.idea.internal.Idea` objects.
        :param list events_rel_aggr: List of relapsed events as :py:class:`mentat.idea.internal.Idea` objects.
        :return: Structured data that cam be used to generate report message
        :rtype: dict
        """
        result = {}
        result["regular"] = EventReporter.aggregate_events(events_reg_aggr)
        result["relapsed"] = EventReporter.aggregate_events(events_rel_aggr)
        result["timezone"] = str(settings.timezone)
        return result

    #---------------------------------------------------------------------------


    def fetch_severity_events(self, abuse_group, severity, time_l, time_h, testdata = False):
        """
        Fetch events with given severity for given abuse group within given time
        iterval.

        :param abuse_group: Abuse group model object.
        :param str severity: Event severity level to fetch.
        :param datetime.datetime time_l: Lower time interval boundary.
        :param datetime.datetime time_h: Upper time interval boundary.
        :param bool testdata: Switch to use test data for reporting.
        :return: List of events matching search criteria.
        :rtype: list
        """
        count, events = self.eventservice.search_events({
            'st_from':        time_l,
            'st_to':          time_h,
            'groups':         [abuse_group.name],
            'severities':     [severity],
            'categories':     ['Test'],
            'not_categories': not testdata
        })
        if not events:
            self.logger.debug(
                "%s: Found no event(s) with severity '%s' and time interval %s -> %s (%s).",
                abuse_group.name,
                severity,
                time_l.isoformat(),
                time_h.isoformat(),
                str(time_h - time_l)
            )
        else:
            self.logger.info(
                "%s: Found %d event(s) with severity '%s' and time interval %s -> %s (%s).",
                abuse_group.name,
                len(events),
                severity,
                time_l.isoformat(),
                time_h.isoformat(),
                str(time_h - time_l)
            )
        return events

    @staticmethod
    def _whois_filter(sources, src, whoismodule, whoismodule_cache):
        """
        Help method for filtering sources by abuse group's networks
        """
        if src not in whoismodule_cache:
            # Source IP must belong to network range of given abuse group.
            whoismodule_cache[src] = bool(whoismodule.lookup(src))
        if whoismodule_cache[src]:
            sources.add(src)
        return sources

    def filter_events(self, events, abuse_group, settings):
        """
        Filter given list of IDEA events according to given abuse group settings.

        :param list events: List of IDEA events as :py:class:`mentat.idea.internal.Idea` objects.
        :param mentat.datatype.sqldb.GroupModel: Abuse group.
        :param mentat.reports.event.ReportingSettings settings: Reporting settings.
        :return: Tuple with list of events that passed filtering, aggregation of them and filtering log as a dictionary.
        :rtype: tuple
        """
        whoismodule = mentat.services.whois.WhoisModule()
        networks = settings.setup_networks()
        whoismodule.setup(networks)
        whoismodule_cache = {}

        filter_list = settings.setup_filters(self.filter_parser, self.filter_compiler)
        result = []
        fltlog = {}
        aggregated_result = {}
        for event in events:
            match = self.filter_event(filter_list, event)
            sources = set()
            if match:
                if len(jpath_values(event, 'Source.IP4') + jpath_values(event, 'Source.IP6')) > 1:
                    event_copy = deepcopy(event)
                    for s in event_copy["Source"]:
                        s["IP4"] = []
                        s["IP6"] = []
                    for src in set(jpath_values(event, 'Source.IP4')):
                        event_copy["Source"][0]["IP4"] = [src]
                        if not self.filter_event(filter_list, event_copy, False):
                            sources = self._whois_filter(sources, src, whoismodule, whoismodule_cache)
                    event_copy["Source"][0]["IP4"] = []
                    for src in set(jpath_values(event, 'Source.IP6')):
                        event_copy["Source"][0]["IP6"] = [src]
                        if not self.filter_event(filter_list, event_copy, False):
                            sources = self._whois_filter(sources, src, whoismodule, whoismodule_cache)

                if sources:
                    self.logger.debug("Event matched filtering rule '%s', some sources allowed through", match)
                else:
                    self.logger.debug("Event matched filtering rule '%s', all sources filtered", match)
                    fltlog[match] = fltlog.get(match, 0) + 1
            else:
                for src in set(jpath_values(event, 'Source.IP4') + jpath_values(event, 'Source.IP6')):
                    sources = self._whois_filter(sources, src, whoismodule, whoismodule_cache)

            if sources:
                result.append(event)
                for src in sources:
                    if str(src) not in aggregated_result:
                        aggregated_result[str(src)] = []
                    aggregated_result[str(src)].append(event)

        if result:
            self.logger.info(
                "%s: Filters let %d events through, %d blocked.",
                abuse_group.name,
                len(result),
                (len(events) - len(result))
            )
        else:
            self.logger.info(
                "%s: Filters blocked all %d events, nothing to report.",
                abuse_group.name,
                len(events)
            )
        return result, aggregated_result, fltlog

    def threshold_events(self, events_aggr, abuse_group, severity, time_h):
        """
        Threshold given list of IDEA events according to given abuse group settings.

        :param dict events_aggr: Aggregation of IDEA events as :py:class:`mentat.idea.internal.Idea` objects by source.
        :param mentat.datatype.sqldb.GroupModel: Abuse group.
        :param str severity: Severity for which to perform reporting.
        :param datetime.datetime time_h: Upper reporting time threshold.
        :return: List of events that passed thresholding.
        :rtype: list
        """
        result = {}
        aggregated_result = {}
        filtered = set()
        for source, events in events_aggr.items():
            for event in events:
                if not self.tcache.event_is_thresholded(event, source, time_h):
                    if source not in aggregated_result:
                        aggregated_result[source] = []
                    aggregated_result[source].append(event)
                    result[event["ID"]] = event
                else:
                    filtered.add(event["ID"])
                    self.tcache.threshold_event(event, source, abuse_group.name, severity, time_h)

        filtered -= set(result.keys())
        if result:
            self.logger.info(
                "%s: Thresholds let %d events through, %d blocked.",
                abuse_group.name,
                len(result),
                len(filtered)
            )
        else:
            self.logger.info(
                "%s: Thresholds blocked all %d events, nothing to report.",
                abuse_group.name,
                len(filtered)
            )
        return list(result.values()), aggregated_result

    def relapse_events(self, abuse_group, severity, time_h):
        """
        Detect IDEA event relapses for given abuse group settings.

        :param mentat.datatype.sqldb.GroupModel: Abuse group.
        :param str severity: Severity for which to perform reporting.
        :param datetime.datetime time_h: Upper reporting time threshold.
        :return: List of events that relapsed.
        :rtype: list
        """
        events = self.eventservice.search_relapsed_events(
            abuse_group.name,
            severity,
            time_h
        )
        if not events:
            self.logger.debug(
                "%s: No relapsed events with severity '%s' and relapse threshold TTL '%s'.",
                abuse_group.name,
                severity,
                time_h.isoformat()
            )
        else:
            self.logger.info(
                "%s: Found %d relapsed event(s) with severity '%s' and relapse threshold TTL '%s'.",
                abuse_group.name,
                len(events),
                severity,
                time_h.isoformat()
            )
        return events

    def aggregate_relapsed_events(self, relapsed):
        """
        :param dict events: Dicetionary of events aggregated by threshold key.
        :return: Events aggregated by source.
        :rtype: dict
        """
        result = []
        aggregated_result = {}
        for event in relapsed:
            result.append(record_to_idea(event))
            for key in event.keyids:
                source = self.tcache.get_source_from_cache_key(key)
                if source not in aggregated_result:
                    aggregated_result[source] = []
                aggregated_result[source].append(result[-1])
        return result, aggregated_result

    def update_thresholding_cache(self, events, settings, severity, time_h):
        """
        :param dict events: Dictionary structure with IDEA events that were reported.
        :param mentat.reports.event.ReportingSettings settings: Reporting settings.
        :param str severity: Severity for which to perform reporting.
        :param datetime.datetime time_h: Upper reporting time threshold.
        """
        ttl = time_h + settings.timing_cfg[severity]['thr']
        rel = ttl - settings.timing_cfg[severity]['rel']
        for source in events.get('regular_aggr', {}):
            for event in events['regular_aggr'][source]:
                self.tcache.set_threshold(event, source, time_h, rel, ttl)
        for source in events.get('relapsed_aggr', {}):
            for event in events['relapsed_aggr'][source]:
                self.tcache.set_threshold(event, source, time_h, rel, ttl)


    #---------------------------------------------------------------------------


    def filter_event(self, filter_rules, event, to_db=True):
        """
        Filter given event according to given list of filtering rules.

        :param list filter_rules: Filters to be used.
        :param mentat.idea.internal.Idea: Event to be filtered.
        :param bool to_db: Save hit to db.
        :return: ``True`` in case any filter matched, ``False`` otherwise.
        :rtype: bool
        """
        for flt in filter_rules:
            if self.filter_worker.filter(flt[1], event):
                if to_db:
                    flt[0].hits += 1
                    flt[0].last_hit = datetime.datetime.utcnow()
                return flt[0].name
        return False

    @staticmethod
    def aggregate_events(events):
        """
        Aggregate given list of events to dictionary structure that can be used to generate report message.

        :param dict events: Structure containing events as :py:class:`mentat.idea.internal.Idea` objects.
        :return: Dictionary structure of aggregated events.
        :rtype: dict
        """
        result = {}
        for ip in events.keys():
            for event in events[ip]:
                event_class = str(jpath_value(event, '_CESNET.EventClass') or '__UNKNOWN__')
                ip_result = result.setdefault(event_class, {}).setdefault(str(ip), {
                    "first_time": datetime.datetime.max,
                    "last_time": datetime.datetime.min,
                    "count": 0,
                    "detectors_count": {},
                    "approx_conn_count": 0,
                    "conn_count": 0,
                    "flow_count": 0,
                    "packet_count": 0,
                    "byte_count": 0,
                    "source": {
                        "hostname": {},
                        "mac": {},
                        "port": {},
                        "proto": {},
                        "url": {},
                        "email": {},
                    },
                    "target": {
                        "hostname": {},
                        "mac": {},
                        "port": {},
                        "proto": {},
                        "url": {},
                        "email": {},
                    },
                })
                ip_result["first_time"] = min(event.get("EventTime") or event["DetectTime"], ip_result["first_time"])
                ip_result["last_time"] = max(event.get("CeaseTime") or event.get("EventTime") or event["DetectTime"], ip_result["last_time"])
                ip_result["count"] += 1
                # Name of last node for identify unique detector names
                ip_result["detectors_count"][event.get("Node", [{}])[-1].get("Name")] = 1
                ip_result["approx_conn_count"] += event["ConnCount"] if event.get("ConnCount") else int(event.get("FlowCount", 0) / 2)

                for data_key, idea_key in (("conn_count", "ConnCount"), ("flow_count", "FlowCount"), ("packet_count", "PacketCount"), ("byte_count", "ByteCount")):
                    ip_result[data_key] += event.get(idea_key, 0)

                for st in ("Source", "Target"):
                    for k in ("Hostname", "MAC", "Port", "Proto", "URL", "Email"):
                        for v in jpath_values(event, st + "." + k):
                            ip_result[st.lower()][k.lower()][v] = 1

        for abuse_value in result.values():
            for ip_value in abuse_value.values():
                ip_value["detectors_count"] = len(ip_value["detectors_count"])
                ip_value["first_time"] = ip_value["first_time"].isoformat()
                ip_value["last_time"] = ip_value["last_time"].isoformat()
                for st in ("source", "target"):
                    for k in ("hostname", "mac", "port", "proto", "url", "email"):
                        ip_value[st][k] = sorted(ip_value[st][k].keys())
        return result

    def choose_attachments(self, ident, settings):
        """
        Choose appropriate report attachments based on the reporting configuration.
        """
        basedirpath = mentat.const.construct_report_dirpath(self.reports_dir, ident)

        attachment_files = []
        if settings.attachments in (mentat.const.REPORTING_ATTACH_JSON, mentat.const.REPORTING_ATTACH_ALL):
            if settings.compress:
                attachment_files.append(
                    os.path.join(
                        basedirpath,
                        "{}.json.zip".format(ident)
                    )
                )
            else:
                attachment_files.append(
                    os.path.join(
                        basedirpath,
                        "{}.json".format(ident)
                    )
                )
        if settings.attachments in (mentat.const.REPORTING_ATTACH_CSV, mentat.const.REPORTING_ATTACH_ALL):
            if settings.compress:
                attachment_files.append(
                    os.path.join(
                        basedirpath,
                        "{}.csv.zip".format(ident)
                    )
                )
            else:
                attachment_files.append(
                    os.path.join(
                        basedirpath,
                        "{}.csv".format(ident)
                    )
                )
        return self._remove_big_attachments(
            attachment_files,
            settings
        )


    #---------------------------------------------------------------------------


    def _remove_big_attachments(self, attachments, settings):
        """
        Truncate the given list of attachment files until the aggregate size of
        all attachment files is below the given limit.
        """
        if not settings.max_size:
            return attachments

        result = []
        cur_size = 0
        for attch in attachments:
            try:
                fst = os.stat(attch)
                cur_size += fst.st_size
                if cur_size > settings.max_size:
                    self.logger.warning(
                        "Attachment file %s is too big to be added to the report, because the configured limit %d would be exceeded.",
                        attch,
                        settings.max_size
                    )
                    break
                result.append(attch)
            except:  # pylint: disable=locally-disabled,bare-except
                continue
        return result

    def _save_to_json_files(self, data, filename):
        """
        Helper method for saving given data into given JSON file. This method can
        be used for saving report data attachments to disk.

        :param dict data: Data to be serialized.
        :param str filename: Name of the target JSON file.
        :return: Paths to the created files.
        :rtype: tuple
        """
        dirpath = mentat.const.construct_report_dirpath(self.reports_dir, filename)
        filepath = os.path.join(dirpath, filename)

        while True:
            try:
                with open(filepath, 'w') as jsonf:
                    json.dump(
                        data,
                        jsonf,
                        default = mentat.idea.internal.Idea.json_default,
                        sort_keys = True,
                        indent = 4
                    )
                break
            except FileNotFoundError:
                os.makedirs(dirpath)

        zipfilepath = "{}.zip".format(filepath)
        with zipfile.ZipFile(zipfilepath, mode = 'w') as zipf:
            zipf.write(filepath, compress_type = zipfile.ZIP_DEFLATED)

        return filepath, zipfilepath

    def _save_to_csv_files(self, data, filename):
        """
        Helper method for saving given data into given CSV file. This method can
        be used for saving report data attachments to disk.

        :param dict data: Data to be serialized.
        :param str filename: Name of the target CSV file.
        :return: Paths to the created files.
        :rtype: tuple
        """
        dirpath = mentat.const.construct_report_dirpath(self.reports_dir, filename)
        filepath = os.path.join(dirpath, filename)

        while True:
            try:
                with open(filepath, 'w', newline='') as csvf:
                    fieldnames = ['date_gmt', 'detected_gmt', 'analyzer', 'detector', 'classification', 'categories', 'src_ip', 'src_host', 'src_port', 'tgt_port', 'src_proto', 'tgt_proto', 'con_cnt', 'date_ts', 'detected_ts', 'note', 'impact']
                    csvwriter = csv.DictWriter(
                        csvf,
                        fieldnames = fieldnames,
                        quoting = csv.QUOTE_MINIMAL,
                        delimiter = ';'
                    )

                    csvwriter.writeheader()
                    for event in data:
                        csvwriter.writerow(csv_dict(event))
                break
            except FileNotFoundError:
                os.makedirs(dirpath)

        zipfilepath = "{}.zip".format(filepath)
        with zipfile.ZipFile(zipfilepath, mode = 'w') as zipf:
            zipf.write(filepath, compress_type = zipfile.ZIP_DEFLATED)

        return filepath, zipfilepath

    def _save_to_files(self, data, filename):
        """
        Helper method for saving given data into given file. This method can be
        used for saving copies of report messages to disk.

        :param dict data: Data to be serialized.
        :param str filename: Name of the target file.
        :return: Path to the created file.
        :rtype: str
        """
        dirpath = mentat.const.construct_report_dirpath(self.reports_dir, filename)
        filepath = os.path.join(dirpath, filename)

        while True:
            try:
                with open(filepath, 'w') as imf:
                    imf.write(data)
                break
            except FileNotFoundError:
                os.makedirs(dirpath)

        zipfilepath = "{}.zip".format(filepath)
        with zipfile.ZipFile(zipfilepath, mode = 'w') as zipf:
            zipf.write(filepath, compress_type = zipfile.ZIP_DEFLATED)

        return filepath, zipfilepath

    def render_report(self, report, settings, template_vars=None, attachment_files=None, srcip=None):
        if template_vars:
            self._get_event_class_data(template_vars["default_event_class"])
        for c in set(report.structured_data["regular"]) | set(report.structured_data["relapsed"]):
            self._get_event_class_data(c)
        # Render report section.
        template = self.renderer.get_template(
            '{}.{}_v2.txt.j2'.format(settings.template, report.type)
        )

        # Force locale to given value.
        self.set_locale(settings.locale)

        # Force timezone to given value.
        self.set_timezone(settings.timezone)

        return template.render(
            dt_c=datetime.datetime.utcnow(),
            report=report,
            source=srcip,

            settings=settings,
            text_width=REPORT_EMAIL_TEXT_WIDTH,
            additional_vars=template_vars,
            attachment_files=attachment_files,
            event_classes_data=self.event_classes_data
        )

    def _mail_report(self, report, settings, attachment_files, result, template_vars, srcip=None):
        """
        Construct email report object and send it.
        """
        # Common report email headers.
        report_msg_headers = {
            'to': settings.emails,
            'report_id': report.label,
            'report_type': report.type,
            'report_severity': report.severity,
            'report_evcount': report.evcount_rep,
            'report_window': '{}___{}'.format(report.dt_from.isoformat(), report.dt_to.isoformat()),
            'report_testdata': report.flag_testdata
        }

        message = self.render_report(report, settings, template_vars, attachment_files, srcip)

        # Report email headers specific for 'summary' reports.
        if report.type == mentat.const.REPORTING_MODE_SUMMARY:
            report_msg_headers['subject'] = self.translator.gettext(REPORT_SUBJECT_SUMMARY).format(
                report.label,
                self.translator.gettext(report.severity).title()
            )
        # Report email headers specific for 'extra' reports.
        else:
            report_msg_headers['subject'] = self.translator.gettext(REPORT_SUBJECT_EXTRA).format(
                report.label,
                self.translator.gettext(report.severity).title(),
                srcip
            )
            report_msg_headers['report_id_par'] = report.parent.label
            report_msg_headers['report_srcip']  = srcip

        report_msg_params = {
            'text_plain': message,
            'attachments': attachment_files
        }
        report_msg = self.mailer.email_send(
            ReportEmail,
            report_msg_headers,
            report_msg_params,
            settings.redirect
        )
        report.flag_mailed = True
        report.mail_to     = report_msg.get_destinations()
        report.mail_dt     = datetime.datetime.utcnow()
        result['mail_to']  = list(
            set(
                result.get('mail_to', []) + report_msg.get_destinations()
            )
        )
