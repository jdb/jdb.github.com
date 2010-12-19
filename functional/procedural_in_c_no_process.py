#!/usr/bin/env python
# procedural_with_processes_in_c_no_process.py

import sys 
from pi import pi

print "Pi with a C extension: %s" % pi(int(sys.argv[1]))
