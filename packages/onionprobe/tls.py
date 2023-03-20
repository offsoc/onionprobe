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

    def query_tls(self, endpoint, config, attempt = 1):
        """
        Tries a TLS connection to the endpoint and update metrics when needed.

        This method does not make any certificate verification upfront when
        connecting to the remote endpoint. This is on purpose, since this is
        just a test procedure to get TLS and certificate information.

        Certificate validity check is already done at OnionprobeHTTP.query_http().

        :type  endpoint: str
        :param endpoint: The endpoint name from the 'endpoints' instance config.

        :type  config: dict
        :param config: Endpoint configuration

        :type  attempt: int
        :param attempt: The current attempt used to determine the maximum
                        number of retries.

        :rtype: bool
        :return: True if the connection succeeded.
                 False on error.

        """

        tor_address = self.get_config('tor_address')
        socks_port  = self.get_config('socks_port')
        timeout     = self.get_config('tls_connect_timeout')
        port        = int(config['port']) if 'port' in config else 443

        # Approach to use when always checking the certificate
        #context                = ssl.create_default_context()
        #context.check_hostname = True
        #context.verify_mode    = ssl.CERT_REQUIRED
        #valid_cert             = 1

        # Approach to use to retrieve whichever certificate, no matter whether it's valid or not
        context                = ssl.SSLContext()
        context.check_hostname = False
        context.verify_mode    = ssl.CERT_NONE
        valid_cert             = 1

        # Metric labels
        labels = {
                'name'    : endpoint,
                'address' : config['address'],
                'port'    : config['port'],
                }

        try:
            self.log('Trying to do a TLS connection to {} on port {} (attempt {})...'.format(
                config['address'], config['port'], attempt))

            with socks.create_connection(
                    (config['address'], port),
                    timeout=timeout, proxy_type=socks.SOCKS5,
                    proxy_addr=tor_address, proxy_port=socks_port, proxy_rdns=True) as sock:
                with context.wrap_socket(sock, server_hostname=config['address']) as tls:
                    result = True

                    self.log('TLS connection succeeded at {} on port {}'.format(
                            config['address'], config['port']))

                    if self.get_config('get_certificate_info'):
                        cert_result = self.get_certificate(endpoint, config, tls)

                    self.info_metric('onion_service_tls_info', {
                        'version'    : tls.version(),
                        'compression': tls.compression(),
                        'cipher'     : tls.cipher(),
                        'stats'      : context.session_stats(),
                        'alpn'       : tls.selected_alpn_protocol(),
                        'npn'        : tls.selected_npn_protocol(),
                        },
                        labels)

        except ssl.SSLZeroReturnError as e:
            result    = False
            error     = e.reason
            exception = 'ssl_zero_return_error'

            self.log(e, 'error')

        except ssl.SSLWantReadError as e:
            result    = False
            error     = e.reason
            exception = 'ssl_want_read_error'

            self.log(e, 'error')

        except ssl.SSLWantWriteError as e:
            result    = False
            error     = e.reason
            exception = 'ssl_want_write_error'

            self.log(e, 'error')

        except ssl.SSLSyscallError as e:
            result    = False
            error     = e.reason
            exception = 'ssl_syscall_error'

            self.log(e, 'error')

        except ssl.SSLEOFError as e:
            result    = False
            error     = e.reason
            exception = 'ssl_eof_error'

            self.log(e, 'error')

        except ssl.SSLCertVerificationError as e:
            result     = False
            error      = e.reason
            exception  = 'ssl_cert_verification_error'
            valid_cert = 0

            self.log(e, 'error')

        except ssl.CertificateError as e:
            result    = False
            error     = e.reason
            exception = 'ssl_certificate_error'

            self.log(e, 'error')

        except ssl.SSLError as e:
            result    = False
            error     = e.reason
            exception = 'ssl_error'

            self.log(e, 'error')

        except socks.GeneralProxyError as e:
            result    = False
            error     = e.socket.err
            exception = 'general_proxy_error'

            self.log(e, 'error')

        except socks.SOCKS5AuthError as e:
            result    = False
            error     = e.socket.err
            exception = 'socks5_auth_error'

            self.log(e, 'error')

        except socks.SOCKS5Error as e:
            result    = False
            error     = e.socket.err
            exception = 'socks5_error'

            self.log(e, 'error')

        except socks.HTTPError as e:
            result    = False
            error     = e.socket.err
            exception = 'http_error'

            self.log(e, 'error')

        except Exception as e:
            result    = False
            exception = 'general_error'

            self.log(e, 'error')

        finally:
            #reachable = 0 if result is False else 1

            if result is False:
                retries = self.get_config('tls_connect_max_retries')

                # Try again until max retries is reached
                if attempt <= retries:
                    return self.query_tls(endpoint, config, attempt + 1)

            # Register the number of TLS attempts on metrics
            #
            # This may be redundant with what's already done at
            # OnionprobeHTTP.query_http(), so that's why it's commented.
            # This could also be controlled by a flag.
            #labels['reachable'] = reachable
            #self.set_metric('onion_service_tls_connection_attempts', attempt, labels)

            return result
