#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Onionprobe test/monitor tool.
#
# Copyright (C) 2022 Silvio Rhatto <rhatto@torproject.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License,
# or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from .config import onionprobe_version

class OnionprobeMetrics:
    """
    Onionprobe class with metrics methods.
    """

    def initialize_prometheus_exporter(self):
        """
        Initialize the Prometheus Exporter
        """

        from prometheus_client import start_http_server

        port = self.get_config('prometheus_exporter_port')

        self.log('Initializing Prometheus HTTP exporter server at port %s...' % (port))
        start_http_server(port)

    def initialize_metrics(self):
        """
        Initialize the metrics subsystem

        It uses Prometheus metrics even if the Prometheus exporter is not in use.

        This means that the Prometheus metrics are always used, even if only for
        internal purposes, saving resources from preventing us to build additional
        metric logic.
        """

        # Import Prometheus data types
        from prometheus_client import Counter, Gauge, Info, Enum

        # The metrics object
        self.metrics = {
            #
            # Metametrics: data about the Onionprobe instance itself
            #

            'onionprobe_version': Info(
                'onionprobe_version',
                'Onionprobe version info',
                ),

            'onionprobe_state': Enum(
                'onionprobe_state',
                'Onionprobe latest state',
                states=['starting', 'probing', 'sleeping', 'stopping']
                ),

            #
            # Probing gauges: the basic data
            #

            'onionprobe_wait': Gauge(
                    'onionprobe_wait',
                    'How long onionprobe waited between two probes',
                ),

            'onion_service_latency': Gauge(
                    'onion_service_latency',
                    'Register Onion Service connection latency in seconds',
                    ['name', 'address', 'protocol', 'port', 'path']
                ),

            'onion_service_reachable': Gauge(
                    'onion_service_reachable',
                    'Register if the Onion Service is reachable: value is 1 for reachability and 0 otherwise',
                    ['name', 'address', 'protocol', 'port', 'path']
                ),

            'onion_service_status_code': Gauge(
                    'onion_service_status_code',
                    'Register Onion Service connection HTTP status code',
                    ['name', 'address', 'protocol', 'port', 'path']
                ),

            'onion_service_descriptor_latency': Gauge(
                    'onion_service_descriptor_latency',
                    'Register Onion Service latency in seconds to get the descriptor',
                    ['name', 'address']
                ),

            'onion_service_descriptor_reachable': Gauge(
                    'onion_service_descriptor_reachable',
                    'Register if the Onion Service descriptor is available: value is 1 for reachability and 0 otherwise',
                    ['name', 'address']
                ),

            'onion_service_match_pattern_matched': Gauge(
                    'onion_service_pattern_matched',
                    'Register a regular expression pattern is matched when connection to the Onion Service: value is 1 for matched pattern and 0 otherwise',
                    ['name', 'address', 'protocol', 'port', 'path', 'pattern']
                ),

            #
            # Probing counters
            #

            'onion_service_fetch_error_counter': Counter(
                    'onion_service_fetch_error_counter',
                    'Counts errors when fetching an Onion Service',
                    ['name', 'address']
                ),

            'onion_service_descriptor_fetch_error_counter': Counter(
                    'onion_service_descriptor_fetch_error_counter',
                    'Counts errors when fetching an Onion Service descriptor',
                    ['name', 'address', 'protocol', 'port', 'path']
                ),

            #
            # Requests exception counter
            #

            # Counter for requests.RequestException
            'onion_service_request_exception': Counter(
                    'onion_service_request_exception',
                    'Counts Onion Service general exception errors',
                    ['name', 'address', 'protocol', 'port', 'path']
                ),

            # Counter for requests.ConnectionError
            'onion_service_connection_error': Counter(
                    'onion_service_connection_error',
                    'Counts Onion Service connection errors',
                    ['name', 'address', 'protocol', 'port', 'path']
                ),

            # Counter for requests.HTTPError
            'onion_service_http_error': Counter(
                    'onion_service_http_error',
                    'Counts Onion Service HTTP errors',
                    ['name', 'address', 'protocol', 'port', 'path']
                ),

            # Counter for requests.TooManyRedirects
            'onion_service_too_many_redirects': Counter(
                    'onion_service_too_many_redirects',
                    'Counts Onion Service too many redirects errors',
                    ['name', 'address', 'protocol', 'port', 'path']
                ),

            # Counter for requests.ConnectionTimeout
            'onion_service_connection_timeout': Counter(
                    'onion_service_connection_timeout',
                    'Counts Onion Service connection timeouts',
                    ['name', 'address', 'protocol', 'port', 'path']
                ),

            # Counter for requests.ReadTimeout
            'onion_service_read_timeuot': Counter(
                    'onion_service_read_timeout',
                    'Counts Onion Service read timeouts',
                    ['name', 'address', 'protocol', 'port', 'path']
                ),

            # Counter for requests.Timeout
            'onion_service_timeout': Counter(
                    'onion_service_timeout',
                    'Counts Onion Service timeouts',
                    ['name', 'address', 'protocol', 'port', 'path']
                ),
            }

        # Set version
        self.metrics['onionprobe_version'].info({
            'version': onionprobe_version,
            })

        # Set initial state
        self.metrics['onionprobe_state'].state('starting')
