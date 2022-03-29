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
import logging

try:
    import stem
except ImportError:
    print("Please install stem library first!")
    raise ImportError

class OnionprobeDescriptor:
    """
    Onionprobe class with Tor descriptor-related methods.
    """

    def get_pubkey_from_address(self, address):
        """
        Extract .onion pubkey from the address

        Leaves out the .onion domain suffix and any existing subdomains.

        :type  address: str
        :param address: Onion Service address

        :rtype: str
        :return: Onion Service public key
        """

        # Extract
        pubkey = address[0:-6].split('.')[-1]

        return pubkey

    def get_descriptor(self, endpoint, config):
        """
        Get Onion Service descriptor from a given endpoint

        :type  endpoint: str
        :param endpoint: The endpoint name from the 'endpoints' instance config.

        :type  config: dict
        :param config: Endpoint configuration

        :rtype: stem.descriptor.hidden_service.InnerLayer or False
        :return: The Onion Service descriptor inner layer on success.
                 False on error.
        """

        self.log('Getting descriptor for {}...'.format(config['address']))

        pubkey    = self.get_pubkey_from_address(config['address'])
        init_time = self.now()

        # Get the descriptor
        try:
            descriptor = self.controller.get_hidden_service_descriptor(pubkey)

        except stem.DescriptorUnavailable as e:
            self.metrics['onion_service_descriptor_reachable'].labels(
                        name=endpoint,
                        address=config['address'],
                    ).set(0)

            self.metrics['onion_service_descriptor_fetch_error_counter'].labels(
                        name=endpoint,
                        address=config['address'],
                    ).inc()

            return False

        except stem.Timeout as e:
            return False

        except stem.ControllerError as e:
            return False

        except ValueError as e:
            return False

        # Ensure it's converted to the v3 format
        #
        # See https://github.com/torproject/stem/issues/96
        #     https://stem.torproject.org/api/control.html#stem.control.Controller.get_hidden_service_descriptor
        #     https://gitlab.torproject.org/legacy/trac/-/issues/25417
        from stem.descriptor.hidden_service import HiddenServiceDescriptorV3
        descriptor = HiddenServiceDescriptorV3.from_str(str(descriptor))

        # Decrypt the inner layer
        inner = descriptor.decrypt(pubkey)

        # Get introduction points
        # See https://stem.torproject.org/api/descriptor/hidden_service.html#stem.descriptor.hidden_service.IntroductionPointV3
        #for introduction_point in inner.introduction_points:
        #    self.log(introduction_point.link_specifiers, 'debug')

        elapsed = self.elapsed(init_time, True)

        self.metrics['onion_service_descriptor_latency'].labels(
                    name=endpoint,
                    address=config['address'],
                ).set(elapsed)

        self.metrics['onion_service_descriptor_reachable'].labels(
                    name=endpoint,
                    address=config['address'],
                ).set(1)

        # Return the inner layer
        return inner
