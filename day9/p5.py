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


def agent_run(agent, user_message):
    try:
        result = agent.invoke({
            "messages" : [{
                "role" : "user",
                "content" : user_message
            }]
        })
        final_mess = result["messages"][-1]
        if isinstance(final_mess.content, str):
            return final_mess.content
        else:
            return final_mess.content[0]["text"]

    except Exception as e:
        return f" agent failed : {e}"



print(agent_run(agent, "what is the user id of 'gau@gmail.com' and is the balance more than 500"))
