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

from io      import StringIO
from configs import OnionprobeConfigCompiler, basepath

try:
    import requests
except ImportError:
    print("Please install requests first!")
    raise ImportError

# Parameters
databases = {
        'real-world-onion-sites' : 'https://github.com/alecmuffett/real-world-onion-sites/raw/master/master.csv',
        #'securedrop'            : 'https://github.com/alecmuffett/real-world-onion-sites/raw/master/securedrop-api.csv',
        }

class RealWorldOnionSites(OnionprobeConfigCompiler):
    """Handles the 'Real-World Onion Sites' database"""

    def build_endpoints_config(self, database):
        result    = requests.get(self.databases[database])
        data      = csv.DictReader(StringIO(result.text))
        endpoints = {}

        for item in data:
            url      = urllib.parse.urlparse(item['onion_url'])
            address  = url.netloc
            protocol = url.scheme if url.scheme != '' else 'http'
            port     = 80 if protocol == 'http' else 443
            paths    = [{
                'path': url.path if url.path != '' else '/',
                }]

            if item['site_name'] not in endpoints:
                endpoints[item['site_name']] = {
                        'address' : address,
                        'protocol': protocol,
                        'port'    : port,
                        'paths'   : paths,
                        }

        return endpoints

if __name__ == "__main__":
    """Process from CLI"""

    instance = RealWorldOnionSites(databases)

    instance.build_onionprobe_config()
