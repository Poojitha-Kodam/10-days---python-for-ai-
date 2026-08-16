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

history = [types.Content(role = "user", parts = [types.Part.from_text(text="what is the id for gau@gmail.com")])]

response = client.models.generate_content(
    model = "gemini-flash-latest",
    contents = history,
    config = types.GenerateContentConfig(
        tools = [get_user],
        automatic_function_calling = types.AutomaticFunctionCallingConfig(disable = True)

    )
)



if response.function_calls:
    call = response.function_calls[0]
    result = get_user(**call.args)

    # Keep Gemini's function-call message in the conversation before sending
    # the matching tool result back to the model.
    history.append(response.candidates[0].content)
    history.append(types.Content(
        # This API accepts function responses in a user message.
        role ="user",
        parts = [types.Part.from_function_response(name=call.name, response={"res":result})]
    ))

    respo = client.models.generate_content(
        model = "gemini-flash-latest",
        contents = history
    )

    print(respo.text)
