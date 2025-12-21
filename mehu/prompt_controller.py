class PromptController:
    def build_prompt(self, user_input, memory, role="Assistant"):
        memory_text = "\n".join(
            [f"{m['role']}: {m['content']}" for m in memory]
        )
        prompt = (
            f"You are a {role} AI Assistant.\n"
            f"Conversation so far:\n{memory_text}\n"
            f"User: {user_input}\n"
            f"Assistant:"
        )
        return prompt
