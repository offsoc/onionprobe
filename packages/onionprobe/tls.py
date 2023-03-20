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

from datetime import timezone

from cryptography.x509              import load_pem_x509_certificate, oid, DNSName
from cryptography.hazmat.primitives import hashes

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

    def get_dns_alt_names_from_cert(self, cert, format='tuple'):
        """
        Get the DNS names from a X.509 certificate's SubjectAltName extension.

        :type  cert: cryptography.x509.Certificate
        :param cert: The X.509 Certificate object.

        :type  format: str
        :param format: The output format, either 'list' or 'tuple' in the
                       same format returned by SSLSocket.getpeercert and
                       accepted by ssl.match_hostname.

        :rtype: list or tuple
        :return: The list or tuple with the certificate's DNS Subject
                 Alternative Names.

        """

        dns_alt_names = cert.extensions.get_extension_for_oid(
                oid.ExtensionOID.SUBJECT_ALTERNATIVE_NAME
                ).value.get_values_for_type(DNSName)

        if format == 'tuple':
            dns_alt_names = tuple(('DNS', item) for item in dns_alt_names)

        return dns_alt_names

    def get_cert_rdns(self, cert, field = 'issuer', format = 'tuple'):
        """
        Get the Relative Distinguished Names (RDNs) from a given X.509
        certificate field like issuer or subject.

        :type field: str
        :param field: The name of the X.509 certificate field
                      ('issuer' or 'subject').

        :type  format: str
        :param format: The output format, either 'list' or 'tuple' in the
                       same format returned by SSLSocket.getpeercert and
                       accepted by ssl.match_hostname.

        :rtype: dict or tuple
        :return: The dict or tuple with the certificate's DNS Subject
                 Alternative Names.

        :type  cert: cryptography.x509.Certificate
        :param cert: The X.509 Certificate object.

        """

        items = {}

        for item in getattr(cert, field):
            name = item.oid._name

            if name not in items:
                items[name] = []

            items[name].append(item.value)

        if format == 'dict':
            return items

        result = []

        for name in items:
            result.append(tuple((name, item) for item in items[name]))

        return tuple(result)

    def get_cert_info(self, cert):
        """
        Get basic information from a X.509 certificate.

        :type  cert: cryptography.x509.Certificate
        :param cert: The X.509 Certificate object.

        :rtype: dict
        :return: Dictionary with basic certificate information in the same
                 format returned by SSLSocket.getpeercert and accepted by
                 ssl.match_hostname.

        """

        # Date format is the same from ssl.cert_time_to_seconds
        date_format = '%b %d %H:%M:%S %Y %Z'

        # The info dictionary
        info = {
                'issuer'           : self.get_cert_rdns(cert, 'issuer'),

                # Convert to aware datetime formats since
                # cryptography.x509.Certificate uses naive objects by default
                'notAfter'         : cert.not_valid_after.replace(tzinfo=timezone.utc).strftime(date_format),
                'notBefore'        : cert.not_valid_before.replace(tzinfo=timezone.utc).strftime(date_format),

                'serialNumber'     : str(cert.serial_number),
                'subject'          : self.get_cert_rdns(cert, 'subject'),
                'subjectAltName'   : self.get_dns_alt_names_from_cert(cert),
                'version'          : int(str(cert.version).replace('Version.v', '')),

                'fingerprintSHA1'  : cert.fingerprint(hashes.SHA1()).hex(':').upper(),
                'fingerprintSHA256': cert.fingerprint(hashes.SHA256()).hex(':').upper(),
        }

        return info

    def get_certificate(self, endpoint, config, tls):
        """
        Get the certificate information from a TLS connection.

        :type  endpoint: str
        :param endpoint: The endpoint name from the 'endpoints' instance config.

        :type  config: dict
        :param config: Endpoint configuration

        :type  tls: ssl.SSLSocket
        :param tls: The TLS socket connection to the endpoint.

        :rtype: bool
        :return: True on success.
                 False on error.

        """

        try:
            # We can't rely on ssl.getpeercert() if the certificate wasn't validated
            #cert_info = tls.getpeercert()

            self.log('Retrieving certificate information for {} on port {}'.format(
                    config['address'], config['port']))

            result           = True
            der_cert         = tls.getpeercert(binary_form=True)
            pem_cert         = ssl.DER_cert_to_PEM_cert(der_cert)
            cert             = load_pem_x509_certificate(bytes(pem_cert, 'utf-8'))
            not_valid_before = cert.not_valid_before.timestamp()
            not_valid_after  = cert.not_valid_after.timestamp()
            info             = self.get_cert_info(cert)
            match_hostname   = 1
            labels           = {
                    'name'    : endpoint,
                    'address' : config['address'],
                    'port'    : config['port'],
                    }

            try:
                match = ssl.match_hostname(info, config['address'])

            except ssl.CertificateError as e:
                match_hostname = 0

            self.info_metric('onion_service_certificate_info', info, labels)

            self.set_metric('onion_service_certificate_not_valid_before_timestamp_seconds', not_valid_before, labels)
            self.set_metric('onion_service_certificate_not_valid_after_timestamp_seconds',  not_valid_after,  labels)
            self.set_metric('onion_service_certificate_match_hostname',                     0,                labels)

            message = 'Certificate for {address} on {port} has subject: {subject}; ' + \
                      'issuer: {issuer}; serial number: {serial_number}; version: {version}; ' + \
                      'notBefore: {not_before}; notAfter: {not_after}; SHA256 fingerprint: {fingerprint}'

            self.log(message.format(
                address       = config['address'],
                port          = config['port'],
                subject       = cert.subject.rfc4514_string(),
                issuer        = cert.issuer.rfc4514_string(),
                serial_number = info['serialNumber'],
                version       = str(info['version']),
                not_before    = info['notBefore'],
                not_after     = info['notAfter'],
                fingerprint   = info['fingerprintSHA256'],
                ))

        except Exception as e:
            result    = False
            exception = 'general_error'

            self.log(e, 'error')

        finally:
            return result
