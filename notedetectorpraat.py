#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 12:17:30 2023

@author: simo
"""
import librosa
import argparse
import parselmouth

def detectNotes(inputFile, outputFile, octave):
    inputAudio = parselmouth.Sound(inputFile)
    pitch = inputAudio.to_pitch()
    pitchValues = pitch.selected_array['frequency']        
    notes = [ '%.3f' % elem for elem in pitchValues ]   
    notes = [(float(f)) for f in notes]
    notes = [i for i in notes if i != 0]
    notes = librosa.hz_to_note(notes, octave=octave)

    with open(outputFile, 'w') as f:
        for note in notes:
           f.write(str(note) + '\n')
    print(f'Noty ulozene do {outputFile}!')
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='skript na detekciu not zo zvukoveho suboru')
    parser.add_argument('inputFile', type=str, help='vstupny audio subor')
    parser.add_argument('outputFile', type=str, help='vystupny subor .txt')
    parser.add_argument('--octave', action='store_true', help='argument pre zobrazenie oktavy prislusneho tonu')
    args = parser.parse_args()
    detectNotes(args.inputFile, args.outputFile, args.octave)
