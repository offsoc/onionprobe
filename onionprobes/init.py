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

# Dependencies
import os
import logging
import random

try:
    import yaml
except ImportError:
    print("Please install pyaml first!")
    raise ImportError

class OnionprobeInit:
    #
    # Initialization logic
    #

    def __init__(self, args):
        """
        Onionprobe class constructor.

        Setup instance configuration.

        :type  args: dict
        :param args: Instance arguments.
        """

        self.args = args
        self.data = []

        # Environment variable handling
        if 'ONIONPROBE_CONFIG' in os.environ and os.environ['ONIONPROBE_CONFIG'] != '':
            args.config = os.environ['ONIONPROBE_CONFIG']

        # Config file handling
        if args.config is not None:
            if os.path.exists(args.config):
                with open(args.config, 'r') as config:
                    self.config = yaml.load(config, yaml.CLoader)
            else:
                raise FileNotFoundError('No such file ' + args.config)
        else:
            self.config = {}

    def initialize(self):
        """
        Onionprobe initialization procedures

        Initializes all Onionprobe subsystems, like the random number generator,
        logging, metrics and a Tor daemon instance.

        :rtype: bol
        :return: True if initialization is successful, False on error
        """

        # Initializes the random number generator
        random.seed()

        # Initializes logging
        if self.initialize_logging() is False:
            return False

        # Initializes the Tor daemon
        if self.initialize_tor() is False:
            return False

        # Authenticate with the Tor daemon
        if self.initialize_tor_auth() is False:
            return False

        # Stream management
        # See https://stem.torproject.org/tutorials/to_russia_with_love.html
        if self.get_config('new_circuit'):
            self.controller.set_conf('__LeaveStreamsUnattached', '1')
            self.controller.add_event_listener(self.new_circuit, stem.control.EventType.STREAM)

            self.circuit_id = None

        # Initialize the Prometheus exporter
        if self.get_config('prometheus_exporter'):
            # Enforce continuous run
            self.config['loop'] = True

            if self.initialize_prometheus_exporter() is False:
                return False

        # Initialize metrics
        self.initialize_metrics()

        return True
