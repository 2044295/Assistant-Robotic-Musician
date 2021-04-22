#!/usr/bin/env python3

import sys
import smml

filename = sys.argv[1]
with open(filename, 'r') as myfile:
    text = ''.join([x.strip() for x in myfile.read().split('\n')])
    smml.nodeio.output(smml.markup.process(text, 'display'))
