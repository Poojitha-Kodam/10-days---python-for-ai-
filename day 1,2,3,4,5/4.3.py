def pick_model(budget: str, task: str) -> str:
    task = task.lower()
    budget = budget.lower()
    if budget == "low":
        return "haiku"
    elif budget == "high" and task == "coding":
        return "opus"
    elif budget == "high" and task == "chat":
        return "sonnet"
    else: return "sonnet"


texts = [("high", "chatting"),
 ("low", "coding"),
  ("high", "coding"),
   ("low", "questioning")]

for i in texts:
    response = pick_model(i[0], i[1])
    print(f"for budget {i[0]} : task {i[1]} ==> model : {response}")







