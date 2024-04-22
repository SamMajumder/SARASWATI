# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 21:30:55 2024

@author: Dr. M
"""

import streamlit as st

def about_page():
    st.title('About This App')
    
    st.write("""
    ## What is this app?
    This app is designed to compare music playlists and individual tracks using advanced data analytics and visualization techniques. It leverages Spotify's API to fetch data and uses UMAP for dimensional reduction to visually compare song characteristics.

    ## Who built this app?
    This app was developed by [Your Name], a passionate data scientist with a keen interest in music technology and machine learning. 

    ## How to use this app?
    - **Compare Playlist**: Navigate to the 'Compare Playlist' page to analyze a Spotify playlist against a track of your choice.
    - **Compare Genre**: Go to the 'Compare Genre' page to explore songs within a specific genre and compare their features.

    ## Source Code
    Interested in the source code? Visit our [GitHub repository](https://github.com/your-github-repo).

    ## Contact Information
    For more information, suggestions, or potential collaborations, feel free to contact us at [your.email@example.com](mailto:your.email@example.com).

    ## Acknowledgements
    Special thanks to everyone who contributed to the development of this project, including advisors, friends, and the open-source community.
    """)


