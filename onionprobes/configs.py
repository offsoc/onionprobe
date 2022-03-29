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

# The base path for this project
basepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir) + os.sep

class OnionprobeConfigCompiler:
    """Base class to build Onionprobe configs from external sources of Onion Services"""

    def __init__(self, databases):
        """
        Constructor for the OnionprobeConfigCompiler class.

        Loads the default Onionprobe configuration to be used as a template.

        Keeps the dictionary of Onion Services databases as a class attribute.

        :type  databases: dict
        :param databases: Dictionary of data sources to fetch .onion sites.
                          Format is { 'database_name': 'database_url' }
        """

        # Save the databases of Onion Services
        self.databases = databases

        # Determine the default configuration file
        default_config = os.path.join(basepath, 'configs', 'tor.yaml')

        # Load the default configuration file as a template
        if os.path.exists(default_config):
            with open(default_config, 'r') as config:
                self.config = yaml.load(config, yaml.CLoader)

    def build_endpoints_config(self, database):
        """
        Build the Onion Service endpoints dictionary.

        This method is only a placeholder.

        By default this method returns an empty dictionary as it's meant to be
        overriden by specific implementations inheriting from the
        OnionprobeConfigCompiler base class and where custom logic for
        extracting .onion endpoints from external databases should be located.

        :type database : str
        :param database: A database name from the databases dictionary. This
                         parameter allows accesing the URL of the external
                         database from the self.databases class attribute.

        :rtype: dict
        :return: Onion Service endpoints in the format accepted by Onionprobe.
        """

        return dict()

    def build_onionprobe_config(self):
        """
        Build an Onionprobe config.

        Writes an Onionprobe-compatible configuration file for each database
        listed in self.databases attribute.

        The Onion Service endpoints are generated from the
        build_endpoints_config() methods. To be effective, it's required that
        classes inheriting from this base class to implement the
        build_endpoints_configs() method.

        The filenames ared derived from the database names (each key from the
        self.databases attribute).
        """

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
