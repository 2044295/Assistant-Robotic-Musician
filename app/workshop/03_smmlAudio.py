#!/usr/bin/env python3

import sys
import argparse
import json
import wave
import audioop
import time

""""""
"""Setup: Use argparse to decide which examples to run"""
parser = argparse.ArgumentParser(
    description='A collection of Python audio experiments')

parser.add_argument('-1', '--sample_one', action='store_true',
                    help='Ex 1: Opening a .wav file')
parser.add_argument('-2', '--sample_two', action='store_true',
                    help='Ex 2: Reading a .wav file')
parser.add_argument('-3', '--sample_three', action='store_true',
                    help='Ex 3: Reading a .wav file in useful frames')
parser.add_argument('--comment', action='store_true',
                    help='Print non-JSON comments to the terminal')
parser.add_argument('--overwrite', action='store_true',
                    help='Overwrite printed data on continuous printing')

argv = parser.parse_args(sys.argv[1:])

""""""
"""Examples"""
# Ex 1: Opening a .wav file
if argv.sample_one:
    results = {
        'open_block': None,
        'open_inline': None,
        'open_nomode': None,
        'open_write': None,
    }

    # open_block: ideal, automatically closes when code block completes
    try:
        with wave.open('Aud8k.wav', 'rb') as audio:
            results['open_block'] = ['opens as stated within the block', str(audio)]
    except:
        results['open_write'] = str(sys.exc_info()[0])

    # open_inline: less ideal, requires manual closure
    try:
        audio = wave.open('Aud11.025k.wav', 'rb')
        results['open_inline'] = ['opens as stated as a general var', str(audio)]
        audio.close()
    except:
        results['open_write'] = str(sys.exc_info()[0])

    # open_nomode: testing what the default opening is (read-only)
    try:
        with wave.open('Aud22.05k.wav') as audio:
            results['open_nomode'] = ['automatically opens read-only', str(audio)]
    except:
        results['open_write'] = str(sys.exc_info()[0])

    # open_write: testing opening with mode 'wb' (write-only)
    # right now, this produces an error, but that's okay; we don't need to write
    try:
        with wave.open('Aud44.1k.wav', 'wb') as audio:
            results['open_write'] = ['opens write-only object', str(audio)]
    except:
        results['open_write'] = str(sys.exc_info()[0])

    if argv.comment: print('Example 1: Methods of Opening .wav files')
    print(json.dumps(results, indent=4))
    print()

# Ex 2: Reading a .wav file
if argv.sample_two:
    results = {}
    with wave.open('Aud8k.wav') as audio:
        results['object'] = str(audio)
        results['sample_width_bt'] = audio.getsampwidth()
        results['sample_rate_hz'] = audio.getframerate()
        results['sample_length_f'] = audio.getnframes()
        results['sample_length_s'] = audio.getnframes()/audio.getframerate()
        results['data'] = str(audio.readframes(30))

    if argv.comment:
        print('Example 2: Reading various .wav file data')
        print('- Reading 30 bytes, for a short reference')
    print(json.dumps(results, indent=2))
    print()

if argv.sample_three:
    results = {}

    if argv.comment:
        print('Example 3: Reading a .wav file in useful frames')
        print('- Reading 30 "frames per second" at 2 frames per second')
        print('- 30 "frames per second" because A1 = 55hz')
        print('- And printing 2 frames per second for the human mind')

    with wave.open('Aud8k.wav') as audio:
        results['object'] = str(audio)
        results['sample_width_bt'] = audio.getsampwidth()
        results['sample_rate_hz'] = audio.getframerate()
        results['sample_length_f'] = audio.getnframes()
        results['sample_length_s'] = audio.getnframes()/audio.getframerate()
        results['frame_size'] = int(results['sample_rate_hz']/30)
        results['frames'] = int(results['sample_length_f']/results['frame_size'])
        for x in range(results['frames']):
            results['data'] = str(audio.readframes(results['frame_size']))
            print(json.dumps(results))
            time.sleep(0.5)

# WHERE TO GO FROM HERE:
# - look into live input
# - get into actual note recognition
