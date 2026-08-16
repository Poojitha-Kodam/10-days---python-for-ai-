from dotenv import load_dotenv
from google import genai 
from google.genai import types


load_dotenv(override=True)

client = genai.Client()

def get_weather(city:str) -> str:
    fake_weather = {
        "hyderabad" : "28 deg, cold",
        "bangalore" : "30 deg, humid"
    }
    return fake_weather.get(city.lower(), "no data")

def get_stock_price(ticker:str) -> str:
    fake_stock = {
        "aapl" : "345678",
        "goog" : "1234567"
    }
    return fake_stock.get(ticker.lower(), "no data")

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

def get_time_zone(city:str) -> str:
    fake_data = {
        "nyc" : "USA (GMT-4)",
        "bangalore" : "UTC/GMT +5:30."
    }
    return fake_data.get(city.lower(), "no data")

TOOL_MAP = {
    "get_weather" : get_weather,
    "get_stock_price" : get_stock_price,
    "convert_currency" : convert_currency,
    "get_time_zone" : get_time_zone
}

history = [types.Content(
    role = "user",
    parts = [
        types.Part.from_text(
            text= "what is the stock price of aapl and convert 100 usd to EUR and convert 100 eur into inr"
        )
    ]
)]

for turn in range(3):
    response = client.models.generate_content(
        model = "gemini-flash-latest",
        contents = history,
        config = types.GenerateContentConfig(
            tools = [get_weather, get_stock_price, convert_currency, get_time_zone],
            automatic_function_calling = types.AutomaticFunctionCallingConfig(disable=True)
        )
    )

    history.append(response.candidates[0].content)

    if response.function_calls:
        for call in response.function_calls:
            real_function = TOOL_MAP[call.name]
            result = real_function(**call.args)

            print(f"Round {turn+1} : {call.name}({call.args}) -> {result}")

            history.append(types.Content(
                role="user",
                parts = [types.Part.from_function_response(name=call.name, response={"Result":result})]
            ))

    else:
        print("\n final answer : ", response.text)
        break