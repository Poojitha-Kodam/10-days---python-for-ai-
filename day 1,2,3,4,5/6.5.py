from google import genai

client = genai.Client()

class Message:
    def __init__(self, role:str, content: str) -> str:
        self.role = role
        self.content = content

    def __str__(self):
        return f"[{self.role}]: {self.content}"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {"role": self.role, "content": self.content}

class Conversation:
    def __init__(self):
        self.messages = []

    def add_message(self, role:str, content: str):
        msg = Message(role, content)
        self.messages.append(msg)
    
    def show_message(self):
        for message in self.messages:
            print(message)

    def count_by_role(self, role: str):
        count = 0
        for msg in self.messages:
            if msg.role == role:
                count += 1
        return count 
    
    def last_n_messages(self, n:int):
        return self.messages[-n:]

    def to_dict_list(self):
        dict_list = []
        for message in self.messages:
            dict_list.append(message.to_dict())
        return dict_list

    def to_prompt_string(self)->str:
        formatted = ""
        for message in self.messages:
            formatted += f"{message.role} : {message.content}"
        return formatted 




convo = Conversation()
convo.add_message("user", "my name is pooja")
prompt = convo.to_prompt_string()
response_1 = client.models.generate_content(
    model = "gemini-flash-latest",
    contents = prompt
)
convo.add_message("AI", response_1.text)


convo.add_message("user", "what is my name")
prompt = convo.to_prompt_string()
response_2 = client.models.generate_content(
    model = "gemini-flash-latest",
    contents = prompt
)
convo.add_message("AI", response_2.text)

convo.show_message()