#!/usr/bin/env python3

import json, curses, os
import smml

"""
with open('samples/sampleSMML.html', 'r') as myfile:
    text = smml.markup.read(myfile.read())
    print(json.dumps(smml.markup.smmlprocess(text, 'display'), indent=2))
"""

"""
# Testing the getPitch functions
frequencies = [
    16.351597831287414,
    439.99999999999994,
    6644.875161279121,
    440,
    1250,
    6644.875161279121,
]

for freq in frequencies:
    print('{} Exact: {}'.format(freq, smml.audiofunc.getPitchExact(freq)))
    print('{} Estimate: {}'.format(freq, smml.audiofunc.getPitchEstimate(freq)))
    print()
"""

# Testing KeyboardInterrupt to end the audio loop
def callback(x):
    raise KeyboardInterrupt
print(smml.audiofunc.audioSetup(callback))

# Testing the Live Audio Loop
try:
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    options = {'sample_rate': 1000}
    def callback(x):
        stdscr.clear(); stdscr.addstr(str(x)); stdscr.refresh()
    state = smml.audiofunc.audioSetup(callback, options)
finally:
    curses.echo()
    curses.nocbreak()
    curses.endwin()
    print(state)

# Testing Frequency Detection (using Live Audio)
try:
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    options = {'sample_rate': 44100}
    def callback(x):
        freq, vol = smml.audiofunc.process(x)
        stdscr.clear(); stdscr.addstr(str(freq)+'\n'+str(vol)); stdscr.refresh()
    state = smml.audiofunc.audioSetup(callback, options)
finally:
    curses.echo()
    curses.nocbreak()
    curses.endwin()
    print(state)

# Testing the Audio File Loop
name = os.path.join(os.path.dirname(__file__), 'samples/Aud8k.wav')

try:
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    options = {'type': 'file', 'file': name,
        'sample_rate': 8000, 'frames_rate': 240}
    def callback(x):
        stdscr.clear(); stdscr.addstr(str(x)); stdscr.refresh()
    state = smml.audiofunc.audioSetup(callback, options)
finally:
    curses.echo()
    curses.nocbreak()
    curses.endwin()
    print(state)

"""
options = {'type': 'file', 'file': name, 'sample_rate': 1000} # erroneous rate
def callback(x):
    pass
print(smml.audiofunc.audioSetup(callback, options)) # confirm that error throws
"""
