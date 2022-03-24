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
A [sample config](onionprobe.yaml] is provided:

    ./onionprobe -c onionprobe.yaml

## Testing

Onionprobe comes with a working test environment with the [sample
configuration](onionprobe.yaml] and based on [Docker
Compose](https://docs.docker.com/compose/), which can be started using

    docker-compose up

Then point your browser to:

* The built-in Prometheus dashboard: https://localhost:9090
* The built-in Onionprobe Prometheus exporter: https://localhost:9091

## Tasks

### Basic

* [x] Take a list of onions to check and make sure that you can always fetch
      descriptors rather than just using cached descriptors etc.
* [x] Randomisation of timing to avoid systemic errors getting lucky and not
      detected.
* [x] Looping support: goes through the list of onions in a loop, testing one
      at a time continuously.
* [x] Flush descriptor caches so testing happens like if a fresh client.
* [x] Support for HTTP status codes.
* [x] Page load latency.
* [x] Ability to fetch a set of paths from each onion.
      Customisable by test path: not all our sites have content at the root,
      but do not bootstrap every time if that can be avoided.
* [x] Need to know about "does the site have useful content?"
      Regex for content inside the page: allow configuring a regex per path for
      what should be found in the returned content/headers.
* [x] Documentation.

### Prometheus integration

* [x] Exports Prometheus metrics for the connection to the onion service, and
      extra metrics per path on the status code for each path returned by the server.
      If using the prometheus exporter with python, consider to just use request and
      beautiful soup to check that the page is returning what one expects.
* [ ] Try to get the descriptor from multiple (if not all) HSDirs where it
      should be available.
* [ ] To get the timings right, the tool should take care of the test frequency and
      just expose the metrics rather than having Prometheus scraping individual
      targets on Prometheus' schedule.
* [ ] Add in additional metrics wherever appropriate.
* [ ] Authentication (if not done by a frontend proxy).
* [ ] Review metrics names and types (use "elapsed" instead of "latency" etc).

### Enhancements

* [x] Dockerfile (and optionally a Docker Compose).
* [x] Better logging.
* [x] Move the repository to the [Onion Services Gitlab group](https://gitlab.torproject.org/tpo/onion-services).
* [ ] Better reporting.
* [ ] Better exception handling.
* [ ] Non-http endpoints (regular TCP).
* [ ] Max retries before throwing an error for getting descriptors and querying the endpoint.
* [ ] More command line options.
* [ ] Refactor into smaller modules.
* [ ] Python packaging (`requirements.txt` or other format).
* [ ] Docstrings.
* [ ] Better documentation.
* [ ] Tests.
* [ ] Custom actions/hooks/triggers.

### Bonus

* [x] Optionally launch it's [own Tor process](https://stem.torproject.org/api/process.html)
      like in [this example](https://stem.torproject.org/tutorials/to_russia_with_love.html#using-pycurl).
* [ ] `ControlSocket` support using `stem.control.Controller.from_socket_file()`.
* [ ] HTTPS certificate validation check/exception.
* [ ] Built-in `HashedControlPort` generation to not leak password information to command as `tor --hash-password` does.
      See discussion [here](https://tor.stackexchange.com/questions/6448/how-does-the-tor-hash-password-option-work#12068).
* [ ] Architecture should be extensible to allow for different reporting options (stdout, Prometheus etc).
* [ ] Multitasking: multiple threads/workers continuously probing endpoints
      with a centralized reporting data structure. This helps splitting
      data gathering from presentation logic, especially with the Prometheus
      exporter. Not a requirement for Prometheus, since the [official client](https://github.com/prometheus/client_python)
      already [uses](https://github.com/prometheus/client_python/blob/789b24a47148f63109626958fe2eb1ad9231f9c3/prometheus_client/exposition.py#L142)
      a [threaded socketserver](https://docs.python.org/3.8/library/socketserver.html#socketserver.ThreadingMixIn).

## Acknowledgements

Thanks:

* @irl for the idea/specs/tasks.
* @hiro for suggestions.

## Alternatives

* [OnionScan](https://onionscan.org/)
* [BrassHornCommunications/OnionWatch: A GoLang daemon for notifying Tor Relay and Hidden Service admins of status changes](https://github.com/BrassHornCommunications/OnionWatch)
* [systemli/prometheus-onion-service-exporter: Prometheus Exporter for Tor Onion Services](https://github.com/systemli/prometheus-onion-service-exporter)
* [prometheus/blackbox_exporter: Blackbox prober exporter](https://github.com/prometheus/blackbox_exporter), which could be configured using `proxy_url`
  pointing to a [Privoxy](http://www.privoxy.org/) instance relaying traffic to `tor` daemon.
