# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 21:30:55 2024

@author: Dr. M
"""

import streamlit as st

def about_page():
    st.title('About SARASWATI')
    
    st.image("https://raw.githubusercontent.com/SamMajumder/SARASWATI/main/SARASWATI.webp", caption='Created using DALL-E by OpenAI.')
    
    st.write("""
    ## What is SARASWATI?
    **S**onification **A**pplication for **R**esearch and **A**udio **S**ynthesis with **W**aveform **A**udio **T**ransformation **I**ntegration (S.A.R.A.S.W.A.T.I.) is a comprehensive suite of tools designed to convert complex data into sound and music. This application provides a user-friendly interface for users to explore data sonification, enabling a deeper understanding and appreciation of data through auditory forms. SARASWATI supports a range of applications from academic research to creative music production.

    ## Who built SARASWATI?
    SARASWATI was developed by Dr. Sambadi Majumder, a data scientist with interest in music technology and machine learning. Inspired by the capabilities of data to tell stories through music, this project aims to make data analytics and sonification accessible to both researchers and artists.

    ## How to use this app?

    ### SARASWATI
    - **Data Sonification**: Navigate to the 'SARASWATI' page to begin the process of sonification. Users can upload their data files in CSV format, select columns for different musical mappings (notes, velocity, and duration), and choose various musical scales and instruments for sonification.
    - **Sonification Settings**: Adjust parameters like tempo, scale, and instrument to customize the sonification. Users can toggle between different scales and instruments to explore various auditory interpretations of their data.
    - **Generate and Download**: After configuring the settings, users can generate the sonification, listen to the generated music, and download both the music file and a corresponding MIDI file.

    ### SARASWATI-AI
    - **Advanced Sonification with AI**: Access the 'SARASWATI-AI' page to employ advanced AI-driven features for sonification. This extension uses neural networks to enhance the sonification process, providing richer musical textures and complexity.
    - **Customize with AI**: Users can input descriptions or select presets that influence the AI's style and output, tailoring the sonification to fit specific moods or themes.
    - **Interact and Modify**: Interactively modify the AI parameters in real-time to hear how changes affect the sonification. This feature allows for immediate auditory feedback, ideal for fine-tuning the AI's output.
    - **Save and Share**: Once satisfied, users can save their customized AI-sonified music and share it directly from the app.

    ### General Usage
    - **Interactive Visualizations**: Both sections of the app include interactive visualizations that display the data and the sonification process, helping users visualize how their data is being transformed into music.
    - **Real-time Feedback**: Adjust settings and hear the changes in real-time, providing a dynamic way to experiment with data sonification and AI enhancements.
    - **Documentation and Help**: Access in-app documentation and tooltips that guide through each step of the process, from data upload to advanced AI customization.

    ## Source Code
    Interested in the source code? Visit our [GitHub repository](https://github.com/SamMajumder/SARASWATI).

    ## Contact Information
    For queries, suggestions, or collaborations, please drop an email [sambadimajumder@gmail.com](mailto:sambadimajumder@gmail.com).

    ## Acknowledgements
    
    ### Bibliography
    A big thanks to the developers of the packages used to create this tool. This work would not exist without these Python packages and models. 
    Thank you so much: 
    
    - **pandas & numpy**:
      - McKinney, W. (2010). Data Structures for Statistical Computing in Python. In *Proceedings of the 9th Python in Science Conference*.
      - Harris, C. R., Millman, K. J., van der Walt, S. J., et al. (2020). Array programming with NumPy. *Nature*, 585(7825), 357–362. https://doi.org/10.1038/s41586-020-2649-2

    - **pretty_midi**:
      - Colin Raffel and Daniel P. W. Ellis. (2014). Intuitive Analysis, Creation and Manipulation of MIDI Data with pretty_midi. In *Late-Breaking Demo Session of the 15th International Society for Music Information Retrieval Conference*.

    - **music21**:
      - Cuthbert, M. S., & Ariza, C. (2010). music21: A Toolkit for Computer-Aided Musicology and Symbolic Music Data. In *Proceedings of the 11th International Society for Music Information Retrieval Conference*.

    - **PyTorch & torchaudio**:
      - Paszke, A., Gross, S., Massa, F., et al. (2019). PyTorch: An Imperative Style, High-Performance Deep Learning Library. In *Advances in Neural Information Processing Systems 32*.
      - Vincent, J., & Bittner, R. M. (2021). torchaudio: Building Blocks for Audio and Speech Processing. *GitHub repository*. https://github.com/pytorch/audio

    - **TensorFlow**:
      - Abadi, M., Agarwal, A., Barham, P., et al. (2016). TensorFlow: Large-Scale Machine Learning on Heterogeneous Distributed Systems. *arXiv preprint arXiv:1603.04467*. https://www.tensorflow.org/

    - **audiocraft & MusicGen**:
      - Copet, J., Kreuk, F., Gat, I., Remez, T., Kant, D., Synnaeve, G., Adi, Y., & Défossez, A. (2023). Simple and Controllable Music Generation. In *Proceedings of the Thirty-seventh Conference on Neural Information Processing Systems*.


    """)



    



    


