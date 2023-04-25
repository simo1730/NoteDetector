#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 15:40:37 2023

@author: simo
"""
import argparse
from aubio import source, pitch
import librosa

def detect_notes(audio_file, output_file, octave):
    # Open audio file
    audio_source = source(audio_file)

    # Set pitch detection parameters
    pitch_detector = pitch("yin", audio_source.samplerate)
    pitch_detector.set_unit("midi")
    pitch_detector.set_tolerance(0.8)

    # Process audio in blocks and detect pitch
    notes = []
    while True:
        audio_block, read = audio_source()
        if read == 0:
            break
        pitch_value = pitch_detector(audio_block)[0]
        actual_note = librosa.midi_to_note(pitch_value, octave=octave)
        notes.append(actual_note)
        

    # Export notes to a text file
    with open(output_file, 'w') as f:
        for note in notes:
            f.write(str(note) + '\n')
    print(f'Successfully detected notes and saved to {output_file}!')

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Detect notes from an audio file.')
    parser.add_argument('audio_file', type=str, help='Path to the input audio file.')
    parser.add_argument('output_file', type=str, help='Path to the output text file.')
    parser.add_argument('--octave', action='store_true', help='Include octave in note output')
    args = parser.parse_args()

    # Detect notes and save to output file
    detect_notes(args.audio_file, args.output_file, args.octave)