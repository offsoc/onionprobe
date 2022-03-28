#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Compile an Onionprobe configuration file from the "Real-World Onion Sites"
# repository.
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
import csv
import urllib.parse

from io import StringIO

try:
    import yaml
except ImportError:
    print("Please install pyaml first!")
    raise ImportError

try:
    import requests
except ImportError:
    print("Please install requests first!")
    raise ImportError

# Parameters
basepath  = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir) + os.sep
databases = {
        'real-world-onion-sites' : 'https://github.com/alecmuffett/real-world-onion-sites/raw/master/master.csv',
        'securedrop'             : 'https://github.com/alecmuffett/real-world-onion-sites/raw/master/securedrop-api.csv',
        }

class RealWorldOnionSites:
    """Handles the 'Real-World Onion Sites' database"""

    def __init__(self):
        default_config = os.path.join(basepath, 'onionprobe.yaml')

        if os.path.exists(default_config):
            with open(default_config, 'r') as config:
                self.config = yaml.load(config, yaml.CLoader)

    def build_onionprobe_config(self):
        for database in databases:
            try:
                result    = requests.get(databases[database])
                sheet     = csv.DictReader(StringIO(result.text))
                endpoints = {}

                for row in sheet:
                    url      = urllib.parse.urlparse(row['onion_url'])
                    address  = url.netloc
                    protocol = url.scheme
                    port     = 80 if url.scheme == 'http' else 443
                    paths    = [{
                        'path': url.path,
                        }]

                    if row['site_name'] not in endpoints:
                        endpoints[row['site_name']] = {
                                'address' : address,
                                'protocol': protocol,
                                'port'    : port,
                                'paths'   : paths,
                                }

                # Create a new config using the default as base
                config = dict(self.config)

                # Replace the endpoints
                config['endpoints'] = endpoints

                # Save
                with open(os.path.join(basepath, 'contrib', database + '.yaml'), 'w') as output:
                    output.write(yaml.dump(config))

            except Exception as e:
                print(e)

            else:
                pass

if __name__ == "__main__":
    """Process from CLI"""

    instance = RealWorldOnionSites()

    instance.build_onionprobe_config()
