# Import Python's built-in tools for running tasks at the same time.
import asyncio
# Import the main Google Gemini AI library.
from google import genai
# Import Gemini helper classes used to build messages and configuration.
from google.genai import types

# Create a client object that lets this program communicate with Gemini.
client = genai.Client()

# Define an asynchronous tool that accepts a stock ticker and returns a price.
async def fetch_stock_price(ticker: str) -> float:
    # Explain the purpose of this function for people reading its documentation.
    """Fetches real-time stock price for a company ticker."""
    # Pause for one second to pretend that a real stock-price API is being called.
    await asyncio.sleep(1.0)
    # Store sample stock prices; a real program would get these from an online API.
    prices = {"AAPL": 175.50, "MSFT": 415.20, "GOOG": 150.10}
    # Convert the ticker to uppercase, return its price, or return 0.0 if it is unknown.
    return prices.get(ticker.upper(), 0.0)

# Map the tool name Gemini uses to the actual Python function it should run.
TOOL_MAP = {"fetch_stock_price": fetch_stock_price}

# Define the main asynchronous function; `query` is the question from the user.
async def run_parallel_agent(query: str):
    # Start the conversation history with the user's question in Gemini's message format.
    history = [types.Content(role="user", parts=[types.Part.from_text(text=query)])]

    # Ask Gemini to read the question and decide whether it needs to call a tool.
    response = client.models.generate_content(
        # Choose the Gemini model that should answer the request.
        model="gemini-flash-latest",
        # Give Gemini all messages seen in the conversation so far.
        contents=history,
        # Provide settings that describe which tools Gemini may request.
        config=types.GenerateContentConfig(
            # Make the stock-price function available as a tool to Gemini.
            tools=[fetch_stock_price],
            # Keep automatic calling off because this script runs the requested tools itself.
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
        )
    )

    # Save Gemini's response in history so the next request includes its tool requests.
    history.append(response.candidates[0].content)

    # Continue only if Gemini asked the program to run one or more functions.
    if response.function_calls:
        # Show how many stock-price lookups Gemini requested.
        print(f"[Loop] Model requested {len(response.function_calls)} parallel calls.")

        # Create an empty list that will hold the async work to be run together.
        tasks = []
        # Visit every function call that Gemini requested.
        for call in response.function_calls:
            # Find the matching Python function by using the function name from Gemini.
            func = TOOL_MAP[call.name]
            # Display which function will run and the arguments Gemini supplied.
            print(f"       -> Scheduling {call.name} for {call.args}")
            # Create the async task with Gemini's arguments and add it to the task list.
            tasks.append(func(**call.args))

        # Run all tasks concurrently, then wait until every task has finished.
        results = await asyncio.gather(*tasks)
        # Display the list of stock prices returned by the completed tasks.
        print(f"[Loop] All parallel calls finished. Results: {results}")

        # Pair each requested function call with the result produced for it.
        for call, result in zip(response.function_calls, results):
            # Add this tool result to the conversation history in Gemini's expected format.
            history.append(types.Content(
                # Mark this as a user-side tool response sent back to Gemini.
                role="user",
                # Include the function name and its returned result.
                parts=[types.Part.from_function_response(name=call.name, response={"result": result})]
            ))

        # Ask Gemini again now that it has the stock prices and can answer the question.
        final_response = client.models.generate_content(
            # Use the same Gemini model for the final answer.
            model="gemini-flash-latest",
            # Send the complete conversation, including the stock-price results.
            contents=history
        )
        # Print Gemini's final human-readable answer to the terminal.
        print(f"\n[Final Response]:\n{final_response.text}")

# Start the asynchronous program and pass in the question to answer.
asyncio.run(run_parallel_agent("What is the difference in price between AAPL and MSFT?"))
