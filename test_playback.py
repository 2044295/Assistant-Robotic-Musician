#!/usr/bin/env python3

import smml
with open('samples/Sample1_FrereJacques.html', 'r') as myfile:
    text = ''.join([x.strip() for x in myfile.readlines()])
    smml.markup.playback(text, 'samples/Sample1_FrereJacques.wav')
