# Onionprobe

![](assets/logo.jpg "Onionprobe")

[Onionprobe][] is a tool for testing and monitoring the status of
[Tor Onion Services](https://community.torproject.org/onion-services/) sites.

It can run a single time or continuously to probe a set of onion services
endpoints and paths, optionally exporting to
[Prometheus](https://prometheus.io) and with [Grafana](https://grafana.com/)
and [Alertmanager](https://github.com/prometheus/alertmanager) support.

Onionprobe can monitor Onion Services from the "outside", i.e, it does not need
to run on the same premises the Onion Services are running: the monitoring tool
can be set anywhere on the Internet, as long as the Tor network can be reached.

Onionprobe's collected data better represents the actual user experience in
terms of Onion Service reachability and performance. It does not collect fine
grained server data like those exposed directly by the Tor daemon (like the
[MetricsPort][] option on [C Tor][]), but it experiments the effective network
latencies and intermittencies a user would face.

Onionprobe allows monitoring _any_ public Onion Service website: you don't have
to be that onionsite operator in order to monitor it. The only thing you need
is to know it's address.

A single Onionprobe instance can monitor many Onion Services, making it
suitable for large infrastructures as well as for researchers interested
in collecting public available data on service reachability.

[Onionprobe]: https://gitlab.torproject.org/tpo/onion-services/onionprobe
[C Tor]: https://gitlab.torproject.org/tpo/core/tor
[MetricsPort]: https://onionservices.torproject.org/apps/web/checklist/#metricsport
