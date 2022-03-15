# Onionprobe

![Onionprobe Logo](assets/logo.jpg "Onionprobe")

Onionprobe is a tool for testing and monitoring the status of
[Tor Onion Services](https://community.torproject.org/onion-services/).

## Specs

Thanks @irl for the idea/specs/tasks and @hiro for suggestions.

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

### Prometheus integration

* [ ] Exports Prometheus metrics for the connection to the onion service, and
      extra metrics per path on the status code for each path returned by the server.
* [ ] Try to get the descriptor from multiple (if not all) HSDirs where it
      should be available.
* [ ] To get the timings right, the tool should take care of the test frequency and
      just expose the metrics rather than having Prometheus scraping individual
      targets on Prometheus' schedule.
* [ ] Add in additional timing metrics wherever appropriate.

### Enhancements

* [x] Dockerfile (and optionally a Docker Compose).
* [ ] Enhanced logging/reporting.
* [ ] Python packaging (`requirements.txt` or other format).
* [ ] Documentation.
* [ ] Tests.

### Bonus

* [x] Optionally launch it's [own Tor process](https://stem.torproject.org/api/process.html)
      like in [this example](https://stem.torproject.org/tutorials/to_russia_with_love.html#using-pycurl).
* [ ] `ControlSocket` support using `stem.control.Controller.from_socket_file()`.
* [ ] Built-in `HashedControlPort` generation see discussion
      [here](https://tor.stackexchange.com/questions/6448/how-does-the-tor-hash-password-option-work#12068).
* [ ] Multitasking: multiple threads/workers continuously probing endpoints
      with a centralized reporting data structure. This helps splitting
      data gathering from presentation logic, especially with the Prometheus
      exporter. Not a requirement for Prometheus, since the [official client](https://github.com/prometheus/client_python)
      already [uses](https://github.com/prometheus/client_python/blob/789b24a47148f63109626958fe2eb1ad9231f9c3/prometheus_client/exposition.py#L142)
      a [threaded socketserver](https://docs.python.org/3.8/library/socketserver.html#socketserver.ThreadingMixIn).

## References

References and inspirations:

* If using the prometheus exporter with python, try to just use request and
  beautiful soup to check that the page is returning what one expects.
* Use the existing blackbox_exporter timing metrics as a model.

## Alternatives

* [OnionScan](https://onionscan.org/)
* [BrassHornCommunications/OnionWatch: A GoLang daemon for notifying Tor Relay and Hidden Service admins of status changes](https://github.com/BrassHornCommunications/OnionWatch)
* [systemli/prometheus-onion-service-exporter: Prometheus Exporter for Tor Onion Services](https://github.com/systemli/prometheus-onion-service-exporter)
* [prometheus/blackbox_exporter: Blackbox prober exporter](https://github.com/prometheus/blackbox_exporter), which could be configured using `proxy_url`
  pointing to a [Privoxy](http://www.privoxy.org/) instance relaying traffic to `tor` daemon.
