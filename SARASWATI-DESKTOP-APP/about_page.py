# -*- coding: utf-8 -*-
"""
Created on Sat May  4 14:26:16 2024

@author: Dr. M
"""

import tkinter as tk
from tkinter import scrolledtext

def create_about_page(parent):
    # Create a frame instead of a new window
    frame = tk.Frame(parent, bg='black')

    # Create a label for the about page title
    about_title = tk.Label(frame, text="About S.A.R.A.S.W.A.T.I", font=("Arial", 18, "bold"), fg="white", bg="black")
    about_title.pack(pady=(10, 10))

    # Create a scrolled text widget for the about content
    about_text = scrolledtext.ScrolledText(frame, width=100, height=30, bg='black', fg='white', font=("Arial", 12), wrap=tk.WORD)
    about_text.pack(padx=20, pady=(10, 20))

    # About content
    content = """
    **S**onification **A**pplication for **R**esearch and **A**udio **S**ynthesis with **W**aveform **A**udio **T**ransformation **I**ntegration (S.A.R.A.S.W.A.T.I.) is a comprehensive suite of tools designed to convert complex data into sound and music. This application provides a user-friendly interface for users to explore data sonification, enabling a deeper understanding and appreciation of data through auditory forms. SARASWATI supports a range of applications from academic research to creative music production.
    ...
    """
    # Insert content into the scrolled text widget and disable editing
    about_text.insert(tk.INSERT, content)
    about_text.config(state='disabled')

    return frame
