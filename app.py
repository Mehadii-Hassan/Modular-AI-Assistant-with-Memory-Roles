import streamlit as st
import threading
import time
import pyttsx3

from config.settings import Settings
from mehu.gemini_engine import GeminiEngine
from mehu.prompt_controller import PromptController
from mehu.memory import Memory
from mehu.assistant import MehuAssistant
from utils.voice_input import listen  # Ensure you have a listen() function

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

# -------------------------
# Sidebar
# -------------------------
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

# -------------------------
# Chat Input & Voice Button
# -------------------------
user_input = st.chat_input("Ask MEHU...")

voice_text = None
if st.button("🎤 Voice Input"):
    voice_text = listen()
    if voice_text:
        st.success(f"🎤 You said: {voice_text}")

# -------------------------
# Handle Input
# -------------------------
voice_mode = False

# Priority to voice input
if voice_text:
    user_input = voice_text
    voice_mode = True

if user_input:
    # 1️⃣ Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 2️⃣ Render all messages
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    # 3️⃣ Assistant thinking placeholder
    assistant_box = st.chat_message("assistant")
    placeholder = assistant_box.empty()
    placeholder.markdown("⌛ MEHU is thinking...")

    # 4️⃣ Generate response
    if voice_mode:
        # Voice input → short response
        response = mehu.respond_short(user_input, role)
    else:
        # Text input → full response
        response = mehu.respond(user_input, role)

    # 5️⃣ Streaming for text input
    if not voice_mode:
        streamed_text = ""
        for word in response.split():
            streamed_text += word + " "
            placeholder.markdown(streamed_text)
            time.sleep(0.03)
    else:
        # Voice input → speak immediately
        placeholder.markdown(response)
        speak(response)

    # 6️⃣ Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})
