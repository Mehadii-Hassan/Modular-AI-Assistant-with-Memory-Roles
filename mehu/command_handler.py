import webbrowser

class CommandHandler:
    def __init__(self):
        self.commands = {
            "open google": "https://www.google.com",
            "open linkedin": "https://www.linkedin.com",
            "open facebook": "https://www.facebook.com",
            "open github": "https://www.github.com",
            "open youtube": "https://www.youtube.com",
        }

    def handle(self, user_input: str):
        text = user_input.lower().strip()

        # Open commands
        if text in self.commands:
            webbrowser.open_new_tab(self.commands[text])
            return f"✅ Opening {text.split()[1].capitalize()} Successfully!"

        # Close commands (not possible directly)
        elif text.startswith("close "):
            site = text.split()[1].capitalize()
            return f"⚠️ Closing {site} tab is not possible directly. Please close it manually."

        # Not a command
        return None
