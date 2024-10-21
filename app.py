import streamlit as st
import requests
from PyPDF2 import PdfReader
import io
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import google.generativeai as genai
import base64
import datetime
import os
from pydub import AudioSegment
from pydub.playback import play

# Replace with your actual Gemini API key
GEMINI_API_KEY = "ENTER YOUR GEMINI KEY"

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

LANGUAGE_OPTIONS = {
    "Hindi": "hi",
    "Kannada": "kn",
    "Telugu": "te",
    "Tamil": "ta",
    "Malayalam": "ml",
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh-CN",
    "Japanese": "ja",
    "Russian": "ru"
}

COMPLEXITY_LEVELS = {
    "Easy": "Use simple words and avoid technical jargon.",
    "Medium": "Use a mix of simple and technical terms, explaining any complex concepts.",
    "Expert": "Use full technical terminology and in-depth explanations."
}

VOICE_OPTIONS = {
    "Female": "female",
    "Male": "male"
}

def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(io.BytesIO(pdf_file.read()))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_gemini_response(input_text, pdf_text="", complexity_level="Medium"):
    prompt = f"""
    You are an AI assistant specializing in technical troubleshooting for tools and machines. 
    Use the following information from the uploaded documentation (if any) to help answer the user's query:

    {pdf_text}

    User Query: {input_text}

    Complexity Level: {COMPLEXITY_LEVELS[complexity_level]}

    Provide a clear and concise response to help troubleshoot the issue, adhering to the specified complexity level.
    """

    model = genai.GenerativeModel('gemini-pro')

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error communicating with Gemini API: {e}")
        return None

def recognize_speech(language_code):
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening... Speak something.")
            audio = recognizer.listen(source, timeout=5)

        try:
            text = recognizer.recognize_google(audio, language=language_code)
            st.success(f"Recognized Speech: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"Could not request results; {e}")
    except AttributeError:
        st.error("PyAudio is not installed. Voice input is unavailable.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

    return None

def translate_text(input_text, target_language_code='en'):
    try:
        translation = GoogleTranslator(source='auto', target=target_language_code).translate(input_text)
        return translation
    except Exception as e:
        st.error(f"Translation error: {e}")
        return None

def text_to_speech(text, language_code='en', voice='female'):
    try:
        tts = gTTS(text=text, lang=language_code, tld='com')
        audio_file = f"translated_audio_{voice}.mp3"
        tts.save(audio_file)
        return audio_file
    except Exception as e:
        st.error(f"Text-to-Speech error: {e}")
        return None

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}" class="btn btn-primary">Download {file_label}</a>'
    return href

def save_uploaded_file(uploaded_file):
    if not os.path.exists("uploaded_files"):
        os.makedirs("uploaded_files")
    file_path = os.path.join("uploaded_files", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def main():
    st.set_page_config(page_title="Velosis AI", page_icon="🤖🌍", layout="wide")

    # Updated Custom CSS
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap');
    
    * {
        font-family: 'Playfair Display', serif !important;
    }
    .stApp {
        background-color: #282c34;
        color: #c7cfd9;
    }
    .stSidebar {
        background-color: #21252b;
    }
    .stButton>button {
        width: 100%;
        background-color: #5c6370;
        color: #c7cfd9;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #6f7886;
    }
    .stTextInput>div>div>input {
        background-color: #3a3f4b;
        color: #c7cfd9;
        border: none;
        border-radius: 4px;
    }
    .centered-header {
        text-align: center;
        font-size: 3rem;
        margin-top: 2rem;
        margin-bottom: 2rem;
        color: #c7cfd9;
    }
    .login-box {
        background-color: #21252b;
        padding: 2rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        width: 300px;
        margin: 0 auto;
    }
    .login-box input {
        width: 100%;
        margin-bottom: 1rem;
        padding: 0.5rem;
        font-size: 0.9rem;
    }
    .login-box button {
        width: 100%;
        padding: 0.5rem;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Initialize language_code with a default value
    language_code = LANGUAGE_OPTIONS["English"]

    if not st.session_state.logged_in:
        st.markdown('<h1 class="centered-header">Velosis AI</h1>', unsafe_allow_html=True)
        with st.container():
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                username = st.text_input("Username", key="username")
                password = st.text_input("Password", type="password", key="password")
                if st.button("Login", key="login_button"):
                    if username == "admin" and password == "admin":
                        st.session_state.logged_in = True
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password. Please try again.")
    else:
        # Sidebar
        with st.sidebar:
            st.title("Menu")
            selected_tab = st.radio("Navigation", ["Chatbot", "Uploaded Files", "Chat History"])
            if st.button("Log out"):
                st.session_state.logged_in = False
                st.warning("You have been logged out. Please refresh the page.")
                st.rerun()

        if selected_tab == "Chatbot":
            # Centered and enlarged "How may I assist you..." header
            st.markdown('<div class="centered-header">How may I assist you...</div>', unsafe_allow_html=True)

            # Chat interface
            chat_container = st.container()

            with chat_container:
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

            # Input area
            user_input = st.text_input("Type your question here...", key="user_input")
            col1, col2, col3 = st.columns([6, 1, 1])
            with col2:
                search_button = st.button("🔍")
            with col3:
                voice_input = st.button("🎤")

            # PDF upload
            uploaded_file = st.file_uploader("Upload Documentation (PDF)", type="pdf")
            if uploaded_file:
                pdf_text = extract_text_from_pdf(uploaded_file)
                st.success("Documentation uploaded successfully!")
                file_path = save_uploaded_file(uploaded_file)
                st.session_state.uploaded_files.append((uploaded_file.name, datetime.datetime.now(), file_path))
            else:
                pdf_text = ""

            # Language and settings box
            with st.expander("Language and Settings"):
                user_language_name = st.selectbox(
                    "Select your language",
                    list(LANGUAGE_OPTIONS.keys())
                )
                # Update language_code based on user selection
                language_code = LANGUAGE_OPTIONS[user_language_name]
                
                complexity_level = st.select_slider(
                    "Select output complexity",
                    options=["Easy", "Medium", "Expert"]
                )

                voice_gender = st.radio("Select voice for text-to-speech", ["Female", "Male"], index=0)

            if search_button and user_input:
                st.session_state.messages.append({"role": "user", "content": user_input})

                # Recognize speech input
                translated_query = translate_text(user_input, 'en')
                response = get_gemini_response(translated_query, pdf_text, complexity_level)
                
                st.session_state.messages.append({"role": "bot", "content": response})

                translated_response = translate_text(response, language_code)
                st.chat_message("bot").markdown(translated_response)

                st.text("Playing generated speech...")
                audio_file = text_to_speech(translated_response, language_code, voice_gender)
                if audio_file:
                    audio_bytes = open(audio_file, 'rb').read()
                    st.audio(audio_bytes, format='audio/mp3')
                    st.markdown(get_binary_file_downloader_html(audio_file, "response_audio"), unsafe_allow_html=True)

            if voice_input:
                recognized_text = recognize_speech(language_code)
                if recognized_text:
                    st.session_state.messages.append({"role": "user", "content": recognized_text})
                    translated_query = translate_text(recognized_text, 'en')
                    response = get_gemini_response(translated_query, pdf_text, complexity_level)
                    
                    st.session_state.messages.append({"role": "bot", "content": response})
                    translated_response = translate_text(response, language_code)
                    st.chat_message("bot").markdown(translated_response)

                    st.text("Playing generated speech...")
                    audio_file = text_to_speech(translated_response, language_code, voice_gender)
                    if audio_file:
                        audio_bytes = open(audio_file, 'rb').read()
                        st.audio(audio_bytes, format='audio/mp3')
                        st.markdown(get_binary_file_downloader_html(audio_file, "response_audio"), unsafe_allow_html=True)

        elif selected_tab == "Uploaded Files":
            st.title("Uploaded Files")
            if len(st.session_state.uploaded_files) > 0:
                for idx, (file_name, upload_time, file_path) in enumerate(st.session_state.uploaded_files):
                    st.write(f"{idx + 1}. {file_name} (Uploaded on: {upload_time})")
                    st.markdown(get_binary_file_downloader_html(file_path, file_name), unsafe_allow_html=True)
            else:
                st.write("No files uploaded yet.")
        
        elif selected_tab == "Chat History":
            st.title("Chat History")
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

if __name__ == "__main__":
    main()