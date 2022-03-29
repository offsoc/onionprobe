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
import argparse
import random
import io

from onionprobes.time       import OnionprobeTime
from onionprobes.init       import OnionprobeInit
from onionprobes.config     import OnionprobeConfig
from onionprobes.logger     import OnionprobeLogger
from onionprobes.tor        import OnionprobeTor
from onionprobes.descriptor import OnionprobeDescriptor
from onionprobes.metrics    import OnionprobeMetrics
from onionprobes.prober     import OnionprobeProber
from onionprobes.http       import OnionprobeHTTP

class Onionprobe(
        # Inherit from subsystems
        OnionprobeInit,
        OnionprobeConfig,
        OnionprobeLogger,
        OnionprobeTime,
        OnionprobeTor,
        OnionprobeDescriptor,
        OnionprobeMetrics,
        OnionprobeProber,
        OnionprobeHTTP,
        ):
    """
    Onionprobe class to test and monitor Tor Onion Services
    """

    #
    # Main application logic
    #

    def run(self):
        """
        Main application loop

        Checks if should be run indefinitely.
        Then dispatch to a round of probes.

        If runs continuously, waits before starting the next round.

        If not, just returns.
        """

        # Check if should loop
        if self.get_config('loop'):
            while True:
                # Call for a round
                self.round()

                # Then wait
                self.wait(self.get_config('sleep'))

        else:
            # Single pass, only one round
            self.round()

    def round(self):
        """
        Process a round of probes

        Each round is composed of the entire set of the endpoints
        which is optionally shuffled.

        Each endpoint is then probed.
        """

        # Shuffle the deck
        endpoints = sorted(self.get_config('endpoints'))

        if self.get_config('shuffle'):
            # Reinitializes the random number generator to avoid predictable
            # results if running countinuously for long periods.
            random.seed()

            endpoints = random.sample(endpoints, k=len(endpoints))

        # Probe each endpoint
        for key, endpoint in enumerate(endpoints):
            self.metrics['onionprobe_state'].state('probing')

            result = self.probe(endpoint)

            # Wait if not last endpoint
            if key != len(endpoints) - 1:
                self.wait(self.get_config('interval'))

    #
    # Cleansing methods
    #

    def close(self):
        """
        Onionprobe teardown procedure.

        Change the internal metrics state to running.

        Stops the built-in Tor daemon.
        """

        self.metrics['onionprobe_state'].state('stopping')
        self.controller.close()

        # Terminate built-in Tor
        if 'tor' in dir(self):
            self.tor.kill()

if __name__ == "__main__":
    """Process from CLI"""

    epilog = """Examples:

      onionprobe -c config.yaml
    """

    description = 'Test and monitor onion services'
    parser      = argparse.ArgumentParser(
                    description=description,
                    epilog=epilog,
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                  )

    parser.add_argument('-c', '--config', help='Read options from configuration file')

    args = parser.parse_args()

    # Dispatch
    try:
        probe = Onionprobe(args)

        if probe.initialize() is not False:
            probe.run()
            probe.close()
        else:
            print('Error: could not initialize')
            exit(1)

    #except (FileNotFoundError, KeyboardInterrupt) as e:
    except Exception as e:
        probe.log(e, 'error')
        probe.close()
        exit(1)
