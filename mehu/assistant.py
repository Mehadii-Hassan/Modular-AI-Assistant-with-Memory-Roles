class MehuAssistant:
    def __init__(self, engine, prompt_controller, memory):
        self.engine = engine
        self.prompt_controller = prompt_controller
        self.memory = memory

    def respond_stream(self, user_input, role="Assistant"):
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
