class MehuAssistant:
    def __init__(self, engine, prompt_controller, memory):
        self.engine = engine
        self.prompt_controller = prompt_controller
        self.memory = memory

    def respond(self, user_input, role = "Assistant"):
        self.memory.add("user", user_input)
        prompt = self.prompt_controller.build_prompt(
            user_input = user_input,
            memory = self.memory.get_history(),
            role = role
        )

        response = self.engine.generate(prompt)
        self.memory.add("assistant", response)
        return response