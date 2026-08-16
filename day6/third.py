from google import genai 
from google.genai import types 

client = genai.Client()

def convert_currency(amount: float, from_currency: str, to_currency: str):
    fake_exchange = {
        "USD" : 95.39,
        "EUR" : 90.0
    }
    inr_amount = amount * fake_exchange.get(from_currency.upper(), 1.0)
    final_amount = inr_amount/fake_exchange.get(to_currency.upper(), 1.0)
    return final_amount


response = client.models.generate_content(
    model = "gemini-flash-latest",
    contents = "convert 100.0 USD to EUR",
    config = types.GenerateContentConfig(
        tools = [convert_currency]
    )
)

print(response.text)