#!/usr/bin/env python3

def read(text):
    """
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
    """

    # For good measure, concatenate to a single line
    text = text.replace('\n', ' ')

    # Initial Variables
    mode = 'read'
    output = ''

    # Main Loop
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

    # lastly, return output (if we get here)
    return(output)
