#!/usr/bin/env python3

import re, json
from ..audiofunc import pitchData

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

# Extract + store data in the bulk "music" grouping -- complete
def interpret_music(data, container):
    # "skip" signal
    if data == '':
        container.append([])
        return('')

    # otherwise, extract the actual data
    index = data.find('<music')
    container.append([data[:index]])
    music = data[index:]
    music = music[music.find('>') + 1:]
    return(music)

# Extract and store data in "section" grouping -- complete
def interpret_section(n, data, container):
    # "skip" signal -- for data that doesn't have a "section" tag
    if data == '':
        container.append('')
        return(n, '') # skipped section neither recorded nor counted

    # if data is not skipped, step to next section
    n += 1

    # extract the section and tag data
    index = data.find('<section')
    tag = data[index:]
    tag = tag[:tag.find('>') + 1]
    section = data[index + len(tag):]
    container.append(data[:index])
    container.append(tag)

    # using regex to match any possible id string
    id = re.search(' id=[\"\'].*[\"\'][ >]', tag)
    if id is not None:
        # check that id matches the expected format
        if id[0][5:-2].startswith('section-{}'.format(n)) is False:
            raise ValueError('{} does not match required format'.format(tag))
            return(n, '') # erroneous section not recorded but still counted

    # everything checks out -- return as normal
    return(n, section)

# Interpret an encountered measure object
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
    container.append(data[:tag_start]) # save necessary ungrouped data
    container.append(tag) # save the tag for reference

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

    container.append(options.copy()) # write options to container -- for display
                                     # to recognize new measure with all options

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

# Interpret encoded note data -- relevant to player and displayer               # needs display upgrade (save name + options)
def interpret_note(i, j, data, options, container):
    # "skip" signal
    if data == '':
        return(i, j, []) # an empty list in the node just gets skipped

    voice = re.search('<voice type=[\"\'][a-z]+[\"\']>', data)
    if voice is not None:
        container.append(voice[0])

    # extract the note and tag data
    tag_start = data.find('<note')
    tag = data[tag_start:]
    tag = tag[:tag.find('>') + 1]
    note = data[tag_start + len(tag):] # note that ungrouped data is dropped

    # try to extract the data as full JSON, else use shorthand                  # needs display upgrade
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

    container.append(note)
    # checking that format is as expected
    if re.fullmatch('[A-G][0-9][+|-]*', pitch) is None:
        if pitch != 'N/A':
            print('Error: Invalid Pitch Detected: {}'.format(pitch))
        return(i, j, []) # if rest or if error, note is skipped

    if re.fullmatch('[0-9]+(/[0-9]+)?', beat) is None:
        print('Error: Invalid Beat Detected: {}'.format(beat))
        return(i, j, [])

    max_beat = float(options['time'].split('/')[0]) + 1 # +1 shows next measure
    if num/denom >= max_beat:
        print('Error: Beat Value Too Large: {}'.format(beat))
        return(i, j, [])

    # get the expected pitch
    pitch_base = pitch[0:2]
    if len(pitch) > 2:
        pitch_acc = pitch[2:]
    else:
        pitch_acc = ''

    pitch_index = pitchData['pitches'].index(pitch_base)
    for char in pitch_acc:
        if char == '+': pitch_index += 1
        if char == '-': pitch_index -= 1
    pitch = pitchData['pitches'][pitch_index]

    # figure out the "node" of the note
    if num/denom < j:
        i[0] += 1 # next measure
        if i[0] > i[1]: # exceeded measure bound -- loop back to beginning
            number = options['number']
            if number == 'auto':
                i = [i[1], i[1]]
            elif number.isdigit():
                i = [int(number), int(number)]
            else:
                i = [int(x) for x in number.split(':')]
        else:
            container.append(options.copy())    # write options to container --
                                                # to recognize new measure

    j = num/denom

    node = '{}.{}'.format(i[0], beat)

    return(i, j, [node, pitch])

# Cleans up the program output -- relevant to player and displayer
def cleanup(nodes):
    cleaned_nodes = []

    # start by concatenating all lists starting with a certain node
    i = 0
    while i < len(nodes):
        item = nodes[i]

        # we only operate on nonempty lists
        if type(item) is list:
            if len(item) > 0:
                node = item[0]

                j = i + 1
                while j < len(nodes):
                    item = nodes[j]
                    # if item is not a nonempty list, don't try to operate
                    if type(item) is not list or len(item) == 0:
                        pass
                    # positive match -- concatenate and clear duplicate
                    elif item[0] == node:
                        item.pop(0)
                        nodes[i] += item
                        nodes[j] = []
                    # do nothing for a negative match -- this allows the program
                    # to detect nodes that appear again in a different voice
                    else:
                        pass
                    j += 1

        i += 1

    # then, loop over the object to recursively clean it up
    for i, item in enumerate(nodes):
        if type(item) is list:
            item = cleanup(item)
            if item != []:
                cleaned_nodes.append(item)
        else:
            if item != '':
                cleaned_nodes.append(item)

    return(cleaned_nodes)

def process(text, mode='player'):
    """
    process(text, mode='player')

    Reads a machine-formatted smml string and processes the SMML-encoded data to
    a serialized JSON object. Provides output in one of two `modes`: 'player' or
    'display'. Recommended to manually strip newlines and whitespace from an
    smml string before calling `process`.

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

    """

    if mode not in ['player', 'display']:
        raise ValueError('Unexpected processing mode found: {}'.format(mode))

    # Starting from the top
    grouping = False
    container = []
    music_nodes = []

    # Entering the text
    # For each segment of SMML, create a unique grouping
    for m, data in enumerate(text.split('</music>')):
        if data.count('<music') == 0:
            data = '' # signal to "skip" the grouping

        music = interpret_music(data, container)
        temp_node = []

        # For each "section," create enumerated groupings
        n = 0 # not using "enumerate" so we can manually count n
        for subdata in music.split('</section>'):
            if subdata.count('<section') == 0:
                subdata = '' # signal to "skip" the section

            n, section = interpret_section(n, subdata, container[m])
            temp_sec = [n, []]

            # For each "measure," go through and enumerate notes
            # using "i" to enumerate - [start, end, [GROUPING??]]]
            i = [0, 0] # not using "enumerate" so we can manually count i
            options = default_options # re-set for new section
            for subsubdata in section.split('</measure>'):
                if subsubdata.count('<measure') == 0:
                    subsubdata = '' # signal to "skip" the measure

                i, measure, options =\
                    interpret_measure(i, subsubdata, options, container[m])

                contained_measures = [[]]

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

    container = cleanup(container)
    music_nodes = cleanup(music_nodes)

    if mode == 'display':
        return(container)
    else:
        return(music_nodes)
