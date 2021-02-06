#!/usr/bin/env python3

import sys
import json

comment = False
if len(sys.argv) > 1:
    if sys.argv[1] == '--comment':
        comment = True

# Reading the data synchronously so it's available whenever we need it
with open('04_PitchData.json', 'r') as myfile:
    freqData = json.loads(myfile.read())

def getPitchExact(freq):
    # Comparing indeces of frequency and specific pitch in respective lists
    if comment: print('Finding Pitch {}'.format(freq))
    try:
        freqIndex = freqData['frequencies'].index(freq)
    except ValueError:
        if comment: print('Pitch not found')
        return(None)
    pitch = freqData['pitches'][freqIndex]

    # Backup for if there is an indexing error in the lists
    if freqData[pitch] == freq:
        # Indeces matched -- expected frequency returns
        if comment: print('Pitch found using index-matching!')
        return(pitch)
    else:
        # Indeces did not match -- brute-force test all possible pitches
        if comment: print('Indices did not line up...')
        for i in range(len(freqData['pitches'])):
          pitch = freqData['pitches'][i]
          if freqData[pitch] == freq:
            if comment: print('Pitch found by discrete-testing method!')
            return(pitch)
        if comment: print('Pitch not found')
        return(None)

def getPitchEstimate(freq):
    # Trying frequency to see if it is exact
    new_freq = freq
    pitch = getPitchExact(new_freq)

    # Backup for if (when) the frequency is not exact
    if pitch is None:
        errors = [None, None]

        # Looping over all dicrete frequencies to measure error
        for i in range(len(freqData['frequencies'])):
          errors[0] = errors[1]
          errors[1] = abs(freq - freqData['frequencies'][i])

          # Turning point detected when error increases -- use previous value
          if errors[0] is not None:
              if errors[1] > errors[0]:
                  new_freq = freqData['frequencies'][i - 1]
                  break

        # And lastly, finding the exact pitch
        pitch = getPitchExact(new_freq)

    error = abs(freq - new_freq) / new_freq
    return([pitch, error])


print(getPitchExact(16.351597831287414))
if comment: print()
print(getPitchExact(439.99999999999994))
if comment: print()
print(getPitchExact(6644.875161279121))
if comment: print()
print(getPitchExact(440))
if comment: print()
print(getPitchEstimate(440))
if comment: print()
print(getPitchEstimate(1250))
if comment: print()
print(getPitchEstimate(6644.875161279121))
print()
