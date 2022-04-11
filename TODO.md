# TODO

## Basic

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

## Meta

* [x] Dockerfile (and optionally a Docker Compose).
* [x] Environment variable controlling the configuration file to use.
* [x] Move the repository to the [Onion Services Gitlab group](https://gitlab.torproject.org/tpo/onion-services).
* [x] Docstrings.
* [x] Refactor into smaller modules.
* [ ] Move tasks to the [issue tracker](https://gitlab.torproject.org/tpo/onion-services/onionprobe/-/issues).

## Prometheus

* [x] Exports Prometheus metrics for the connection to the onion service, and
      extra metrics per path on the status code for each path returned by the server.
      If using the prometheus exporter with python, consider to just use request and
      beautiful soup to check that the page is returning what one expects.
* [x] Add in additional metrics wherever appropriate.
* [x] To get the timings right, the tool should take care of the test frequency and
      just expose the metrics rather than having Prometheus scraping individual
      targets on Prometheus' schedule.
* [ ] Authentication (if not done by a frontend proxy).

## Probing

* [x] Set timeout at `get_hidden_service_descriptor()`.
* [x] Set timeout at `Requests`.
* [x] Set `CircuitStreamTimeout` in the built-in Tor daemon.
* [x] HTTPS certificate validation check/exception.
* [x] Max retries before throwing an error when getting descriptors.
      This could help answering the following questions:
    * [When an onion service lookup has failed at the first k HSDirs we tried, what are the chances it will still succeed?](https://gitlab.torproject.org/tpo/network-health/analysis/-/issues/28)
    * [What's the average number of hsdir fetches before we get the hsdesc?](https://gitlab.torproject.org/tpo/core/tor/-/issues/13208)
* [x] Max retries before throwing an error when querying the endpoint.

## Enhancements

* [x] Better logging.
* [x] Better exception handling.
* [ ] Better reporting/outputs.
* [ ] Additional command line options.
* [ ] Support for URL fragments.
* [ ] Daemon mode.

## Metrics

* [x] Status: sleeping, probing, starting or stopping.
* [x] Match found / not found.
* [x] Metric units in the description.
* [x] Number of introduction points.
* [x] Timestamp label.
* [x] Register HSDir used to fetch the descriptor.
      Check the [control-spec](https://gitlab.torproject.org/tpo/core/torspec/-/blob/main/control-spec.txt)
      for `HSFETCH` command and the `HS_DESC` event ([using SETEVENTS](https://stem.torproject.org/tutorials/down_the_rabbit_hole.html)).
      Relevant issues:
* [ ] Current introduction points (info metric type?).
* [ ] Response size.
* [ ] Response content type.
* [ ] Other relevant response metadata and headers.
* [ ] Review metrics names and types (use "elapsed" instead of "latency", "query" instead of "fetch" etc).

## Logging

* [ ] Logfile support.
* [ ] Parseable log format.

## Tests

* [ ] Gitlab CI.
* [ ] Testing subsystem.
* [ ] Test cases:
  * [ ] Descriptor unavailable.
  * [ ] Invalid descriptor.
  * [ ] Invalid X.509 certificate.
  * [ ] Connection errors / timeout.
  * [ ] Path not found.
  * [ ] Pattern not found.

## Packaging

* [x] Python packaging (PyPI, `requirements.txt` or other format).
* [ ] Distro packaging (Debian, ArchLinux, rpm).

## Documentation

* [x] Manpage.
* [ ] Better documentation.
* [ ] API Docs.

## Plumbing

* [ ] Clear the Stem Controller cache at every path probing and not only for each endpoint probing.
* [ ] Handling SIGKILL and other signals.
* [ ] `ControlSocket` support using `stem.control.Controller.from_socket_file()`.
* [ ] Built-in `HashedControlPort` generation to not leak password information to command as `tor --hash-password` does.
      See discussion [here](https://tor.stackexchange.com/questions/6448/how-does-the-tor-hash-password-option-work#12068).

## Bonus

* [x] Optionally launch it's [own Tor process](https://stem.torproject.org/api/process.html)
      like in [this example](https://stem.torproject.org/tutorials/to_russia_with_love.html#using-pycurl).
* [x] Script that compiles configuration from [real-world-onion-sites](https://github.com/alecmuffett/real-world-onion-sites) repository.
* [x] Script that compiles configuration from [the SecureDrop API](https://securedrop.org/api/v1/directory/).
* [ ] Non-http endpoints (regular TCP).
* [ ] Support for [Client Authorization](https://community.torproject.org/onion-services/advanced/client-auth/).
* [ ] Try to get the descriptor from multiple (if not all) HSDirs where it should be available.
* [ ] Watch for config file changes (hot reload).
* [ ] Fetch config from external application, like `securedrop.py` or `real-world-onion-sites.py`.
* [ ] Architecture should be extensible to allow for different reporting options (stdout, Prometheus etc).
* [ ] Custom actions/hooks/triggers.
* [ ] Work as a Nagios/Icinga plugin, perhaps using the [nagiosplugin](https://pypi.org/project/nagiosplugin/) Python class.
      See [issue with discussion](https://gitlab.torproject.org/tpo/tpa/team/-/issues/27634).
* [ ] Work as a [Zabbix plugin](https://www.zabbix.com/integrations/python).
* [ ] Multitasking: multiple threads/workers continuously probing endpoints
      with a centralized reporting data structure. This helps splitting
      data gathering from presentation logic, especially with the Prometheus
      exporter. Not a requirement for Prometheus, since the [official client](https://github.com/prometheus/client_python)
      already [uses](https://github.com/prometheus/client_python/blob/789b24a47148f63109626958fe2eb1ad9231f9c3/prometheus_client/exposition.py#L142)
      a [threaded socketserver](https://docs.python.org/3.8/library/socketserver.html#socketserver.ThreadingMixIn).
