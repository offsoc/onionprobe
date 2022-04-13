% ONIONPROBE(1) Onionprobe User Manual
% Silvio Rhatto <rhatto@torproject.org>
% Apr 13, 2022

# NAME

Onionprobe - a test and monitoring tool for Onion Services sites

# SYNOPSIS

usage: onionprobe [-h]
                  [-c CONFIG]
                  [-v]
                  [--circuit_stream_timeout CIRCUIT_STREAM_TIMEOUT]
                  [--control_password CONTROL_PASSWORD]
                  [--control_port CONTROL_PORT]
                  [--descriptor_max_retries DESCRIPTOR_MAX_RETRIES]
                  [--descriptor_timeout DESCRIPTOR_TIMEOUT]
                  [--endpoints [ONION-ADDRESS1 ...]]
                  [--http_connect_max_retries HTTP_CONNECT_MAX_RETRIES]
                  [--http_connect_timeout HTTP_CONNECT_TIMEOUT]
                  [--http_read_timeout HTTP_READ_TIMEOUT]
                  [--interval INTERVAL]
                  [--launch_tor | --no-launch_tor]
                  [--log_level LOG_LEVEL]
                  [--loop | --no-loop]
                  [--new_circuit | --no-new_circuit]
                  [--prometheus_exporter | --no-prometheus_exporter]
                  [--prometheus_exporter_port PROMETHEUS_EXPORTER_PORT]
                  [--randomize | --no-randomize]
                  [--shuffle | --no-shuffle]
                  [--sleep SLEEP]
                  [--socks_port SOCKS_PORT]
                  [--tor_address TOR_ADDRESS]

# DESCRIPTION

Onionprobe is a tool for testing and monitoring the status of Tor Onion
Services sites.

It can run a single time or continuously to probe a set of
onion services endpoints and paths, optionally exporting to Prometheus.

# OPTIONS

-v, --version
:   Display version

-h, --help
:   Display basic help

-c, --config CONFIG
:   Specify configuration file to use. All command line parameters can be
    specified inside a YAML file. Additional command line parameters override
    those set in the configuration file.

--circuit_stream_timeout CIRCUIT_STREAM_TIMEOUT
:   Sets how many seconds until a stream is detached from a circuit and try a new circuit

--control_password CONTROL_PASSWORD
:   Set Tor control password or use a password prompt (system-wide Tor service)
    or auto-generate a temporary password (built-in Tor service)

--control_port CONTROL_PORT
:   Tor control port

--descriptor_max_retries DESCRIPTOR_MAX_RETRIES
:   Max retries when fetching a descriptor

--descriptor_timeout DESCRIPTOR_TIMEOUT
:   Timeout in seconds when retrieving an Onion Service descriptor

-e, --endpoint ONION-ADDRESS1 [ONION-ADDRESS2 ... ONION-ADDRESSN]
:   Add .onion URLs to the list of endpoints to be tested

--http_connect_max_retries HTTP_CONNECT_MAX_RETRIES
:   Max retries when doing a HTTP/HTTPS connection to an Onion Service

--http_connect_timeout HTTP_CONNECT_TIMEOUT
:   Connection timeout for HTTP/HTTPS requests

--http_read_timeout HTTP_READ_TIMEOUT
:   Read timeout for HTTP/HTTPS requests

--interval INTERVAL
:   Max random interval in seconds between probing each endpoint

--launch_tor, --no-launch_tor
:   Whether to launch it's own Tor daemon (set to false to use the system-wide
    Tor process) (default: True)

--log_level LOG_LEVEL
:   Log level: debug, info, warning, error or critical

--loop, --no-loop
:   Run Onionprobe continuously (default: False)

--new_circuit, --no-new_circuit
:   Get a new circuit for every stream (default: False)

--prometheus_exporter, --no-prometheus_exporter
:   Enable Prometheus exporting functionality (default: False)

--prometheus_exporter_port PROMETHEUS_EXPORTER_PORT
:   Set the Prometheus exporter port

--randomize, --no-randomize
:   Randomize the interval between each probing (default: True)

--shuffle, --no-shuffle
:   Shuffle the list of endpoints at each probing round (default: True)

--sleep SLEEP
:   Max random interval in seconds to wait between each round of tests

--socks_port SOCKS_PORT
:   Tor SOCKS port

--tor_address TOR_ADDRESS
:   Tor listening address if the system-wide service is used

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
