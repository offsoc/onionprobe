# Development

Onionprobe development guidelines and workflow are listed here.

## Release procedure

Release cycle workflow.

### Version update

Set the version number:

    ONIONPROBE_VERSION=1.1.0

Update the version in some files, like:

* `debian/changelog` (via `dch -i`)
* `packages/onionprobe/config.py`
* `setup.cfg`

### Regenerate the manpage

    make manpage

### Register the changes

* Update the ChangeLog.
* Commit and tag. Push changes and tags.

### Build packages

Build and then upload the Python package in the Test PyPi instance:

    make build-python-package
    make upload-python-test-package

Try the test package in a fresh virtual machine, eg:

    sudo apt-get install -y python3-pip tor
    pip install -i https://test.pypi.org/simple/ \
                --extra-index-url https://pypi.org/simple \
                onionprobe==$ONIONPROBE_VERSION

Make sure to test after installation. If the the package works as expected,
upload it to PyPi:

    make upload-python-package
