#!/usr/bin/env python3

import sys
import argparse
import json
import curses
import wave
import numpy as np
import time
import pyaudio

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
parser.add_argument('-4', '--sample_four', action='store_true',
                    help='Ex 4: Reading microphone input in useful frames')
parser.add_argument('-5', '--sample_five', action='store_true',
                    help='Ex 5: FFT Extraction of .wav frames')
parser.add_argument('-6', '--sample_six', action='store_true',
                    help='Ex 6: FFT Extraction of live input frames')
parser.add_argument('-7', '--sample_seven', action='store_true',
                    help='Ex 7: Various experiments into volume')
parser.add_argument('--gate', action='store', default='100',
                    help='Variable defining the "noise gate," any int')
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
        results['open_block'] = str(sys.exc_info()[0])

    # open_inline: less ideal, requires manual closure
    try:
        audio = wave.open('Aud11.025k.wav', 'rb')
        results['open_inline'] = ['opens as stated as a general var', str(audio)]
        audio.close()
    except:
        results['open_inline'] = str(sys.exc_info()[0])

    # open_nomode: testing what the default opening is (read-only)
    try:
        with wave.open('Aud22.05k.wav') as audio:
            results['open_nomode'] = ['automatically opens read-only', str(audio)]
    except:
        results['open_nomode'] = str(sys.exc_info()[0])

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
    if argv.comment:
        print('Example 2: Reading various .wav file data')
        print('- Reading 30 bytes, for a short reference')

    results = {}
    with wave.open('Aud8k.wav') as audio:
        # Extracting various important metadata (size and framerate)
        results['object']           = str(audio)
        results['sample_width_bt']  = audio.getsampwidth()
        results['sample_rate_hz']   = audio.getframerate()
        results['sample_length_f']  = audio.getnframes()
        results['sample_length_s']  = audio.getnframes()/audio.getframerate()

        # Reading the data
        data = audio.readframes(30)
        results['data'] = str(data)

        # Defining the format of the unpacked data (must calibrate for width)
        fmt_str = '{:.0f}h'.format(len(data)/results['sample_width_bt'])
        if argv.comment: print('fmt_str: {}'.format(fmt_str))
        if argv.comment: print('length of data: {}'.format(len(data)));

        # Extracting the data as numbers (using floats for the sake of JSON)
        numbers = np.array(wave.struct.unpack(fmt_str, data), dtype='float')
        results['numbers'] = list(numbers)
        if argv.comment: print('shape of array: {}'.format(numbers.shape))

    # And last but not least, printing the data
    if argv.comment: print(json.dumps(results, indent=2))
    print(numbers)
    print()

# Ex 3: Reading a .wav file in useful frames
if argv.sample_three:
    results = {}

    with wave.open('Aud8k.wav') as audio:
        if argv.comment:
            print('Example 3: Reading a .wav file in useful frames')
            print('- Reading 30 "frames per second" at 4 frames per second')
            print('- 30 "frames per second" because A1 = 55hz')
            print('- And printing 2 frames per second for the human mind')
            time.sleep(5)

        # Extracting and calculating important metadata (size, framerate)
        results['object']           = str(audio)
        results['sample_width_bt']  = audio.getsampwidth()
        results['sample_rate_hz']   = audio.getframerate()
        results['sample_length_f']  = audio.getnframes()
        results['sample_length_s']  = audio.getnframes()/audio.getframerate()
        results['frame_sz']         = int(results['sample_rate_hz']/30)
        results['frames']           = \
            int(results['sample_length_f']/results['frame_sz'])

        # Using a try-finally block so if/when curses complains, nothing breaks
        try:
            # Starting the data display window (using curses)
            stdscr = curses.initscr()
            curses.noecho()
            curses.cbreak()

            for x in range(results['frames']):
                stdscr.clear()
                # Reading data for the given frame; header updates automatically
                data = audio.readframes(results['frame_sz'])
                results['data'] = str(data)

                # Defining format of the unpacked data (must control for width)
                fmt_str = '{:.0f}h'.format(len(data)/results['sample_width_bt'])
                if argv.comment: stdscr.addstr('fmt_str: {}\n'.format(fmt_str))
                if argv.comment: stdscr.addstr('length: {}\n'.format(len(data)))

                # Extracting the data as numbers (floats for the sake of JSON)
                nums = np.array(wave.struct.unpack(fmt_str, data),dtype='float')
                results['numbers'] = list(nums)
                if argv.comment: stdscr.addstr('shape: {}\n'.format(nums.shape))

                # Printing the data for the given frame
                stdscr.addstr(0, 0, str(nums))
                stdscr.refresh()
                time.sleep(0.25)
        finally:
            # And, last but not least, closing the data display window
            curses.echo()
            curses.nocbreak()
            curses.endwin()

# Ex 4: Reading microphone input
if argv.sample_four:
    if argv.comment:
        print('Example 4: Reading microphone input in useful frames')
        print('- Reading 30 "frames" per second (because A1 = 55hz)')
        print('- Using 1k audio as a demonstration: 33 bytes per frame')
        time.sleep(5)

    results = {}

    # Defining the important metadata (we can do that for the microphone)
    results['sample_rate_hz']   = 1000   # smaller, so curses doesn't break
    results['frame_sz']         = int(results['sample_rate_hz']/30)
    results['sample_width_bt']  = 2 # appears to work -- assume the same
    results['audio_format']     = pyaudio.paInt16
    results['channels']         = 1

    # Creating the audio input object with the given requirements
    audio = pyaudio.PyAudio()
    stream = audio.open(format=results['audio_format'],
                        channels=results['channels'],
                        rate=results['sample_rate_hz'], input=True,
                        frames_per_buffer=results['frame_sz'])

    try:
        # Start listening to audio
        stream.start_stream()

        # Start the data display window
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        frame = 0

        while True:
            stdscr.clear()
            # Reading the data for the given frame; header updates automatically
            data = stream.read(results['frame_sz'])
            results['data'] = str(data)

            # Defining the format of the unpacked data (must control for width)
            fmt_str = '{:.0f}h'.format(len(data)/results['sample_width_bt'])
            if argv.comment: print('fmt_str: {}'.format(fmt_str))
            if argv.comment: print('length of data: {}'.format(len(data)));

            # Extracting the data as numbers (using floats for the sake of JSON)
            numbers = np.array(wave.struct.unpack(fmt_str, data), dtype='float')
            results['numbers'] = list(numbers)
            if argv.comment: print('shape of array: {}'.format(numbers.shape))

            # Printing the data for the given frame
            if argv.comment: print(json.dumps(results, indent=2))
            stdscr.addstr('Frame {}\n'.format(frame))
            stdscr.addstr(str(numbers) + '\n')
            stdscr.refresh()
            frame += 1
    except KeyboardInterrupt:
        print("Done recording")
    except Exception as e:
        print(str(e))
    finally:
        # Close the display window (so terminal doesn't freak out)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

        # Close the stream (so that nothing is unresolved)
        stream.stop_stream()
        stream.close()
        audio.terminate()

# Ex 5: FFT Extraction (Audio)
if argv.sample_five:
    results = {}

    with wave.open('Aud8k.wav') as audio:
        if argv.comment:
            print('Example 5: Extracting FFT Data from useful .wav frames')
            print('- Reading 30 "frames per second" at 4 frames per second')
            print('- 30 "frames per second" because A1 = 55hz')
            print('- And printing 2 frames per second for the human mind')
            time.sleep(5)

        # Extracting and calculating important metadata (size, framerate)
        results['object']           = str(audio)
        results['sample_width_bt']  = audio.getsampwidth()
        results['sample_rate_hz']   = audio.getframerate()
        results['sample_length_f']  = audio.getnframes()
        results['sample_length_s']  = audio.getnframes()/audio.getframerate()
        results['frame_sz']         = int(results['sample_rate_hz']/30)
        results['frames']           = \
            int(results['sample_length_f']/results['frame_sz'])

        # Starting the data display window (using curses)
        try:
            stdscr = curses.initscr()
            curses.noecho()
            curses.cbreak()

            frame = 0

            for x in range(results['frames']):
                stdscr.clear()
                # Reading the frame data; header updates automatically
                data = audio.readframes(results['frame_sz'])
                results['data'] = str(data)

                # Defining the format of the unpacked data
                fmt_str = '{:.0f}h'.format(len(data)/results['sample_width_bt'])
                if argv.comment: print('fmt_str: {}\n'.format(fmt_str))
                if argv.comment: print('length: {}\n'.format(len(data)));

                # Extracting the data as numbers (floats for JSON)
                numbers = np.array(wave.struct.unpack(fmt_str, data),\
                    dtype='float')
                results['numbers'] = list(numbers)
                if argv.comment: print('shape: {}\n'.format(numbers.shape))

                # Performing and Interpreting the Fourier Transformation
                fft_data = abs(np.fft.rfft(numbers))**2
                    # adjust to ignore the complex and negative results
                results['fft_data'] = list(fft_data)

                # find the max and the conversion factor
                fft_max = fft_data[1:].argmax() + 1
                conversion = results['sample_rate_hz']/results['frame_sz']

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

                # Printing the data for the given frame
                if argv.comment: print(json.dumps(results, indent=2))
                stdscr.addstr('Frame {}\n'.format(frame))
                stdscr.addstr(str(numbers) + '\n')
                stdscr.addstr(str(fft_data) + '\n')
                stdscr.addstr('Detected Frequency: {:.0f} Hz'.format(freq) \
                    + '\n')
                stdscr.refresh()
                frame += 1
                time.sleep(0.25)
        except Exception as e:
            print(str(e))
        finally:
            # And, last but not least, closing the data display window
            curses.echo()
            curses.nocbreak()
            curses.endwin()

# Ex 6: FFR Extraction (Live)
if argv.sample_six:
    if argv.comment:
        print('Example 6: Extracting FFT data from useful input frame')
        print('- Reading 30 "frames" per second (because A1 = 55hz)')
        print('- Using 1k audio as a demonstration: 266 bytes per frame')
        time.sleep(5)

    results = {}

    # Defining the important metadata (we can do that for the microphone)
    results['sample_rate_hz']   = 1000   # smaller, so curses doesn't break
    results['frame_sz']         = int(results['sample_rate_hz']/30)
    results['sample_width_bt']  = 2 # appears to work -- assume the same
    results['audio_format']     = pyaudio.paInt16
    results['channels']         = 1

    # Creating the audio input object with the given requirements
    audio = pyaudio.PyAudio()
    stream = audio.open(format=results['audio_format'],
                        channels=results['channels'],
                        rate=results['sample_rate_hz'], input=True,
                        frames_per_buffer=results['frame_sz'])

    try:
        # Start listening to audio
        stream.start_stream()

        # Start the data display window
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        frame = 0

        while True:
            stdscr.clear()
            # Reading the data for the given frame; header updates automatically
            data = stream.read(results['frame_sz'])
            results['audio_data'] = str(data)

            # Defining the format of the unpacked data (must control for width)
            fmt_str = '{:.0f}h'.format(len(data)/results['sample_width_bt'])
            if argv.comment: print('fmt_str: {}'.format(fmt_str))
            if argv.comment: print('length of data: {}'.format(len(data)));

            # Extracting the data as numbers (using floats for the sake of JSON)
            numbers = np.array(wave.struct.unpack(fmt_str, data), dtype='float')
            results['numbers'] = list(numbers)
            if argv.comment: print('shape of array: {}'.format(numbers.shape))

            # Performing and Interpreting the Fourier Transformation
            fft_data = abs(np.fft.rfft(numbers))**2 # ignore complex & negative
            results['fft_data'] = list(fft_data)

            # find the max and the conversion factor
            fft_max = fft_data[1:].argmax() + 1
            conversion = results['sample_rate_hz']/results['frame_sz']

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

            # Printing the data for the given frame
            if argv.comment: print(json.dumps(results, indent=2))
            stdscr.addstr('Frame {}\n'.format(frame))
            stdscr.addstr(str(numbers) + '\n')
            stdscr.addstr(str(fft_data) + '\n')
            stdscr.addstr('Detected Frequency: {:.0f} Hz'.format(freq) + '\n')
            stdscr.refresh()
            frame += 1
    except KeyboardInterrupt:
        print("Done recording")
    except Exception as e:
        print(str(e))
    finally:
        # Close the display window (so terminal doesn't freak out)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

        # Close the stream (so that nothing is unresolved)
        stream.stop_stream()
        stream.close()
        audio.terminate()

# Ex 7: Volume Experiments
if argv.sample_seven:
    results = {}

    if argv.comment:
        print('Example 7: Various experiments into volume')
        print('- Using only live audio for the best feedback')
        print('- Skipping FFT algorithm, since it is unrelated to volume')
        print('- Finding regular sum, absolute-value sum, and square sum')
        print('- Main use: detecting "silence"')
        time.sleep(5)

    # Defining the important metadata (we can do that for the microphone)
    results['sample_rate_hz']   = 1000   # smaller, so curses doesn't break
    results['frame_sz']         = int(results['sample_rate_hz']/30)
    results['sample_width_bt']  = 2 # appears to work -- assume the same
    results['audio_format']     = pyaudio.paInt16
    results['channels']         = 1

    # Creating the audio input object with the given requirements
    audio = pyaudio.PyAudio()
    stream = audio.open(format=results['audio_format'],
                        channels=results['channels'],
                        rate=results['sample_rate_hz'], input=True,
                        frames_per_buffer=results['frame_sz'])

    # Using a try-finally block so if/when curses complains, nothing breaks
    try:
        # Start listening to audio
        stream.start_stream()

        # Start the data display window
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        frame = 0

        while True:
            stdscr.clear()
            # Reading the data for the given frame; header updates automatically
            data = stream.read(results['frame_sz'])
            results['data'] = str(data)

            # Defining the format of the unpacked data (must control for width)
            fmt_str = '{:.0f}h'.format(len(data)/results['sample_width_bt'])
            if argv.comment: print('fmt_str: {}'.format(fmt_str))
            if argv.comment: print('length of data: {}'.format(len(data)));

            # Extracting the data as numbers (using floats for the sake of JSON)
            numbers = np.array(wave.struct.unpack(fmt_str, data), dtype='float')
            results['numbers'] = list(numbers)
            if argv.comment: print('shape of array: {}'.format(numbers.shape))

            # Various calculations
            gate = int(argv.gate)           # minimum required value to record
            vol_sum = sum(numbers)          # summing with no ops; useless
            vol_abs = sum(abs(numbers))     # absolute values - rather useful
            vol_sqr = sum(numbers ** 2)     # sum of the squares of the bytes
            vol_adj = sum([abs(x) for x in numbers if abs(x) > gate]) # best
                # it seems like a noise gate of 10 covers "silence" just fine

            # Printing the data for the given frame
            stdscr.addstr('Frame: {}\n'.format(frame))
            stdscr.addstr('Sum of Recorded Bytes: {}\n'.format(vol_sum))
            stdscr.addstr('Absolute-Value Sum: {}\n'.format(vol_abs))
            stdscr.addstr('Sum of the Squares: {}\n'.format(vol_sqr))
            stdscr.addstr('Noise-Gate Adjusted Volume: {}\n'.format(vol_adj))
            stdscr.addstr('vol_adj/vol_abs: {}\n'.format(vol_adj/vol_abs))
            stdscr.refresh()
            frame += 1
    except KeyboardInterrupt:
        print("Done recording")
    except Exception as e:
        print(str(e))
    finally:
        # Close the display window (so terminal doesn't freak out)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

        # Close the stream (so that nothing is unresolved)
        stream.stop_stream()
        stream.close()
        audio.terminate()
