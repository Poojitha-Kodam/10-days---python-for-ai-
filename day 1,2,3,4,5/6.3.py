from google import genai

client = genai.Client()

def summarize_in_one_line(text:str) -> str:
    prompt = f"Summarize the following text in one line: \n\n{text}"
    response = client.models.generate_content(
        model = "gemini-flash-latest",
        contents = prompt
    )
    return response.text

paragraph = "Trees are vital living parts of our natural environment. They give us fresh oxygen to breathe every day. They absorb harmful carbon dioxide from the air. Green leaves and strong branches offer cool shade. Many birds and animals build homes in trees. Their deep roots keep the soil safe and firm. Trees also give us sweet fruits, wood, and useful medicine. They help bring rain and keep the weather pleasant. Planting more trees makes our Earth green and healthy. We must protect all trees to save our future."

summary = summarize_in_one_line(paragraph)

print(summary)
