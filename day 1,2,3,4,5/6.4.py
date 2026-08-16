from google import genai

client = genai.Client()

def ask_with_retry(prompt:str, max_attempts:int = 3) -> str:
    for attempt in range(1, max_attempts+1):
        try:
            response = client.models.generate_content(
                model = "gemini-flash-latest",
                contents = prompt
            )
            print("successful on attempt", attempt)
            return response.text
        except Exception as e:
            print(f"failed on attempt {attempt} at {e}")
    return "all attempts failed"



a1 = ask_with_retry("what is ai in one line?")


print(a1)
