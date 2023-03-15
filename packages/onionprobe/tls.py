#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Onionprobe test/monitor tool.
#
# Copyright (C) 2023 Silvio Rhatto <rhatto@torproject.org>
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

try:
    import socks
except ImportError:
    print("Please install PySocks first!")
    raise ImportError

import ssl

class OnionprobeTLS:
    """
    Onionprobe class with TLS methods.
    """

    def get_certificate(self, endpoint, config, attempt = 1):
        """
        Gets the endpoint's TLS certificate.

        :type  endpoint: str
        :param endpoint: The endpoint name from the 'endpoints' instance config.

        :type  config: dict
        :param config: Endpoint configuration

        :type  attempt: int
        :param attempt: The current attempt used to determine the maximum number of retries.

        """

        tor_address            = self.get_config('tor_address')
        socks_port             = self.get_config('socks_port')
        timeout                = self.get_config('http_connect_timeout')
        port                   = int(config['port']) if 'port' in config else 443
        context                = ssl.create_default_context()
        context.check_hostname = False

        self.log('Retrieving X.509 certificate from {} on port {}...'.format(config['address'], port))

        try:
            with socks.create_connection(
                    (config['address'], port),
                    timeout=timeout, proxy_type=socks.SOCKS5,
                    proxy_addr=tor_address, proxy_port=socks_port, proxy_rdns=True) as sock:
                with context.wrap_socket(sock, server_hostname=config['address']) as tls:
                    cert_info = tls.getpeercert()
                    result    = True

                    print(tls.version())
                    print(cert_info)

        except ssl.SSLZeroReturnError as e:
            result  = False
            error   = e.reason

            self.log(e, 'error')

        except ssl.SSLWantReadError as e:
            result  = False
            error   = e.reason

            self.log(e, 'error')

        except ssl.SSLWantWriteError as e:
            result  = False
            error   = e.reason

            self.log(e, 'error')

        except ssl.SSLSyscallError as e:
            result  = False
            error   = e.reason

            self.log(e, 'error')

        except ssl.SSLEOFError as e:
            result  = False
            error   = e.reason

            self.log(e, 'error')

        except ssl.SSLCertVerificationError as e:
            result  = False
            error   = e.reason

            self.log(e, 'error')

        except ssl.CertificateError as e:
            result  = False
            error   = e.reason

            self.log(e, 'error')

        except ssl.SSLError as e:
            result  = False
            error   = e.reason

            self.log(e, 'error')

        except socks.GeneralProxyError as e:
            result = False
            error  = e.socket.err

            self.log(e, 'error')

        except socks.SOCKS5AuthError as e:
            result = False
            error  = e.socket.err

            self.log(e, 'error')

        except socks.SOCKS5Error as e:
            result = False
            error  = e.socket.err

            self.log(e, 'error')

        except socks.HTTPError as e:
            result = False
            error  = e.socket.err

            self.log(e, 'error')

        except Exception as e:
            result = False

            self.log(e, 'error')

        return result
