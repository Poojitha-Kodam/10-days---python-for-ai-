from dotenv import load_dotenv

load_dotenv(override=True)

from google import genai 
from google.genai import types

client = genai.Client()

def get_weather(city:str) -> str:
    """gets current weather for the city"""
    fake_weather = {
        "bangalore" : "28 deg, humid",
        "hyderabad" : "30 deg, hot"
    }  
    return fake_weather.get(city.lower(), "not found")

def get_stock_price(ticker:str) -> str:
    """gets stock price by ticker"""
    fake_stock = {
        "aapl" : "234567",
        "goog" : "2345678"
    }
    return fake_stock.get(ticker.lower(), "not found")

def convert_currency(amount:float, from_currency:str, to_currency:str) -> str:
    """converts an amount from currency to another"""
    rates = {
        "usd": 83.0,
        "eur": 90.0, 
        "inr": 1.0
    }
    inr = amount*rates.get(from_currency.lower(), 1.0)
    result = inr/rates.get(to_currency.lower(), 1.0)
    return f"{result: .2f} {to_currency.upper()}"


TOOL_MAP = {
    "get_weather" : get_weather,
    "get_stock_price" : get_stock_price,
    "convert_currency" : convert_currency
}

history = [types.Content(
    role = "user",
    parts = [
        types.Part.from_text(
            text = "what is the weather in bangalore, the stock price of aapl and convert 100 usd to EUR?"
        )
    ]
)]

for turn in range(4):
    response = client.models.generate_content(
        model = "gemini-flash-latest",
        contents = history,
        config = types.GenerateContentConfig(
            tools = [get_weather, get_stock_price, convert_currency],
            automatic_function_calling = types.AutomaticFunctionCallingConfig(disable = True)
        )
    )

    history.append(response.candidates[0].content)

    if response.function_calls:
        for call in response.function_calls:
            real_func = TOOL_MAP[call.name]
            result = real_func(**call.args)

            print(f"Round {turn+1} : {call.name}({call.args}) -> {result}")


            history.append(types.Content(
                role="user",
                parts = [types.Part.from_function_response(name = call.name, response = {"result" : result})]
            ))

    else:
        print("\n\n Final answer : ", response.text)
        break