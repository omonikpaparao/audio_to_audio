import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import tempfile
from googletrans import Translator

# Function to translate text
def translate_text(text, target_language):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text

# Function to transcribe audio to text
def transcribe_audio(audio_file, language):
    recognizer = sr.Recognizer()
    
    # Use the audio file for transcription
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        
        try:
            # Transcribe the audio using Google Speech Recognition with the user-specified language
            transcribed_text = recognizer.recognize_google(audio_data, language=language)
            return transcribed_text
        except sr.UnknownValueError:
            return "Sorry, the audio could not be understood."
        except sr.RequestError as e:
            return f"Could not request results; {e}"

# Function to convert text to speech
def text_to_speech(text, language='en'):
    # Initialize gTTS object
    tts = gTTS(text=text, lang=language, slow=False)
    
    # Save the speech to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        tts.save(temp_file.name)
        return temp_file.name

# Streamlit UI
st.title("Translate the Audio File to another language Audio File")

# File uploader to upload the .wav audio file
uploaded_file = st.file_uploader("Upload a .wav file", type=["wav"])

if uploaded_file is not None:
    # Displaying the uploaded audio file
    st.audio(uploaded_file, format='audio/wav')

    # User provides the language for transcription
    language_option = st.selectbox("Select the language of the audio", 
                                  ["en", "te", "hi", "ta", "kn", "ml", "kn", "mr", "or", "kok", "bn", "sa", "ur", "gu", "pa", "as", "ks"])

    # Button to trigger transcription
    if st.button("Transcribe Audio"):
        # Step 1: Transcribe the audio to text in the provided language (ASR)
        transcribed_text = transcribe_audio(uploaded_file, language_option)
        
        if transcribed_text:
            st.subheader("Text for the given Audio File:")
            st.write(transcribed_text)
            input_text = transcribed_text

            # Step 2: Translate the transcribed text
            languages = ["en", "te", "hi", "ta", "kn", "ml", "kn", "mr", "or", "kok", "bn", "sa", "ur", "gu", "pa", "as", "ks"]
            target_language = st.selectbox("Select target language to translate the audio text", languages)

            # Step 3: Translate the transcribed text when button is clicked (NMT)
            if st.button("Translate and Convert to Speech"):
                if input_text:
                    translated_text = translate_text(input_text, target_language)
                    #st.subheader("Translated Text:")
                    #st.write(translated_text)

                    # Convert the translated text to speech (TTS)
                    audio_file = text_to_speech(translated_text, target_language)
                    
                    # Play the audio file
                    st.audio(audio_file, format='audio/mp3')
                else:
                    st.warning("Something went wrong with the translation process.")
