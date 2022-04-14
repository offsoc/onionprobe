% ONIONPROBE(1) Onionprobe User Manual
% Silvio Rhatto <rhatto@torproject.org>
% Apr 14, 2022

# NAME

Onionprobe - a test and monitoring tool for Onion Services sites

# SYNOPSIS

onionprobe [-h] [-c CONFIG] [-v] [--circuit_stream_timeout CIRCUIT_STREAM_TIMEOUT] [--control_password CONTROL_PASSWORD] [--control_port CONTROL_PORT] [--descriptor_max_retries DESCRIPTOR_MAX_RETRIES]
                  [--descriptor_timeout DESCRIPTOR_TIMEOUT] [-e [ONION-ADDRESS1 ...]] [--http_connect_max_retries HTTP_CONNECT_MAX_RETRIES] [--http_connect_timeout HTTP_CONNECT_TIMEOUT] [--http_read_timeout HTTP_READ_TIMEOUT]
                  [--interval INTERVAL] [--launch_tor | --no-launch_tor] [--log_level LOG_LEVEL] [--loop | --no-loop] [--new_circuit | --no-new_circuit] [--prometheus_exporter | --no-prometheus_exporter]
                  [--prometheus_exporter_port PROMETHEUS_EXPORTER_PORT] [--randomize | --no-randomize] [--shuffle | --no-shuffle] [--sleep SLEEP] [--socks_port SOCKS_PORT] [--tor_address TOR_ADDRESS]


# DESCRIPTION

Onionprobe is a tool for testing and monitoring the status of Tor Onion
Services sites.

It can run a single time or continuously to probe a set of
onion services endpoints and paths, optionally exporting to Prometheus.

# FULL INVOCATION, OPTIONS, EXAMPLES AND METRICS

    onionprobe [-h] [-c CONFIG] [-v] [--circuit_stream_timeout CIRCUIT_STREAM_TIMEOUT] [--control_password CONTROL_PASSWORD] [--control_port CONTROL_PORT] [--descriptor_max_retries DESCRIPTOR_MAX_RETRIES]
                      [--descriptor_timeout DESCRIPTOR_TIMEOUT] [-e [ONION-ADDRESS1 ...]] [--http_connect_max_retries HTTP_CONNECT_MAX_RETRIES] [--http_connect_timeout HTTP_CONNECT_TIMEOUT] [--http_read_timeout HTTP_READ_TIMEOUT]
                      [--interval INTERVAL] [--launch_tor | --no-launch_tor] [--log_level LOG_LEVEL] [--loop | --no-loop] [--new_circuit | --no-new_circuit] [--prometheus_exporter | --no-prometheus_exporter]
                      [--prometheus_exporter_port PROMETHEUS_EXPORTER_PORT] [--randomize | --no-randomize] [--shuffle | --no-shuffle] [--sleep SLEEP] [--socks_port SOCKS_PORT] [--tor_address TOR_ADDRESS]

    Test and monitor onion services

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            Read options from configuration file. All command line parameters can be specified inside a YAML file. Additional command line parameters override those set in the configuration file.
      -v, --version         show program's version number and exit
      --circuit_stream_timeout CIRCUIT_STREAM_TIMEOUT
                            Sets how many seconds until a stream is detached from a circuit and try a new circuit
      --control_password CONTROL_PASSWORD
                            Set Tor control password or use a password prompt (system-wide Tor service) or auto-generate a temporary password (built-in Tor service)
      --control_port CONTROL_PORT
                            Tor control port
      --descriptor_max_retries DESCRIPTOR_MAX_RETRIES
                            Max retries when fetching a descriptor
      --descriptor_timeout DESCRIPTOR_TIMEOUT
                            Timeout in seconds when retrieving an Onion Service descriptor
      -e [ONION-ADDRESS1 ...], --endpoints [ONION-ADDRESS1 ...]
                            Add endpoints to the test list
      --http_connect_max_retries HTTP_CONNECT_MAX_RETRIES
                            Max retries when doing a HTTP/HTTPS connection to an Onion Service
      --http_connect_timeout HTTP_CONNECT_TIMEOUT
                            Connection timeout for HTTP/HTTPS requests
      --http_read_timeout HTTP_READ_TIMEOUT
                            Read timeout for HTTP/HTTPS requests
      --interval INTERVAL   Max random interval in seconds between probing each endpoint
      --launch_tor, --no-launch_tor
                            Whether to launch it's own Tor daemon (set to false to use the system-wide Tor process) (default: True)
      --log_level LOG_LEVEL
                            Log level: debug, info, warning, error or critical
      --loop, --no-loop     Run Onionprobe continuously (default: False)
      --new_circuit, --no-new_circuit
                            Get a new circuit for every stream (default: False)
      --prometheus_exporter, --no-prometheus_exporter
                            Enable Prometheus exporting functionality (default: False)
      --prometheus_exporter_port PROMETHEUS_EXPORTER_PORT
                            Set the Prometheus exporter port
      --randomize, --no-randomize
                            Randomize the interval between each probing (default: True)
      --shuffle, --no-shuffle
                            Shuffle the list of endpoints at each probing round (default: True)
      --sleep SLEEP         Max random interval in seconds to wait between each round of tests
      --socks_port SOCKS_PORT
                            Tor SOCKS port
      --tor_address TOR_ADDRESS
                            Tor listening address if the system-wide service is used

    Examples:

          onionprobe -c configs/tor.yaml
          onionprobe -e http://2gzyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid.onion

    Available metrics:

      onionprobe_version:
            Onionprobe version information
      onionprobe_state:
            Onionprobe latest state
      onionprobe_wait:
            Records how long Onionprobe waited between two probes
      onion_service_latency:
            Register Onion Service connection latency in seconds
      onion_service_reachable:
            Register if the Onion Service is reachable: value is 1 for reachability and 0 otherwise
      onion_service_connection_attempts:
            Register the number of attempts when trying to connect to an Onion Service
      onion_service_status_code:
            Register Onion Service connection HTTP status code
      onion_service_descriptor_latency:
            Register Onion Service latency in seconds to get the descriptor
      onion_service_descriptor_reachable:
            Register if the Onion Service descriptor is available: value is 1 for reachability and 0 otherwise
      onion_service_descriptor_fetch_attempts:
            Register the number of attempts required when trying to get an Onion Service descriptor
      onion_service_introduction_points_number:
            Register the number of introduction points in the Onion Service descriptor
      onion_service_pattern_matched:
            Register whether a regular expression pattern is matched when connection to the Onion Service: value is 1 for matched pattern and 0 otherwise
      onion_service_valid_certificate:
            Register whether the Onion Service HTTPS certificate is valid: value is 1 for valid and 0 otherwise, but only for sites reachable using HTTPS
      onion_service_fetch_error_counter:
            Counts errors when fetching an Onion Service
      onion_service_descriptor_fetch_error_counter:
            Counts errors when fetching an Onion Service descriptor
      onion_service_request_exception:
            Counts Onion Service general exception errors
      onion_service_connection_error:
            Counts Onion Service connection errors
      onion_service_http_error:
            Counts Onion Service HTTP errors
      onion_service_too_many_redirects:
            Counts Onion Service too many redirects errors
      onion_service_connection_timeout:
            Counts Onion Service connection timeouts
      onion_service_read_timeout:
            Counts Onion Service read timeouts
      onion_service_timeout:
            Counts Onion Service timeouts
      onion_service_certificate_error:
            Counts HTTPS certificate validation errors


# FILES

/etc/onionprobe
:  System-wide Onionprobe configuration files.

# LIMITATIONS

Onionprobe currently has the following limitations:

1. Only works for Onion Services websites, i.e, those served via
   either HTTP or HTTPS.

# SEE ALSO

The *README* file distributed with Onionprobe contains the full documentation.

The Onionprobe source code and all documentation may be downloaded from
<https://gitlab.torproject.org/onion-services/onionprobe>.
