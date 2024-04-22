# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 22:29:48 2024

@author: Dr. M
"""

from utils import *



def main():
    # Ask the user to input the path to the CSV file
    csv_file = input("Enter the path to your CSV file: ")
    df = pd.read_csv(csv_file)

    # Ask the user to select columns for note mapping, velocity mapping, and duration mapping
    print("Available columns in the dataset:", df.columns.tolist())
    note_column = input("Select column for note mapping: ")
    velocity_column = input("Select column for velocity mapping: ")
    duration_column = input("Select column for duration mapping: ")

    # Ask the user if they want inverse mapping for notes, velocity, and duration
    reverse_note_mapping = input("Inverse note mapping? (yes/no): ").lower() == 'yes'
    reverse_velocity_mapping = input("Inverse velocity mapping? (yes/no): ").lower() == 'yes'
    reverse_duration_mapping = input("Inverse duration mapping? (yes/no): ").lower() == 'yes'

    # Ask the user to select a scale, instrument, and tempo
    scale_name = input(f"Select scale (available scales: {list(scales.keys())}): ")
    instrument_name = input("Select instrument (e.g., 'Violin'): ")
    tempo = int(input("Enter the tempo (e.g., 120): "))
    
    # Ask the user for the duration mapping limits
    lower_limit = float(input("Enter the lower limit for note duration (e.g., 0.1): "))
    upper_limit = float(input("Enter the upper limit for note duration (e.g., 4): "))

    # Ask the user for an output directory path
    output_dir = input("Enter the path to the output directory: ")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    midi_output_file = os.path.join(output_dir, 'sonification.mid')

    # Convert the data to MIDI with the specified mappings
    midi_data = convert_to_midi(
        column=df[note_column],
        output_file=midi_output_file,
        velocity_column=df[velocity_column],
        duration_column=df[duration_column],
        scale_name=scale_name,
        instrument_name=instrument_name,
        tempo=tempo,
        reverse_note_mapping=reverse_note_mapping,
        reverse_velocity_mapping=reverse_velocity_mapping,
        reverse_duration_mapping=reverse_duration_mapping,
        lower_limit=lower_limit,
        upper_limit=upper_limit
    )

    total_duration = sum([note.end for note in midi_data.instruments[0].notes]) - sum([note.start for note in midi_data.instruments[0].notes])
    
    print(f"Total duration of the track: {total_duration} seconds")
    print(f"Midi file saved to {midi_output_file}") 
    
    
if __name__ == '__main__':
    main()