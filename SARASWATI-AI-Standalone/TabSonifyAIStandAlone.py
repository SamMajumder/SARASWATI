# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 10:35:34 2024

@author: samba
"""

import tkinter as tk
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import threading
from tkinter import filedialog
import pandas as pd 
import os
from utils import *
from midi_conversion import *
from GenerateMusicAI import * 

# Function to get all instrument names from pretty_midi
def get_instrument_names():
    # Returns a list of instrument names for MIDI program numbers 0-127
    return [pretty_midi.program_to_instrument_name(i) for i in range(128)]


app = ctk.CTk()
app.title('Data Sonification App')
app.geometry('1200x800')
ctk.set_appearance_mode("dark")  # Enable dark mode

# Function to load the file, update the DataFrame, and the ComboBoxes
def load_file():
    global loaded_df  # Declare the global variable to hold the DataFrame
    filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if filepath:
        file_path_label.configure(text=filepath)  # Update the label with the file path
        loaded_df = pd.read_csv(filepath)  # Load the data into the DataFrame
        update_comboboxes(loaded_df.columns)  # Update the ComboBoxes with the new columns


def update_comboboxes(columns):
    column_list = ["Select a column"] + list(columns)
    note_combobox.configure(values=column_list)
    velocity_combobox.configure(values=column_list)
    duration_combobox.configure(values=column_list)



def run_sonification_thread():
    thread = threading.Thread(target=run_sonification)
    thread.start()


def run_sonification():
    global loaded_df

    if loaded_df is not None:
        # Collect inputs from GUI
        note_column = note_combobox.get()
        velocity_column = velocity_combobox.get()
        duration_column = duration_combobox.get()
        scale_name = scale_combobox.get()
        instrument_name = instrument_combobox.get()
        tempo = int(tempo_entry.get())
        lower_limit = float(lower_limit_entry.get())
        upper_limit = float(upper_limit_entry.get())
        reverse_note_mapping = inverse_note_checkbox.get()
        reverse_velocity_mapping = inverse_velocity_checkbox.get()
        reverse_duration_mapping = inverse_duration_checkbox.get()
        music_description = description_entry.get()  # Assume there's an entry in the GUI for this
        initial_duration = float(initial_duration_entry.get())  # Same here

        output_dir = filedialog.askdirectory()
        if not output_dir:
            status_label.configure(text="Operation cancelled. No output directory selected.")
            return

        midi_output_file = os.path.join(output_dir, 'sonification.mid')
        wav_output_file = os.path.join(output_dir, 'generated_music.wav')

        # Convert data to MIDI
        midi_data, scale_factor, csv_file_path = convert_to_midi(
            column=loaded_df[note_column],
            output_file=midi_output_file,
            velocity_column=loaded_df[velocity_column],
            duration_column=loaded_df[duration_column],
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

        # Convert MIDI to text for music generation
        sonification_text = midi_to_text(midi_data)
        combined_prompt = f"{music_description}. Use the following notes, start times, end times, and durations for the composition: {sonification_text}"

        # Generate initial music
        # Update progress bar 1 to show music generation progress
        progress_bar1.set(1.0)

        initial_music_tensor = generate_music(combined_prompt, initial_duration, wav_output_file)

        # Optionally extend the music
        progress_bar2.set(0.0)
        if extend_music_checkbox.get():  # Assume you have a checkbox for this
            extension_duration = float(extension_duration_entry.get())
            prompt_duration = float(prompt_duration_entry.get())
            continued_music_tensor = continue_music(initial_music_tensor, extension_duration, prompt_duration)
            extended_output_path = os.path.join(output_dir, 'extended_music.wav')
            save_audio(continued_music_tensor, 32000, extended_output_path)
            progress_bar2.set(1.0)

        status_label.configure(text="Sonification and music generation complete. Check the output directory.")
    else:
        status_label.configure(text="Please load data to process.")


    


# Top section for file loading
# Top section frame for loading CSV and mapping controls
top_frame = ctk.CTkFrame(app)
top_frame.pack(side="top", fill="x", padx=20, pady=20)

# Load CSV button and file path label
load_button = ctk.CTkButton(top_frame, text="Load CSV", command=load_file)
load_button.pack(side="left", padx=10, pady=10)

file_path_label = ctk.CTkLabel(top_frame, text="No file loaded")
file_path_label.pack(side="left", padx=10)

# Frame for the note mapping controls
note_frame = ctk.CTkFrame(top_frame)
note_frame.pack(side="left", padx=10, fill="both", expand=True)
note_heading = ctk.CTkLabel(note_frame, text="Note Mapping", font=("Arial", 12))
note_heading.pack(pady=5)
note_combobox = ctk.CTkComboBox(note_frame, values=["Select a column"])
note_combobox.pack(pady=10)
inverse_note_checkbox = ctk.CTkCheckBox(note_frame, text="Inverse Note Mapping")
inverse_note_checkbox.pack()

# Frame for the velocity mapping controls
velocity_frame = ctk.CTkFrame(top_frame)
velocity_frame.pack(side="left", padx=10, fill="both", expand=True)
velocity_heading = ctk.CTkLabel(velocity_frame, text="Velocity Mapping", font=("Arial", 12))
velocity_heading.pack(pady=5)
velocity_combobox = ctk.CTkComboBox(velocity_frame, values=["Select a column"])
velocity_combobox.pack(pady=10)
inverse_velocity_checkbox = ctk.CTkCheckBox(velocity_frame, text="Inverse Velocity Mapping")
inverse_velocity_checkbox.pack()

# Frame for the duration mapping controls
duration_frame = ctk.CTkFrame(top_frame)
duration_frame.pack(side="left", padx=10, fill="both", expand=True)
duration_heading = ctk.CTkLabel(duration_frame, text="Duration Mapping", font=("Arial", 12))
duration_heading.pack(pady=5)
duration_combobox = ctk.CTkComboBox(duration_frame, values=["Select a column"])
duration_combobox.pack(pady=10)
inverse_duration_checkbox = ctk.CTkCheckBox(duration_frame, text="Inverse Duration Mapping")
inverse_duration_checkbox.pack()


# Middle section for user inputs with more structured frames
middle_frame = ctk.CTkFrame(app)
middle_frame.pack(side="top", fill="x", padx=20, pady=20)

# Frame for scale and instrument selection
selection_frame = ctk.CTkFrame(middle_frame)
selection_frame.pack(side="left", padx=20, pady=10)  # Aligned to the left, no expand, no fill

# Scale selection within the selection frame
scale_label = ctk.CTkLabel(selection_frame, text="Select Scale:")
scale_label.pack(pady=5)  # Vertical packing
scale_combobox = ctk.CTkComboBox(selection_frame, values=list(scales.keys()))
scale_combobox.pack(pady=5)

# Frame for scale and instrument selection
selection_frame = ctk.CTkFrame(middle_frame)
selection_frame.pack(side="left", padx=20, pady=10)  # Aligned to the left, no expand, no fill


# Instrument selection within the selection frame
instrument_label = ctk.CTkLabel(selection_frame, text="Instrument:")
instrument_label.pack(pady=5)  # Vertical packing
instrument_names = get_instrument_names()
instrument_combobox = ctk.CTkComboBox(selection_frame, values=instrument_names)
instrument_combobox.pack(pady=5)


# Frame for scale and instrument selection
selection_frame = ctk.CTkFrame(middle_frame)
selection_frame.pack(side="left", padx=20, pady=10)  # Aligned to the left, no expand, no fill

# Tempo Entry
tempo_label = ctk.CTkLabel(selection_frame, text="Tempo (BPM):")
tempo_label.pack(pady=5)
tempo_entry = ctk.CTkEntry(selection_frame, width=100)
tempo_entry.pack(pady=5)

# Frame for scale and instrument selection
selection_frame = ctk.CTkFrame(middle_frame)
selection_frame.pack(side="left", padx=20, pady=10)  # Aligned to the left, no expand, no fill


# Upper Limit Entry for Note Duration
upper_limit_label = ctk.CTkLabel(selection_frame, text="Upper Limit for Note Duration:")
upper_limit_label.pack(pady=5)
upper_limit_entry = ctk.CTkEntry(selection_frame, width=100)
upper_limit_entry.pack(pady=5)

# Frame for scale and instrument selection
selection_frame = ctk.CTkFrame(middle_frame)
selection_frame.pack(side="left", padx=20, pady=10)  # Aligned to the left, no expand, no fill


# Lower Limit Entry for Note Duration
lower_limit_label = ctk.CTkLabel(selection_frame, text="Lower Limit for Note Duration:")
lower_limit_label.pack(pady=5)
lower_limit_entry = ctk.CTkEntry(selection_frame, width=100)
lower_limit_entry.pack(pady=5)

# Frame for the new music generation and extension controls
# Frame for the new music generation and extension controls
music_gen_frame = ctk.CTkFrame(middle_frame)
music_gen_frame.pack(side="top", fill="x", padx=20, pady=10)

# Music description entry
description_label = ctk.CTkLabel(music_gen_frame, text="Music Description:")
description_label.pack(pady=5)
description_entry = ctk.CTkEntry(music_gen_frame, width=200)
description_entry.pack(pady=5)

# Initial music duration entry
initial_duration_label = ctk.CTkLabel(music_gen_frame, text="Initial Duration (sec):")
initial_duration_label.pack(pady=5)
initial_duration_entry = ctk.CTkEntry(music_gen_frame, width=100)
initial_duration_entry.pack(pady=5)

# Function to toggle extension entries based on checkbox
def toggle_extension_entries():
    if extend_music_checkbox.get():
        extension_duration_entry.configure(state="normal")
        prompt_duration_entry.configure(state="normal")
    else:
        extension_duration_entry.configure(state="disabled")
        prompt_duration_entry.configure(state="disabled")


# Combined label for extension and prompt duration
extension_prompt_label = ctk.CTkLabel(music_gen_frame, text="Extension and Prompt Durations:")
extension_prompt_label.pack(pady=5)

# Extension duration entry with descriptive placeholder
extension_duration_entry = ctk.CTkEntry(music_gen_frame, placeholder_text="Extension Duration (sec)", state="disabled")
extension_duration_entry.pack(pady=5)

# Prompt duration entry with descriptive placeholder
prompt_duration_entry = ctk.CTkEntry(music_gen_frame, placeholder_text="Prompt Duration (sec)", state="disabled")
prompt_duration_entry.pack(pady=5)

# Checkbox to enable/disable extension entries
extend_music_checkbox = ctk.CTkCheckBox(music_gen_frame, text="Extend Music", command=toggle_extension_entries)
extend_music_checkbox.pack(pady=10)



# Middle section for user inputs with more structured frames
middle_frame = ctk.CTkFrame(app)
middle_frame.pack(side="top", fill="x", padx=20, pady=20)

status_label = ctk.CTkLabel(app, text="")
status_label.pack(side="bottom", fill="x", padx=10, pady=10)  # Adjust the position as needed

# Create a new frame for the progress bars and the run button
progress_and_run_frame = ctk.CTkFrame(middle_frame)
progress_and_run_frame.pack(side="top", fill="x", padx=20, pady=10)

# Create the first progress bar
progress_bar1 = ctk.CTkProgressBar(progress_and_run_frame, orientation="horizontal")
progress_bar1.pack(side="left", fill="x", padx=10, expand=True)

# Create the second progress bar
progress_bar2 = ctk.CTkProgressBar(progress_and_run_frame, orientation="horizontal")
progress_bar2.pack(side="left", fill="x", padx=10, expand=True)

# Move the run button to the new frame
run_button = ctk.CTkButton(progress_and_run_frame, text="Run Sonification", command=run_sonification_thread)
run_button.pack(side="right", padx=10)

app.mainloop()



