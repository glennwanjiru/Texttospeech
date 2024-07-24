import streamlit as st
from gtts import gTTS
from pydub import AudioSegment
import os
import uuid
import tempfile
import io

# Define function to convert text to audio
def convert_to_audio(text, lang='en', slow=False):
    unique_filename = f"output_{uuid.uuid4().hex}.mp3"
    try:
        tts = gTTS(text=text, lang=lang, slow=slow)
        tts.save(unique_filename)
        return unique_filename
    except Exception as e:
        st.error(f"An error occurred while converting text to audio: {e}")
        return None

# Define function to save audio
def save_audio(audio_file, format='mp3'):
    try:
        # Create a temporary file to save the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{format}') as tmp_file:
            audio = AudioSegment.from_file(audio_file)
            audio.export(tmp_file.name, format=format)
            return tmp_file.name
    except Exception as e:
        st.error(f"An error occurred while saving the file: {e}")
        return None

# Streamlit app
st.title("Text to Audio Converter")

text = st.text_area("Enter text to convert to audio", height=150)
format_option = st.selectbox("Select audio format", ["mp3", "wav", "ogg"])

if st.button("Convert to Audio"):
    if text.strip():
        st.write("Converting text to audio...")
        audio_file = convert_to_audio(text)
        if audio_file:
            with open(audio_file, "rb") as f:
                audio_bytes = f.read()
            st.audio(audio_bytes, format='audio/mp3')
            st.session_state.audio_file = audio_file
            st.success(f"Audio saved as {audio_file}")
        else:
            st.error("Failed to convert text to audio.")
    else:
        st.warning("Please enter some text to convert.")

if 'audio_file' in st.session_state:
    audio_file = st.session_state.audio_file

    if st.button("Save Audio"):
        saved_path = save_audio(audio_file, format_option)
        if saved_path:
            st.success(f"Audio saved to {saved_path}")
        else:
            st.error("Failed to save audio.")

if st.button("Clear Text"):
    st.session_state.pop('audio_file', None)  # Clear the saved audio file from session state
    st.text_area("Enter text to convert to audio", value='', height=150)
    st.experimental_rerun()
