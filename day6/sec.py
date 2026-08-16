from google import genai 
from google.genai import types 

client = genai.Client()

def get_stock_price(ticker:str) -> str:
    print("get_stock_price was called with ", ticker)
    fake_data = {
        "AAPL" : "12345",
        "WERT" : "5678",
        "DFGH" : "34567"    
    }
    return fake_data.get(ticker.upper(), "no ticker found")


response = client.models.generate_content(
    model = "gemini-flash-latest",
    contents = "what is price of aapl?",
    config = types.GenerateContentConfig(
        tools = [get_stock_price]
    )
)

print(response.text)