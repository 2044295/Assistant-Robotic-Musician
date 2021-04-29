#!/usr/bin/env python3

# Import Packages - must run in virtual environment
import chippy, time
import wave
import numpy as np
synth = chippy.Synthesizer(44100)

"""
# Creating a single wave of each type
sine_wave = synth.sine_pcm(length=2, frequency=440, amplitude=0.8)
saw_wave = synth.saw_pcm(length=2, frequency=440, amplitude=0.8)
triangle_wave = synth.triangle_pcm(length=2, frequency=440, amplitude=0.8)
fm_wave = synth.fm_riff(length=2, carrier=440, modulator=122, amplitude=0.9, mod_amplitude=1.0)
square_wave = synth.pulse_riff(length=3, frequency=183, duty_cycle=25)

synth.save_wave(sine_wave, '1_sine_wave.wav')
synth.save_wave(saw_wave, '2_saw_wave.wav')
synth.save_wave(triangle_wave, '3_triangle_wave.wav')
synth.save_wave(fm_wave, '4_fm_wave.wav')
synth.save_wave(square_wave, '5_square_wave.wav')
"""

# Creating a "melody" of sorts: Sweet Child o' Mine
frequencies = [
    587.3295358348151,
    1174.6590716696303,
    879.9999999999999,
    783.9908719634985,
    1567.981743926997,
    879.9999999999999,
    1479.9776908465376,
    879.9999999999999,
    587.3295358348151,
    1174.6590716696303,
    879.9999999999999,
    783.9908719634985,
    1567.981743926997,
    879.9999999999999,
    1479.9776908465376,
    879.9999999999999,
    659.2551138257398,
    1174.6590716696303,
    879.9999999999999,
    783.9908719634985,
    1567.981743926997,
    879.9999999999999,
    1479.9776908465376,
    879.9999999999999,
    659.2551138257398,
    1174.6590716696303,
    879.9999999999999,
    783.9908719634985,
    1567.981743926997,
    879.9999999999999,
    1479.9776908465376,
    879.9999999999999,
    783.9908719634985,
    1174.6590716696303,
    879.9999999999999,
    783.9908719634985,
    1567.981743926997,
    879.9999999999999,
    1479.9776908465376,
    879.9999999999999,
    783.9908719634985,
    1174.6590716696303,
    879.9999999999999,
    783.9908719634985,
    1567.981743926997,
    879.9999999999999,
    1479.9776908465376,
    879.9999999999999,
    587.3295358348151,
    1174.6590716696303,
    879.9999999999999,
    783.9908719634985,
    1567.981743926997,
    879.9999999999999,
    1479.9776908465376,
    879.9999999999999,
    587.3295358348151,
]
waves = [synth.sine_pcm(length=0.25, frequency=x, amplitude=0.8) for x in frequencies]
sweet_child_o_mine = waves[0]
n = 1
while n < len(waves):
    sweet_child_o_mine += waves[n]
    n += 1
synth.save_wave(sweet_child_o_mine, 'sweet_child_o_mine.wav')

# Attempting simplest harmony -- using numpy and wave?
wave_1 = synth.sine_pcm(length=7.0, frequency=130.8127826502993, amplitude=0.8) # C3
wave_2 = synth.sine_pcm(length=6.0, frequency=195.99771799087463, amplitude=0.8) # G3
wave_3 = synth.sine_pcm(length=5.0, frequency=293.6647679174076, amplitude=0.8) # D4
wave_4 = synth.sine_pcm(length=4.0, frequency=311.12698372208087, amplitude=0.8) # Eb4
wave_5 = synth.sine_pcm(length=3.0, frequency=466.16376151808987, amplitude=0.8) # Bb4
sounds = [wave_1, wave_2, wave_3, wave_4, wave_5]

# Putting it all together
def unpack(waveform):
    fmt = '{:.0f}h'.format(len(waveform)/2)
    numbers = np.array(wave.struct.unpack(fmt, waveform), dtype='float')
    return(numbers)

def delay(sound, delay, rate=44100):
    delay = np.zeros(int(rate * delay))
    return(np.array(list(delay) + list(sound)))

sounds = [delay(unpack(x), 1.0 * i) for i, x in enumerate(sounds)]
print(sounds)
mysound = sum(sounds)
mysound = mysound / (np.max(mysound) / 32766.0) # adjust so that we don't blow out speakers
print(np.max(mysound), np.min(mysound))
mysound = mysound.astype('<h').tostring()
synth.save_wave(mysound, 'nausicaa.wav') # conveniently, numpy arrays are automatically structs
