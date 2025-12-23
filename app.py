import streamlit as st
from mehu.assistant import JarvisAssistant
from mehu.gemini_engine import GeminiEngine
from mehu.prompt_controller import PromptController
from mehu.memory import Memory
from config.settings import Settings

st.title("🧠 JARVIS – AI Assistant")

settings = Settings()
engine = GeminiEngine(settings.load_api_key())
memory = Memory()
prompt_controller = PromptController()
jarvis = JarvisAssistant(engine, prompt_controller, memory)

user_input = st.chat_input("Ask JARVIS...")
if user_input:
    response = jarvis.respond(user_input)
    st.chat_message("assistant").write(response)

# Sidebar
if st.sidebar.button("Clear Memory"):
    memory = Memory()  # reset file
    st.sidebar.success("Memory cleared!")
