#!/usr/bin/env python3

from . import audiofunc, markup

default_options = {
    'type': 'live',
    'file': '-',
    'sample_rate': 8000,
    'frames_rate': 30,
}

def track(text, callback, a4=440, args=default_options):
    """
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
    """
    # Processing given smml
    data = ''.join([x.strip() for x in text.split('\n')])
    nodes = markup.smmlprocess(data)[0]

    # Preparing the audio loop
    frame = 0
    counter = [0, 0]
    def test_match(numbers):
        # get current information
        node = nodes[counter[0]][1][counter[1]] # section - data list - node
        freq, vol = audiofunc.process(numbers)
        pitch = audiofunc.getPitchEstimate(freq, a4)

        # and decide if we have a match
        if pitch[0] in node:
            callback([node[0], pitch])  # output node information
            counter[1] += 1             # start waiting for next node

            # check if we have exceeded the current section
            if counter[1] >= len(nodes[counter[0]][1]):
                counter[0] += 1 # step to next section
                counter[1]  = 0 # and reset the beat count
                if counter[0] >= len(nodes): # end of piece
                    raise KeyboardInterrupt # ends the audio loop
                else:
                    callback(["SECTION {}".format(counter[0])])

    # Starting the audio loop
    state = audiofunc.audioSetup(test_match, args)
    return(state)
