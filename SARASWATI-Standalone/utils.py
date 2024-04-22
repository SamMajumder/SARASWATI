# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 10:06:29 2024

@author: Dr. M
"""

import pandas as pd
import numpy as np
import pretty_midi
import music21
import os 
import torch
import torchaudio
import audiocraft
from audiocraft.models import MusicGen
import tensorflow as tf

import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
import threading
from tkinter import filedialog


### 
# Function to generate modes for a given scale in all 12 keys
def generate_modes(scale_class, mode_names):
    modes = {}
    for key_pitch in music21.scale.ChromaticScale().getPitches('C', 'B'):
        key_scale = scale_class(tonic=key_pitch)
        for mode_number, mode_name in enumerate(mode_names, start=1):
            mode_key = f"{key_pitch.name} {mode_name}"
            mode_pitches = [p.name for p in key_scale.getPitches()[:len(mode_names)]]  # Get pitches for the mode
            modes[mode_key] = [music21.pitch.Pitch(p).midi % 12 for p in mode_pitches]  # Get MIDI numbers for one octave
    return modes

### 
# Generate scales and modes
major_scale_modes = ['Ionian', 'Dorian', 'Phrygian', 'Lydian', 'Mixolydian', 'Aeolian', 'Locrian']
melodic_minor_modes = ['Melodic Minor', 'Dorian b2', 'Lydian Augmented', 'Lydian Dominant', 'Mixolydian b6', 'Locrian #2', 'Altered Scale']
harmonic_minor_modes = ['Harmonic Minor', 'Locrian #6', 'Ionian #5', 'Dorian #4', 'Phrygian Dominant', 'Lydian #2', 'Altered Diminished']

major_modes = generate_modes(music21.scale.MajorScale, major_scale_modes)
melodic_minor_modes = generate_modes(music21.scale.MelodicMinorScale, melodic_minor_modes)
harmonic_minor_modes = generate_modes(music21.scale.HarmonicMinorScale, harmonic_minor_modes)

### Manually define the Harmonic Major Scale and Double Harmonic Major Scale
def harmonic_major_scale(tonic):
    scale_intervals = ['P1', 'M2', 'M3', 'P4', 'P5', 'm6', 'M7']
    return music21.scale.ConcreteScale(pitches=[music21.pitch.Pitch(tonic).transpose(interval) for interval in scale_intervals])

def double_harmonic_major_scale(tonic):
    scale_intervals = ['P1', 'm2', 'M3', 'P4', 'P5', 'm6', 'M7']
    return music21.scale.ConcreteScale(pitches=[music21.pitch.Pitch(tonic).transpose(interval) for interval in scale_intervals])

### Generate modes for the Harmonic Major Scale and Double Harmonic Major Scale
harmonic_major_modes = ['Harmonic Major', 'Dorian b5', 'Phrygian b4', 'Lydian b3', 'Mixolydian b2', 'Lydian Augmented #2', 'Locrian bb7']
double_harmonic_major_modes = ['Double Harmonic Major', 'Lydian #2 #6', 'Ultra Phrygian', 'Hungarian Minor', 'Oriental', 'Ionian Augmented #2', 'Locrian bb3 bb7']

harmonic_major_modes = generate_modes(harmonic_major_scale, harmonic_major_modes)
double_harmonic_major_modes = generate_modes(double_harmonic_major_scale, double_harmonic_major_modes)

### Combine all modes into a single dictionary
scales = {**major_modes, **melodic_minor_modes, **harmonic_minor_modes, **harmonic_major_modes, **double_harmonic_major_modes}

### 
# Function to map data to notes in a scale
def map_data_to_scale(data, scale, reverse_mapping=False, octave_shift=0):
    scale_notes = [music21.pitch.Pitch(note).midi + (octave_shift * 12) for note in scale]
    if reverse_mapping:
        mapped_notes = np.interp(data, (data.min(), data.max()), (max(scale_notes), min(scale_notes)))
    else:
        mapped_notes = np.interp(data, (data.min(), data.max()), (min(scale_notes), max(scale_notes)))
    return [scale_notes[np.argmin(np.abs(note - scale_notes))] for note in mapped_notes]


## a function to map velocity 
def map_velocity(data, reverse_mapping=False):
    mapped_velocity = np.interp(data, (data.min(), data.max()), (0, 127))
    if reverse_mapping:
        mapped_velocity = 127 - mapped_velocity
    return np.clip(mapped_velocity, 0, 127)  # Ensure values are within the MIDI range



## a function to map duration 
def map_duration(data, lower_limit=0.1, upper_limit=4, reverse_mapping=False):
    mapped_duration = np.interp(data, (data.min(), data.max()), (lower_limit, upper_limit))
    if reverse_mapping:
        mapped_duration = upper_limit - (mapped_duration - lower_limit)
    return np.clip(mapped_duration, lower_limit, upper_limit)  # Ensure values are within the specified range




### 
# a function to convert to midi 
def convert_to_midi(column, output_file, velocity_column, duration_column, scale_name='C Ionian', instrument_name='Acoustic Grand Piano', tempo=120, reverse_note_mapping=False, reverse_velocity_mapping=False, reverse_duration_mapping=False, lower_limit=0.1, upper_limit=4):
    if scale_name not in scales:
        raise ValueError(f"Scale '{scale_name}' not found. Please choose from the available scales.")

    try:
        instrument_program = pretty_midi.instrument_name_to_program(instrument_name)
    except KeyError:
        raise ValueError(f"Instrument '{instrument_name}' not found. Please choose from the available instruments.")

    midi_data = pretty_midi.PrettyMIDI(initial_tempo=tempo)
    instrument = pretty_midi.Instrument(program=instrument_program)

    scale = scales[scale_name]
    mapped_notes = map_data_to_scale(column, scale, reverse_mapping=reverse_note_mapping)
    mapped_velocities = map_velocity(velocity_column, reverse_mapping=reverse_velocity_mapping)
    mapped_durations = map_duration(duration_column, lower_limit=lower_limit, upper_limit=upper_limit, reverse_mapping=reverse_duration_mapping)

    # Create a CSV file with the mappings
    mapping_data = {
        'Original_Value': column,
        'Mapped_Note': [pretty_midi.note_number_to_name(int(note)) for note in mapped_notes],
        'Original_Value_velocity': velocity_column,
        'Mapped_Velocity': mapped_velocities,
        'Original_Value_note_duration': duration_column,
        'Mapped_Note_Duration': mapped_durations
    }
    mapping_df = pd.DataFrame(mapping_data)
    mapping_df.to_csv(output_file.replace('.mid', '_mapping.csv'), index=False)

    for i, note_number in enumerate(mapped_notes):
        note = pretty_midi.Note(
            velocity=int(mapped_velocities[i]),
            pitch=int(note_number),
            start=i * float(mapped_durations[i]),
            end=(i + 1) * float(mapped_durations[i])
        )
        instrument.notes.append(note)

    midi_data.instruments.append(instrument)
    midi_data.write(output_file)
    return midi_data


