# S.A.R.A.S.W.A.T.I. :

<p align="center">
  <img src="https://raw.githubusercontent.com/SamMajumder/SARASWATI/main/SARASWATI.webp" alt="Concept Image">
  <br>
  Created using DALL-E by OpenAI
</p>

## Introduction
**S**onification **A**pplication for **R**esearch and **A**udio **S**ynthesis with **W**aveform **A**udio **T**ransformation **I**ntegration (S.A.R.A.S.W.A.T.I.) is a comprehensive suite of tools designed to transform data into sound and music through sophisticated sonification techniques. It consists of various components that cater to different needs, from standalone applications to interactive web apps, enhancing both research and creative exploration.

## Background
Named after Saraswati, the Hindu goddess of knowledge, music, art, wisdom, and learning, the SARASWATI project embodies the fusion of data science and musical artistry. The goddess Saraswati is traditionally depicted with a veena, representing the harmony of data with auditory aesthetics through sonification. This name reflects the project's goal to enable a deeper understanding and appreciation of data through the medium of sound.

## Components
### SARASWATI-basecode
Contains the base Python scripts for both SARASWATI and SARASWATI-AI applications. These scripts are the backbone of the project, providing core functionality for data processing, sonification, and AI-driven music synthesis.

### SARASWATI-standalone
This directory includes the code necessary to run SARASWATI as a standalone executable GUI application, ideal for users who prefer a desktop application without the need to setup a web environment.

### SARASWATI-AI-standalone
Similar to SARASWATI-standalone, this contains all required scripts to compile a standalone executable for the SARASWATI AI-enhanced version, offering advanced features like AI-driven data interpretation and music generation.

### SARASWATI-Streamlit
Hosts the Streamlit-based web application, which is split into three main pages:
- **About**: Provides detailed information about SARASWATI and its capabilities.
- **SARASWATI**: Allows users to interact with the standard sonification tools via a web interface.
- **SARASWATI-AI**: Integrates AI functionalities for a more advanced sonification and music synthesis experience.

Check out the app here: [SARASWATI Streamlit App](https://saraswati-ai.streamlit.app/)

## Getting Started
Instructions for setting up and running the various components of SARASWATI. This section will include steps to install dependencies, as well as how to launch both the standalone and Streamlit applications.

## Usage
### SARASWATI-basecode
- **Data Upload**: Load your CSV files directly through the script prompts.
- **Parameter Adjustments**: Configure settings such as note mapping, velocity mapping, duration mapping, and musical scales.
- **Sonification**: Execute the script to convert data into MIDI files, which can be played back or further processed.

### SARASWATI-standalone and SARASWATI-AI-standalone
- **Installation**: Download the executable from the provided links and run it on your local machine.
- **Data Input**: Use the GUI to load your data files and set parameters via intuitive controls.
- **Running Sonification**: Process the data to generate sound directly from the application.
- **AI Features (SARASWATI-AI)**: Explore AI-enhanced sonification options for a more dynamic auditory representation of your data.

### SARASWATI-Streamlit
- **Web Access**: Access the application through any web browser by navigating to the hosted URL or running it locally via Streamlit.
- **Interactive GUI**: Interact with sliders, buttons, and fields to customize the sonification process.
- **Live Output**: Listen to the sonified output or download the generated music files for further use.


## Contact
For support, feedback, or inquiries, please reach out to the SARASWATI development team at [sambadimajumder@gmail.com](mailto:sambadimajumder@gmail.com). We are dedicated to improving the tool and fostering a vibrant community around data sonification.

## Acknowledgments

A big thanks to the developers of the Python packages that were used to create this tool. This work would not be possible without the hard work of these amazing Python developers.

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
