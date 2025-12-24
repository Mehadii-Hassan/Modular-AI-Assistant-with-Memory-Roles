class PromptController:
    def __init__(self, role="General"):
        self.role = role

    def build_prompt(self, user_input, memory):
        history_list = memory.get_history()
        history = "\n".join(
            [f"{msg['role']}: {msg['message']}" for msg in history_list]
        )

        # Role-based personality
        if self.role == "Tutor":
            system_instructions = "You are MEHU, a patient tutor. Explain concepts step by step."
        elif self.role == "Coder":
            system_instructions = "You are MEHU, a coding assistant. Provide clean, efficient code and debugging help."
        elif self.role == "Mentor":
            system_instructions = "You are MEHU, a career mentor. Give professional advice and guidance."
        else:
            system_instructions = "You are MEHU, a helpful AI assistant."

        return f"{system_instructions}\n{history}\nUser: {user_input}\nAssistant:" 
