from google import genai

client = genai.Client()

class Message:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

class Conversation:
    def __init__(self):
        self.messages = []

    def add_message(self, role: str, content: str):
        self.messages.append(Message(role, content))

    def to_prompt_string(self) -> str:
        # This is the "glue everything together" step
        formatted = ""
        for msg in self.messages:
            formatted += f"{msg.role}: {msg.content}\n"
        return formatted

    def show_message(self):
        for msg in self.messages:
            print(f"[{msg.role}]: {msg.content}")


# --- Actual multi-turn logic starts here ---

convo = Conversation()

# Turn 1
user_input_1 = "My favorite animal is a tiger."
convo.add_message("user", user_input_1)

prompt_so_far = convo.to_prompt_string()
response_1 = client.models.generate_content(
    model="gemini-flash-latest",
    contents=prompt_so_far
)
convo.add_message("assistant", response_1.text)

# Turn 2 — this is where "memory" is tested
user_input_2 = "What's my favorite animal?"
convo.add_message("user", user_input_2)

prompt_so_far = convo.to_prompt_string()  # NOTE: now includes turn 1 AND turn 2
response_2 = client.models.generate_content(
    model="gemini-flash-latest",
    contents=prompt_so_far
)
convo.add_message("assistant", response_2.text)

# Show the whole thing
convo.show_message()