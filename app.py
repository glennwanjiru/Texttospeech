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

# Define function to save audio to a downloadable format
def save_audio(audio_file, format='mp3'):
    try:
        audio = AudioSegment.from_file(audio_file)
        with io.BytesIO() as audio_buffer:
            audio.export(audio_buffer, format=format)
            audio_buffer.seek(0)
            return audio_buffer.read()
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
            st.success(f"Audio generated. You can now save it.")
        else:
            st.error("Failed to convert text to audio.")
    else:
        st.warning("Please enter some text to convert.")

if 'audio_file' in st.session_state:
    audio_file = st.session_state.audio_file

    if st.button("Save Audio"):
        audio_bytes = save_audio(audio_file, format_option)
        if audio_bytes:
            st.download_button(
                label="Download audio file",
                data=audio_bytes,
                file_name=f"converted_audio.{format_option}",
                mime=f"audio/{format_option}"
            )
        else:
            st.error("Failed to save audio.")

if st.button("Clear Text"):
    st.session_state.pop('audio_file', None)  # Clear the saved audio file from session state
    st.experimental_rerun()
