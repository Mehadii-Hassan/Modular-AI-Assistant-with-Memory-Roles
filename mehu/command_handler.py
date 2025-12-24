import webbrowser
import os
import platform
import subprocess

class CommandHandler:
    def __init__(self):
        # Web commands
        self.web_commands = {
            "open google": "https://www.google.com",
            "open linkedin": "https://www.linkedin.com",
            "open facebook": "https://www.facebook.com",
            "open github": "https://github.com/Mehadii-Hassan",
            "open youtube": "https://www.youtube.com",
        }

        # System commands
        self.system_commands = {
            "open calculator": self.open_calculator,
            "open notepad": self.open_notepad,
        }

    def handle(self, user_input: str):
        text = user_input.lower().strip()

        # Search command
        if text.startswith("search google for"):
            query = text.replace("search google for", "").strip()
            webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")
            return f"🔎 Searching Google for: {query}"

        # Multi-command execution
        if " and " in text:
            commands = [cmd.strip() for cmd in text.split(" and ")]
            responses = []
            for cmd in commands:
                resp = self.handle(cmd)  
                if resp:
                    responses.append(resp)
            return " | ".join(responses)

        # Web commands
        if text in self.web_commands:
            webbrowser.open_new_tab(self.web_commands[text])
            return f"✅ Opening {text.split()[1].capitalize()} Successfully!"

        # System commands
        elif text in self.system_commands:
            self.system_commands[text]()
            return f"✅ Executing {text.title()} Successfully!"

        # Close commands (not possible directly)
        elif text.startswith("close "):
            site = text.split()[1].capitalize()
            return f"⚠️ Closing {site} tab/app is not possible directly. Please close it manually."

        # Not a command
        return None

    
    # System command implementations
    def open_calculator(self):
        os_name = platform.system()
        if os_name == "Windows":
            subprocess.Popen("calc.exe")
        elif os_name == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", "Calculator"])
        elif os_name == "Linux":
            subprocess.Popen(["gnome-calculator"])

    def open_notepad(self):
        os_name = platform.system()
        if os_name == "Windows":
            subprocess.Popen("notepad.exe")
        elif os_name == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", "TextEdit"])
        elif os_name == "Linux":
            subprocess.Popen(["gedit"])
