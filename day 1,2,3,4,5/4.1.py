def route_request(user_input: str) -> str:
    user_input = user_input.lower()
    if "weather" in user_input:
        return "TOOL: get_weather"
    elif "calculate" in user_input or "+" in user_input or "-" in user_input or "*" in user_input or "/" in user_input:
        return "TOOL: calculate"   
    elif "hello" in user_input or "hi" in user_input:
        return "response :hello i am here to assist you"
    else:
        return " response: i an in learning stage now"


test_inputs = ["What's the weather today?", "calculate 5+3", "hi", "tell me a joke"]


for msg in test_inputs:
    response = route_request(msg)
    print(f"User : {msg} => Assistant: {response}")