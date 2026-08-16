from dotenv import load_dotenv
from google import genai 
from google.genai import types


load_dotenv(override=True)

client = genai.Client()

def get_recipe(dish:str) -> str:
    fake_recipe = {
        "chicken curry" : "chicken",
        "mutton curry" : "mutton",
        "omlette" : "eggs"
    }

    return fake_recipe.get(dish.lower(), "no dish found")

def check_ingredients(ingredient:str) -> str:
    fake_stock = {
        "chicken" : "2 kg available",
        "eggs" : "12 available",
        "mutton" : "0 kg available"
    }

    return fake_stock.get(ingredient.lower(), "no ingredient available")

def convert_units(amount:int, to_unit:str, from_unit:str)-> str:
    fake_units = {
        "cups" : 240,
        "kg" : 1000,
        "ml" : 1,
        "g" : 1 
    }
    base = amount * fake_units.get(from_unit.lower(), 1.0)
    final = base / fake_units.get(to_unit.lower(), 1.0)

    return f"{final: .2f} {to_unit}"



TOOL_MAP = {
    "get_recipe":get_recipe,
    "check_ingredients" : check_ingredients,
    "convert_units" :convert_units
}

history = [types.Content(
    role="user",
    parts = [types.Part.from_text(
        text="i want to make chicken curry, check what is the main ingredient and if i have that in enough stock and convert 2 cups of chicken into kg"
    )]
)]

for turn in range(3):
    response = client.models.generate_content(
        model = "gemini-flash-latest",
        contents = history,
        config = types.GenerateContentConfig(
            tools = [get_recipe, check_ingredients, convert_units],
            automatic_function_calling = types.AutomaticFunctionCallingConfig(
                disable=True
            )
        )
    )

    history.append(response.candidates[0].content)

    if response.function_calls:
        for call in response.function_calls:
            main_func = TOOL_MAP[call.name]
            res = main_func(**call.args)

            print(f"Round {turn+1} : {call.name}({call.args}) -> {res}")

            history.append(
                types.Content(
                    role="user",
                    parts=[types.Part.from_function_response(
                        name=call.name,
                        response={"result":res}
                    )]
                )
            )

    else:
        print(f" Final response : {response.text}")
        break