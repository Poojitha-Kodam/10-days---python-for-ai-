# Import the main Google Gemini AI library.
from google import genai
# Import helper classes for creating Gemini messages and configuration.
from google.genai import types

# Create a client object that lets this program communicate with Gemini.
client = genai.Client()

# Define a normal Python function that finds a user ID from an email address.
def get_user_id(email: str) -> str:
    # Explain the purpose of this function for people reading its documentation.
    """Looks up a user's ID from their email."""
    # Create a small example database where each email has a user ID.
    db = {"sam@email.com": "usr-999"}
    # Make the email lowercase, return its ID, or say "not found" if it is missing.
    return db.get(email.lower(), "not found")


# Begin the conversation history with the user's question in Gemini's message format.
history = [types.Content(role="user", parts=[types.Part.from_text(text="What is the user ID for sam@email.com?")])]

# Allow at most three rounds: Gemini can request a tool, receive its result, then answer.
for turn in range(3):
    # Ask Gemini to process the conversation so far.
    response = client.models.generate_content(
        # Choose the Gemini model that should respond.
        model="gemini-flash-latest",
        # Send every previous message in the conversation.
        contents=history,
        # Set options for the model and its available tools.
        config=types.GenerateContentConfig(
            # Let Gemini know that it may request the get_user_id function.
            tools=[get_user_id],
            # Keep automatic tool calling off because this program handles calls itself.
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
        )
    )

    # Save Gemini's response so it is included in the next conversation round.
    history.append(response.candidates[0].content)

    # Check whether Gemini asked this program to run a function.
    if response.function_calls:
        # Take the first function call requested by Gemini.
        call = response.function_calls[0]
        # Run the requested function using the arguments Gemini provided.
        result = get_user_id(**call.args)
        # Print details about the tool call and the result for learning and debugging.
        print(f"Round {turn+1}: called {call.name}({call.args}) → {result}")

        # Add the function's result to the conversation in Gemini's expected format.
        history.append(types.Content(
            # Mark this message as a user-side response containing the tool result.
            role="user",
            # Include the function name and the value it returned.
            parts=[types.Part.from_function_response(name=call.name, response={"result": result})]
        ))
    # If there was no function request, Gemini has given its final answer.
    else:
        # Print the final text response from Gemini.
        print(f"\nFinal answer: {response.text}")
        # Leave the loop because the program has finished its work.
        break
