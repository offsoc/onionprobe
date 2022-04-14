#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Generates Onionprobe manpage from CLI usage and templates.
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
import os
import datetime
import re
from onionprobe.config import cmdline_parser, basepath

def generate():
    """
    Produces the manpage in Markdown format.

    Apply argument parser usage and help into a template.

    """

    # Set inputs and outputs
    template   = os.path.join(basepath, 'docs', 'man', 'onionprobe.1.md.tmpl')
    output     = os.path.join(basepath, 'docs', 'man', 'onionprobe.1.md')

    # Initialize the command line parser
    parser     = cmdline_parser()

    # Compile some handy regexps
    lines      = re.compile('^',    re.MULTILINE)
    trailing   = re.compile('^ *$', re.MULTILINE)

    # Compile template variables
    usage      = parser.format_usage().replace('usage: ', '')
    invocation = trailing.sub('', lines.sub('    ', parser.format_help())).replace('usage: ', '')
    date       = datetime.datetime.now().strftime('%b %d, %Y')

    with open(template, 'r') as template_file:
        with open(output, 'w') as output_file:
            contents = template_file.read()

            output_file.write(contents.format(date=date, usage=usage, invocation=invocation))

# Process from CLI
if __name__ == "__main__":
    generate()
