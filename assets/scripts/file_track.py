#!/usr/bin/env python3

import sys
import smml

filename = sys.argv[1]
with open('samples/sampleSimple.html', 'r') as myfile:
    smml.track(myfile.read(), smml.nodeio.output)
