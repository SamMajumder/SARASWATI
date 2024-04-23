# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 19:15:21 2024

@author: Dr. M
"""

from utils import * 


# Function to get all instrument names from pretty_midi
def get_instrument_names():
    # Returns a list of instrument names for MIDI program numbers 0-127
    return [pretty_midi.program_to_instrument_name(i) for i in range(128)]


app = ctk.CTk()
app.title('SARASWATI')
app.geometry('800x600')
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



def run_sonification():
    global loaded_df  
    if loaded_df is not None:
        # Collect inputs from GUI
        note_column = note_combobox.get()
        velocity_column = velocity_combobox.get()
        duration_column = duration_combobox.get()
        scale_name = scale_combobox.get()
        instrument_name = instrument_combobox.get()
        tempo = int(tempo_entry.get())  # Make sure to validate this input
        lower_limit = float(lower_limit_entry.get())  # And this one
        upper_limit = float(upper_limit_entry.get())  # And also this one
        reverse_note_mapping = inverse_note_checkbox.get()
        reverse_velocity_mapping = inverse_velocity_checkbox.get()
        reverse_duration_mapping = inverse_duration_checkbox.get()

        output_dir = filedialog.askdirectory()  # Lets user select the directory for output
        if not output_dir:
            return  # Stop if no directory is selected

        midi_output_file = os.path.join(output_dir, 'sonification.mid')
        
        # Perform the sonification using the provided function
        midi_data = convert_to_midi(
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
            upper_limit=upper_limit
        )
        
        total_duration = sum([note.end for note in midi_data.instruments[0].notes]) - sum([note.start for note in midi_data.instruments[0].notes])
        
        # Update the status label with the result
        status_label.configure(text=f"Sonification complete. Total duration: {total_duration} seconds. File saved to {midi_output_file}")
    else:
        # Update the status label to prompt the user to load data
        status_label.configure(text="Please load data to process.")



# Top section for file loading
load_button = ctk.CTkButton(app, text="Load CSV", command=load_file)
load_button.pack(side="top", padx=10, pady=20)

file_path_label = ctk.CTkLabel(app, text="No file loaded")
file_path_label.pack(side="top", padx=10, pady=10)

# Middle section for user inputs with more structured frames
middle_frame = ctk.CTkFrame(app)
middle_frame.pack(side="top", fill="x", padx=20, pady=20)

# Frame for the note mapping controls
note_frame = ctk.CTkFrame(middle_frame)
note_frame.pack(side="left", padx=10, fill="both", expand=True)
note_heading = ctk.CTkLabel(note_frame, text="Note Mapping", font=("Arial", 12))
note_heading.pack(pady=5)
note_combobox = ctk.CTkComboBox(note_frame, values=["Select a column"])
note_combobox.pack(padx=10, pady=10)
inverse_note_checkbox = ctk.CTkCheckBox(note_frame, text="Inverse Note Mapping")
inverse_note_checkbox.pack(padx=10)

# Frame for the velocity mapping controls
velocity_frame = ctk.CTkFrame(middle_frame)
velocity_frame.pack(side="left", padx=10, fill="both", expand=True)
velocity_heading = ctk.CTkLabel(velocity_frame, text="Velocity Mapping", font=("Arial", 12))
velocity_heading.pack(pady=5)
velocity_combobox = ctk.CTkComboBox(velocity_frame, values=["Select a column"])
velocity_combobox.pack(padx=10, pady=10)
inverse_velocity_checkbox = ctk.CTkCheckBox(velocity_frame, text="Inverse Velocity Mapping")
inverse_velocity_checkbox.pack(padx=10)

# Frame for the duration mapping controls
duration_frame = ctk.CTkFrame(middle_frame)
duration_frame.pack(side="left", padx=10, fill="both", expand=True)
duration_heading = ctk.CTkLabel(duration_frame, text="Duration Mapping", font=("Arial", 12))
duration_heading.pack(pady=5)
duration_combobox = ctk.CTkComboBox(duration_frame, values=["Select a column"])
duration_combobox.pack(padx=10, pady=10)
inverse_duration_checkbox = ctk.CTkCheckBox(duration_frame, text="Inverse Duration Mapping")
inverse_duration_checkbox.pack(padx=10) 


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

# Middle section for user inputs with more structured frames
middle_frame = ctk.CTkFrame(app)
middle_frame.pack(side="top", fill="x", padx=20, pady=20)


status_label = ctk.CTkLabel(app, text="")
status_label.pack(side="bottom", fill="x", padx=10, pady=10)  # Adjust the position as needed


# Place the "Run Sonification" button in the middle beneath the existing options
run_button_frame = ctk.CTkFrame(middle_frame)
run_button_frame.pack(side="top", fill="x", padx=20, pady=10)
run_button = ctk.CTkButton(run_button_frame, text="Run Sonification", command=run_sonification)
run_button.pack(pady=20)


app.mainloop()





