# Development

Onionprobe development guidelines and workflow are listed here.

## Release procedure

Release cycle workflow.

### Version update

Set the version number:

    ONIONPROBE_VERSION=1.2.1

Update the version in some files, like:

    dch -i # debian/changelog
    $EDITOR packages/onionprobe/config.py
    $EDITOR docker-compose.yml
    $EDITOR setup.cfg

### Regenerate the manpage

    make manpage

### Register the changes

Update the ChangeLog:

    $EDITOR ChangeLog

Commit and tag:

    git diff # review
    git commit -a -m "Feat: Onionprobe $ONIONPROBE_VERSION"
    git tag -s $ONIONPROBE_VERSION -m "Onionprobe $ONIONPROBE_VERSION"

Push changes and tags. Example:

    git push origin        && git push upstream
    git push origin --tags && git push upstream --tags

Once a tag is pushed, a [GitLab release][] is created.

[GitLab release]: https://docs.gitlab.com/ee/user/project/releases/

### Build packages

Build and then upload the Python package in the Test PyPi instance:

    make build-python-package
    make upload-python-test-package

Try the test package in a fresh virtual machine, which can be installed
directly from [Test PyPI](https://test.pypi.org):

    sudo apt-get install -y python3-pip tor
    pip install -i https://pypi.org/simple/ \
                --extra-index-url https://test.pypi.org/simple \
                --break-system-packages \
                onionprobe==$ONIONPROBE_VERSION

Make sure to test after installation. If the the package works as expected,
upload it to PyPi:

    make upload-python-package

### Announcement

Announce the new release:

* Post a message to the [Tor Forum][], using the [onion-services-announce tag][].
* Send a message to the [tor-announce][] mailing list ONLY in special cases,
  like important security issues (severity `HIGH` or `CRITICAL`).

Template:

```
Subject: [RELEASE] Onionprobe [security] release $ONIONPROBE_VERSION

Greetings,

We just released [Onionprobe][] $ONIONPROBE_VERSION, a tool for testing and
monitoring the status of Onion Services.

[This release fixes a security issue. Please upgrade as soon as possible!]

[This release [also] requires a database migration for those using the monitoring node:]
[https://onionservices.torproject.org/apps/web/onionprobe/upgrading/]

[Onionprobe]: https://onionservices.torproject.org/apps/web/onionprobe

# ChangeLog

$CHANGELOG
```

[tor-announce]: https://lists.torproject.org/cgi-bin/mailman/listinfo/tor-announce
[Tor Forum]: https://forum.torproject.org
[onion-services-announce tag]: https://forum.torproject.org/tag/onion-services-announce

## Testing

### Writing and trying unit tests for Prometheus

The [Prometheus][] alerts shipped by Onionprobe are tested by the `prom` [CI job][].
The configuration is available under the [configs/prometheus][] folder.

#### Workflow

A quick workflow to try tests before pushing to CI can be set with the
[standalone][] node:

    ./onionprobe-monitor up
    ./onionprobe-monitor shell prometheus
    promtool test rules /etc/prometheus/prometheus-tests.yml

[Prometheus]: https://prometheus.io/
[CI job]: https://docs.gitlab.com/ee/ci
[configs/prometheus]: https://gitlab.torproject.org/tpo/onion-services/onionprobe/-/tree/main/configs/prometheus
[standalone]: standalone.md

#### References

References for understanding and writing unit tests for [Prometheus][]:

* [Unit Testing for Rules | Prometheus](https://prometheus.io/docs/prometheus/latest/configuration/unit_testing_rules/)
* [Sleep Soundly: Reliable Alerting with Unit Testing in Prometheus | by Rubén Cougil Grande | Medium](https://medium.com/@rcougil/sleep-soundly-realiable-alerting-with-unit-testing-in-prometheus-260c652a3f9)
* [A Guide to Unit Testing Prometheus Alerts - Aviator Blog](https://www.aviator.co/blog/a-guide-to-unit-testing-prometheus-alerts/#)
* [Testing alerts - prometheus · Wiki · The Tor Project / TPA / TPA team · GitLab](https://gitlab.torproject.org/tpo/tpa/team/-/wikis/service/prometheus#testing-alerts)
