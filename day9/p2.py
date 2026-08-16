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

agent = create_agent(
    model = "google_genai:gemini-flash-latest",
    tools = [get_stock],
    system_prompt = "you are an helpful stocks assistant"
)

result = agent.invoke(
    {"messages" : [
        {"role":"user", "content" : "what is the stock price of aapl?"}
    ]}
)


final_result = result["messages"][-1]

if isinstance(final_result.content, str):
    print(final_result.content)
else:
    print(final_result.content[0]["text"])