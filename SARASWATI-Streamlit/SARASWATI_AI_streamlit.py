# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 11:11:42 2024

@author: Dr. M
"""

from utils import *
import streamlit as st
import zipfile
from io import BytesIO

def run_saraswati_ai():
    st.title('SARASWATI AI')

    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Uploaded Data:")
        st.dataframe(df)

        note_column = st.selectbox("Select column for note mapping:", df.columns)
        velocity_column = st.selectbox("Select column for velocity mapping:", df.columns)
        duration_column = st.selectbox("Select column for duration mapping:", df.columns)
        reverse_note_mapping = st.checkbox("Inverse note mapping?")
        reverse_velocity_mapping = st.checkbox("Inverse velocity mapping?")
        reverse_duration_mapping = st.checkbox("Inverse duration mapping?")
        scale_name = st.selectbox("Select scale", list(scales.keys()))
        instrument_names = [pretty_midi.program_to_instrument_name(i) for i in range(128)]
        instrument_name = st.selectbox("Select instrument", instrument_names)
        tempo = st.number_input("Enter the tempo (e.g., 120)", min_value=60, max_value=240, value=120)
        lower_limit = st.number_input("Enter the lower limit for note duration (e.g., 0.1)")
        upper_limit = st.number_input("Enter the upper limit for note duration (e.g., 4)")
        initial_duration = st.number_input("Enter the duration for the initial music track (in seconds)")
        user_prompt = st.text_input("Enter your prompt for style customization (e.g., 'violin music in the style of Vivaldi')")

        extend_music = st.checkbox("Extend this music further?")
        if extend_music:
            extension_duration = st.number_input("Enter additional duration for the music (in seconds):", min_value=1, step=1, value=10)
            prompt_duration = st.number_input("Enter the duration of the existing music to use as a prompt (in seconds):", min_value=1, step=1, value=5)

        if st.button("Generate Music"):
            output_dir = './output'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            midi_output_file = os.path.join(output_dir, 'sonification.mid')

            # MIDI conversion and initial music generation logic here
            midi_data, scale_factor, csv_output_path = convert_to_midi_with_max_durartion(
                df[note_column],
                midi_output_file,
                df[velocity_column],
                df[duration_column],
                scale_name,
                instrument_name,
                tempo,
                reverse_note_mapping,
                reverse_velocity_mapping,
                reverse_duration_mapping,
                lower_limit,
                upper_limit,
                initial_duration
            )

            description = f"{user_prompt}. Use the following notes, start times, end times, and durations for the composition: {midi_to_text(midi_data)}"
            initial_music_tensor = generate_music(description, initial_duration, midi_output_file.replace('.mid', '.wav'))
            st.success("Initial music generation completed!")

            if extend_music:
                # Music extension logic here
                continued_music_tensor = continue_music(initial_music_tensor, extension_duration, prompt_duration)
                continued_output_path = os.path.join(output_dir, 'extended_music.wav')
                save_audio(continued_music_tensor, 32000, continued_output_path)
                st.success("Extended music generated and available for download.")

                with open(continued_output_path, "rb") as fp:
                    st.download_button("Download Extended Music", fp, "extended_music.wav", "audio/wav")

                # Zip file creation logic for downloading the entire package
                zip_file_path = os.path.join(output_dir, 'sonification_package.zip')
                with zipfile.ZipFile(zip_file_path, 'w') as zf:
                    zf.write(midi_output_file, arcname='sonification.mid')
                    zf.write(csv_output_path, arcname='sonification_mapping.csv')
                    zf.write(midi_output_file.replace('.mid', '.wav'), arcname='initial_music.wav')
                    zf.write(continued_output_path, arcname='extended_music.wav')

                with open(zip_file_path, "rb") as fp:
                    st.download_button("Download Sonification Package", fp, "sonification_package.zip", "application/zip")

