#!/usr/bin/env python3

import sys
import smml

filename = sys.argv[1]
with open(filename, 'r') as myfile:
    try:
        audiofile = '.'.join(filename.split('.')[:-1]) + '.wav'
        smml.track(myfile.read(), smml.nodeio.output,\
            args={'type': 'file', 'file': audiofile, 'sample_rate': 44100})
    except KeyboardInterrupt:
        pass
