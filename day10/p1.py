import json
import os
from dotenv import load_dotenv
load_dotenv(override=True)
from langchain.agents import create_agent

HISTORY_FILE = "chat_history.json"

def load_history() -> list:
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(messages: list):
    with open(HISTORY_FILE, "w") as f:
        json.dump(messages, f, indent=2)

def get_weather(city: str) -> str:
    """Gets current weather for a city."""
    fake = {"bangalore": "28°C, humid"}
    return fake.get(city.lower(), "no data")

agent = create_agent(
    model="google_genai:gemini-flash-latest",
    tools=[get_weather],
    system_prompt="You are a helpful assistant."
)

def get_answer(result) -> str:
    final_message = result["messages"][-1]
    if isinstance(final_message.content, str):
        return final_message.content
    return final_message.content[0]["text"]

# Load whatever history exists from a PREVIOUS run
messages = load_history()
messages.append({"role": "user", "content": "What's the weather in Bangalore?"})

result = agent.invoke({"messages": messages})
print(get_answer(result))

# Save the FULL updated history (as plain dicts, not LangChain objects) back to disk
messages_to_save = []
for m in result["messages"]:
        if m.type in ["human", "ai"]:
            messages_to_save.append({
                "role" : m.type,
                "content" : m.content
            })

save_history(messages_to_save)