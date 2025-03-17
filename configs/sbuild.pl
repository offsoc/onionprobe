#
# Onionprobe sbuild config.
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
# Adapted from https://wiki.debian.org/sbuild
# Set the chroot mode to be unshare.

$chroot_mode = 'unshare';

$external_commands = { "build-failed-commands" => [ [ '%SBUILD_SHELL' ] ] };

# Uncomment below to specify the distribution; this is the same as passing `-d unstable` to sbuild.
# Specifying the distribution is currently required for piuparts when the changelog targets UNRELEASED.  See #1088928.
#$distribution = 'experimental';
$distribution = 'unstable';
#$distribution = 'bookworm-backports';

# Specify an extra repository; this is the same as passing `--extra-repository` to sbuild.
#$extra_repositories = ['deb http://deb.debian.org/debian bookworm-backports main'];
#$extra_repositories = ['deb http://deb.debian.org/debian experimental main'];

# Specify the build dependency resolver; this is the same as passing `--build_deps_resolver` to sbuild.
# When building with extra repositories, often 'aptitude' is better than 'apt' (the default).
#$build_dep_resolver = 'aptitude';

# Build Architecture: all packages; this is the same as passing `-A` to sbuild.
$build_arch_all = 1;

# Build the source package in addition to the other requested build artifacts; this is the same as passing `-s` to sbuild.
$build_source = 1;

# Produce a .changes file suitable for a source-only upload; this is the same as passing `--source-only-changes` to sbuild.
$source_only_changes = 1;

## Run lintian after every build (in the same chroot as the build); use --no-run-lintian to override.
$run_lintian = 1;
# Display info tags.
#$lintian_opts = ['--display-info', '--verbose', '--fail-on', 'error,warning', '--info'];
# Display info and pedantic tags, as well as overrides.
#$lintian_opts = ['--display-info', '--verbose', '--fail-on', 'error,warning', '--info', '--pedantic', '--show-overrides'];
$lintian_opts = ['-i', '-I', '--pedantic'];

## Run autopkgtest after every build (in a new, clean, chroot); use --no-run-autopkgtest to override.
$run_autopkgtest = 1;
# Specify autopkgtest options.  The commented example below is the default since trixie.
#$autopkgtest_opts = ['--apt-upgrade', '--', 'unshare', '--release', '%r', '--arch', '%a' ];

## Run piuparts after every build (in a new, temporary, chroot); use --no-run-piuparts to override.
# this does not work in bookworm
$run_piuparts = 1;
# Build a temporary chroot.
$piuparts_opts = ['--no-eatmydata', '--distribution=%r', '--fake-essential-packages=systemd-sysv'];
# Build a temporary chroot that uses apt-cacher-ng as a proxy to save bandwidth and time and doesn't disable eatmydata to speed up processing.
#$piuparts_opts = ['--distribution=%r', '--bootstrapcmd=mmdebstrap --skip=check/empty --variant=minbase --aptopt="Acquire::http { Proxy \"http://127.0.0.1:3142\"; }"'];
