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
upgraded to a new [postgres image][] version.

[tianon/docker-postgres-upgrade]: https://github.com/tianon/docker-postgres-upgrade
[tpo/onion-services/onionprobe#70]: https://gitlab.torproject.org/tpo/onion-services/onionprobe/-/issues/70
[postgres image]: https://hub.docker.com/_/postgres
[^docker-postgres-upgrade]: See [tpo/onion-services/onionprobe#70][] for more information.


```shell
$ docker volume inspect onionprobe_postgres
[
    {
        "CreatedAt": "2023-02-01T17:53:55Z",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.project": "onionprobe",
            "com.docker.compose.version": "1.27.4",
            "com.docker.compose.volume": "postgres"
        },
        "Mountpoint": "/var/lib/docker/volumes/onionprobe_postgres/_data",
        "Name": "onionprobe_postgres",
        "Options": null,
        "Scope": "local"
    }
]
$ WORK=/some/working/path/postgres-upgrade-testing
$ mkdir -p $WORK
$ cd $WORK
$ OLD="`sudo cat /var/lib/docker/volumes/onionprobe_postgres/_data/PG_VERSION`"
$ NEW='15'
$ PGUSER=grafana
$ mkdir $OLD
$ mkdir -p $NEW/data
$ chmod 700 $NEW/data
$ sudo cp -a /var/lib/docker/volumes/onionprobe_postgres/_data/ $OLD/data
$ docker pull "postgres:$OLD"
$ docker pull "postgres:$NEW"
$ docker run --rm \
  -e PGUSER=$PGUSER -e POSTGRES_INITDB_ARGS=--username=$PGUSER \
  -v "$WORK":/var/lib/postgresql \
  "tianon/postgres-upgrade:$OLD-to-$NEW" \
  --link
$ docker rm postgres-upgrade-testing
$ docker run -dit \
  -e PGUSER=$PGUSER -e POSTGRES_INITDB_ARGS=--username=$PGUSER \
  --name postgres-upgrade-testing \
  -e POSTGRES_PASSWORD=password \
  -v "$WORK/$NEW/data":/var/lib/postgresql/data \
  "postgres:$NEW" # see https://github.com/tianon/docker-postgres-upgrade/issues/70
$ sleep 5
$ docker logs --tail 100 postgres-upgrade-testing
$ docker stop postgres-upgrade-testing
$ docker rm postgres-upgrade-testing
$ echo "host all all all scram-sha-256" sudo tee -a $NEW/data/pg_hba.conf # see https://github.com/tianon/docker-postgres-upgrade/issues/1
$ sudo mv /var/lib/docker/volumes/onionprobe_postgres/_data /var/lib/docker/volumes/onionprobe_postgres/_data.`date +%Y%m%d`
$ sudo cp -a $NEW/data /var/lib/docker/volumes/onionprobe_postgres/_data
```

Sample database upgrade output:

    The files belonging to this database system will be owned by user "postgres".
    This user must also own the server process.

    The database cluster will be initialized with locale "en_US.utf8".
    The default database encoding has accordingly been set to "UTF8".
    The default text search configuration will be set to "english".

    Data page checksums are disabled.

    fixing permissions on existing directory /var/lib/postgresql/15/data ... ok
    creating subdirectories ... ok
    selecting dynamic shared memory implementation ... posix
    selecting default max_connections ... 100
    selecting default shared_buffers ... 128MB
    selecting default time zone ... Etc/UTC
    creating configuration files ... ok
    running bootstrap script ... ok
    performing post-bootstrap initialization ... ok
    syncing data to disk ... initdb: warning: enabling "trust" authentication for local connections
    initdb: hint: You can change this by editing pg_hba.conf or using the option -A, or --auth-local and --auth-host, the next time you run initdb.
    ok


    Success. You can now start the database server using:

        pg_ctl -D /var/lib/postgresql/15/data -l logfile start

    Performing Consistency Checks
    -----------------------------
    Checking cluster versions                                   ok
    Checking database user is the install user                  ok
    Checking database connection settings                       ok
    Checking for prepared transactions                          ok
    Checking for system-defined composite types in user tables  ok
    Checking for reg* data types in user tables                 ok
    Checking for contrib/isn with bigint-passing mismatch       ok
    Creating dump of global objects                             ok
    Creating dump of database schemas                           ok
    Checking for presence of required libraries                 ok
    Checking database user is the install user                  ok
    Checking for prepared transactions                          ok
    Checking for new cluster tablespace directories             ok

    If pg_upgrade fails after this point, you must re-initdb the
    new cluster before continuing.

    Performing Upgrade
    ------------------
    Analyzing all rows in the new cluster                       ok
    Freezing all rows in the new cluster                        ok
    Deleting files from new pg_xact                             ok
    Copying old pg_xact to new server                           ok
    Setting oldest XID for new cluster                          ok
    Setting next transaction ID and epoch for new cluster       ok
    Deleting files from new pg_multixact/offsets                ok
    Copying old pg_multixact/offsets to new server              ok
    Deleting files from new pg_multixact/members                ok
    Copying old pg_multixact/members to new server              ok
    Setting next multixact ID and offset for new cluster        ok
    Resetting WAL archives                                      ok
    Setting frozenxid and minmxid counters in new cluster       ok
    Restoring global objects in the new cluster                 ok
    Restoring database schemas in the new cluster               ok
    Adding ".old" suffix to old global/pg_control               ok

    If you want to start the old cluster, you will need to remove
    the ".old" suffix from /var/lib/postgresql/14/data/global/pg_control.old.
    Because "link" mode was used, the old cluster cannot be safely
    started once the new cluster has been started.

    Linking user relation files                                 ok
    Setting next OID for new cluster                            ok
    Sync data directory to disk                                 ok
    Creating script to delete old cluster                       ok
    Checking for extension updates                              ok

    Upgrade Complete
    ----------------
    Optimizer statistics are not transferred by pg_upgrade.
    Once you start the new server, consider running:
        /usr/lib/postgresql/15/bin/vacuumdb --all --analyze-in-stages

    Running this script will delete the old cluster's data files:
        ./delete_old_cluster.sh
