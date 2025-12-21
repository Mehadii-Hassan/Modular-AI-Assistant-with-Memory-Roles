import streamlit as st
import threading
import time
import pyttsx3

from config.settings import Settings
from mehu.gemini_engine import GeminiEngine
from mehu.prompt_controller import PromptController
from mehu.memory import Memory
from mehu.assistant import MehuAssistant
from utils.voice_input import listen  # make sure you have a listen() function

# -------------------------
# Initialize TTS Engine
# -------------------------
tts_engine = pyttsx3.init()
tts_engine.setProperty("rate", 170)
voices = tts_engine.getProperty("voices")
tts_engine.setProperty("voice", voices[1].id)

def speak(text):
    """Threaded TTS to avoid Streamlit blocking"""
    def run_tts(txt):
        tts_engine.say(txt)
        tts_engine.runAndWait()
    t = threading.Thread(target=run_tts, args=(text,))
    t.start()

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="MEHU AI", layout="centered")
st.title("🧠 MEHU – Your AI Assistant")

# Sidebar
role = st.sidebar.selectbox(
    "Select Role",
    ["Assistant", "Tutor", "Coding Assistant", "Career Mentor"]
)

if st.sidebar.button("🗑 Clear Memory"):
    Memory().clear()
    st.session_state.messages = []
    st.success("Memory Cleared")

# -------------------------
# Initialize Core
# -------------------------
settings = Settings()
engine = GeminiEngine(settings.load_api_key())
memory = Memory()
prompt_controller = PromptController()
mehu = MehuAssistant(engine, prompt_controller, memory)

# -------------------------
# Session state for chat
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "voice_queue" not in st.session_state:
    st.session_state.voice_queue = []

# Render previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# -------------------------
# Voice input button
# -------------------------
col1, col2 = st.columns([3,1])
with col1:
    user_input = st.chat_input("Ask MEHU...")
with col2:
    if st.button("🎤 Voice Input"):
        voice_text = listen()
        if voice_text:
            st.session_state.voice_queue.append(voice_text)
            st.success(f"🎤 You said: {voice_text}")

# -------------------------
# Handle Input
# -------------------------
voice_mode = False

# Priority to voice input
if st.session_state.voice_queue:
    user_input = st.session_state.voice_queue.pop(0)
    voice_mode = True

if user_input:
    # 1️⃣ Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)

    # 2️⃣ Assistant placeholder
    assistant_box = st.chat_message("assistant")
    placeholder = assistant_box.empty()
    placeholder.markdown("⌛ MEHU is thinking...")

    # 3️⃣ Generate streaming response
    streamed_text = ""
    for token in mehu.respond_stream(user_input, role):
        streamed_text += token
        placeholder.markdown(streamed_text)
        time.sleep(0.03)  # typing effect

    # 4️⃣ Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": streamed_text})

    # 5️⃣ Voice output if voice mode
    if voice_mode:
        speak(streamed_text)
