# Requirements — every single one maps to a specific day you've already done:
# A menu loop (Day 3 — conditionals/loops): on startup, show options like 1. Ask the agent something  2. View saved conversation  3. Exit, loop until the user picks exit.
# At least 4 tools, with a genuine 2-step dependency chain (Day 6/8/9): e.g. get_account_id(email) → get_transactions(account_id) → categorize_spending(transactions) → check_budget_status(category, amount) (your own design, doesn't have to match exactly — just needs real dependency, not just independent lookups).
# create_agent + agent.invoke() (Day 9) as the actual reasoning engine — no manual loop needed this time, you've already proven you can build that by hand.
# try/except around every real API call (Day 5) — menu should never crash the whole program on a failed call; print an error and return to the menu instead.
# File persistence (Day 10) — load conversation history from a JSON file on startup, save it after every turn, so closing and reopening the program preserves context.
# Genuine multi-turn proof — ask the agent something, then in a separate menu interaction, ask a follow-up that only makes sense if history truly persisted (e.g. "what did you say my balance was again?").
# Classes optional but encouraged (Day 4) — e.g. wrap the menu logic or persistence logic in a small class if it feels natural; not mandatory, your call.

import json
import os

from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv(override=True)

HIST_FILE = "finance.json"

def load_history():
    if os.path.exists(HIST_FILE):
        try:
            with open(HIST_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            return f" Exception: {e}"
    return []

def save_history(messages):
    try:
        with open(HIST_FILE, "w") as f:
            return json.dump(messages, f, indent=2)
    except Exception as e:
        return f" Exception : {e}"

def get_account_id(email):
    """gets account id for given email"""
    fake_ids = {
        "poo@gmail.com" : "acc100",
        "gau@gmail.com" : "acc200"
    }
    return fake_ids.get(email.lower(), "no email found")

def get_transactions(account_id):
    """gets transactions for the particular account id"""
    fake_transactions = {
        "acc100" : [{"category":"food", "amount": 500},{"category":"groc", "amount": 700}, {"category":"food", "amount": 200}],
        "acc200" : [{"category":"food", "amount": 900}]
    }
    return fake_transactions.get(account_id.lower(), "no id found")

def categorize_spending(account_id, category):
    """categorize the amount based on category"""
    transactions = get_transactions(account_id)
    if isinstance(transactions, str):
        return 0
    total = 0
    for transaction in transactions:
        if transaction["category"].lower() == category.lower():
            total+=transaction["amount"]

    return total 

def budget_details(account_id, category, budget):
    """gets a budget details """
    total = categorize_spending(account_id, category)

    if budget >= total:
        remaining = budget - total
        return f"you have {remaining} remaining in budget, spending is in budget"
    else:
        exceeded = total - budget
        return f"you have exceeded the amount by {exceeded}"

agent = create_agent(
    model="google_genai:gemini-flash-latest",
    tools=[get_account_id, get_transactions, categorize_spending, budget_details],
    system_prompt="""you are an helpful assistant:

    Do not invent financial information.
    Only use information returned by the tools.
    """
)

def get_answer(result):
    final_answer = result["messages"][-1]
    try:
        if isinstance(final_answer.content, str):
            return final_answer.content
        return final_answer.content[0]["text"]
    except Exception as e:
        return f" agent failed to load : {e}"
    return []

def run_agent(messages):
    try:
        result = agent.invoke({
            "messages" : messages
        })
        return get_answer(result)
    except Exception as e:
        return f"agent failed : {e}"

def add_message(messages, role, content):
    return messages.append({
        "role":role,
        "content":content
    })


def main():
    messages = load_history()

    print("=" * 60)
    print("        FINANCE AI ASSISTANT")
    print("=" * 60)

    if messages:
        print("Continue the conversation")
    else:
        print("Start a new conversation")

    while True:
        print("\n Choose one of the below option:")
        print("\n 1. Ask your question")
        print("\n 2. View history")
        print("\n 3. Delete History")
        print("\n 4. Exit")

        choice = input("\n choose")

        if choice == "1":
            ques = input("\n You:")

            if not ques.strip():
                print("please enter your question")
                continue
            add_message(messages, "user", ques)

            answer = run_agent(messages)
            print(f"agent answer: {answer}")
            add_message(messages, "assistant", answer)

            save_history(messages)
        elif choice == "2":
            save_history(messages)

            print("\n Conversation")

            for message in messages:
                print(f"{message["role"].upper()} : {message["content"]}")

        elif choice == "3":
            messages = []

            save_history(messages)

            print("Conversation Deleted")

        elif choice == "4":
            save_history(messages)

            print("Conversation Saved")

            break
        else:
            print("invalid choice")



if __name__ == "__main__":
    main()

    