# -*- coding: utf-8 -*-
"""
Created on Fri May  3 18:40:55 2024

@author: Dr. M
"""


import os
import sys
import tkinter as tk
from tkinter import PhotoImage

def create_title_page(parent):
    frame = tk.Frame(parent, bg='black')
    frame.pack(fill='both', expand=True)

    title_label = tk.Label(frame, text="S.A.R.A.S.W.A.T.I.", font=("Arial", 24, "bold"), fg="white", bg="black")
    title_label.pack(pady=(20, 10))

    # Determine if running as a script or frozen executable
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the pyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app 
        # path into variable _MEIPASS'.
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    photo_path = os.path.join(application_path, "SARASWATI.png")
    frame.image = PhotoImage(file=photo_path)
    image_label = tk.Label(frame, image=frame.image, bg="black")
    image_label.pack(pady=(10, 20))

    return frame
