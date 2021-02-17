# Sheet Music Markup Language: SMML

### Contents
- [Contents](#contents)
- [How it Works](#how-it-works)
- [Structuring a Piece](#structuring-a-piece)
    - [The Piece Unit](#the-piece-unit)
    - [The Section Unit](#the-section-unit)
- [Measures](#measures)
    - [Time Signature and Meter](#time-signature-and-meter)
    - [Key Signature](#key-signature)
    - [Measure Numbers](#measure-numbers)
    - [Measures Other](#measures-other)
    - [Grouping](#grouping)
- [Notes](#notes)
    - [Pitch](#pitch)
    - [Beat and Length](#beat-and-length)
    - [Staccato](#staccato)
    - [Identifier](#identifier)
    - [Notes Other](#notes-other)
    - [Note Shorthand](#note-shorthand)
- [Further Reading](#further-reading)
    - [More on Markup and Articulation](#more-on-markup-and-articulation)
    - [On the Programming End of Things](#on-the-programming-end-of-things)

### How it Works
`SMML` works by creating a nested structure of information that is both machine-
and human-readable, much like its inspiration, `HTML`. Mimicking the structure
of music, contained in the nested format `notes { measures { sections { pieces`,
every note is represented by a unique object, with its own identifier and
musical properties (pitch and length), which is the child of a measure with its
own properties (time and key signatures), which is the child of a section that
is the child of a piece.

Ultimately, information on the section, measure, and beat of a note is used to
create an explicit, unchanging tree representing the whole piece. This tree is
the basis for the displayed sheet music as well as the data structure that the
audio processor reads as it interprets live data. However, while the audio
processor uses an explicit tree, `SMML` provides for a variety of implied
formatting options, including grouping of measures, implied sectioning, and
even implied measure groupings. This implied structure can be created using
multiple-value identifiers (such as beat "1.1.1") or by re-setting identifier
values every so often.

`SMML` provides a great deal of structural freedom in the above regard. However,
if data is supplied that does not match one of the explicit or implied forms
described in this documentation, any programs processing the `SMML` will
indicate this error and rely on the user to fix it, rather than trying to
interpret in a manner not explicitly addressed.

Limited support for articulation is provided, addressing primarily those
features, such as relative dynamics, which are easily implemented and may
provide useful information to the audio processor as it follows the live
performance. Such features will be implemented in a predictive `if-then` format,
in which the program creates rules for all of the various outcomes of an
ambiguous passage (such as one that repeats twice at different volumes).

Ultimately, this abstract data tree serves as the conceptual bridge between the
human-readable sheet music that `SMML` displays in an `HTML` environment and the
machine-readable input data that can be interpreted as or matched to live audio.
`SMML` provides a concrete notation format for this data tree. For more on how
to create such a data tree, read on.

### Structuring a Piece
##### The Piece Unit
- All sheet music must be contained within the `<music></music>` environment
- The `music` tag is comparable to the `script` container tag
    - The primary difference is that the language is still roughly HTML
- All standard HTML tags should function properly inside the `music` environment
    - All header tags (`h1`, `h2`, `h3`, etc.)---ideal for titles, etc.
    - Other tags serve no obvious purpose but should not break in `music`
    - Essentially, this should be a customizable extension of HTML
- The `music` tag is practically just a `div` with a default class and with
  certain HTML extensions (outlined below)
    - The opening tag may include various options or extensions, but the closing
      tag must exactly match `</music>`, or an error will occur

```css
div.music {
  background: white;
  border-style: inset; /* up for debate */
  margin: 25px 10%;
  align: center;
  text-align: center;
  font-family: Georgia, serif;
}

div.jazz {
  font-family: "Brush Script MT", sans-serif;
}
```

##### The Section Unit
- Every piece is automatically divided into sections for processing; even if
  there is only a "Section I," all music must exist within a section
    - Conceptually, all music exists contained in some form of container
    - For processing purposes, section grouping must be explicitly stated
    - Any data not grouped into a section will be ignored
- A section, as a unit, is just a `div`, which may contain text, IDs, etc.
- Identifiers in the form of `id="section-<NUM>-<STR>"` will create a manual
  section identifier; otherwise, they will be numbered automatically
    - `<NUM>` must be an integer that matches the expected enumeration
    - `<STR>` may be any desired string, which `SMML` uses to track the piece
    - Any break from this format will raise an error
    - `SMML` will interpret any ungrouped measures based on their numbers
- All section markup (titles, etc.) must be manually provided

### Measures
- Like sections, measures are comparable to `div`s, but they have their own tag
    - Just like sections, all measure grouping must be explicitly stated --
      and notes not grouped inside of a measure are simply ignored
- `<measure></measure>` creates a `measure` object, with certain properties:

```
<measure options="<OPTIONS>"></measure>s

options: {
  'time': '4/4',
  'meter': 'simple',
  'key': 'C',
  'number': 'auto',
  'grouping': 'n/a'
  'other': {
    'placement': '-X-',
  }
}
```

- `<OPTIONS>` must be replaced by an inline JSON object
- The `options` dictionary outlined above lists the defaults for each option
    - Not all options need be provided -- only options changing from the default
    - When a `measure` sets a new option, the processor adopts that option as
      the default until a new option is selected, which becomes the new default:

```
<!--two measures of 3/4 and a measure of 5/8-->

<measure options="{time: '3/4'}"></measure>
<measure></measure>
<measure options="{time: '5/8'}"></measure>
```

##### Time Signature and Meter
- `time`: the time signature, specifying the number and type of beat
    - Can be any time signature, should be string `'int/int'`
- `meter`: the meter of the measure---`simple`, `compound`, or `asym`
    - Determines the beaming of eighth notes, sixteenth notes, etc.

##### Key Signature
- `key`: the key signature of the measure, specifically the major key
    - The key of Am, for example, would be `key: 'C'`
    - Key should be specified using pitch notation outlined for notes
      (i.e. $\rm D\flat$ major as `key: 'D-'`)

##### Measure Numbers
- `number`: the measure number `'n'` or range of numbers `'m:n'`
    - To simplify the notation process, measures with identical properties may
      be grouped into a single `measure` object
    - `number` should be a string containing an integer or a range of integers
      (i.e. `2:7`)
    - For more on numbering, see: [How it Works](#how-it-works)

##### Measures Other
- `other`: a dictionary of additional customizations for measures
    - `placement`: the formatting of a measure; `-` indicates a measure break
      with no rules, `--` indicates a measure break that should not split across
      lines, and `|` indicates a measure break that splits across lines

##### Grouping
- `grouping`: indicates any repetition in measures
    - By default, `'n/a'`---indicates no repetition
    - When a grouping is provided, it should be as `'identifier[indices]'`,
      where `identifier` is some string and `indices` are integers or a range of
      integers (i.e. `1:3`) during which the measure or measure group appears
- Within a document, `measures` may be organized into `divs` with no impact on
  the organization of the piece: all structural organization occurs via numbers
  or identifiers (but `div`s may be used for writer clarity of mind)

### Notes
- Note objects are created with `<note></note>`---comparable to `<p></p>`
- Although the connection between musical notes and SMML notes is tenuous at
  best, the `note` object is designed to be a middle ground between easy
  transformation into a music note and easy interpretation as a sound wave

```
<note>
  {
    pitch: 'C4',
    beat: '3/2',
    length: '1/4',
    staccato: False,
    identifier: 'n/a',
    other: {
      dynamics: 'n/a',
      lyrics: '',
    }
  }
</note>
```

##### Pitch
- `pitch`: a string indicating the scientific pitch of the note
    - Format: `'<Capital Letter>' + '<Integer>'`
    - Accidentals are indicated with one or more `+`, `-`, or `=`, which is
      appended after the note name (i.e. `E4++`)
        - No accidentals such as `C#4`, `Db5`, etc.
        - Key signature accidentals are not automatically included -- i.e., in
          `key: 'D'`, the pitch `'C4'` would have a natural sign while the
          pitch `'C4+'` would have no accidentals
        - Accidental notes that match the specified key signature have their
          accidental dropped when SMML is displayed
    - Microtones are indicated with `+` or `-` an integer or a float, in cents
- The current version of SMML does not support multiple voices or multi-staff
  instruments (such as the piano)

##### Beat and Length
- `beat`: a string indicating the starting beat of the note
- `length`: a string indicating the length (in beats) of the note
- Both `beat` and `length` strings should be in the format of an integer or an
  improper fraction, since all notated music is mathematically perfect
- By default, the `beat` property of a note inherits a section and measure
  number from its `section` and `measure` containers
    - In ambiguous cases, such as in grouped measures or outside of a measure,
      these properties may be provided in the form `X.X/X` or `X.X.X/X`
- The `length` property of a note may exceed the length of a measure
    - This is useful for audio processing tools, as it prevents the
      stress of combining tied notes, as well as the notational complexity
    - Visual `SMML` processors will interpret length into a certain note or
      combination of notes, as appropriate

##### Staccato
- `staccato`: a boolean value indicating whether or not a note is staccato
- This is the only articulation markup provided in the current version of
  `SMML`; for more on articulation, see [Further Reading](#further-reading)

##### Identifier
- `identifier`:  a string associated with a particular note object
- By default (such as when the value is `'n/a'`), a note's starting beat
  (including section and measure) serves as its identifier, with an added number
  indicating index in a chord stack where necessary
    - For example, `1.3.5/3.2` identifies the second-lowest note beginning
      on the second triplet of the second beat of the third measure
- A custom identifier may be supplied if desired
- Notes may be grouped into `div`s with no effect on the musical structure

##### Notes Other
- `dynamics`: the expression text for the relative dynamics of a given note
- `lyrics`: text to be placed below the note on the staff

##### Note Shorthand
```
<note>C4, 1, 4</note>
```

- The inner text of a shorthand note node will be automatically parsed as string
  values for the keys that make up the properties of the note
    - To save space, values are parsed positionally
    - Required order: `pitch, beat, length, [staccato, identifier, other]`
- The following arguments are required: `pitch`, `beat`, `length`
- The remaining arguments, `staccato`, `identifier`, and `other`, may be
  provided in that positional order, if the default values are not appropriate

### Further Reading
##### More on Markup and Articulation
- The current pre-alpha version of `SMML` provides very limited support for
  articulation, providing only those necessary for audio processing, plus a few
  additional features that are simple to implement
- The following articulation markup is supported:
    - Repeats, created by grouping measures
    - Time and Key Signature, necessary properties of measures
    - Pitch (including Accidentals), Starting Beat, and Length
    - Staccato, necessary for differentiating in audio processing
    - Relative Dynamics, a simple property useful for audio processing
    - Lyrics, text placed underneath a given note
- The following articulation markup is *not* supported:
    - Tempo Indicators, both explicit and relative
    - Multiple-Staff and Multiple-Voice sheet music
    - Qualitative Articulation, such as slurs, tenuto, etc.
    - Performance Text, such as _rubato_, _freely_, etc.
    - Custom Measure Numbering, including Rehearsal Letters/Numbers
    - Any other features not listed as supported
- Have a new feature to add to the list, or a patch enabling support of an
  unsupported feature? Let us know! Create an issue, fork, or pull request
  right on GitHub
    - At the moment, the highest two priorities are support for tempo and
      multiple- staff and voice music, as these are severe limitations
