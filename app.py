import streamlit as st
import json
from mehu.assistant import JarvisAssistant
from mehu.gemini_engine import GeminiEngine
from mehu.prompt_controller import PromptController
from mehu.memory import Memory
from config.settings import Settings

st.title("🧠 MEHU – AI Assistant")

# Sidebar controls
st.sidebar.header("⚙️ Controls")
role = st.sidebar.selectbox("Choose MEHU Role", ["General", "Tutor", "Coder", "Mentor"])

if st.sidebar.button("Clear Memory"):
    open("conversation.json", "w").write("[]")
    st.sidebar.success("Memory cleared!")

# Initialize core components
settings = Settings()
engine = GeminiEngine(settings.load_api_key())
memory = Memory()
prompt_controller = PromptController(role=role)
jarvis = JarvisAssistant(engine, prompt_controller, memory)

# Display previous chat history
for msg in memory.get_history():
    st.chat_message(msg["role"]).write(msg["message"])

# Chat input
user_input = st.chat_input("Ask MEHU...")
if user_input:
    st.chat_message("user").write(user_input)
    response = jarvis.respond(user_input)

    if "⚠️ Error" in response:
        st.warning(response)
    else:
        st.chat_message("assistant").write(response)
