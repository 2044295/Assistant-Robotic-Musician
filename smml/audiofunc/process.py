#!/usr/bin/env python3

import numpy as np

default_options = {
    'type': 'live',
    'file': '-',
    'sample_rate': 8000,
    'frames_rate': 30,
}

def process(numbers, gate=10, args=default_options):
    """
    process(numbers, gate=10, args=default_options)

    default_options = {
        'type': 'live',
        'file': '-',
        'sample_rate': 8000,
        'frames_rate': 30,
    }

    Processes "numbers" (must be an np.ndarray), as produced by
    smml.audiofunc.audioSetup(), to determine the dominant frequency and a
    rough measure of volume. Uses a Fast Fourier Transformation to determine
    the frequency, and sums the amplitude of the waveform to estimate volume.

    Must be supplied with a noise gate (defaults to 10, can be 0 for purest
    audio) which is used to adjust the waveform, primarily to reduce background
    noise. Must also be supplied with a dictionary of options, as the frame rate
    is a necessary conversion factor for the FFT Algorithm.

    Returns the extract frequency and estimated volume.
    """

    # Verifying and importing options
    options = default_options
    for arg in args.keys():
        value = args[arg]
        if arg in options.keys():
            if arg == 'type' and value not in ['live', 'file']:
                raise ValueError('Cannot parse audio type {}'.format(value))
            if arg == 'sample_rate' and type(value) not in [int, float]:
                raise TypeError('sample_rate cannot be {}'.format(type(value)))
            if arg == 'frames_rate' and type(value) not in [int, float]:
                raise TypeError('sample_rate cannot be {}'.format(type(value)))
            options[arg] = value
        else:
            raise ValueError('Unexpected Option Provided: {}'.format(arg))

    # Check that "numbers" is given as a numpy array
    if type(numbers) is not np.ndarray:
        raise TypeError('"numbers" argument is not of type numpy.ndarray')

    # Implement Noise Gate and Approximate Volume
    adjusted = numbers * (numbers > gate) # implement noise gate
    vol_adj = sum(abs(adjusted))    # approximate volume using amplitude
    if vol_adj == 0:
        return(0, 0)

    # Perform and Interpret the Fourier Transformation
    fft_data = abs(np.fft.rfft(adjusted))**2 # ignore complex & negative

    # find the max and the conversion factor
    fft_max = fft_data[1:].argmax() + 1
    conversion = options['frames_rate']

    # use quadratic interpolation around the max
    if sum(fft_data) == 0:
        freq = 0
    elif fft_max != len(fft_data)-1:
        y0,y1,y2 = np.log(fft_data[fft_max-1:fft_max+2:])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        # find the frequency and output it
        freq = (fft_max+x1) * conversion
    else:
        freq = fft_max * conversion

    # Returning all processed data
    return(freq, vol_adj)
