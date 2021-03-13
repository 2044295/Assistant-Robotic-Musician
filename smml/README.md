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
    getPitchExact.py    # Detects exact matches to pitches in a pitchData object
    getPitchEstimate.py # Finds the nearest match in a pitchData object
    pitchData.py        # Generates and returns matching frequencies and pitches
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

##### `markup/`
- Imports the following: `read,` `smmlprocess`
- Defines various functions that operate on SMML-encoded data

```python
> import smml
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
