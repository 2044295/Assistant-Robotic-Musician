#!/usr/bin/env python3

import sys
import json

comment = False
if len(sys.argv) > 1:
    if sys.argv[1] == '--comment':
        comment = True

# Set the standard
A4 = 440
C4 = A4 / (2 ** (9/12)) # C is 9 half-steps below A

# Write the Alphabet
alphabet = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Create the Object
keyboard = {"frequencies": [], "pitches": []}

# Loop over all 8 octaves (including those incomplete on the keyboard)
for x in range(9):
    fundamental = C4/(2 ** (4 - x))
    octave = [fundamental * (2 ** (x/12)) for x in range(12)]
    if comment: print(x, fundamental, octave)

    for n, freq in enumerate(octave):
        keyboard["frequencies"].append(freq)
        keyboard["pitches"].append(alphabet[n] + str(x))
        keyboard[alphabet[n] + str(x)] = freq

# And lastly, output the data
if comment: print()
print(json.dumps(keyboard, indent=2))
