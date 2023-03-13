# Upgrading

Onionprobe adopts the [Semantic Versioning 2.0.0][], which means that any major
version might have breaking changes on previous installations.

The [ChangeLog][] file contains the list of main changes from version to version, including
breaking changes.

The following subsections documents other upgrade procedures, such as database updates.

[Semantic Versioning 2.0.2]: https://semver.org/spec/v2.0.0.html
[ChangeLog]: https://gitlab.torproject.org/tpo/onion-services/onionprobe/-/blob/main/ChangeLog.md

## Standalone monitoring node

Upgrade procedures for the [standalone monitoring node](standalone.md).

[PostgreSQL]: https://postgresql.org

### PostgreSQL database

This procedure is based on the [tianon/docker-postgres-upgrade][]
approach[^docker-postgres-upgrade] and needs to be done whenever Onionprobe is
upgraded to a new [postgres image][] version:

1. Stop the monitoring node: `docker compose down`.
2. Run the upgrade script and follow it's instructions: `./scripts/upgrade-postgresql-database`.
3. Start the containers: `make run-containers`.

[tianon/docker-postgres-upgrade]: https://github.com/tianon/docker-postgres-upgrade
[tpo/onion-services/onionprobe#70]: https://gitlab.torproject.org/tpo/onion-services/onionprobe/-/issues/70
[postgres image]: https://hub.docker.com/_/postgres
[^docker-postgres-upgrade]: See [tpo/onion-services/onionprobe#70][] for more information.
