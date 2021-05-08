#!/usr/bin/env python3

import chippy, wave
import numpy as np
from .process import process
from ..audiofunc import pitchData

def playback(text, filename, tempo=120, sample_rate=44100):
    """
    DOCUMENTATION
    """

    nodes = process(text)   # the individual nodes to be played
    note_length = 60/tempo  # measured in seconds

    synth = chippy.Synthesizer(sample_rate)

    sound_nodes = np.array([], dtype='float')

    for music in nodes:
        for section in music:
            for node in section[1:][0]:
                waves = [synth.saw_pcm(length=note_length, frequency=pitchData[x], amplitude=0.8) for x in node[1:]]

                fmt = '{:.0f}h'.format(len(waves[0])/2)
                waves = [np.array(wave.struct.unpack(fmt, x), dtype='float') for x in waves]
                mysound = sum(waves)
                mysound = mysound / (np.max(mysound) / 32766.0)
                sound_nodes = np.append(sound_nodes, mysound)

    synth.save_wave(sound_nodes.astype('<h').tostring(), filename)
