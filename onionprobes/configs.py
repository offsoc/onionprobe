#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Handle Onionprobe configurations.
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

try:
    import yaml
except ImportError:
    print("Please install pyaml first!")
    raise ImportError

basepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir) + os.sep

class OnionprobeConfigCompiler:
    """Build an Onionprobe config from an external source of .onion sites"""

    def __init__(self, databases):
        self.databases = databases
        default_config = os.path.join(basepath, 'configs', 'tor.yaml')

        if os.path.exists(default_config):
            with open(default_config, 'r') as config:
                self.config = yaml.load(config, yaml.CLoader)

    def build_onionprobe_config(self):
        for database in self.databases:
            try:
                # Build list of endpoints
                endpoints = self.build_endpoints_config(database)

                # Create a new config using the default as base
                config = dict(self.config)

                # Replace the endpoints
                config['endpoints'] = endpoints

                # Save
                with open(os.path.join(basepath, 'configs', database + '.yaml'), 'w') as output:
                    output.write(yaml.dump(config))

            except Exception as e:
                print(e)
