#!/usr/bin/env python3

import wave
import pyaudio
import numpy as np

default_options = {
    'type': 'live',
    'file': '-',
    'sample_rate': 8000,
    'frames_rate': 30,
}

def audioSetup(callback, args=default_options):
    """
    audioSetup(callback, args=default_options)

    default_options = {
        'type': 'live',
        'file': '-',
        'sample_rate': 8000,
        'frames_rate': 30,
    }

    Creates an object that reads audio data as frames and processes the data
    as specified in "callback." Can read microphone input ('type': 'live') at
    any standard sample rate, and can read audio files ('type': 'file') at the
    sample rate in which the file is encoded. The 'file' option specifies the
    audio file to read, and is ignored when reading microphone input. The
    'frames_rate' option specifies the rate at which the computer should output
    data, controlling how much data it reads before processing a frame.

    Reads audio data frame by frame in a loop that repeats until a stop signal
    is received: KeyboardInterrupt for microphone input, EOF for audio file.
    Returns 1 on successful completion.
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

    # Calculate more numbers for audio processor
    options['audio_format'] = pyaudio.paInt16
    options['frames_size']  = int(options['sample_rate']/options['frames_rate'])
    options['sample_width'] = 2
    options['channels']     = 1

    # Starting the audio instance
    if options['type'] == 'live':
        # Create the live audio object
        audio = pyaudio.PyAudio()
        stream = audio.open(format=options['audio_format'],
                            channels=options['channels'],
                            rate=options['sample_rate'], input=True,
                            frames_per_buffer=options['frames_size'])

        # Run this loop for each frame
        try:
            frame = 0
            while True:
                data = stream.read(options['frames_size'])

                # Format for unpacking data (control for width)
                fmt = '{:.0f}h'.format(len(data)/options['sample_width'])

                # Extracting and processing the data (using floats for JSON)
                numbers = np.array(wave.struct.unpack(fmt, data), dtype='float')
                callback(numbers) # to end, callback raises KeyboardInterrupt

                frame += 1
        # KeyboardInterrupt triggers a normal, successful ending
        except KeyboardInterrupt:
            stream.stop_stream()
            stream.close()
            audio.terminate()
            return(1)
        # Otherwise, some other error occured -- still must close sream
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()
    else:
        # Open the recorded audio file
        with wave.open(options['file']) as audio:
            frames = audio.getnframes()/options['frames_size']
            frame = 0

            if options['sample_rate'] != audio.getframerate():
                raise ValueError('{} Hz'.format(options['sample_rate']) +
                    ' does not match sample rate of ' +
                    'audio file {}'.format(options['file']))

            # Loop to run for each frame
            while frame < frames:
                data = audio.readframes(options['frames_size'])

                # Format for unpacking data (control for width)
                fmt = '{:.0f}h'.format(len(data)/options['sample_width'])

                # Extracting and processing the data (using floats for JSON)
                numbers = np.array(wave.struct.unpack(fmt, data), dtype='float')
                callback(numbers)

                frame += 1

            # And read final partial frame, if there is one
            # If there are fewer bytes than requested, readframes returns less
            data = audio.readframes(options['frames_size'])

            # Format for unpacking data (control for width)
            fmt = '{:.0f}h'.format(len(data)/options['sample_width'])

            # Extracting and processing the data (using floats for JSON)
            numbers = np.array(wave.struct.unpack(fmt, data), dtype='float')
            callback(numbers)

            frame += 1
        return(1)
