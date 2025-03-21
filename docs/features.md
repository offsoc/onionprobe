# Onionprobe features

## Monitor from anywhere

Onionprobe can monitor [Onion Services][] from the "outside", i.e, it does not need
to run on the same premises the Onion Services are running: the monitoring tool
can be set anywhere on the Internet, as long as the Tor network can be reached.

[Onion Services]: https://community.torproject.org/onion-services/

## Monitor any public service

Onionprobe allows monitoring _any_ public Onion Service website: you don't have
to be that onionsite operator in order to monitor it. The only thing you need
is to know it's address.

## Monitor many services at once

A single Onionprobe instance can monitor many Onion Services, making it
suitable for large infrastructures as well as for researchers interested
in collecting public available data on service reachability.

## Get data that represents the user experience

Onionprobe's collected data better represents the actual user experience in
terms of Onion Service reachability and performance. It does not collect fine
grained server data like those exposed directly by the Tor daemon (like the
[MetricsPort][] option on [C Tor][]), but it experiments the effective network
latencies and intermittencies a user would face.

[C Tor]: https://gitlab.torproject.org/tpo/core/tor
[MetricsPort]: https://onionservices.torproject.org/apps/web/checklist/#metricsport

## Runs out-of-the box

Onionprobe's [standalone monitoring node](standalone.md) comes with everything
needed to test, measure and visualize Onion Service connectivity data, all
batteries included.

Still, advanced Onion Service Operators can run just the core Onionprobe
service, or even use it as a library in other applications.
Check out the [installation options](installation.md) for details.
