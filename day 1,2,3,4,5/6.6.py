from google import genai 

client = genai.Client()

def translate_text(text:str, target_language:str) -> str:
    prompt = f"convert the \n\n {text} \n\n into {target_language}"
    response = client.models.generate_content(
        model = "gemini-flash-latest",
        contents = prompt
    )
    return response.text


res_1 = translate_text("hello how are you", "hindi")
res_2 = translate_text("had dinner", "marathi")

print(res_1)
print("*"*50)
print(res_2)