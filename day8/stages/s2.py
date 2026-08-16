from google import genai 
from google.genai import types 

client = genai.Client()


def get_user(email:str):
    db = {
        "sam@gmail.com" : "user999",
        "poo@gmail.com" : "user567"
    }

    return db.get(email.lower(), "not found")


response = client.models.generate_content(
    model = "gemini-flash-latest",
    contents = "what is the user id of poo@gmail.com",
    config = types.GenerateContentConfig(
        tools = [get_user]
    )
)

print(response.text)