# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 10:22:59 2024

@author: Dr. M
"""

from utils import *


def main():
    # User inputs and settings
    csv_file = input("Enter the path to your CSV file: ")
    df = pd.read_csv(csv_file)
    print("Available columns in the dataset:", df.columns.tolist())
    note_column = input("Select column for note mapping: ")
    velocity_column = input("Select column for velocity mapping: ")
    duration_column = input("Select column for duration mapping: ")
    reverse_note_mapping = input("Inverse note mapping? (yes/no): ").lower() == 'yes'
    reverse_velocity_mapping = input("Inverse velocity mapping? (yes/no): ").lower() == 'yes'
    reverse_duration_mapping = input("Inverse duration mapping? (yes/no): ").lower() == 'yes'
    scale_name = input(f"Select scale (available scales: {list(scales.keys())}): ")
    instrument_name = input("Select instrument (e.g., 'Violin'): ")
    tempo = int(input("Enter the tempo (e.g., 120): "))
    lower_limit = float(input("Enter the lower limit for note duration (e.g., 0.1): "))
    upper_limit = float(input("Enter the upper limit for note duration (e.g., 4): "))
    initial_duration = float(input("Enter the duration for the initial music track (in seconds): "))
    output_dir = input("Enter the path to the output directory: ")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    midi_output_file = os.path.join(output_dir, 'sonification.mid')
    wav_output_file = os.path.join(output_dir, 'generated_music.wav')

    # MIDI conversion
    # Convert data to MIDI and handle CSV output
    midi_data, scale_factor, csv_file_path = convert_to_midi_with_max_durartion(
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
        upper_limit=upper_limit,
        max_duration=initial_duration
    )

    print(f"CSV mapping file saved to {csv_file_path}")

    # Textual MIDI data for prompt
    sonification_text = midi_to_text(midi_data)
    user_prompt = input("Enter your prompt for style customization (e.g., 'violin music in the style of Vivaldi'): ")
    combined_prompt = f"{user_prompt}. Use the following notes, start times, end times, and durations for the composition: {sonification_text}"

    # Generate initial music
    initial_music_tensor = generate_music(combined_prompt, initial_duration, wav_output_file)

    # Ask user if they want to extend the music and for how long
    if input("Do you want to extend this music further? (yes/no): ").lower() == 'yes':
        extension_duration = int(input("Enter additional duration for the music (in seconds): "))
        prompt_duration = float(input("Enter the duration of the existing music to use as a prompt (in seconds): "))
        continued_music_tensor = continue_music(initial_music_tensor, extension_duration, prompt_duration)

        # Save the extended music
        continued_output_path = os.path.join(output_dir, 'extended_music.wav')
        save_audio(continued_music_tensor, sample_rate=32000, file_path=continued_output_path)
        print(f"Extended music generated and saved to {continued_output_path}")

    print(f"Initial music generated and saved to {wav_output_file}") 
    
    
if __name__ == '__main__':
    main()