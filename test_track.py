#!/usr/bin/env python3

import smml
with open('samples/sampleSimple.html', 'r') as myfile:
    smml.track(myfile.read(), smml.nodeio.output)
