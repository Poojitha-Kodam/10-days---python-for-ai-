from google import genai 
from google.genai import types

client = genai.Client()


def get_user(email:str) -> str:
    fake_users = {
        "sam@gmail.com" : "user899",
        "poo@gmail.com" : "user456",
        "gau@gmail.com" : "user478"
    }
    return fake_users.get(email.lower(), "not found")


response = client.models.generate_content(
    model = "gemini-flash-latest",
    contents = "what is the id for gau@gmail.com",
    config = types.GenerateContentConfig(
        tools = [get_user],
        automatic_function_calling = types.AutomaticFunctionCallingConfig(disable = True)
    
    )
)

if response.function_calls:
    call = response.function_calls[0]
    res1 = get_user(**call.args)
    print(res1)
    respo = client.models.generate_content(
        model = "gemini-flash-latest",
        contents = f"this is the result {res1}. now answer: what is the id for gau@gmail.com"

    )

    print(respo.text)
