def agent_loop(text:str) -> str:
    text = text.lower()
    if "weather" in text:
        return "tool : weather"
    elif "calculate" in text:
        return "tool : calculate"
    elif "search" in text:
        return "tool : search"
    else:
        return "direct"


counts = {"weather" : 0,  "calculate" : 0, "search" : 0, "direct" : 0}


texts = ["what is the weather", "calculate this", "search for this", "hello", "is weather good"]

for i in texts:
    response = agent_loop(i)
    print(f"{i} : {response}")
    if "weather" in response:
        counts["weather"] += 1
    elif "calculate" in response:
        counts["calculate"] += 1
    elif "search" in response:
        counts["search"] += 1
    else:
        counts["direct"] += 1

print(counts)