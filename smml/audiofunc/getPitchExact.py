#!/usr/bin/env python3

from . import genPitch, pitchData

def getPitchExact(freq, a4=440):
    """
    getPitchExact(freq, a4=440)

    Determines an exact frequency-pitch match using a pitchData JSON object from
    genPitch(a4). Uses pre-generated smml.audiofunc.pitchData when a4 == 440, to
    save CPU time. The function takes the given freq and determines its index,
    then finds the corresponding pitch at that index, then checks that this
    frequency and pitch are a matched pair of values.

    If "freq" is not contained in the generated pitchData object, returns None.
    """

    # Ensure that pitchData is around the correct pitch
    if a4 != 440:
        pitchData = genPitch(a4)

    # Comparing indeces of frequency and specific pitch in respective lists
    try:
        freqIndex = pitchData['frequencies'].index(freq)
    except ValueError:
        return(None)

    pitch = pitchData['pitches'][freqIndex]

    # Backup for if there is an indexing error in the lists
    if pitchData[pitch] == freq: # Indices match -- return value
        return(pitch)
    else: # Indices do not match -- brute-force test all possible pitches
        for i in range(len(pitchData['pitches'])):
            pitch = pitchData['pitches'][i]
            if pitchData[pitch] == freq:
                return(pitch)
        return(None)
