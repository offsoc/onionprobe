# Onionprobe

![](assets/logo.jpg "Onionprobe")

Onionprobe is a tool for testing and monitoring the status of
[Tor Onion Services](https://community.torproject.org/onion-services/) sites.

It can run a single time or continuously to probe a set of onion services
endpoints and paths, optionally exporting to [Prometheus](https://prometheus.io).

## Requirements

Onionprobe requires the following software:

* [Python 3](https://www.python.org)
* [Stem Tor Control library](https://stem.torproject.org)
* [Prometheus Python client](https://github.com/prometheus/client_python)
* [PyYAML](https://pyyaml.org)
* [Requests](https://docs.python-requests.org)
* [PySocks](https://github.com/Anorov/PySocks)
* [Tor daemon](https://gitlab.torproject.org/tpo/core/tor)

On [Debian](https://debian.org), they can be installed using

    sudo apt install python3 python3-prometheus-client \
                     python3-stem python3-cryptography \
                     python3-yaml python3-requests     \
                     python3-socks tor

## Installation

Onionprobe is [available on PyPI](https://pypi.org/project/keyring/):

    pip install onionprobe

It's also possible to run it directly from the Git repository:

    git clone https://gitlab.torproject.org/tpo/onion-services/onionprobe
    cd onionprobe

## Usage

Simply ask Onionprobe to try an Onion Service site:

    onionprobe -e http://2gzyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid.onion

It's possible to supply multiple addresses:

    onionprobe -e <onion-address1> <onionaddress2> ...

Onionprobe also accepts a configuration file with a list of .onion endpoints
and options. A [detailed sample config](configs/tor.yaml) is provided and can
be invoked with:

    onionprobe -c configs/tor.yaml

By default, Onionprobe starts it's own Tor daemon instance, so the `tor` binary
must be available in the system.

Full usage and available metrics is provided passing the `-h` flag:

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

    Test and monitor onion services

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            Read options from configuration file
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

## Testing

Onionprobe comes with a working test environment with the [sample
configuration](configs/tor.yaml) and based on [Docker
Compose](https://docs.docker.com/compose/), which can be started using

    docker-compose up

Then point your browser to:

* The built-in Prometheus dashboard: https://localhost:9090
* The built-in Onionprobe Prometheus exporter: https://localhost:9091

## Compiled configurations

Besides the [sample config](configs/tor.yaml) containing sites listed at
https://onion.torproject.org, Onionprobe comes also with other example configs:

1. [Real-World Onion Sites](https://github.com/alecmuffett/real-world-onion-sites) .onions at
   [real-world-onion-sites.yaml](configs/real-world-onion-sites.yaml), generated by the
   [real-world-onion-sites.py](packages/real-world-onion-sites.py) script.
2. [The SecureDrop API](https://securedrop.org/api/v1/directory/) .onions at
   [securedrop.yaml](configs/securedrop.yaml), generated by the
   [securedrop.py](packages/securedrop.py) script.

You can build your own configuration compiler by using the
[OnionprobeConfigCompiler](onionprobes/configs.py) class.

## Folder structure and files

Relevant folders and files in this repository:

* `assets`: logos and other stuff.
* `configs`: miscelaneous configurations.
* `containers`: container configurations.
* `docs`: documentation.
* `packages`: python packages codebase.
* `scripts`: provisioning and other configuration scripts.
* `tests`: test procedures.
* `vendors`: other third-party libraries and helpers.
* `kvmxfile`: please ignore this if you're not a [KVMX](https://kvmx.fluxo.info) user.
* `.env`: should be manually created if you plan to use custom configuration with Docker Composer.
* `docker-compose.yml`: service container configuration.

## Tasks

See [TODO](TODO.md) and the [issue tracker](https://gitlab.torproject.org/tpo/onion-services/onionprobe/-/issues).

## Acknowledgements

Thanks:

* @irl for the idea/specs/tasks.
* @hiro for suggestions.
* @arma and @juga for references.
* @anarcat for Python and Debian packaging guidance.

## Alternatives

* [OnionScan](https://onionscan.org/)
* [BrassHornCommunications/OnionWatch: A GoLang daemon for notifying Tor Relay and Hidden Service admins of status changes](https://github.com/BrassHornCommunications/OnionWatch)
* [systemli/prometheus-onion-service-exporter: Prometheus Exporter for Tor Onion Services](https://github.com/systemli/prometheus-onion-service-exporter)
* [prometheus/blackbox_exporter: Blackbox prober exporter](https://github.com/prometheus/blackbox_exporter), which could be configured using `proxy_url`
  pointing to a [Privoxy](http://www.privoxy.org/) instance relaying traffic to `tor` daemon.

## References

Related software and libraries with useful routines:

* [onbasca](https://gitlab.torproject.org/tpo/network-health/onbasca)
* [sbws](https://gitlab.torproject.org/tpo/network-health/sbws)
* [Stem](https://stem.torproject.org/)
* [txtorcon](https://txtorcon.readthedocs.io/en/latest/)
* [Onionbalance](https://onionbalance.readthedocs.io/en/latest/)
* [hs-health](https://gitlab.com/hs-health/hs-health)

Relevant issues:

* [Write a hidden service hsdir health measurer](https://gitlab.torproject.org/tpo/network-health/metrics/analysis/-/issues/13209)
* [Write tool for onion service health assessment (#28841)](https://gitlab.torproject.org/tpo/core/tor/-/issues/28841)
