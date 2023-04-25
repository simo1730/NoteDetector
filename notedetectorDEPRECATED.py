#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 15:40:37 2023

@author: simo
"""
from aubio import source, pitch
import librosa
import argparse

def detectNotes(inputFile, outputFile, octave):
    inputAudio = source(inputFile)

    detectPitch = pitch("yin", inputAudio.samplerate)
    detectPitch.set_unit("midi")
    detectPitch.set_silence(-200)

    notes = []
    while True:
        audio_block, read = inputAudio()
        if read == 0:
            break
        pitchValue = detectPitch(audio_block)[0]
        currentNote = librosa.midi_to_note(pitchValue, octave=octave)
        notes.append(currentNote)
        

    with open(outputFile, 'w') as f:
        for note in notes:
            f.write(str(note) + '\n')
    print(f'Noty ulozene do {outputFile}!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='skript na detekciu not zo zvukoveho suboru')
    parser.add_argument('inputFile', type=str, help='vstupny audio subor')
    parser.add_argument('outputFile', type=str, help='vystupny subor .txt')
    parser.add_argument('--octave', action='store_true', help='nepovinny argument pre zobrazenie oktavy (zobrazovanie nie je vo vsetkych pripadoch spravne)')
    args = parser.parse_args()
    detectNotes(args.inputFile, args.outputFile, args.octave)