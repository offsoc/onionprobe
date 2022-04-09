#
# Onionprobe Makefile.
#
# This Makefile is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3 of the License, or any later version.
#
# This Makefile is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place - Suite 330, Boston, MA 02111-1307, USA
#

.PHONY: configs

#
# Containers
#

run-containers:
	@docker-compose up -d

watch-containers:
	@watch docker-compose ps

log-containers:
	@docker-compose logs -f

#
# Configs
#

configs:
	@./packages/real-world-onion-sites.py
	@./packages/securedrop.py

#
# Packaging
#

clean:
	@find -name __pycache__ -exec rm -rf {} \;

build-package: clean
	@python3 -m build

upload-test-package:
	@twine upload --skip-existing --repository testpypi dist/*

upload-package:
	@twine upload --skip-existing dist/*
