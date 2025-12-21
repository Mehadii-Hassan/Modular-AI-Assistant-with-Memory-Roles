import streamlit as st
import time
import pyttsx3
import speech_recognition as sr
import threading

from config.settings import Settings
from mehu.gemini_engine import GeminiEngine
from mehu.prompt_controller import PromptController
from mehu.memory import Memory
from mehu.assistant import MehuAssistant


st.set_page_config(page_title="MEHU AI", layout="centered")
st.title("🧠 MEHU – Your AI Assistant")

# -------------------- SIDEBAR --------------------
role = st.sidebar.selectbox(
    "Select Role",
    ["Assistant", "Tutor", "Coding Assistant", "Career Mentor"]
)

if st.sidebar.button("🗑 Clear Memory"):
    Memory().clear()
    st.session_state.messages = []
    st.success("Memory Cleared")

# -------------------- INIT CORE --------------------
settings = Settings()
engine = GeminiEngine(settings.load_api_key())
memory = Memory()
prompt_controller = PromptController()
mehu = MehuAssistant(engine, prompt_controller, memory)

# -------------------- SESSION STATE --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------- TTS ENGINE --------------------
tts_engine = pyttsx3.init("sapi5")
tts_engine.setProperty("rate", 160)
voices = tts_engine.getProperty("voices")
tts_engine.setProperty("voice", voices[1].id)

def speak(text):
    """Speak text asynchronously"""
    def run_speech():
        tts_engine.say(text)
        tts_engine.runAndWait()
    threading.Thread(target=run_speech, daemon=True).start()

# -------------------- VOICE INPUT --------------------
def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language="en-in")
        return query
    except:
        st.error("Could not recognize voice")
        return ""

# -------------------- RENDER PREVIOUS MESSAGES --------------------
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# -------------------- INPUT SELECTION --------------------
input_type = st.radio("Input Type", ["Text", "Voice"])

user_input = ""
if input_type == "Text":
    user_input = st.chat_input("Ask MEHU...")
elif input_type == "Voice":
    if st.button("🎤 Speak Now"):
        user_input = get_voice_input()

# -------------------- PROCESS INPUT --------------------
if user_input:
    # Show user message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Assistant placeholder
    assistant_placeholder = st.chat_message("assistant").empty()
    assistant_placeholder.markdown("⌛ MEHU is thinking...")

    # Generate response
    if input_type == "Text":
        # Streaming word-by-word
        streamed_text = ""
        for token in mehu.respond_stream(user_input, role):
            streamed_text += token
            assistant_placeholder.markdown(streamed_text)
            time.sleep(0.03)  # adjust typing speed
        response = streamed_text
    else:  # Voice input
        # Short response for voice
        response = mehu.respond_short(user_input, role)
        assistant_placeholder.markdown(response)
        speak(response)  # speak only for voice input

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})
