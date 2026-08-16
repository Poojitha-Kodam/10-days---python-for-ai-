from google import genai

client = genai.Client()


class Message:
    def __init__(self, role, content):
        self.role = role
        self.content = content

    def __str__(self):
        return f"{self.role} : {self.content}"
    def __repr__(self):
        return __str__

class Conversation:
    def __init__(self):
        self.messages = []
    def add_message(self, role, content):
        msg = Message(role, content)
        self.messages.append(msg)
    def to_llm_feed(self):
        formatted = ""
        for message in self.messages:
            formatted += f"{message.role} : {message.content}"
        return formatted 
    def show_messages(self):
        for mes in self.messages:
            print(mes)
    


conv = Conversation()
conv.add_message("user", "i love flowers and gifts a lot")
prompt = conv.to_llm_feed()
response_1 = client.models.generate_content(
    model = "gemini-flash-latest",
    contents = prompt
)
conv.add_message("AI", response_1.text)

conv.add_message("user", "i also love movies which are relatable")
prompt = conv.to_llm_feed()
response_2 = client.models.generate_content(
    model = "gemini-flash-latest",
    contents = prompt
)
conv.add_message("AI", response_2.text)

conv.add_message("user", "what do i love?")
prompt = conv.to_llm_feed()
response_3 = client.models.generate_content(
    model = "gemini-flash-latest",
    contents = prompt
)
conv.add_message("AI", response_3.text)


conv.show_messages()