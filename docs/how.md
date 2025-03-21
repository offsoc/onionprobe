# How Onionprobe works

Roughly speaking, Onionprobe does the following:

* Reads a configuration where a number of Onion Services can be declared.
* It can be kept running in a loop, continuously trying to connect to each Onion
  Service.
* Metrics are collected and can be exported for each service tested, in the
  [Prometheus][] format.

Details on what's tested and reported are available in the [troubleshooting
page](troubleshooting.md).

[Prometheus]: https://prometheus.io
