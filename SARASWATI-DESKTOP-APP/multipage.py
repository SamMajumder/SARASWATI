# -*- coding: utf-8 -*-
"""
Created on Sun May  5 09:21:08 2024

@author: Dr. M 
"""


import tkinter as tk
import customtkinter as ctk  # Make sure to import this
from tkinter import PhotoImage
from title_page import *
from about_page import *
from main_page import *

def main():
    root = tk.Tk()
    root.title('S.A.R.A.S.W.A.T.I')
    root.geometry('1200x800')

    # Set CustomTkinter to use dark mode globally
    ctk.set_appearance_mode("dark")  # This will affect only CustomTkinter widgets

    container = tk.Frame(root, bg='black')  # Set container background to black for dark mode
    container.pack(side="top", fill="both", expand=True)

    frames = {}

    for F in (create_title_page, create_about_page, create_main_page):
        page_name = F.__name__
        frame = F(container)
        frames[page_name] = frame
        frame.pack(fill="both", expand=True)
        frame.pack_forget()

    def show_frame(page_name):
        # Forget all frames first to ensure only one is visible at a time
        for f in frames.values():
            f.pack_forget()
        # Show the requested frame
        frame = frames[page_name]
        frame.pack(fill="both", expand=True)
        print(f"Showing {page_name}")  # Debugging line to see what's happening

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    page_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Pages", menu=page_menu)
    page_menu.add_command(label="Title Page", command=lambda: show_frame("create_title_page"))
    page_menu.add_command(label="About Page", command=lambda: show_frame("create_about_page"))
    page_menu.add_command(label="Main Page", command=lambda: show_frame("create_main_page"))

    show_frame("create_title_page")  # Start with the title page visible

    root.mainloop()

if __name__ == "__main__":
    main()