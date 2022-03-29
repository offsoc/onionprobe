#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Compile an Onionprobe configuration file from the Secure Drop API.
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
import json
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
        'securedrop': 'https://securedrop.org/api/v1/directory/?format=json',
        }

class SecureDropSites(OnionprobeConfigCompiler):
    """Handles the Secure Drop API database"""

    def build_endpoints_config(self, database):
        result    = requests.get(self.databases[database])
        data      = json.load(StringIO(result.text))
        endpoints = {}

        for item in data:
            #url      = urllib.parse.urlparse(item['onion_address'])
            #address  = url.netloc
            #protocol = url.scheme if url.scheme != '' else 'http'
            #port     = 80 if protocol == 'http' else 443
            #paths    = [{
            #    'path': url.path if url.path != '' else '/',
            #    }]
            address  = item['onion_address']
            protocol = 'http'
            port     = 80
            paths    = [{
                'path': '',
                }]

            if item['title'] not in endpoints:
                #endpoints[item['onion_name']] = {
                endpoints[item['title']] = {
                        'address' : address,
                        'protocol': protocol,
                        'port'    : port,
                        'paths'   : paths,
                        }

        return endpoints

if __name__ == "__main__":
    """Process from CLI"""

    instance = SecureDropSites(databases)

    instance.build_onionprobe_config()
