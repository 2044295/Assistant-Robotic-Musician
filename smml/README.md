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

foo
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

Finds the nearest discrete pitch for which "freq" matches and returns a list of
that pitch and the percentage of error. Uses getPitchExact for determining pitch
once the nearest frequency is found; matches to a pitchData JSON object from
genPitch(a4), with the pre-generated smml.audiofunc.pitchData when a4 == 440.
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
