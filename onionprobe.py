#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Onionprobe test/monitor tool.
#
# Copyright (C) 2022 Silvio Rhatto <rhatto@torproject.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License,
# or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Dependencies
from modules.onionprobe.app    import Onionprobe
from modules.onionprobe.config import cmdline

if __name__ == "__main__":
    """Process from CLI"""

    args = cmdline()

    # Dispatch
    try:
        probe = Onionprobe(args)

        if probe.initialize() is not False:
            probe.run()
            probe.close()
        else:
            print('Error: could not initialize')
            exit(1)

    #except (FileNotFoundError, KeyboardInterrupt) as e:
    except Exception as e:
        probe.log(e, 'error')
        probe.close()
        exit(1)
