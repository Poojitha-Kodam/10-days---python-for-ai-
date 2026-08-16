from dotenv import load_dotenv
load_dotenv()  # reads .env in the current folder and loads it into the environment

from google import genai 
from google.genai import types

client = genai.Client()


def check_username(username:str) -> bool:
    taken_usernames = ["pooja", "gauatmi", "nirmala", "madhukar"]

    return username.lower() not in taken_usernames 


response = client.models.generate_content(
    model = "gemini-flash-lite-latest",
    contents = "is the username 'pooja' available?",
    config = types.GenerateContentConfig(
        tools = [check_username]
    )
)

print(response.text)



## python code with no api to check the above condition

username_to_check = "pooja"
is_available = check_username(username_to_check)

if is_available:
    print(f"congrats the username {username_to_check} is available")
else:
    alt1 = username_to_check + "123"
    alt2 = username_to_check + "dev"
    print(f" sorry {username_to_check} is not available. try {alt1} or {alt2}")