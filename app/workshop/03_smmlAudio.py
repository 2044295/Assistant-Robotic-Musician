#!/usr/bin/env python3

import sys
import argparse
import json
import wave
import audioop

""""""
"""Setup: Use argparse to decide which examples to run"""
parser = argparse.ArgumentParser(
    description='A collection of Python audio experiments')

parser.add_argument('-1', '--sample_one', action='store_true',
                    help='Ex 1: Opening a .wav file')

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
    try:
        with wave.open('Aud44.1k.wav', 'wb') as audio:
            results['open_write'] = ['opens write-only object', str(audio)]
    except:
        results['open_write'] = str(sys.exc_info()[0])

    print(json.dumps('Example 1: Methods of Opening .wav files'))
    print(json.dumps(results, indent=4))
    print()
