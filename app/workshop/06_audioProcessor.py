#!/usr/bin/env python3

# importing necessary packages
import sys
import json
import argparse
import time
import curses
import wave
import pyaudio
import numpy as np

# setting up the arguments
parser = argparse.ArgumentParser(
    description='An experiment in processing audio with live output')

parser.add_argument('-c', '--comment', action='store_true',
                    help='display (many) helpful comments as the program runs')
parser.add_argument('-d', '--display-curses', action='store_true',
                    help='generate a curses instance for overwriteable output')
parser.add_argument('-j', '--json', action='store_true',
                    help='display all output as NodeJS-compatible JSON objects\
                         (overrides other display arguments)')
parser.add_argument('--test-json', action='store_true',
                    help='test Python3-NodeJS I/O with delay between "print"\
                         statements (overrides all other arguments)')

argv = parser.parse_args(sys.argv[1:])
if argv.json:
    argv.comment = False
    argv.display_curses = False

if argv.comment: print(argv)

# the functions (would be "imported" from package)
def getPitchExact(freq):
    # Comparing indeces of frequency and specific pitch in respective lists
    if argv.comment: print('Finding Pitch {}'.format(freq))
    try:
        freqIndex = freqData['frequencies'].index(freq)
    except ValueError:
        if argv.comment: print('Pitch not found')
        return(None)
    pitch = freqData['pitches'][freqIndex]

    # Backup for if there is an indexing error in the lists
    if freqData[pitch] == freq:
        # Indeces matched -- expected frequency returns
        if argv.comment: print('Pitch found using index-matching!')
        return(pitch)
    else:
        # Indeces did not match -- brute-force test all possible pitches
        if argv.comment: print('Indices did not line up...')
        for i in range(len(freqData['pitches'])):
          pitch = freqData['pitches'][i]
          if freqData[pitch] == freq:
            if argv.comment: print('Pitch found by discrete-testing method!')
            return(pitch)
        if argv.comment: print('Pitch not found')
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

# defining the important metadata (we can do that for the microphone)
a_info = {}
a_info['sample_rate_hz']   = 8000
a_info['frame_sz']         = int(a_info['sample_rate_hz']/30)
a_info['sample_width_bt']  = 2 # appears to work -- assume the same
a_info['audio_format']     = pyaudio.paInt16
a_info['channels']         = 1
a_info['gate']             = 10  # standard noise gate -- seems sufficient
a_info['error']            = 1 # standard allowable error -- seems sufficient

def process(data, a_info=a_info):
    # Defining the format of the unpacked data (must control for width)
    fmt_str = '{:.0f}h'.format(len(data)/a_info['sample_width_bt'])
    if argv.comment:
        print('fmt_str: {}'.format(fmt_str))
        print('length of data: {}'.format(len(data)));

    # Extracting the data as numbers (using floats for the sake of JSON)
    numbers = wave.struct.unpack(fmt_str, data)
    numbers = np.array([x if x > a_info['gate'] else 0 for x in numbers])
    a_info['numbers'] = list(numbers)
    if argv.comment: print('shape of array: {}'.format(numbers.shape))

    # Performing and Interpreting the Fourier Transformation
    fft_data = abs(np.fft.rfft(numbers))**2 # ignore complex & negative
    a_info['fft_data'] = list(fft_data)

    # find the max and the conversion factor
    fft_max = fft_data[1:].argmax() + 1
    conversion = a_info['sample_rate_hz']/a_info['frame_sz']

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

    # get the pitch and decide what to do with it
    pitch = getPitchEstimate(freq)
    if pitch[1] < a_info['error']:
        return(pitch, freq)
    else:
        pitch = [None, pitch[1]]
        return(pitch, freq)

def callback(in_data, frame_count, time_info, status):
    if argv.display_curses: stdscr.clear() # start new frame

    # processing data to a useful pitch
    pitch, freq = process(in_data)

    # interpreting the pitch data
    data = music_nodes[node[0]][1][node[1]] # section - data list - node
    if pitch[0] in data:
        print(json.dumps([data[0], pitch])) # output node information
        node[1] += 1 # step to next node
        signal = pyaudio.paContinue # and indicate that we keep listening
        if node[1] >= len(music_nodes[node[0]][1]):
            node[0] += 1 # step to next section
            node[1]  = 0 # and reset the beat count
            if node[0] >= len(music_nodes):
                signal = pyaudio.paComplete # stop the stream
            else:
                print(json.dumps("SECTION {}".format(node[0])))
    else:
        signal = pyaudio.paContinue # keep listening for an accurate pitch
        if argv.display_curses:
            stdscr.addstr(str(data) + '\n')
            stdscr.addstr('Frequency: ' + str(freq) + '\n')
            stdscr.addstr('Pitch: ' + str(pitch) + '\n')

    if argv.display_curses:
        stdscr.refresh()

    return(in_data, signal)


# main loop
if argv.test_json:
    random_data = [
        'foo', 'bar', 69, 420,
        ['sample', 'list'],
        {'sample': 'dictionary'}
    ]
    for item in random_data:
        print(json.dumps(item))
        sys.stdout.flush() # important for the NodeJS counterpart
        time.sleep(1)
else:
    # simple way to load data -- replace with package "import"
    music_nodes = json.loads(sys.stdin.read())
    if argv.comment: print(json.dumps(music_nodes, indent=2))

    # from "04_PitchFreq.py" -- when in package, just import
    with open('04_PitchData.json', 'r') as myfile:
        freqData = json.loads(myfile.read())

    # Creating the audio input object with the given requirements
    audio = pyaudio.PyAudio()
    stream = audio.open(format=a_info['audio_format'],
                        channels=a_info['channels'],
                        rate=a_info['sample_rate_hz'], input=True,
                        frames_per_buffer=a_info['frame_sz'],
                        stream_callback=callback)

    # Using a try-finally block so if/when curses complains, nothing breaks
    try:
        # Start the data display window
        if argv.display_curses:
            stdscr = curses.initscr()
            curses.noecho()
            curses.cbreak()

        frame = 0
        node  = [0, 0]

        # Start listening to audio
        stream.start_stream()

        while stream.is_active():
            time.sleep(1/30)
    except KeyboardInterrupt:
        print("Done recording")
    except Exception as e:
        if argv.display_curses:
            stdscr.addstr(str(e) + '\n')
            stdscr.refresh()
        else:
            print(str(e))
    finally:
        # Close the stream (so that nothing is unresolved)
        try:
            stream.stop_stream()
            stream.close()
            audio.terminate()
        except:
            # if the stream overflows, it closes automatically
            if argv.comment: print("Stream already closed")

        if argv.display_curses:
            time.sleep(2.5)
            curses.echo()
            curses.nocbreak()
            curses.endwin()

        # wrap up -- end signal, close down the display
        if argv.json:
            print(json.dumps(["DONE"]))
        else:
            print("DONE")
