class PromptController:
    def build_prompt(self, user_input, memory):
        history_list = memory.get_history()  # returns list of dicts
        history = "\n".join(
            [f"{msg['role']}: {msg['message']}" for msg in history_list]
        )
        system_instructions = "You are JARVIS, a helpful AI assistant."
        return f"{system_instructions}\n{history}\nUser: {user_input}\nAssistant:"
