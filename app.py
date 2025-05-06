from gtts import gTTS
import streamlit as st

st.title("Speechii - Text to Speech App")

# Get user input
text = st.text_area("Enter text to convert to speech:")

# Language (en for English)
language = 'en'

if st.button("Convert to Speech"):
    if text:
        # Create gTTS object
        tts = gTTS(text=text, lang=language, slow=False)

        # Save audio
        tts.save("output.mp3")

        # Play audio in Streamlit
        audio_file = open("output.mp3", "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
    else:
        st.warning("Please enter some text first.")
