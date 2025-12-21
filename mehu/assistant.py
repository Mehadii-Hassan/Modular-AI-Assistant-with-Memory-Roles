class MehuAssistant:
    def __init__(self, engine, prompt_controller, memory):
        self.engine = engine
        self.prompt_controller = prompt_controller
        self.memory = memory

    def respond_stream(self, user_input, role="Assistant"):
        """
        Full streaming response (text input)
        Yields token by token for Streamlit typing effect
        """
        # Save user message
        self.memory.add("user", user_input)

        # Build prompt
        prompt = self.prompt_controller.build_prompt(
            user_input=user_input,
            memory=self.memory.get_history(),
            role=role
        )

        full_response = ""

        # Stream from Gemini
        for token in self.engine.stream(prompt):
            full_response += token
            yield token

        # Save assistant message
        self.memory.add("assistant", full_response)

    def respond_short(self, user_input, role="Assistant"):
        """
        Short response for voice input
        Returns only first sentence
        """
        # Use normal respond_stream but collect full response once
        full_response = ""
        for token in self.respond_stream(user_input, role):
            full_response += token
        # Take only first sentence
        short_response = full_response.split(".")[0] + "."
        return short_response
