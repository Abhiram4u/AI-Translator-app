import streamlit as st
import google.generativeai as genai
import tempfile
from gtts import gTTS
import tempfile
import os
API_KEY = os.getenv("API_KEY")  # for  Secure api keys
# this api key is securely deployed in streamlit community cloud, it will automaticaly inject key to the environment




if not API_KEY:
    st.error("API Key is missing. Please set it in your environment variables.")
else:
    genai.configure(api_key=API_KEY)


st.set_page_config(page_title="AI Translator", layout="wide")
st.markdown("<h1 style='text-align: center;'>AI Translator</h1>", unsafe_allow_html=True)

st.info(
    "⚠️ **Note**: This translator might not always be 100% accurate. Sometimes, the translation may contain mistakes. If the translation seems off, please try re-translating. Thank you for understanding!"
)


languages = {
    "English": "English",
    "French": "French",
    "Spanish": "Spanish",
    "German": "German",
    "Hindi": "Hindi",
    "Chinese": "Chinese",
    "Japanese": "Japanese",
    "Russian": "Russian",
    "Telugu": "Telugu",
    "Tamil": "Tamil",
    "Malayalam": "Malayalam",
    "Kannada": "Kannada",
    "Marathi": "Marathi",
    "Bengali": "Bengali",
    "Urdu": "Urdu",
    "Italian": "Italian",
    "Portuguese": "Portuguese",
    "Korean": "Korean",
    "Arabic": "Arabic",
    "Thai": "Thai"
}


col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Enter Text")
    text_input = st.text_area("Type or Paste text here:", height=150, placeholder="Hello! How are you?")
    target_language = st.selectbox("🌍 Choose Target Language:", list(languages.keys()))

    if st.button("Translate"):
        if text_input:
            with st.spinner("Translating... "):
               
                prompt = f"Translate this text to {target_language}. Input can be Romanized (typed in English letters) or in the original script. \n\nInput: {text_input}"
                model = genai.GenerativeModel("gemini-pro")
                response = model.generate_content(prompt)
                translated_text = response.text


                st.success(translated_text)

                #for Speech Output
                with st.spinner("Generating Audio 🎶"):
                    language_code = languages.get(target_language, None)
                    if language_code is None:
                        st.warning(f"Sorry, we don't support '{target_language}' for speech. Switching to English.")

                        language_code = "en"  # Default to English if the language is not found
                    #else:
                        #st.warning(" Please enter text to translate.")

                    try:
                        # Generate speech output using gTTS
                        tts = gTTS(translated_text, lang=language_code)
                        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                        tts.save(temp_audio.name)

                        # Play the audio in Streamlit
                        st.audio(temp_audio.name, format="audio/mp3")
                    except ValueError as e:
                        # If the ValueError occurs (invalid language), fallback to English with a simple message
                        #st.warning(f"Sorry, we couldn't generate speech for '{target_language}'. Using English instead.")
    
                        tts = gTTS(translated_text, lang="en")
                        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                        tts.save(temp_audio.name)

                        # Play the fallback audio
                        st.audio(temp_audio.name, format="audio/mp3")
                    except Exception as e:
                        # Catch any other unexpected errors and display a simple message
                        st.error("Something went wrong. Please try again.")

with col2:
    st.markdown("### Features")
    st.write("**Supports 20+ Languages**")
    st.write("**Instant Translation**")
    st.write("**Text-to-Speech Output** 🎤")
    
