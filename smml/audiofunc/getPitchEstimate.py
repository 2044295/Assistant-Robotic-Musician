#!/usr/bin/env python3

from . import pitchData, getPitchExact

def getPitchEstimate(freq, a4=440):
    # Ensure that pitchData is around the correct pitch
    if a4 != 440:
        pitchData = genPitch(a4)

    # Trying frequency to see if it is exact
    new_freq = freq
    pitch = getPitchExact(new_freq, a4)

    # Backup for if (when) the frequency is not exact
    if pitch is None:
        errors = [None, None]

        # Looping over all dicrete frequencies to measure error
        for i in range(len(pitchData['frequencies'])):
          errors[0] = errors[1]
          errors[1] = abs(freq - pitchData['frequencies'][i])

          # Turning point detected when error increases -- use previous value
          if errors[0] is not None:
              if errors[1] > errors[0]:
                  new_freq = pitchData['frequencies'][i - 1]
                  break

        # And lastly, finding the exact pitch
        pitch = getPitchExact(new_freq, a4)

    error = abs(freq - new_freq) / new_freq
    return([pitch, error])
