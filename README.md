# EDGE TTS GUI

EDGE TTS GUI is a graphical user interface (GUI) application built with [CustomTkinter](https://github.com/tomschimansky/customtkinter) that utilizes the `edge-tts` library to convert text to speech using Microsoft's online text-to-speech service. This application allows users to input text, select a voice, and adjust speech parameters such as rate, pitch, and volume. It also provides options to preview the generated speech and save it as an audio file.

## Features

- **Voice Selection:** Choose from a wide range of available voices.
- **Adjustable Parameters:** Customize the rate, pitch, and volume of the speech.
- **Preview:** Listen to the generated speech before saving.
- **Save Options:** Save the generated speech with different naming conventions.
- **Internet Connectivity Check:** Ensures that the application is connected to the internet before performing any text-to-speech operations.

## Installation

#### Method 1:

1. **Download the Standalone Executable:**
    - Go to the [Releases](https://github.com/schr-0dinger/edge_tts_gui/releases) page.
    - Download the latest version of `edge_tts_gui.exe`.

2. **Run the Application:**
    - Double-click the downloaded `edge_tts_gui.exe` file to start the application.


#### Method 2:

###### Prerequisites:

- Python 3.x
- Dependencies

0. Install dependencies:

        pip install edge-tts CTkMessageBox customtkinter pydub
    

1. ** Clone the repo **

        git clone https://github.com/schr-0dinger/edge_tts_gui.git

2. ** Run edge_tts_gui.py ** 

        python edge_tts_gui.py
    

## Usage

1. **Interface Overview:**
    - **Text Input:** Enter the text you want to convert to speech.
    - **Voice Selection:** Select a voice from the dropdown menu.
    - **Adjust Parameters:** Use the sliders to adjust rate, pitch, and volume.
    - **Generate:** Click the "GENERATE" button to save the speech as an audio file.
    - **Preview:** Click the "PREVIEW" button to listen to the speech before saving.
    - **Save Options:** Choose how you want to name the output file.

## To-do List

- ~~ Add option to switch between MP3/WAV format ~~
- Fix faulty preview function
- Fix 0-100 volume slider

## Dependencies

All necessary dependencies are bundled within the standalone executable, so you don't need to install anything else if you using the executable.

## Project Description

This project is essentially a GUI version of the `edge-tts` library, which allows users to use Microsoft Edge's online text-to-speech service from Python WITHOUT needing Microsoft Edge, Windows, or an API key.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.
      
## Acknowledgements

Special thanks to the developers of the `edge-tts` library for making this project possible.

