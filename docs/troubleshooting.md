# Onionprobe Troubleshooting

This section documents common problems with Onion Services reported by
Onionprobe, and gives hints in how to diagnose and solve them.

## What is tested

Onionprobe performs several tests in Onionprobe endpoints, being able to check:

1. Onion Service descriptor reachability.
2. Onion Service reachability.
3. TLS Certificate validity for the Onion Service, but only
    * If TLS/HTTPS is expected for the Onion Service.
    * If the certificate check is enabled (with the `--tls_verify`
      [option][man]).
4. HTTP status code for the Onion Service.

[man]: man/README.md

For some of these tests, [Prometheus][] alerting rules are available in the
[default configuration][prometheus-rules.yml], to be triggered in case of
failures.

The meaning of these alerts, along with basic steps to fix problems, are
given in the next section.

[Prometheus]: https://prometheus.io/
[prometheus-rules.yml]: https://gitlab.torproject.org/tpo/onion-services/onionprobe/-/blob/main/configs/prometheus/prometheus-rules.yml

## Prometheus alerts

### Onion Service unreachable

This alert means that Onionprobe was unable to connect to the Onion Service.

There are many causes for this alert:

1. The Onion Service is offline.
2. There is a problem with the Tor connectivity in the machine Onionprobe runs.
3. There is a problem with the Onion Service descriptor (details below).

!!! tip "Checking Onion Service reachability"

    To check whether the service is really offline, try connecting manually from
    another machine.

!!! note "Fixing an offline Onion Service"

    Fixing an offline Onion Service depends on how it's configured.  Usually,
    restarting the service does the job.

    Please check the related documentation from the Onion Service tool you're
    using.

    Example: if you're using [Onionspray][], check it's [troubleshooting
    guide](../onionspray/guides/troubleshooting.md).

[Onionspray]: ../onionspray/README.md

### Onion Service descriptor unreachable

Onionprobe is unable to fetch the Onion Service descriptor for a given service.
This descriptor is a document with directions for connecting to the Onion Service.
If the descriptor is unreachable, there's no way a connection to the service can happen.

There are many causes for this alert:

1. The descriptor might not be available in the Onion Service Descriptor
   Directory (also called `HSDir`) when the service is offline or have issues
   preventing a descriptor upload in the responsible `HSDirs`.
    * _To check whether the service is really offline, try connect manually from
     another machine_ (check the section above for details).
2. Onionprobe itself had trouble to connect to one of the current `HSDirs`
   hosting the descriptor, possibly due to a problem in the machine Onionprobe
   runs or due to temporary unreachability issues with the Tor network. To test that,
    * _Check whether the machine were Onionprobe runs is able reach the Tor network_.
3. The `HSDir` has issues: maybe it's offline, or overloaded, or under Denial
   of Service (DoS).

### Invalid TLS certificate for the Onion Service

This alert means that the Onion Service is listening to TLS connections, but it's
offering an invalid certificate.

The TLS certificate might be invalid in various ways, like:

1. It's self-signed. Some HTTP Onion Services offer self-signed certs, and
   while some applications may accept these self-signed certificates for Onion
   Services without displaying warnings, Onionprobe will complain if the
   certificate is self-signed and the `--tls_verify` [option][man]
   is active (which might be the default).
2. The TLS certificate expired.
3. It's `SubjectAltName` does not match the Onion Service address.
4. It's malformed or don't pass other validation tests done by the TLS library
   on the client side.
5. If there's problem in the connection between the Onion Service server and a
   backend application. This is uncommon, but might happen.
   Since Onion Services uses peer-to-peer encryption between the client
   and the service, an invalid TLS certificate usually only means a service
   misconfiguration. But if the connection between the Onion Service server and
   the backend application is compromised, there are chances that an invalid
   certificate means someone (or something) was able to tamper the connection
   between the Onion Service and the backend.

A fix for this alert involves:

1. Generating a new TLS certificate for the service.
   This is the most common fix for this alert.
2. Double checking the connection between the Onion Service server and the
   backend application, to make sure that the expected certificate is
   presented.

### Expiring TLS certificate for the Onion Service

This alert is triggered when a TLS certificate offered by an Onion Service
will expire in less than a week.

A fix for this alert involves generating a new TLS certificate for the service.

### Unexpected HTTP status code

This alert fires when Onionprobe receives an unexpected HTTP status code.
By default, Onionprobe expects a HTTP `200` status code, but this can be
configured for each path tested on each Onion Service.

An unexpected status code might mean that the application served by the
Onion Service is malfunctioning.
