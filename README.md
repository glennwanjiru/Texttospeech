# Texttospeech App
This application allows you to convert text to audio files (MP3, WAV, OGG) with customizable settings like speech rate, volume, and format. It provides a user-friendly interface for easy text input, format selection, playback controls, and saving options.

Features:
Convert text to speech using Google Text-to-Speech (gTTS).
Choose the output format (MP3, WAV, OGG).
Adjust speech rate, volume, and pitch (limited functionality with gTTS).
Play, pause, and stop audio playback.
Save the generated audio file to your desired location.
Clear the text area for new conversions.
Installation:
Prerequisites:

Python 3.x (Download from https://www.python.org/downloads/)
Required libraries: tkinter, gtts, pydub, pygame, ttkthemes
Using pip:

Open a terminal or command prompt.
Make sure you have pip installed (usually comes with Python). You can check by running python -m pip --version
Install the required libraries using the following command:
Bash
pip install tkinter gtts pydub pygame ttkthemes
Use code with caution.

Running the application:
Open a terminal or command prompt and navigate to the directory where you saved this Python script (TextToAudioApp.py).
Run the script using the following command:
Bash
python TextToAudioApp.py
Use code with caution.

This will launch the Text to Audio Converter application with a graphical interface.

Using the application:
Enter Text: Type the text you want to convert to audio in the large text area provided.
Select Format: Choose your desired output format (MP3, WAV, OGG) from the dropdown menu.
Adjust Settings (Optional):
You can adjust the speech rate using the slider under "Speech Rate".
The volume can be controlled using the slider under "Volume". (Note: Pitch adjustment has limited functionality with gTTS).
Convert to Audio: Click the "Convert to Audio" button. The progress bar will indicate the conversion process.
Playback and Saving:
Once the conversion is complete, the playback controls (Play, Pause, Stop) and "Save Audio" button will become enabled.
Use the playback controls to listen to the generated audio.
Click "Save Audio" to choose a location and filename to save the audio file.
