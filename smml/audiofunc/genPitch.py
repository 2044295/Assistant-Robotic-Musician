#!/usr/bin/env python3

import json

def genPitch(a4=440):
    """
    genPitch(a4=440)

    Generates a discrete list of matched frequencies and pitches, based on the
    given frequency for A4 (using A440 as a standard). Returns a JSON object
    containing an ordered list of frequencies, and ordered list of pitches, and
    frequencies indexed by pitch. The standard A440 list is available as
    smml.audiofunc.pitchData.
    """

    # Set the standard
    C4 = A4 / (2 ** (9/12)) # C is 9 half-steps below A

    # Write the Alphabet
    alphabet = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    # Create the Object
    keyboard = {"frequencies": [], "pitches": []}

    # Loop over all 8 octaves (including those incomplete on the keyboard)
    for x in range(9):
        fundamental = C4/(2 ** (4 - x))
        octave = [fundamental * (2 ** (x/12)) for x in range(12)]

        for n, freq in enumerate(octave):
            keyboard["frequencies"].append(freq)
            keyboard["pitches"].append(alphabet[n] + str(x))
            keyboard[alphabet[n] + str(x)] = freq

    # And lastly, output the data
    return(keyboard)
