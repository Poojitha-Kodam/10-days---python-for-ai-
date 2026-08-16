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

    

class Tool:
    def __init__(self, name:str, description:str) -> str:
        self.name = name 
        self.description = description
    
    def describe(self):
        return f"Tool : {self.name} - {self.description}"

class Agent:
    def __init__(self, name:str):
        self.name = name 
        self.tools = []
    
    def add_tool(self, tool_name: str):
        self.tools.append(tool_name)

    def list_tools(self):
        for i, tool in enumerate(self.tools, start = 1):
            print(f"{i} : {tool}")



convo = Conversation()
convo.add_message("user", "Hi there")
convo.add_message("assistant", "Hello! How can I help?")
convo.add_message("user", "What's 2+2?")
convo.add_message("assistant", "4")
convo.add_message("user", "bye")
convo.add_message("assistant", "goodbye")
print()
convo.show_message()
print("User messages:", convo.count_by_role("user"))
print()
print(convo.last_n_messages(2))
print(convo.to_dict_list())
print()
tool = Tool("weather", "fetching the weather details")
print(tool.describe())
print()
agent = Agent("poojitha")
agent.add_tool("weather")
agent.add_tool("calculator")
agent.add_tool("coding")
agent.list_tools()
print()