# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 11:10:41 2024

@author: Dr. M
"""

from utils import *
import streamlit as st
import zipfile
from io import BytesIO

def run_saraswati():
    st.title('SARASWATI: Data Sonification Tool')
    uploaded_file = st.file_uploader("Choose a CSV file", type='csv')
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Uploaded Data:")
        st.dataframe(df)  # Display the uploaded CSV data

        note_column = st.selectbox("Select column for note mapping:", df.columns)
        velocity_column = st.selectbox("Select column for velocity mapping:", df.columns)
        duration_column = st.selectbox("Select column for duration mapping:", df.columns)

        reverse_note_mapping = st.checkbox("Inverse note mapping?")
        reverse_velocity_mapping = st.checkbox("Inverse velocity mapping?")
        reverse_duration_mapping = st.checkbox("Inverse duration mapping?")

        scale_name = st.selectbox("Select scale", list(scales.keys()))
        instrument_names = [pretty_midi.program_to_instrument_name(i) for i in range(128)]
        instrument_name = st.selectbox("Select instrument", instrument_names)
        tempo = st.number_input("Enter the tempo (e.g., 120)", min_value=60, max_value=240, value=120, step=1)
        lower_limit = st.number_input("Enter the lower limit for note duration (e.g., 0.1)")
        upper_limit = st.number_input("Enter the upper limit for note duration (e.g., 4)")

        if st.button("Sonify Data"):
            output_dir = './output'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            midi_output_file = os.path.join(output_dir, 'sonification.mid')

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

            st.success("Sonification completed successfully!")
            zip_file_path = os.path.join(output_dir, 'sonification_package.zip')
            with zipfile.ZipFile(zip_file_path, 'w') as zf:
                zf.write(midi_output_file, arcname='sonification.mid')
                zf.write(midi_output_file.replace('.mid', '_mapping.csv'), arcname='sonification_mapping.csv')

            with open(zip_file_path, "rb") as fp:
                btn = st.download_button(
                    label="Download Sonification Package",
                    data=fp,
                    file_name='sonification_package.zip',
                    mime="application/zip"
                )

    
