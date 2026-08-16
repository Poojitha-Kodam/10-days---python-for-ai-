
fake_response = {
    "model": "claude-sonet-5",
    "role": "assistant",
    "content": [
        {"type": "text", "text": "the sky is blue in color"}
    ],
    "usage": {"input_tokens": 12,
              "output_tokens" : 6}
}

first_block = fake_response["model"]

second_block = fake_response["content"][0]
print(second_block)
print(second_block["text"])

for block in fake_response['content']:
  if block["type"] == "text":
    print("model said:", block["text"])


total_tokens = fake_response["usage"]["input_tokens"] + fake_response["usage"]["output_tokens"]
print(total_tokens)