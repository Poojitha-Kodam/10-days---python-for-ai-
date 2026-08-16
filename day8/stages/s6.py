from dotenv import load_dotenv

load_dotenv(override=True)


from google import genai 
from google.genai import types

client = genai.Client()

def get_user(email:str) -> str:
    fake_users = {
        "sam@gmail.com" : "user888",
        "gau@gmail.com" : "user886"
    }

    return fake_users.get(email.lower(), "not found")

history = [types.Content(
    role="user",
    parts = [types.Part.from_text(
        text="what is the id for gau@gmail.com"
    )]
)]

for turn in range(3):
    response = client.models.generate_content(
        model = "gemini-flash-latest",
        contents = history,
        config = types.GenerateContentConfig(
            tools = [get_user],
            automatic_function_calling = types.AutomaticFunctionCallingConfig(disable=True)
        )
    )

    history.append(response.candidates[0].content)

    if response.function_calls:
        call = response.function_calls[0]
        result = get_user(**call.args)
        print(f"Round {turn+1}: {call.name}({call.args}) -> {result}")

        history.append(
            types.Content(
                role="user",
                parts=[types.Part.from_function_response(name=call.name, response={"result":result})]
            )
        )

    else:
        print("final answer : ", response.text)
        break




