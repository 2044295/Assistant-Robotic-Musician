# Python3: `smml`
## Package Overview

- <https://docs.python.org/3/tutorial/modules.html#packages>

### Structure
```
smml/                 # The main smml package
  __init__.py         # Initializes the smml package
  audiofunc/          # Subpackage of various audio processing methods
    __init__.py         # Initializes the subpackage
    audioSetup.py       # Sets up the desired audio object with given callback
    genPitch.py         # Generates and returns matching frequencies and pitches
    getPitchEstimate.py # Finds the nearest match in a pitchData object
    getPitchExact.py    # Detects exact matches to pitches in a pitchData object
    pitchData.json      # A pre-generated pitchData object around A440
    process.py          # A method dealing with FFT and Volume calculations
  markup/             # Subpackage for handling reading and writing SMML
    __init__.py         # Initializes the subpackage
    read.py             # Read SMML and returning a cleaned-up string
    smmlprocess.py      # Process an SMML string to time-pitch nodes
  nodeio.py           # Methods handling NodeJS I/O
  track.py            # Putting it all together into a single function
```

##### Top: `__init__.py`
- Imports the following: `audiofunc`, `markup`, `nodeio`, and `track`
- Initializes the package and makes all contained functions available for use

```python
> import smml
> dir(smml)

[
  '__builtins__',
  '__cached__',
  '__doc__',
  '__file__',
  '__loader__',
  '__name__',
  '__package__',
  '__path__',
  '__spec__',
  'audiofunc',
  'markup',
  'nodeio',
  'track'
]
```

##### `audiofunc/`
```python
> dir(smml.audiofunc)

[
  '__builtins__',
  ...,
  'audioSetup',
  'genPitch',
  'getPitchEstimate',
  'getPitchExact',
  'pitchData',
  'process'
]
```

```
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
```

```
genPitch(a4=440)

Generates a discrete list of matched frequencies and pitches, based on the
given frequency for A4 (using A440 as a standard). Returns a JSON object
containing an ordered list of frequencies, and ordered list of pitches, and
frequencies indexed by pitch. The standard A440 list is available as
smml.audiofunc.pitchData.
```

```
getPitchEstimate(freq, a4=440)

Finds the nearest discrete pitch for which "freq" matches and returns a list
of that pitch and the percentage of error. Uses getPitchExact for determining
pitch once the nearest frequency is found; matches to a pitchData JSON object
from genPitch(a4), with the pre-generated smml.audiofunc.pitchData when a4 ==
440.
```

```
getPitchExact(freq, a4=440)

Determines an exact frequency-pitch match using a pitchData JSON object from
genPitch(a4). Uses pre-generated smml.audiofunc.pitchData when a4 == 440, to
save CPU time. The function takes the given freq and determines its index,
then finds the corresponding pitch at that index, then checks that this
frequency and pitch are a matched pair of values.

If "freq" is not contained in the generated pitchData object, returns None.
```

```
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
```

##### `markup/`
- Imports the following: `read,` `smmlprocess`
- Defines various functions that operate on SMML-encoded data

```python
> dir(smml.markup)

[
  '__builtins__',
  ...,
  'read',
  'smmlprocess'
]
```

```
read(text)

Reads a string of human-readable smml data and returns a machine-formatted
smml string, containing only characters necessary for processing.

text: string object

Reads the string in one of three modes:
- read mode, removing all whitespace
  the default, highest-level mode
- tag mode, reducing all whitespace to a single character
  mid-level mode, contained between each '<' to the first following '>'
- content mode, preserving without question all text (except newlines)
  lowest-level mode, contained within each `note` tag
```

```
smmlprocess(text, mode='player')

Reads a machine-formatted smml string (see smml.markup.read) and processes
the SMML-encoded data to a serialized JSON object. Provides output in one
of two `modes`: 'player' or 'display'.

'Player' output returns a JSON list of "nodes" that describes the expected
pitch(es) at each such "node," a numerical marker of a certain position in
the piece. Specifically, this list contains each "music" object outlined
in an SMML file; these "music" objects are lists of "sections." These
sections are then sublists that contain a section number at index 0 and
however many nodes the section contains; each node listing its identifier
at index 0 and all expected pitches in the following indices.

'Display' output returns a JSON object with all information necessary to
generate an HTML-based sheet music display. This mode is currently
underdeveloped.
```

##### `nodeio`
```python
> dir(smml.markup)

[
  '__builtins__',
  ...,
  'output',
]
```

```
output(text)

Outputs given "text" as an individual data package readable by NodeJS (among
others). Text must be given in a JSON serializable. Output will flush stdin
after each package so that receiving scripts immediately detect the line.
```

##### `track`
```
track(text, callback, a4=440 args=default_options)

default_options = {
    'type': 'live',
    'file': '-',
    'sample_rate': 8000,
    'frames_rate': 30,
}

The function that puts it all together.

Given "text," a string of HTML/SMML, processes that text to a tree of nodes
(smml.markup.read and smml.markup.smmlprocess). Then creates an
audio-listening loop (smml.audiofunc.audioSetup) with the options specified
in "args." The audio loop callback processes the waveform to a frequency
and a pitch around a4 and compares that frequency to the node tree,
determining when the next node in a piece is reached. At this moment, the
node identifier, as well as the detected pitch, are passed to the specified
"callback."

Note that "track" operates only on the first SMML fragment detected in
"text," so if multiple "music" tags appear in an HTML file, the parent
script must select which tag to send to "track."

Note also that, as the function can detect only one dominant pitch at a
time, a single pitch in a chord triggers the detection of that node. This
offers some room for human error, but also makes the program marginally
fallible.

Parameters
----------
text : string
    Text data containing the SMML to be audio-tracked. Tracks only the first
    SMML object detected (the first "<music>" tag)

callback : function
    The callback function called each time a node is detected.

a4 : int or float
    The numerical value of the frequency that should be used to generate a
    pitchData object. Using A440 as a standard.

args : dictionary
    A dictionary of options, passed to the options argument of "audioSetup."

Passes
------
node : list
    Information about the detected node, passed to "callback" the instant
    that node is detected. Contains a string (index 0) identifying the node
    and a list (index 1) that specifies detected pitch and error measure.

Returns
-------
state : integer
    Returns the "state" integer returned by "audioSetup" -- returns 1
    when the audio loop completes successfully.
```
