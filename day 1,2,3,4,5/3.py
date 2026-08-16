response = {
    "model": "claude-sonet-5",
    "role": "assistant",
    "message": {"role": "user",
                "content": "what is the weather",
                "timestamp": 234567345}
}

# for block in response["message"]:
#   if block["role"] == "user":
#     print(f"{block['content']}")


print(f"[{response["message"]["role"]}] : {response["message"]["content"]}")



print()
print()



conversation = [
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello! How can I help?"},
    {"role": "user", "content": "What's 2+2?"},
    {"role": "assistant", "content": "4"}
]


for i in conversation:
  print(f"{i["role"]} : {i["content"]}")


user_c = 0
assis_c = 0

for i in conversation:
  if i["role"] == "user":
    user_c+=1
  elif i["role"] == "assistant":
    assis_c += 1
print(f"count of user msgs: {user_c} and count of assistant msgs: {assis_c}")



print()
print()


api_response = {
    "id": "msg_01",
    "content": [
        {"type": "text", "text": "Let me check that for you."},
        {"type": "tool_use", "name": "get_weather", "input": {"city": "Bangalore", "unit": "celsius"}}
    ],
    "stop_reason": "tool_use"
}

for block in api_response["content"]:
  if block["type"] == "text":
    print("model says:", block["text"])
  elif block["type"] == "tool_use":
    print(f"Tool call: {block["name"]} with args: {block["input"]}")
    print(f"{block["input"]["city"]}")