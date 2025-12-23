import streamlit as st
from mehu.assistant import JarvisAssistant
from mehu.gemini_engine import GeminiEngine
from mehu.prompt_controller import PromptController
from mehu.memory import Memory
from config.settings import Settings

# Title
st.title("🧠 Mehu – AI Assistant")

# Initialize core components
settings = Settings()
engine = GeminiEngine(settings.load_api_key())
memory = Memory()
prompt_controller = PromptController()
jarvis = JarvisAssistant(engine, prompt_controller, memory)

# Sidebar controls
st.sidebar.header("⚙️ Controls")
if st.sidebar.button("Clear Memory"):
    # Reset conversation file
    open("conversation.json", "w").write("[]")
    st.sidebar.success("Memory cleared!")

# Display previous chat history
for msg in memory.get_history():
    st.chat_message(msg["role"]).write(msg["message"])

# Chat input
user_input = st.chat_input("Ask JARVIS...")
if user_input:
    # Show user message
    st.chat_message("user").write(user_input)

    # Get assistant response
    response = jarvis.respond(user_input)

    # Show assistant message
    st.chat_message("assistant").write(response)
