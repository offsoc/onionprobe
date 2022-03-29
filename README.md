# Onionprobe

![Onionprobe Logo](assets/logo.jpg "Onionprobe")

Onionprobe is a tool for testing and monitoring the status of
[Tor Onion Services](https://community.torproject.org/onion-services/).

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

Just clone the repository

    git clone https://gitlab.torproject.org/tpo/onion-services/onionprobe
    cd onionprobe

## Usage

Right now Onionprobe works only with a configuration file.
A [sample config](configs/tor.yaml] is provided:

    ./onionprobe -c configs/tor.yaml

## Testing

Onionprobe comes with a working test environment with the [sample
configuration](configs/tor.yaml] and based on [Docker
Compose](https://docs.docker.com/compose/), which can be started using

    docker-compose up

Then point your browser to:

* The built-in Prometheus dashboard: https://localhost:9090
* The built-in Onionprobe Prometheus exporter: https://localhost:9091

## Tasks

See [TODO](TODO.md) and the [issue tracker](https://gitlab.torproject.org/tpo/onion-services/onionprobe/-/issues).

## Acknowledgements

Thanks:

* @irl for the idea/specs/tasks.
* @hiro for suggestions.
* @arma and @juga for references.

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
