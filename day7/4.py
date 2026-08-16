from google import genai
from google.genai import types

client = genai.Client()

def get_weather(city: str) -> str:
    """Gets current weather for a city.

    Args:
        city: The city name.
    """
    fake_data = {"bangalore": "28°C, humid", "delhi": "35°C, hot"}
    return fake_data.get(city.lower(), "no data")


# Step 1: send the user's question, tools available, but AUTOMATIC calling turned OFF
response = client.models.generate_content(
    model="gemini-flash-latest",
    contents="What's the weather in Bangalore?",
    config=types.GenerateContentConfig(
        tools=[get_weather],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
    )
)

# Step 2: check — did the model decide to call a tool?
if response.function_calls:
    call = response.function_calls[0]
    print(f"Model wants to call: {call.name} with args: {call.args}")

    # Step 3: WE manually execute the real function ourselves
    result = get_weather(**call.args)
    print(f"Tool result: {result}")

    # Step 4: send the result BACK to the model so it can form a final answer
    # We build a follow-up message showing what the tool returned
    followup = client.models.generate_content(
        model="gemini-flash-latest",
        contents=f"The weather tool returned: '{result}'. Now answer the user's original question: What's the weather in Bangalore?",
    )
    print("Final answer:", followup.text)
else:
    # Model answered directly without needing a tool
    print("Final answer:", response.text)