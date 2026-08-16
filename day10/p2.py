import json
import os
from dotenv import load_dotenv
load_dotenv(override=True)
from langchain.agents import create_agent

HIST_FILE = "chat_hist.json"

def load_history():
    if os.path.exists(HIST_FILE):
        with open(HIST_FILE, "r") as f:
            return json.load(f)
    return []


def save_history(messages):
    with open(HIST_FILE, "w") as f:
        json.dump(messages, f, indent=2)


def get_weather(city:str) -> str:
    """gets weather information for the given city"""
    fake_data = {
        "bangalore" : "humid and 28 deg",
        "hyderabad" : "cool and 25 deg"
    }
    return fake_data.get(city.lower(), "no data")

agent = create_agent(
    model="google_genai:gemini-flash-latest",
    tools=[get_weather],
    system_prompt="you are a helpful assistant in weather data"
)

def final_result(result):
    final_res = result["messages"][-1]
    if isinstance(final_res.content, str):
        return final_res.content
    return final_res.content[0]["text"]


messages = load_history()
messages.append({"role":"user", "content":"what is the weather in bangalore?"})

result = agent.invoke({"messages" : messages})
print(final_result(result))

messages_to_save = [
    {
        "role":m.type if hasattr(m, "type") else m["role"],
        "content":m.content if hasattr(m, "content") else m["content"]
    }
    for m in result["messages"]
]
save_history(messages_to_save)

