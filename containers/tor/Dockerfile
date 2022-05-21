FROM debian:stable
MAINTAINER Silvio Rhatto <rhatto@torproject.org>

ENV APP="tor"
ENV APP_BASE="/etc"
ENV SHELL="/bin/bash"

WORKDIR ${APP_BASE}/${APP}

RUN apt-get update && \
    apt-get install -y \
    tor basez \
    && rm -rf /var/lib/apt/lists/*

COPY containers/tor/torrc ${APP_BASE}/${APP}/torrc

RUN chown -R debian-tor. ${APP_BASE}/${APP}/torrc

RUN chmod 600 ${APP_BASE}/${APP}/torrc

USER debian-tor

ENTRYPOINT [ "/usr/bin/tor", "-f", "/etc/tor/torrc" ]

EXPOSE 9050 9051
