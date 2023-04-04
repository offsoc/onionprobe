# Development

Onionprobe development guidelines and workflow are listed here.

## Release procedure

Release cycle workflow.

### Version update

Set the version number:

    ONIONPROBE_VERSION=1.1.0

Update the version in some files, like:

    dch -i # debian/changelog
    $EDITOR packages/onionprobe/config.py
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

### Build packages

Build and then upload the Python package in the Test PyPi instance:

    make build-python-package
    make upload-python-test-package

Try the test package in a fresh virtual machine, eg:

    sudo apt-get install -y python3-pip tor
    pip install -i https://pypi.org/simple/ \
                --extra-index-url https://test.pypi.org/simple \
                onionprobe==$ONIONPROBE_VERSION

Make sure to test after installation. If the the package works as expected,
upload it to PyPi:

    make upload-python-package
