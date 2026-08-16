from dotenv import load_dotenv
load_dotenv(override=True)

from langchain.agents import create_agent

def get_stock(ticker:str) -> str:
    """Get the stock price for a given ticker symbol."""
    fake_data = {
        "aapl" : 34567,
        "goog" : 23456
    }
    return fake_data.get(ticker.lower(), "no data")

def currency_converter(amount:int, to_currency:str, from_currency:str) -> str:
    """Gets the converted currency value for the given amount"""
    rates = {
        "usd" : 83.0,
        "eur" : 92.0,
        "inr" : 1.0
    }
    base = amount * rates.get(from_currency.lower(), 1.0)
    final = base / rates.get(to_currency.lower(), 1.0)
    return f"{final} {to_currency}"


agent = create_agent(
    model = "google_genai:gemini-flash-latest",
    tools = [get_stock, currency_converter],
    system_prompt = "you are a helpful agent"
)


result = agent.invoke(
    {
        "messages" : [{
            "role" : "user",
            "content" : "what is the stock price of aapl and convert 100 usd to inr"
        }]
    }
)

final_result = result["messages"][-1]

if isinstance(final_result.content, str):
    print(final_result.content)
else:
    print(final_result.content[0]["text"])