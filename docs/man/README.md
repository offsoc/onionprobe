# Onionprobe manual page

## NAME

Onionprobe - a test and monitoring tool for Onion Services sites

## SYNOPSIS

onionprobe [-h] [-c CONFIG] [-v]
                  [--circuit_stream_timeout CIRCUIT_STREAM_TIMEOUT]
                  [--control_password CONTROL_PASSWORD]
                  [--control_port CONTROL_PORT]
                  [--descriptor_max_retries DESCRIPTOR_MAX_RETRIES]
                  [--descriptor_timeout DESCRIPTOR_TIMEOUT]
                  [-e [ONION-ADDRESS1 ...]]
                  [--get_certificate_info | --no-get_certificate_info]
                  [--http_connect_max_retries HTTP_CONNECT_MAX_RETRIES]
                  [--http_connect_timeout HTTP_CONNECT_TIMEOUT]
                  [--http_read_timeout HTTP_READ_TIMEOUT]
                  [--interval INTERVAL] [--launch_tor | --no-launch_tor]
                  [--log_level LOG_LEVEL] [--loop | --no-loop]
                  [--metrics_port METRICS_PORT]
                  [--metrics_port_policy METRICS_PORT_POLICY]
                  [--new_circuit | --no-new_circuit]
                  [--prometheus_exporter | --no-prometheus_exporter]
                  [--prometheus_exporter_port PROMETHEUS_EXPORTER_PORT]
                  [--randomize | --no-randomize] [--rounds ROUNDS]
                  [--shuffle | --no-shuffle] [--sleep SLEEP]
                  [--socks_port SOCKS_PORT]
                  [--test_tls_connection | --no-test_tls_connection]
                  [--tls_connect_max_retries TLS_CONNECT_MAX_RETRIES]
                  [--tls_connect_timeout TLS_CONNECT_TIMEOUT]
                  [--tls_verify | --no-tls_verify] [--tor_address TOR_ADDRESS]


## DESCRIPTION

Onionprobe is a tool for testing and monitoring the status of Tor Onion
Services sites.

It can run a single time or continuously to probe a set of
onion services endpoints and paths, optionally exporting to Prometheus.

## FULL INVOCATION, OPTIONS, EXAMPLES AND METRICS

    onionprobe [-h] [-c CONFIG] [-v]
                      [--circuit_stream_timeout CIRCUIT_STREAM_TIMEOUT]
                      [--control_password CONTROL_PASSWORD]
                      [--control_port CONTROL_PORT]
                      [--descriptor_max_retries DESCRIPTOR_MAX_RETRIES]
                      [--descriptor_timeout DESCRIPTOR_TIMEOUT]
                      [-e [ONION-ADDRESS1 ...]]
                      [--get_certificate_info | --no-get_certificate_info]
                      [--http_connect_max_retries HTTP_CONNECT_MAX_RETRIES]
                      [--http_connect_timeout HTTP_CONNECT_TIMEOUT]
                      [--http_read_timeout HTTP_READ_TIMEOUT]
                      [--interval INTERVAL] [--launch_tor | --no-launch_tor]
                      [--log_level LOG_LEVEL] [--loop | --no-loop]
                      [--metrics_port METRICS_PORT]
                      [--metrics_port_policy METRICS_PORT_POLICY]
                      [--new_circuit | --no-new_circuit]
                      [--prometheus_exporter | --no-prometheus_exporter]
                      [--prometheus_exporter_port PROMETHEUS_EXPORTER_PORT]
                      [--randomize | --no-randomize] [--rounds ROUNDS]
                      [--shuffle | --no-shuffle] [--sleep SLEEP]
                      [--socks_port SOCKS_PORT]
                      [--test_tls_connection | --no-test_tls_connection]
                      [--tls_connect_max_retries TLS_CONNECT_MAX_RETRIES]
                      [--tls_connect_timeout TLS_CONNECT_TIMEOUT]
                      [--tls_verify | --no-tls_verify] [--tor_address TOR_ADDRESS]

    Test and monitor onion services

    options:
      -h, --help            show this help message and exit
      -c, --config CONFIG   Read options from configuration file. All command line
                            parameters can be specified inside a YAML file.
                            Additional command line parameters override those set
                            in the configuration file.
      -v, --version         show program's version number and exit
      --circuit_stream_timeout CIRCUIT_STREAM_TIMEOUT
                            Sets how many seconds until a stream is detached from
                            a circuit and try a new circuit (default: 60)
      --control_password CONTROL_PASSWORD
                            Set Tor control password or use a password prompt
                            (system-wide Tor service) or auto-generate a temporary
                            password (built-in Tor service) (default: None)
      --control_port CONTROL_PORT
                            Tor control port (default: 19051)
      --descriptor_max_retries DESCRIPTOR_MAX_RETRIES
                            Max retries when fetching a descriptor (default: 5)
      --descriptor_timeout DESCRIPTOR_TIMEOUT
                            Timeout in seconds when retrieving an Onion Service
                            descriptor (default: 30)
      -e, --endpoints [ONION-ADDRESS1 ...]
                            Add endpoints to the test list
      --get_certificate_info, --no-get_certificate_info
                            Whether to get certificate information when testing
                            TLS/HTTPS endpoints. Requires --test_tls_connection to
                            take effect.
      --http_connect_max_retries HTTP_CONNECT_MAX_RETRIES
                            Max retries when doing a HTTP/HTTPS connection to an
                            Onion Service (default: 3)
      --http_connect_timeout HTTP_CONNECT_TIMEOUT
                            Connection timeout for HTTP/HTTPS requests (default:
                            30)
      --http_read_timeout HTTP_READ_TIMEOUT
                            Read timeout for HTTP/HTTPS requests (default: 30)
      --interval INTERVAL   Max random interval in seconds between probing each
                            endpoint (default: 60)
      --launch_tor, --no-launch_tor
                            Whether to launch it's own Tor daemon (set to false to
                            use the system-wide Tor process)
      --log_level LOG_LEVEL
                            Log level : debug, info, warning, error or critical
                            (default: info)
      --loop, --no-loop     Run Onionprobe continuously
      --metrics_port METRICS_PORT
                            Tor Metrics port (MetricsPort). An empty value means
                            it is disabled
      --metrics_port_policy METRICS_PORT_POLICY
                            Tor Metrics port policy (MetricsPortPolicy). An empty
                            value means it is disabled' (default: reject *)
      --new_circuit, --no-new_circuit
                            Get a new circuit for every stream
      --prometheus_exporter, --no-prometheus_exporter
                            Enable Prometheus exporting functionality
      --prometheus_exporter_port PROMETHEUS_EXPORTER_PORT
                            Set the Prometheus exporter port (default: 9935)
      --randomize, --no-randomize
                            Randomize the interval between each probing
      --rounds ROUNDS       Run only a limited number of rounds (i.e., the number
                            of times that Onionprobe tests all the configured
                            endpoints). Requires the "loop" option to be enabled.
                            Set to 0 to disable this limit. (default: 0)
      --shuffle, --no-shuffle
                            Shuffle the list of endpoints at each probing round
      --sleep SLEEP         Max random interval in seconds to wait between each
                            round of tests (default: 60)
      --socks_port SOCKS_PORT
                            Tor SOCKS port (default: 19050)
      --test_tls_connection, --no-test_tls_connection
                            Whether to run a specific test for TLS endpoints
      --tls_connect_max_retries TLS_CONNECT_MAX_RETRIES
                            Max retries when doing a TLS connection to an Onion
                            Service (default: 3)
      --tls_connect_timeout TLS_CONNECT_TIMEOUT
                            Connection timeout for TLS connections (default: 30)
      --tls_verify, --no-tls_verify
                            Whether to verify TLS/HTTPS certificates
      --tor_address TOR_ADDRESS
                            Tor listening address if the system-wide service is
                            used (default: 127.0.0.1)

    Examples:

          onionprobe -c configs/tor.yaml
          onionprobe -e http://2gzyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid.onion

    Available metrics:

      onionprobe_version:
            Onionprobe version information
      onionprobe_state:
            Onionprobe latest state
      onionprobe_wait_seconds:
            Records how long Onionprobe waited between two probes in seconds
      onion_service_latency_seconds:
            Register Onion Service connection latency in seconds
      onion_service_reachable:
            Register if the Onion Service is reachable: value is 1 for reachability and 0 otherwise
      onion_service_connection_attempts:
            Register the number of attempts when trying to connect to an Onion Service in a probing round
      onion_service_tls_security_level:
            An integer representing the SSL security level for the context.See SSL_CTX_get_security_level(3) manpage for details.
      onion_service_status_code:
            Register Onion Service connection HTTP status code
      onion_service_unexpected_status_code:
            Register if an Onion Service connection returned an unexpected HTTP status code: 1 for unexpected and 0 otherwise
      onion_service_descriptor_latency_seconds:
            Register Onion Service latency in seconds to get the descriptor
      onion_service_descriptor_reachable:
            Register if the Onion Service descriptor is available: value is 1 for reachability and 0 otherwise
      onion_service_descriptor_fetch_attempts:
            Register the number of attempts required when trying to get an Onion Service descriptor in a probing round
      onion_service_descriptor_revision_counter:
            Register Onion Service descriptor revision counter
      onion_service_descriptor_lifetime_seconds:
            Register Onion Service descriptor lifetime in seconds
      onion_service_descriptor_outer_wrapper_size_bytes:
            Register Onion Service outer wrapper descriptor size in bytes (decrypted)
      onion_service_descriptor_second_layer_size_bytes:
            Register Onion Service second layer descriptor size in bytes (decrypted)
      onion_service_is_single:
            Indicates whether the server is using the single hop Onion Service circuit mode: value is 1 if this is a single onion service, 0 otherwise
      onion_service_introduction_points_number:
            Register the number of introduction points in the Onion Service descriptor
      onion_service_pow_enabled:
            Whether Proof of Work (PoW) defense is enabled in the Onion Service: value is 1 when PoW is enabled, 0 otherwise
      onion_service_pow_v1_seed:
            The Proof of Work (PoW) decoded seed for the v1 scheme
      onion_service_pow_v1_effort:
            The Proof of Work (PoW) suggested effort for the v1 scheme
      onion_service_pow_v1_expiration_seconds:
            The Proof of Work (PoW) seed expiration time for the v1 scheme
      onion_service_pattern_matched:
            Register whether a regular expression pattern is matched when connection to the Onion Service: value is 1 for matched pattern and 0 otherwise
      onion_service_valid_certificate:
            Register whether the Onion Service HTTPS certificate is valid: value is 1, 0 for invalid, 2 for untested. Only for sites reachable using HTTPS
      onion_service_certificate_not_valid_before_timestamp_seconds:
            Register the beginning of the validity period of the certificate in UTC.This does not mean necessarily that the certificate is CA-validated.Value is represented as a POSIX timestamp
      onion_service_certificate_not_valid_after_timestamp_seconds:
            Register the end of the validity period of the certificate in UTC.This does not mean necessarily that the certificate is CA-validated.Value is represented as a POSIX timestamp
      onion_service_certificate_expiry_seconds:
            Register how many seconds are left before the certificate expire.Negative values indicate how many seconds passed after the certificate already expired.
      onion_service_certificate_match_hostname:
            Register whether a provided server certificate matches the server hostname in a TLS connection: value is 1 for matched hostname and 0 otherwise. Check is done both on the commonName and subjectAltName fields. A value of 1 does not mean necessarily that the certificate is CA-validated.
      hsdir_latency_seconds:
            Register HSDir latency in seconds to fetch a descriptor
      onion_service_fetch_requests:
            Counts the total number of requests to access an Onion Service
      onion_service_fetch_error:
            Counts the total number of errors when fetching an Onion Service
      onion_service_descriptor_fetch_requests:
            Counts the total number of requests to fetch an Onion Service descriptor
      onion_service_descriptor_fetch_error:
            Counts the total number of errors when fetching an Onion Service descriptor
      onion_service_generic_error:
            Counts the total number of errors not tracked by other metrics
      onion_service_request_exception:
            Counts the total number of Onion Service general exception errors
      onion_service_connection_error:
            Counts the total number of Onion Service connection errors
      onion_service_http_error:
            Counts the total number of Onion Service HTTP errors
      onion_service_too_many_redirects:
            Counts the total number of Onion Service too many HTTP redirect errors
      onion_service_connection_timeout:
            Counts the total number of Onion Service connection timeouts
      onion_service_read_timeout:
            Counts the total number of Onion Service read timeouts
      onion_service_timeout:
            Counts the total number of Onion Service timeouts
      onion_service_certificate_error:
            Counts the total number of HTTPS certificate validation errors
      onion_service_descriptor:
            Onion Service descriptor information, including state and Hidden Service Directory (HSDir) used
      onion_service_tls:
            Register miscellaneous TLS information for a given Onion Service, such as version and ciphers
      onion_service_certificate:
            Register miscellaneous TLS certificate information for a given Onion Service, such as version and fingerprints
      onion_service_probe_status:
            Register information about the last test made to a given Onion Service, including POSIX timestamp


## CONFIGURATION FILE FORMAT

This is a sample configuration file that can be adapted:

    ---
    # Sample config file for Onionprobe
    #
    # Copyright (C) 2022 The Tor Project, Inc.
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

    # Log level: debug, info, warning, error or critical
    log_level: 'info'

    # Whether to launch it's own Tor daemon (set to false to use the system-wide Tor service)
    launch_tor: true

    # Tor listening address if the system-wide service is used
    #tor_address: 'tor'
    tor_address: '127.0.0.1'

    # Tor SOCKS port
    #
    # Use a non-default Tor SOCKS port to avoid conflict with any existing
    # system-wide Tor process listening at TCP port 9050.
    #socks_port: 9050
    socks_port: 19050

    # Tor control port
    #
    # Use a non-default Tor control port to avoid conflict with any existing
    # system-wide Tor process listening at TCP port 9051.
    #control_port: 9051
    control_port: 19051

    # Tor control password
    #
    # Set to false to
    #
    # * Use a temporary auto-generated password when using the built-in Tor
    #   service.
    # * Show a password prompt when using the system-wide Tor service.
    #
    # Do not use the example value in production, as this password is available
    # publicly
    #control_password: false
    #control_password: 'hackedpasswdbSkUMOr2vIlL5u2YEMA1YpwKj08'

    # Whether to run continuously
    loop: true

    # Tor Metrics port (MetricsPort)
    # An empty value means it is disabled
    #
    # WARNING: Before enabling this, it is important to understand that exposing
    # tor metrics publicly is dangerous to the Tor network users. Please take extra
    # precaution and care when opening this port. Set a very strict access policy
    # with `metrics_port_policy` and consider using your operating systems firewall
    # features for defense in depth.
    #
    # We recommend, for the prometheus format, that the only address that can
    # access this port should be the Prometheus server itself. Remember that the
    # connection is unencrypted (HTTP) hence consider using a tool like stunnel to
    # secure the link from this port to the server.
    #
    # Example settings for the metrics_port parameter:
    #
    #   metrics_port: '9936'         # localhost only on port 9936
    #   metrics_port: '0.0.0.0:9936' # binds to all IPv4 addresses in the host
    #
    metrics_port: ''

    # Tor Metrics port policy (MetricsPortPolicy)
    # An empty value means it is disabled
    #
    # Example settings for the metrics_port_policy parameter:
    #
    #   metrics_port_policy: 'accept 172.19.0.100'
    #   metrics_port_policy: 'accept 127.0.0.1,accept 172.19.0.100'
    #   metrics_port_policy: 'accept *'
    #
    # This should work by default for Docker containers in the 172.16.0.0/12 subnet
    # (not recommended):
    #
    #   metrics_port_policy: 'accept 172.16.0.0/12'
    #
    # This should work by default for a local network, including local Docker
    # containers (not recommended):
    #
    #   metrics_port_policy: 'accept 192.168.0.0/16,accept 10.0.0.0/8,accept 172.16.0.0/12'
    #
    metrics_port_policy: 'reject *'

    # Whether to enable Prometheus exporter functionality
    # Setting it to true automatically enables countinuos run (loop)
    prometheus_exporter: true

    # Prometheus exporter port
    prometheus_exporter_port: 9935

    # Max random time in seconds between probing each endpoint
    interval: 5

    # Max random time in seconds to wait between each round of tests (a round = a
    # pass among all defined endpoints)
    sleep: 5

    # Whether to shuffle list to scramble the ordering of the probe to avoid
    # the endpoint list to be guessed by a third party.
    #
    # This shuffles the list every time Onionprobe starts a new round of
    # tests.
    shuffle: true

    # Whether to randomize both the interval and the sleep time for privacy
    # concerns and to avoid systematic errors
    randomize: true

    # Run only a limited number of rounds (i.e., the number of times that
    # Onionprobe tests all the configured endpoints).
    # Requires the "loop" option to be enabled.
    # Set to 0 to disable this limit.
    rounds: 0

    # Max retries when fetching a descriptor
    # By default it is set to the number of HSDirs the client usually fetch minus one
    # See discussion at https://gitlab.torproject.org/tpo/network-health/analysis/-/issues/28
    descriptor_max_retries: 5

    # Timeout in seconds when retrieving an Onion Service descriptor
    descriptor_timeout: 30

    # Connection timeout for HTTP/HTTPS requests
    http_connect_timeout: 30

    # Max retries when doing a HTTP/HTTPS connection to an Onion Service
    http_connect_max_retries: 3

    # Read timeout for HTTP/HTTPS requests
    http_read_timeout: 30

    # Whether to get a new circuit for every stream
    new_circuit: false

    # Sets how many seconds until a stream is detached from a circuit and try a new
    # circuit (CircuitStreamTimeout Tor daemon config)
    circuit_stream_timeout: 60

    # Whether to verify TLS/HTTPS certificates
    tls_verify: true

    # Whether to run a specific test for TLS endpoints
    test_tls_connection: true

    # Whether to get certificate information when testing TLS/HTTPS endpoints.
    # Requires "test_tls_connection" set to true to take effect.
    get_certificate_info: true

    # Connection timeout for TLS connections
    tls_connect_timeout: 30

    # Max retries when doing a TLS connection to an Onion Service
    tls_connect_max_retries: 3

    # The list of endpoints to be tested
    endpoints:
      # Using addresses from https://onion.torproject.org
      www.torproject.org:
        address: '2gzyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid.onion'
        protocol: 'http'
        port: 80
        paths:
          - path   : '/'
            # Specifying a per-path pattern makes Onionprobe look for it in the
            # request and hence operating like a basic check if the endpoint
            # is operational.
            #
            # Accepts patterns using Python's regex format
            pattern: 'Tor Project'

            # The allowed HTTP status codes for this endpoint
            # Any code not in this list will set an unexpected status code metric
            allowed_statuses:
              - 200
      2019.www.torproject.org:
        address: jqyzxhjk6psc6ul5jnfwloamhtyh7si74b4743k2qgpskwwxrzhsxmad.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      alertmanager1.torproject.org:
        address: sbgubiq7c3r7zp22gnl4pjfwisk2plbxwhbwcluwjegbxzwhq7a2ucyd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      alertmanager2.torproject.org:
        address: uqduzmqiesrjqw2n7rc66h267mmbsxzacohrfhpoxm746wa46yh25jqd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      archive.torproject.org:
        address: uy3qxvwzwoeztnellvvhxh7ju7kfvlsauka7avilcjg7domzxptbq7qd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      aus1.torproject.org:
        address: ot3ivcdxmalbsbponeeq5222hftpf3pqil24q3s5ejwo5t52l65qusid.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      aus2.torproject.org:
        address: b5t7emfr2rn3ixr4lvizpi3stnni4j4p6goxho7lldf4qg4hz5hvpqid.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      blog.torproject.org:
        address: pzhdfe7jraknpj2qgu5cz2u3i4deuyfwmonvzu5i3nyw4t4bmg7o5pad.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      bridges.torproject.org:
        address: yq5jjvr7drkjrelzhut7kgclfuro65jjlivyzfmxiq2kyv5lickrl4qd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      cloud.torproject.org:
        address: ui3cpcohcoko6aydhuhlkwqqtvadhaflcc5zb7mwandqmcal7sbwzwqd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      collector.torproject.org:
        address: pgmrispjerzzf2tdzbfp624cg5vpbvdw2q5a3hvtsbsx25vnni767yad.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      collector2.torproject.org:
        address: urscdffm73o4y6hpp3r43bgmudq42hq2ibdpkld6a7hy3qa44qbvc2yd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      community.torproject.org:
        address: xmrhfasfg5suueegrnc4gsgyi2tyclcy5oz7f5drnrodmdtob6t2ioyd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      consensus-health.torproject.org:
        address: tkskz5dkjel4xqyw5d5l3k52kgglotwn6vgb5wrl2oa5yi2szvywiyid.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      crm.torproject.org:
        address: 6ojylpznauimd2fga3m7g24vd7ebkzlemxdprxckevqpzs347ugmynqd.onion
        paths:
        - allowed_statuses:
          - 401
          path: /
        port: 80
        protocol: http
      db.torproject.org:
        address: epnxy4oscv3yh2fjwfrvctnjsmj5ta5uxdkq6k2ce7borqvcsk4qxhid.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      deb.torproject.org:
        address: apow7mjfryruh65chtdydfmqfpj5btws7nbocgtaovhvezgccyjazpqd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      dev.crm.torproject.org:
        address: eewp4iydzyu2a5d6bvqadadkozxdbhsdtmsoczu2joexfrjjsheaecad.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      dist.torproject.org:
        address: scpalcwstkydpa3y7dbpkjs2dtr7zvtvdbyj3dqwkucfrwyixcl5ptqd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      exonerator.torproject.org:
        address: pm46i5h2lfewyx6l7pnicbxhts2sxzacvsbmqiemqaspredf2gm3dpad.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      extra.torproject.org:
        address: kkr72iohlfix5ipjg776eyhplnl2oiv5tz4h2y2bkhjix3quafvjd5ad.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      forum.torproject.org:
        address: v236xhqtyullodhf26szyjepvkbv6iitrhjgrqj4avaoukebkk6n6syd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 443
        protocol: https
      gitlab.torproject.org:
        address: eweiibe6tdjsdprb4px6rqrzzcsi22m4koia44kc5pcjr7nec2rlxyad.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      grafana1.torproject.org:
        address: 7zjnw5lx2x27rwiocxkqdquo7fawj46mf2wiu2l7e6z6ng6nivmdxnad.onion
        paths:
        - allowed_statuses:
          - 401
          path: /
        port: 80
        protocol: http
      grafana2.torproject.org:
        address: f3vd6fyiccuppybkxiblgigej3pfvvqzjnhd3wyv7h4ee5asawf2fhqd.onion
        paths:
        - allowed_statuses:
          - 401
          path: /
        port: 80
        protocol: http
      ircbouncer.torproject.org:
        address: moz5kotsnjony4oxccxfo4lwk3pvoxmdoljibhgoonzgzjs5oemtjmqd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      karma1.torproject.org:
        address: t5z367d2omuewjvrwqsdd2bixlh6dektuf2hhe2hc2tpvk4bosb4u4yd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      karma2.torproject.org:
        address: h6necup44ztozsqs3my6g5pjljptqnm4auqrqcy6jdctoqvznmvh3qqd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      lists-01.torproject.org:
        address: e6r6heg2ucmlm2po5yrxzf6k23ta5wwbt2adogjcyntlaiopytjz35yd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      metrics-api.torproject.org:
        address: yc3galza3gejn3taziuhhgrwt4bdtwmom25zby7jphfwbeirvkmcdvqd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      metrics-db.torproject.org:
        address: lk6lj36rfj32u2rjceujj3o7otgujm6fw5hyyxr6jko6pkfasb2z6eid.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      metrics.torproject.org:
        address: hctxrvjzfpvmzh2jllqhgvvkoepxb4kfzdjm6h7egcwlumggtktiftid.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      moat.torproject.org:
        address: z7m7ogzdhu43nosvjtsuplfmuqa3ge5obahixydhmzdox6owwxfoxzid.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      newsletter.torproject.org:
        address: a4ygisnerpgtc5ayerl22pll6cls3oyj54qgpm7qrmb66xrxts6y3lyd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      nightlies.tbb.torproject.org:
        address: umj4zbqdfcyevlkgqgpq6foxk3z75zzxsbgt5jqmfxofrbrjh3crbnad.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      nyx.torproject.org:
        address: 3ewfgrt4gzfccp6bnquhqb266r3zepiqpnsk3falwygkegtluwuyevid.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      onion.torproject.org:
        address: xao2lxsmia2edq2n5zxg6uahx6xox2t7bfjw6b5vdzsxi7ezmqob6qid.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      onionservices.torproject.org:
        address: ttevhjjsjxz6uqqcjkbig5cycd7n7xv7cmd6f5fcvrqaaa7f3bj36wad.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      openpgpkey.torproject.org:
        address: 2yldcptk56shc7lwieozoglw3t5ghty7m6mf2faysvfnzccqavbu2mad.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      people.torproject.org:
        address: 5ecey6oe4rocdsfoigr4idu42cecm2j7zfogc3xc7kfn4uriehwrs6qd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      prometheus1.torproject.org:
        address: ydok5jiruh3ak6hcfdlm2g7iuraaxcomeckj2nucjsxif6qmrrda2byd.onion
        paths:
        - allowed_statuses:
          - 401
          path: /
        port: 80
        protocol: http
      prometheus2.torproject.org:
        address: vyo6yrqhl3by7d6n5t6hjkflaqbarjpqjnvapr5u5rafk4imnfrmcjyd.onion
        paths:
        - allowed_statuses:
          - 401
          path: /
        port: 80
        protocol: http
      rbm.torproject.org:
        address: nkuz2tpok7ctwd5ueer5bytj3bm42vp7lgjcsnznal3stotg6vyaakyd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      rdsys-moat.torproject.org:
        address: jcbdm4biw3aac57snk34brzc5fghbszrzde47idnlanj6kf6jmocdgqd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      research.torproject.org:
        address: xhqthou6scpfnwjyzc3ekdgcbvj76ccgyjyxp6cgypxjlcuhnxiktnqd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      review.torproject.net:
        address: zhkhhhnppc5k6xju7n25rjba3wuip73jnodicxl65qdpchrwvvsilcyd.onion
        paths:
        - allowed_statuses:
          - 401
          path: /
        port: 80
        protocol: http
      rpm.torproject.org:
        address: 4ayyzfoh5qdrokqaejis3rdredhvf22n3migyxfudpkpunngfc7g4lqd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      snowflake.torproject.org:
        address: oljlphash3bpqtrvqpr5gwzrhroziw4mddidi5d2qa4qjejcbrmoypqd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      spec.torproject.org:
        address: i3xi5qxvbrngh3g6o7czwjfxwjzigook7zxzjmgwg5b7xnjcn5hzciad.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      staging.crm.torproject.org:
        address: pt34uujusar4arrvsqljndqlt7tck2d5cosaav5xni4nh7bmvshyp2yd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      status.torproject.org:
        address: eixoaclv7qvnmu5rolbdwba65xpdiditdoyp6edsre3fitad777jr3ad.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      stem.torproject.org:
        address: mf34jlghauz5pxjcmdymdqbe5pva4v24logeys446tdrgd5lpsrocmqd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      styleguide.torproject.org:
        address: 7khzpw47s35pwo3lvtctwf2szvnq3kgglvzc22elx7of2awdzpovqmqd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      submission.torproject.org:
        address: givpjczyrb5jjseful3o5tn3tg7tidbu4gydl4sa5ekpcipivqaqnpad.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      support.torproject.org:
        address: rzuwtpc4wb3xdzrj3yeajsvm3fkq4vbeubm2tdxaqruzzzgs5dwemlad.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      survey.torproject.org:
        address: eh5esdnd6fkbkapfc6nuyvkjgbtnzq2is72lmpwbdbxepd2z7zbgzsqd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      svn-archive.torproject.org:
        address: b63iq6es4biaawfilwftlfkw6a6putogxh4iakei2ioppb7dsfucekyd.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      tagtor.torproject.org:
        address: lx75vwrdgdgzpnnewquw2kngajieq6lqbblawoufjkf6fyqexhu4iiad.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      tb-manual.torproject.org:
        address: dsbqrprgkqqifztta6h3w7i2htjhnq7d3qkh3c7gvc35e66rrcv66did.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      test-data.tbb.torproject.org:
        address: umbk3kbgov4ekg264yulvbrpykfye7ohguqbds53qn547mdpt6o4qkad.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      test.crm.torproject.org:
        address: a4d52y2erv4eijii66cpnyqn7rsnnq3gmtrsdxzt2laoutvu4gz7fwid.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http
      www.onion-router.net:
        address: tttyx2vwp7ihml3vkhywwcizv6nbwrikpgeciy3qrow7l7muak2pnhad.onion
        paths:
        - allowed_statuses:
          - 200
          path: /
        port: 80
        protocol: http


## EXIT STATUS

If any tested endpoint had a failure on any probing, then the exit status is 1.
Otherwise, the exit status is 0.

## FILES

/etc/onionprobe
:  System-wide Onionprobe configuration files.

## LIMITATIONS

Onionprobe currently has the following limitations:

1. Only works for Onion Services websites, i.e, those served via
   either HTTP or HTTPS.

2. Currently Onionprobe probes runs in a single thread.

3. For other limitations, check the list of issues  available at the Onionprobe
   source code repository.

## SEE ALSO

The *docs/* folder distributed with Onionprobe contains the full documentation,
which should also be available at <https://onionservices.torproject.org/apps/web/onionprobe/>.

The Onionprobe source code and all documentation may be downloaded from
<https://gitlab.torproject.org/tpo/onion-services/onionprobe>.
