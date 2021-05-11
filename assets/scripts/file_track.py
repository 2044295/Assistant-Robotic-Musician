#!/usr/bin/env python3

import sys
import smml

filename = sys.argv[1]
with open(filename, 'r') as myfile:
    try:
        smml.track(myfile.read(), smml.nodeio.output)
    except KeyboardInterrupt:
        pass
