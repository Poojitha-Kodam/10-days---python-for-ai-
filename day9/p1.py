from dotenv import load_dotenv
load_dotenv(override=True)

from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    fake_data = {"bangalore": "28°C, humid", "paris": "18°C, cloudy"}
    return fake_data.get(city.lower(), "no data")

agent = create_agent(
    model="google_genai:gemini-flash-latest",
    tools=[get_weather],
    system_prompt="You are a helpful assistant."
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in Bangalore?"}]}
)
final_message = result["messages"][-1]
if isinstance(final_message.content, str):
    print(final_message.content)
else:
    print(final_message.content[0]["text"])