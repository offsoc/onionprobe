% ONIONPROBE(1) Onionprobe User Manual
% Silvio Rhatto <rhatto@torproject.org>
% Apr 11, 2022

# NAME

Onionprobe - a test/monitor tool for Onion Services sites

# SYNOPSIS

onionprobe [-h] [-c <*config*>] [-e <*onion-address1*> ...] [-v]

# DESCRIPTION

Onionprobe is a tool for testing and monitoring the status of Tor Onion
Services sites.

It can run a single time or continuously to probe a set of
onion services endpoints and paths, optionally exporting to Prometheus.

# OPTIONS

-v, --version
:   Display version

-h, --help
:   Display basic help

-c, --config <*config*>
:   Specify configuration file to use

-e, --endpoint <*onion-address1*> [<*onion-address2*> ... <*onion-addressN*>]
:   Add .onion URLs to the list of endpoints to be tested

# FILES

/etc/onionprobe
:  System-wide Onionprobe configuration files.

# LIMITATIONS

Onionprobe currently has the following limitations:

1. Only works for Onion Services websites, i.e, those served via
   either HTTP or HTTPS.

# SEE ALSO

The *README* file distributed with Onionprobe contains the full documentation.

The Onionprobe source code and all documentation may be downloaded from
<https://gitlab.torproject.org/onion-services/onionprobe>.
