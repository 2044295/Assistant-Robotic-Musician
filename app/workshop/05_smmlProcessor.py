#!/usr/bin/env python3

import re
import json

### From "../HTML/smmlReader.py" -- when in package, just import
import sys
filename = sys.argv[1]
with open(filename, 'r') as myfile:
    text = myfile.read().replace('\n', '')

    mode = 'read'
    output = ''

    while len(text) != 0:
        # READ mode: skip all whitespace; look for tags; read general characters
        if mode == 'read':
            if text[0] == '<':              # START OF A TAG CASE
                mode = 'tag'                    # set mode for next iteration
                output += text[0]               # add the first tag character
                text    = text[1:]              # and remove before looping
                if text[:4] == 'note':          # NOTE TAG special case below
                    mode = 'content'                # set mode for the future
                    n = text.find('>')              # lowest index - end of tag
                    output += text[:n+1]            # add ALL tag text to output
                    text    = text[n+1:]            # and remove from the string
            elif text[0] == ' ':            # WHITESPACE CASE
                text = text.lstrip(' ')         # skip whitespace
            else:                           # GENERAL CASE
                output += text[0]               # add character to output
                text    = text[1:]              # and remove before looping

        # TAG mode: reduce all whitespace to a single space character
        elif mode == 'tag':
            if text[0] == ' ':              # WHITESPACE CASE
                output += ' '                   # add single ' ' for whitespace
                text    = text.lstrip(' ')      # and strip all whitespace
            elif text[0] == '<':            # START TAG CASE -- raises error
                raise ValueError('Cannot start a new tag (<) within a tag')
            elif text[0] == '>':            # END TAG CASE -- end tag mode
                mode = 'read'                   # return to read mode
                output += '>'                   # add character to output
                text    = text[1:]              # and remove before looping
            else:                           # GENERAL CASE
                output += text[0]               # add character to output
                text    = text[1:]              # and remove before looping

        # CONTENT mode: preserve all text
        elif mode == 'content':
            if text[:2] == '</':            # END NOTE TAG CASE
                mode = 'read'                   # return to read mode
                n = text.find('>')              # lowest index - end of tag
                output += text[:n+1]            # add the closing tag
                text    = text[n+1:]            # and remove before looping
            else:                           # GENERAL CASE
                output += text[0]              # add character to output
                text    = text[1:]             # and remove before looping

        # if none of these cases are true, there must be an error
        else:
            raise ValueError('Invalid mode detected')

text = output # this would be the "return" in the actual program

### Some arguments
comment = False
if '--comment' in sys.argv:
    comment = True
if comment:
    print(output)

### From "04_PitchFreq.py" -- when in package, just import
with open('04_PitchData.json', 'r') as myfile:
    freqData = json.loads(myfile.read())

# Main
## Defining some defaults and interpretations
keysigs = {
    'C': [],
    'G': ['F+'],
    'D': ['F+', 'C+'],
    'A': ['F+', 'C+', 'G+'],
    'E': ['F+', 'C+', 'G+', 'D+'],
    'B': ['F+', 'C+', 'G+', 'D+', 'A+'],
    'F+': ['F+', 'C+', 'G+', 'D+', 'A+', 'E+'],
    'C+': ['F+', 'C+', 'G+', 'D+', 'A+', 'E+', 'B+'],
    'F': ['B-'],
    'B-': ['B-', 'E-'],
    'E-': ['B-', 'E-', 'A-'],
    'A-': ['B-', 'E-', 'A-', 'D-'],
    'D-': ['B-', 'E-', 'A-', 'D-', 'G-'],
    'G-': ['B-', 'E-', 'A-', 'D-', 'G-', 'C-'],
    'C-': ['B-', 'E-', 'A-', 'D-', 'G-', 'C-', 'F-'],
}
default_options = {
    'time': '4/4',
    'meter': 'simple',
    'key': 'C',
    'number': 'auto',
    'grouping': 'n/a',
    'other': {
        'placement': '-X-'
    }
}

### First, process the bulk "music" grouping -- extract + store the data
def interpret_music(data, container):
    # "skip" signal
    if data == '':
        container.append([])
        return('')

    # otherwise, extract the actual data
    music = data[data.find('<music'):]
    music = music[music.find('>') + 1:]
    container.append([music])
    return(music)

### Next, extract and store the data properly grouped into sections
def interpret_section(n, data, container):
    # "skip" signal -- for data that doesn't have a "section" tag
    if data == '':
        container.append('')
        return(n, '') # skipped section neither recorded nor counted

    # if data is not skipped, step to next section
    n += 1

    # extract the section and tag data
    tag_start = data.find('<section')
    tag = data[tag_start:]
    tag = tag[:tag.find('>') + 1]
    section = data[tag_start + len(tag):] # note that ungrouped data is dropped
    container.append(tag)
    container.append(section)

    # using regex to match any possible id string
    id = re.search(' id=[\"\'].*[\"\'][ >]', tag)
    if id is not None:
        # check that id matches the expected format
        if id[0][5:-2].startswith('section-{}'.format(n)) is False:
            print('Error: {} does not match required format'.format(tag))
            return(n, '') # erroneous section not recorded but still counted

    # everything checks out -- return as normal
    return(n, section)

### Program interprets an encountered measure object
def interpret_measure(i, data, options, container):
    # "skip" signal
    if data == '':
        container.append('')
        return(i, '', options) # skipped text neither recorded nor counted

    # extract the measure and tag data
    tag_start = data.find('<measure')
    tag = data[tag_start:]
    tag = tag[:tag.find('>') + 1]
    measure = data[tag_start + len(tag):] # note that ungrouped data is dropped
    container.append(tag)
    container.append(measure)

    # extract options from the tag
    new_options = re.search(' options=[\"\']\{.*\}[\"\'][ >]', tag)
    if new_options is not None:
        new_options = new_options[0][10:-2]
        new_options = json.loads(new_options)

        # check that the time signature is valid
        if 'time' in new_options.keys():
            time = new_options.pop('time')
            if re.fullmatch('[0-9]+/[0-9]+', time) is None:
                print('Error: Invalid Time Detected: {}'.format(time))
            else:
                options['time'] = time

        # check that the meter is valid
        if 'meter' in new_options.keys():
            meter = new_options.pop('meter')
            if meter not in ['simple', 'compound', 'asym']:
                print('Error: Invalid Meter Detected: {}'.format(meter))
            else:
                options['meter'] = meter

        # check that the key signature is valid
        if 'key' in new_options.keys():
            key = new_options.pop('key')
            if key not in keysigs.keys():
                print('Error: Invalid Key Detected: {}'.format(key))
            else:
                options['key'] = key

        # check that numbering is valid
        if 'number' in new_options.keys():
            number = new_options.pop('number')
            number_test = re.fullmatch('[0-9]+(:[0-9]+)?', number)
            if number.startswith(str(i[1] + 1)) is False or number_test is None:
                print('Error: Invalid Number Detected: {}'.format(number))
            else:
                options['number'] = number

        # lastly, check that all keys are valid
        for option in new_options.keys():
            if option not in options.keys:
                print('Error: Invalid Option Detected: {}'.format(option))
            else:
                options[option] = new_options[option] # update option

    # process options
    number = options['number']
    if number == 'auto':
        i = [i[1]+1, i[1]+1]
    elif number.isdigit():
        i = [int(number), int(number)]
    else:
        i = [int(x) for x in number.split(':')]

    # SOMETHING TO DO WITH GROUPING

    # and last but not least, return all the processed data
    return(i, measure, options)

### Program interprets encoded note data
def interpret_note(i, j, data, options, container):
    # "skip" signal
    if data == '':
        container.append('')
        return(i, j, []) # an empty list in the node just gets skipped

    # extract the note and tag data
    tag_start = data.find('<note')
    tag = data[tag_start:]
    tag = tag[:tag.find('>') + 1]
    note = data[tag_start + len(tag):] # note that ungrouped data is dropped
    container.append(note)

    # try to extract the data as full JSON
    note_data = re.search('\{.*\}', tag)
    if note_data is not None:
        note_data = json.loads(new_options)
        pitch = note_data['pitch']
        beat = note_data['beat']
        length = note_data['length']
    else:
        note_data = [x.strip() for x in note.split(',')]
        pitch = note_data[0]
        beat = note_data[1]
        length = note_data[2]

    if re.fullmatch('[0-9]+/[0-9]+', beat) is not None:
        beatlist = [int(x) for x in beat.split('/')]
        num, denom = beatlist[0], beatlist[1]
    else:
        num, denom = int(beat), 1

    # checking that format is as expected
    if re.fullmatch('[A-G][0-9][+|-]*', pitch) is None:
        print('Error: Invalid Pitch Detected: {}'.format(pitch))
        return(i, j, [])

    if re.fullmatch('[0-9]+(/[0-9]+)?', beat) is None:
        print('Error: Invalid Beat Detected: {}'.format(beat))
        return(i, j, [])

    if num/denom > float(options['time'].split('/')[0]):
        print('Error: Beat Value Too Large: {}'.format(beat))
        return(i, j, [])

    # get the expected pitch
    pitch_base = pitch[0:2]
    if len(pitch) > 2:
        pitch_acc = pitch[2:]
    else:
        pitch_acc = ''

    pitch_index = freqData['pitches'].index(pitch_base)
    for char in pitch_acc:
        if char == '+': pitch_index += 1
        if char == '-': pitch_index -= 1
    pitch = freqData['pitches'][pitch_index]
    # freq = freqData[pitch] -- not used; program detects pitch + error to match

    # figure out the "node" of the note
    if num/denom < j:
        i[0] += 1 # next measure

    j = num/denom

    node = '{}.{}'.format(i[0], beat)

    return(i, j, [node, pitch])

### Program cleans up its output
def cleanup(nodes):
    cleaned_nodes = []

    # start by concatenating all lists starting with a certain node
    node = [None, 0]
    for i, item in enumerate(nodes):
        # we only operate on nonempty lists
        if type(item) is list:
            if len(item) > 0:
                # positive match -- concatenate and clear duplicate
                if item[0] == node[0]:
                    item.pop(0)
                    nodes[node[1]] += item
                    nodes[i] = []
                # negative match -- tell the computer we've a new node
                else:
                    node = [item[0], i]

    # then, loop over the object to recursively clean it up
    for i, item in enumerate(nodes):
        if type(item) is list:
            if item != []:
                cleaned_nodes.append(cleanup(item))
        else:
            cleaned_nodes.append(item)

    return(cleaned_nodes)

## Starting from the top
section = 1
measure = 1
grouping = False
container = []
music_nodes = []

### Entering the text
#### For each segment of SMML, create a unique grouping
for m, data in enumerate(text.split('</music>')):
    if data.count('<music') == 0:
        data = '' # signal to "skip" the grouping

    music = interpret_music(data, container)
    temp_node = []

    #### For each "section," create enumerated groupings
    n = 0 # not using "enumerate" so we can manually count n
    for subdata in music.split('</section>'):
        if subdata.count('<section') == 0:
            subdata = '' # signal to "skip" the section

        n, section = interpret_section(n, subdata, container[m])
        temp_sec = [n, []]

        #### For each "measure," go through and enumerate notes
        # using "i" to enumerate - [start, end, [GROUPING??]]]
        i = [0, 0] # not using "enumerate" so we can manually count i
        options = default_options # re-set for new section
        for subsubdata in section.split('</measure>'):
            if subsubdata.count('<measure') == 0:
                subsubdata = '' # signal to "skip" the measure

            i, measure, options =\
                interpret_measure(i, subsubdata, options, container[m])

            j = 0 # use to track when a multi-measure "loops" around
            for notedata in measure.split('</note>'):
                if notedata.count('<note') == 0:
                    notedata = '' # signal to "skip" the note

                i, j, note =\
                    interpret_note(i, j, notedata, options, container[m])
                temp_sec[1].append(note)

        if section != '':
            temp_node.append(temp_sec)

    if music != '':
        music_nodes.append(temp_node)

music_nodes = cleanup(music_nodes)

if comment:
    print(json.dumps(container, indent=2))
for node in music_nodes:
    print(json.dumps(node, indent=2))
