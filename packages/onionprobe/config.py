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
import argparse

try:
    import yaml
except ImportError:
    print("Please install pyaml first!")
    raise ImportError

# The Onionprobe version string
# Uses Semantic Versioning 2.0.0
# See https://semver.org
onionprobe_version = '0.2.2'

# The base path for this project
basepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir) + os.sep

# Describe configuration options
config = {
        'log_level': {
            'description': 'Log level: debug, info, warning, error or critical',
            'default': 'info',
            'argparse_action': 'store',
            },

        'launch_tor': {
            'description': "Whether to launch it's own Tor daemon (set to false to use the system-wide Tor process)",
            'default': True,
            'argparse_action': argparse.BooleanOptionalAction,
            },

        'tor_address': {
            'description': 'Tor listening address if the system-wide service is used',
            'default': '127.0.0.1',
            'argparse_action': 'store',
            },

        'socks_port': {
            'description': 'Tor SOCKS port',
            'default': 19050,
            'argparse_action': 'store',
            },

        'control_port': {
            'description': 'Tor control port',
            'default': 19051,
            'argparse_action': 'store',
            },

        'control_password': {
            'description': 'Set Tor control password or use a password prompt (system-wide Tor service) or auto-generate a temporary password (built-in Tor service)',
            'default': None,
            'argparse_action': 'store',
            },

        'loop': {
            'description': 'Run Onionprobe continuously',
            'default': False,
            'argparse_action': argparse.BooleanOptionalAction,
            },

        'prometheus_exporter': {
            'description': 'Enable Prometheus exporting functionality',
            'default': False,
            'argparse_action': argparse.BooleanOptionalAction,
            },

        'prometheus_exporter_port': {
            'description': 'Set the Prometheus exporter port',
            'default': 9091,
            'argparse_action': 'store',
            },

        'shuffle': {
            'description': 'Shuffle the list of endpoints at each probing round',
            'default': True,
            'argparse_action': argparse.BooleanOptionalAction,
            },

        'randomize': {
            'description': 'Randomize the interval between each probing',
            'default': True,
            'argparse_action': argparse.BooleanOptionalAction,
            },

        'new_circuit': {
            'description': 'Get a new circuit for every stream',
            'default': False,
            'argparse_action': argparse.BooleanOptionalAction,
            },

        'interval': {
            'description': 'Max random interval in seconds between probing each endpoint',
            'default': 60,
            'argparse_action': 'store',
            },

        'sleep': {
            'description': 'Max random interval in seconds to wait between each round of tests',
            'default': 60,
            'argparse_action': 'store',
            },

        'descriptor_max_retries': {
            'description': 'Max retries when fetching a descriptor',
            'default': 5,
            'argparse_action': 'store',
            },

        'descriptor_timeout': {
            'description': 'Timeout in seconds when retrieving an Onion Service descriptor',
            'default': 30,
            'argparse_action': 'store',
            },

        'http_connect_timeout': {
            'description': 'Connection timeout for HTTP/HTTPS requests',
            'default': 30,
            'argparse_action': 'store',
            },

        'http_connect_max_retries': {
            'description': 'Max retries when doing a HTTP/HTTPS connection to an Onion Service',
            'default': 3,
            'argparse_action': 'store',
            },

        'http_read_timeout': {
            'description': 'Read timeout for HTTP/HTTPS requests',
            'default': 30,
            'argparse_action': 'store',
            },

        'circuit_stream_timeout': {
            'description': 'Sets how many seconds until a stream is detached from a circuit and try a new circuit',
            'default': 60,
            'argparse_action': 'store',
            },

        'endpoints': {
            'description': 'The list of endpoints to be tested',
            'default': {
                'www.torproject.org': {
                    'address' : '2gzyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid.onion',
                    'protocol': 'http',
                    'port'    : '80',
                    'paths'   : [
                        {
                            'path'   : '/',
                            'pattern': 'Tor Project',
                            },
                        ],
                    },
                }
            },
        }

def cmdline():
    """
    Evalutate the command line.

    :return: Command line arguments.
    """

    epilog = """Examples:

      onionprobe -c configs/tor.yaml
      onionprobe -e http://2gzyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid.onion
    """

    epilog += """\nAvailable metrics:
    """

    from .metrics import metrics

    for metric in metrics:
        item = metrics[metric].describe()[0]

        epilog += "\n  {}:\n        {}".format(item.name, item.documentation)

    description = 'Test and monitor onion services'
    parser      = argparse.ArgumentParser(
                    description=description,
                    epilog=epilog,
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                  )

    parser.add_argument('-c', '--config', help='Read options from configuration file')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + onionprobe_version)

    for argument in sorted(config):
        if argument == 'endpoints':
            parser.add_argument('-e', '--endpoints', nargs='*', help='Add endpoints to the test list', metavar="ONION-ADDRESS1")

        else:
            parser.add_argument(
                    '--' + argument,
                    help=config[argument]['description'],
                    default=config[argument]['default'],
                    type=type(config[argument]['default']),
                    action=config[argument]['argparse_action'],
                    )

    args = parser.parse_args()

    if args.config is None and args.endpoints is None:
        parser.print_usage()
        exit(1)

    return args

class OnionprobeConfig:
    """
    Onionprobe class with configuration-related methods.
    """

    def get_config(self, item, default = None):
        """
        Helper to get instance configuration

        Retrieve a config parameter from the self.config object or use a
        default value as fallback

        :type  item: str
        :param item: Configuration item name

        :param default: Default config value to be used as a fallback if there's
                        no self.config[item] available.
                        Defaults to None

        :return: The configuration parameter value or the default fallback value.
        """

        if item in self.config:
            return self.config[item]

        # Optionally override the default with an argument provided
        elif default is not None:
            self.config[item] = default

            return default

        return config[item]['default']

class OnionprobeConfigCompiler:
    """Base class to build Onionprobe configs from external sources of Onion Services"""

    def __init__(self, databases, template_config = None, output_path = None):
        """
        Constructor for the OnionprobeConfigCompiler class.

        Loads the default Onionprobe configuration to be used as a template.

        Keeps the dictionary of Onion Services databases as a class attribute.

        :type  databases: dict
        :param databases: Dictionary of data sources to fetch .onion sites.
                          Format is { 'database_name': 'database_url' }

        :type  template_config: str
        :param template_config: Configuration file path to be used as template

        :type  output_path: str
        :param output_path: Output folder where configs are written
        """

        # Save the databases of Onion Services
        self.databases = databases

        # Determine the default configuration file
        if template_config is None:
            template_config = os.path.join(basepath, 'configs', 'tor.yaml')

        # Determine the output path
        if output_path is None:
            self.output_path = os.path.join(basepath, 'configs')
        else:
            self.output_path = output_path

        # Load the default configuration file as a template
        if os.path.exists(template_config):
            with open(template_config, 'r') as config:
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
                with open(os.path.join(self.output_path, database + '.yaml'), 'w') as output:
                    output.write(yaml.dump(config))

            except Exception as e:
                print(e)
