# TODO

## Meta

* [ ] Move tasks to the [issue tracker](https://gitlab.torproject.org/tpo/onion-services/onionprobe/-/issues).
* [ ] CONTRIBUTING instructions.

## Prometheus

* [ ] Authentication (if not done by a frontend proxy).
* [ ] Support for Onion Service exporter endpoint with optional client authorization.

## Enhancements

* [ ] Reporting with CSV and JSON outputs.
* [ ] Support for URL fragments.
* [ ] Daemon mode.
* [ ] Option to run just for a fixed number of iterations.
* [ ] Option to run just for a definite amount of time.
* [ ] Option to run until a given date.
* [ ] Configuration:
  * [ ] Config file auto lookup:
    * Current folder.
    * `$XDG_CONFIG_HOME/onionprobe`: local configurations.
    * `$sysconfigdir/onionprobe`.
  * [ ] Config file description field.

## Metrics

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

* [ ] Other distros (ArchLinux, rpm, *BSDs).

## Documentation

* [ ] Better documentation.
* [ ] API Docs.

## Plumbing

* [ ] Clear the Stem Controller cache at every path probing and not only for each endpoint probing.
* [ ] `ControlSocket` support using `stem.control.Controller.from_socket_file()`.
* [ ] Built-in `HashedControlPort` generation to not leak password information to command as `tor --hash-password` does.
      See discussion [here](https://tor.stackexchange.com/questions/6448/how-does-the-tor-hash-password-option-work#12068).

## Bonus

* [ ] Non-http endpoints (regular TCP).
* [ ] Support for [Client Authorization](https://community.torproject.org/onion-services/advanced/client-auth/).
* [ ] Try to get the descriptor from multiple (if not all) HSDirs where it should be available.
* [ ] Watch for config file changes (hot reload), possibly using
      [watchdog](https://pythonhosted.org/watchdog/) ([debian package](https://tracker.debian.org/pkg/python-watchdog)).
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
* [ ] Support for heartbeat mode: an authenticated and persistent Onion Service
      with enables other Onionprobe instances to check if the current instance is
      up and running, allowing for notifications and other actions in case of
      failure.
