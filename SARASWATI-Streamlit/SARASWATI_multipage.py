# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 11:13:33 2024

@author: Dr. M
"""

import streamlit as st
from streamlit_option_menu import option_menu

### importing the pages 
from SARASWATI_streamlit import run_saraswati
from SARASWATI_AI_streamlit import run_saraswati_ai
from about_page import *


  
   
def main():
    st.title('SARASWATI')
    # Sidebar navigation
    #st.sidebar.title('Navigation')
    selected = option_menu("Menu", ["About", "SARASWATI", "SARASWATI-AI"],
                           icons=['info-circle', 'music-note-beamed', 'music-note-list'],
                           menu_icon="cast", default_index=0)

    if selected == "About":
        about_page()
    elif selected == "SARASWATI":
        run_saraswati()
    elif selected == "SARASWATI-AI":
        run_saraswati_ai()

if __name__ == "__main__":
    main()