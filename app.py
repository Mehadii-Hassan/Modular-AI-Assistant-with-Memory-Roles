import streamlit as st
import json
from mehu.assistant import JarvisAssistant
from mehu.gemini_engine import GeminiEngine
from mehu.prompt_controller import PromptController
from mehu.memory import Memory
from config.settings import Settings

# -------------------------------
# Theme polish (Streamlit config)
# -------------------------------
# 👉 Create a folder `.streamlit/config.toml` with this content:
# [theme]
# primaryColor="#00FFAA"
# backgroundColor="#0E1117"
# secondaryBackgroundColor="#262730"
# textColor="#FAFAFA"
# font="sans serif"

# -------------------------------
# Greeting message
# -------------------------------
st.title("🧠 JARVIS – Your AI Assistant")
st.write("👋 Hello! I’m JARVIS, your personal AI companion. Ready to help you learn, code, or plan your career!")

# -------------------------------
# Sidebar controls
# -------------------------------
st.sidebar.header("⚙️ Controls")

# Role switching
role = st.sidebar.selectbox("Choose JARVIS Role", ["General", "Tutor", "Coder", "Mentor"])

# Clear memory button
if st.sidebar.button("Clear Memory"):
    open("conversation.json", "w").write("[]")
    st.sidebar.success("Memory cleared!")

# -------------------------------
# Core initialization
# -------------------------------
settings = Settings()
engine = GeminiEngine(settings.load_api_key())
memory = Memory()
prompt_controller = PromptController(role=role)
jarvis = JarvisAssistant(engine, prompt_controller, memory)

# -------------------------------
# Session greeting (first time)
# -------------------------------
if not memory.get_history():
    st.chat_message("assistant").write("👋 Hi, I’m JARVIS. How can I help you today?")

# -------------------------------
# Display previous chat history
# -------------------------------
for msg in memory.get_history():
    st.chat_message(msg["role"]).write(msg["message"])

# -------------------------------
# Chat input
# -------------------------------
user_input = st.chat_input("Ask JARVIS...")
if user_input:
    st.chat_message("user").write(user_input)
    response = jarvis.respond(user_input)

    if "⚠️ Error" in response:
        st.warning(response)
    else:
        st.chat_message("assistant").write(response)
