from google import genai
from google.genai import types

client = genai.Client()


def get_weather(city:str):
    """ get weather for the city"""

    fake_weather = {
        "bangalore": "28 deg, humid",
        "mumbai" : "30 deg, hot",
        "delhi" : "25 deg, cold"
    }
    return fake_weather.get(city.lower(), "no data found")


response = client.models.generate_content(
    model = "gemini-flash-latest",
    contents = "what is the weather in bangalore?",
    config = types.GenerateContentConfig(
        tools = [get_weather]
    )
)


print(response.text)