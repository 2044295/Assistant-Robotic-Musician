#!/usr/bin/env python3

import sys
import smml

filename = sys.argv[1]
with open(filename, 'r') as myfile:
    text = smml.markup.read(myfile.read())
    smml.nodeio.output(smml.markup.smmlprocess(text, 'display'))
