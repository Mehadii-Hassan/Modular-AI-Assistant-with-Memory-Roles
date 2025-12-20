import streamlit as st
from config.settings import Settings
from mehu.gemini_engine import GeminiEngine
from mehu.prompt_controller import PromptController
from mehu.memory import Memory
from mehu.assistant import MehuAssistant

st.set_page_config(page_title="MEHU AI", layout="centered")
st.title("🧠 MEHU – Your AI Assistant")

# Sidebar
role = st.sidebar.selectbox("Select Role", ["Assistant", "Tutor", "Coding Assistant", "Career Mentor"])
if st.sidebar.button("🗑 Clear Memory"):
    Memory().clear()
    st.success("Memory Cleared")

# Init core
settings = Settings()
engine = GeminiEngine(settings.load_api_key())
memory = Memory()
prompt_controller = PromptController()
mehu = MehuAssistant(engine, prompt_controller, memory)

# Chat UI
user_input = st.chat_input("Ask MEHU...")

if user_input:
    reply = mehu.respond(user_input, role)
    st.chat_message("user").write(user_input)
    st.chat_message("assistant").write(reply)
