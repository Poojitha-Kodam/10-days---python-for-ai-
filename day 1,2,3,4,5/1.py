def build_prompt(user_name: str, topic: str) -> str:
  prompt = f"you are a helpful assistant. {user_name} wants to know about {topic}. explain it simply."
  return prompt 

name = input("enter your name")
topic = input("enter your topic ")

final_prompt = build_prompt(name, topic)

print("final prompt")

print(final_prompt)
print("length of prompt:", len(final_prompt),"characters")


# def build_system_prompt(role:str, tone:str, constraints:str) -> str:
#   prompt = f"you are a {role}. Respond in a {tone} tone. constraints: {constraints}"
#   return prompt 

# role = input("enter role")
# tone = input("enter tone")
# constraints = input("enter contraints")


# final_system_prompt = build_system_prompt(role, tone, constraints)

# print(final_system_prompt)

