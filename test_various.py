#!/usr/bin/env python3

import json
import smml

"""
with open('samples/sampleSMML.html', 'r') as myfile:
    text = smml.markup.read(myfile.read())
    print(json.dumps(smml.markup.smmlprocess(text, 'display'), indent=2))
"""

# Testing the getPitch functions
frequencies = [
    16.351597831287414,
    439.99999999999994,
    6644.875161279121,
    440,
    1250,
    6644.875161279121,
]

for freq in frequencies:
    print('{} Exact: {}'.format(freq, smml.audiofunc.getPitchExact(freq)))
    print('{} Estimate: {}'.format(freq, smml.audiofunc.getPitchEstimate(freq)))
    print()
