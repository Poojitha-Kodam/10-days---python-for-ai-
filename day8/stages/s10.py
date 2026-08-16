from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(override=True)
client = genai.Client()


# --- TOOL 1: independent ---
def get_destination_info(city: str) -> str:
    """Gets the country a given city is located in."""
    fake_cities = {
        "paris": "france",
        "tokyo": "japan",
        "bangalore": "india"
    }
    return fake_cities.get(city.lower(), "unknown")


# --- TOOL 2: depends on tool 1's output (the country) ---
def get_exchange_rate(country: str) -> str:
    """Gets the local currency's exchange rate to USD for a country."""
    fake_rates = {
        "france": "1 USD = 0.92 EUR",
        "japan": "1 USD = 149 JPY",
        "india": "1 USD = 83 INR"
    }
    return fake_rates.get(country.lower(), "no data")


# --- TOOL 3: independent, own conversion table ---
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Converts an amount between two currencies."""
    rates = {"usd": 1.0, "eur": 0.92, "jpy": 149.0, "inr": 83.0}
    usd_amount = amount / rates.get(from_currency.lower(), 1.0)
    result = usd_amount * rates.get(to_currency.lower(), 1.0)
    return f"{result:.2f} {to_currency.upper()}"


TOOL_MAP = {
    "get_destination_info": get_destination_info,
    "get_exchange_rate": get_exchange_rate,
    "convert_currency": convert_currency
}


def run_agent_turn(history: list, user_question: str) -> list:
    """Runs one full agent loop for a new user question, using existing history."""
    history.append(types.Content(role="user", parts=[types.Part.from_text(text=user_question)]))

    for turn in range(4):
        try:
            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=history,
                config=types.GenerateContentConfig(
                    tools=[get_destination_info, get_exchange_rate, convert_currency],
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
                )
            )
        except Exception as e:
            print(f"API call failed: {e}")
            return history  # bail out gracefully, don't crash, keep whatever history we had

        history.append(response.candidates[0].content)

        if response.function_calls:
            for call in response.function_calls:
                real_function = TOOL_MAP[call.name]
                result = real_function(**call.args)
                print(f"Round {turn+1}: {call.name}({call.args}) -> {result}")

                history.append(types.Content(
                    role="user",
                    parts=[types.Part.from_function_response(name=call.name, response={"result": result})]
                ))
        else:
            print("\nFinal answer:", response.text)
            break

    return history


# --- Turn 1 ---
conversation_history = []
conversation_history = run_agent_turn(
    conversation_history,
    "I'm traveling to Paris — what currency will I need and what's the exchange rate?"
)

print("\n" + "="*50 + "\n")

# --- Turn 2 — only answerable correctly if history genuinely carried over ---
conversation_history = run_agent_turn(
    conversation_history,
    "Convert 200 USD to that currency."
)