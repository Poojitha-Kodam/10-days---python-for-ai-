from dotenv import load_dotenv
load_dotenv(override=True)

from langchain.agents import create_agent

def get_user_id(email:str) -> str:
    """gets user id for the given email"""
    fake_ids = {
        "sam@gmail.com" : "user888",
        "gau@gmail.com" : "user999"
    }
    return fake_ids.get(email.lower(), "no data")

def get_balance(id:str) -> int:
    """gets balance for the given user id"""
    fake_bal = {
        "user888" : 500,
        "user999" : 678
    }
    return fake_bal.get(id.lower(), "no data")


agent = create_agent(
    model = 'google_genai:gemini-flash-latest',
    tools = [get_user_id, get_balance],
    system_prompt = "you are an helpful agent in banking sector"

)

messages = [{
    "role" : "user",
    "content" : "what is the user id for 'sam@gmail.com'?"
}]

result = agent.invoke({
    "messages" : messages
})

messages = result["messages"] + [{
    "role" : "user",
    "content" : "is the balance more than 400?"
}]

result1 = agent.invoke({
    "messages" : messages
}) 

final_result = result1["messages"][-1]

if isinstance(final_result.content, str):
    print(final_result.content)
else:
    print(final_result.content[0]["text"])