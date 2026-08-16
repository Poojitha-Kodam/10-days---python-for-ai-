from google import genai 
from google.genai import types 

client = genai.Client()

def get_weather(city:str):
    fake_weather = {
        "hyderabad" : "28 deg, humid",
        "bangalore" : "30 deg, cool"
    }

    return fake_weather.get(city.lower(), "city not found")


def get_stock_price(ticker:str):
    fake_stocks = {
        "AAPL": 3456,
        "ASDF": 23456,
        "WERT": 56789
    }
    return fake_stocks.get(ticker.upper(), "no ticker found")


response = client.models.generate_content(
    model = "gemini-flash-latest",
    contents = "what is the weather in hyderabad and stock price of aapl?",
    config = types.GenerateContentConfig(
        tools = [get_weather, get_stock_price]
    )
)


print(response.text)