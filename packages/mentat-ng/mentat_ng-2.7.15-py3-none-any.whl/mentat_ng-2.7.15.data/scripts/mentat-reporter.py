#!python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license.
#-------------------------------------------------------------------------------


"""
This Mentat module is a script providing periodical event reports to target abuse
groups.

To view built-in help please execute the application with ``--help`` command line
option::

    mentat-reporter.py --help

To view local documentation please use ``pydoc3``::

    pydoc3 mentat.module.reporter

This script is implemented using the :py:mod:`pyzenkit.zenscript` framework and
so it provides all of its core features. See the documentation for more in-depth
details.


License
^^^^^^^

Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
Use of this source is governed by the MIT license.
"""


__author__  = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


#
# Custom libraries.
#
from mentat.module.reporter import MentatReporterScript

#
# Execute the script.
#
if __name__ == "__main__":

    MentatReporterScript().run()
