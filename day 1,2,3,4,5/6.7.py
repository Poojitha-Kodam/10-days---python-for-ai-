from google import genai 

client = genai.Client()

def word_count(prompt:str) -> str:
    try:
        response = client.models.generate_content(
            model = "gemini-flash-latest",
            contents = prompt
        )
        print(response.text)
        response_word = response.text.split()
        return len(response_word)

    except Exception as e:
        print("error")
        return -1

    
words = word_count("who is the prime minister of india?")
print(words)