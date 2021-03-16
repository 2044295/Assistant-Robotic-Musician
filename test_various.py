#!/usr/bin/env python3

import json
import smml

with open('samples/sampleSMML.html', 'r') as myfile:
    text = smml.markup.read(myfile.read())
    print(json.dumps(smml.markup.smmlprocess(text, 'display'), indent=2))
