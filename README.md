# Texttospeech App

# Text to Audio Converter

## Overview

The **Text to Audio Converter** application allows users to convert text into audio files using the Google Text-to-Speech (gTTS) service. This application also supports playback controls, including play, pause, and stop, and allows users to save the generated audio in various formats.

## Features

- Convert text to audio with customizable speech rate and volume.
- Play, pause, and stop the generated audio.
- Save the audio file in MP3, WAV, or OGG formats.
- Clear the text area for new input.

## Requirements

To run this application, you'll need Python installed on your system along with several libraries. You can install the required libraries using `pip`. 

### Libraries

- `tkinter` (for GUI components)
- `gtts` (for text-to-speech conversion)
- `pydub` (for audio file handling)
- `pygame` (for audio playback)
- `ttkthemes` (for themed widgets)
- `uuid` (for generating unique filenames)
- `os` (for file operations)

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/glennwanjiru/Texttospeech
    ```

2. Navigate to the project directory:

    ```sh
    cd your-repository
    ```

3. Install the required Python packages:

    ```sh
    pip install gtts pydub pygame ttkthemes
    ```

4. **Optional**: Install `ffmpeg` for audio format support with `pydub`. Follow the installation instructions from [FFmpeg's official website](https://ffmpeg.org/download.html).

## Usage

1. Run the application:

    ```sh
    python text_to_audio_app.py
    ```

2. Enter the text you want to convert in the text area.

3. Adjust the speech rate and volume using the sliders.

4. Click **"Convert to Audio"** to generate the audio file.

5. Use the **"Play"** button to listen to the audio, **"Pause"** to pause, and **"Stop"** to stop playback.

6. Click **"Save Audio"** to save the audio file to your desired location and format.

7. Use **"Clear Text"** to empty the text area for new input.

## Troubleshooting

- **Audio Playback Issues**: Ensure `pygame` is correctly installed and that your system's audio is functioning.
- **File Saving Errors**: Check that the audio file exists before attempting to save and ensure you have write permissions to the chosen directory.



## Contributing

Feel free to fork the repository and submit pull requests. Any improvements, bug fixes, or feature additions are welcome!


