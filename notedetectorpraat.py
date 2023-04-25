#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 12:17:30 2023

@author: simo
"""
#pouzitie: python 'inputFile' 'outputFile' --octave
#nacita vstupny audio subor, vystupom je graf zakladnej frekvencie v case a zoznam zakladnych frekvencii audio suboru prevedenych na tony
# skript prevedie audio subor pomocou kniznice parselmouth(Praat) na zoznam zakladnych frekvencii

import librosa
import argparse
import parselmouth
import matplotlib.pyplot as plt
import numpy as np

#funkcia pre detekciu nnot
def detectNotes(inputFile, outputFile, octave):
    #vlozeny audio subor
    inputAudio = parselmouth.Sound(inputFile)
    #pomocou Praat kniznice prevedenie na frekvenncne pasmo
    pitch = inputAudio.to_pitch()
    #hodnoty frekvencii nacita do zoznamu
    pitchValues = pitch.selected_array['frequency']    
    #zaokruhli na 3 desatinne miesta    
    notes = [ '%.3f' % elem for elem in pitchValues ]
    #prevod na float
    notes = [(float(f)) for f in notes]
    #odstranenie nul
    notes = [i for i in notes if i != 0]
    #prevod frekvencie na notu (ton)
    notes = librosa.hz_to_note(notes, octave=octave)
    
    #graficke zobrazenie azkladnej frekvencie
    pitchValues = pitch.selected_array['frequency']   
    pitchValues[pitchValues==0] = np.nan
    plt.plot(pitch.xs(), pitchValues, 'o', markersize=5, color='w')
    plt.plot(pitch.xs(), pitchValues, 'o', markersize=2)
    plt.grid(False)
    plt.ylim(0, pitch.ceiling)
    plt.xlabel("cas [s]")
    plt.ylabel("f0 [Hz]")
    plt.savefig(outputFile + ".png")

    #zapis not do suboru
    with open(outputFile, 'w') as f:
        for note in notes:
           f.write(str(note) + '\n')
    print(f'Noty ulozene do {outputFile}!')
    

#inicializazcia skriptu
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='skript na detekciu not zo zvukoveho suboru')
    parser.add_argument('inputFile', type=str, help='vstupny audio subor')
    parser.add_argument('outputFile', type=str, help='vystupny subor')
    parser.add_argument('--octave', action='store_true', help='argument pre zobrazenie oktavy prislusneho tonu')
    args = parser.parse_args()
    detectNotes(args.inputFile, args.outputFile, args.octave)