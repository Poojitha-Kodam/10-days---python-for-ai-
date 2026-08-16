from dotenv import load_dotenv
load_dotenv(override=True)
from langchain.agents import create_agent


def get_customer_id(email: str) -> str:
    """Looks up a customer's ID from their email."""
    db = {"priya@mail.com": "cust-001", "raj@mail.com": "cust-002"}
    return db.get(email.lower(), "not found")


def get_subscription_tier(customer_id: str) -> str:
    """Gets the subscription tier for a given customer ID."""
    tiers = {"cust-001": "premium", "cust-002": "free"}
    return tiers.get(customer_id.lower(), "unknown")


def check_priority_eligible(tier: str) -> str:
    """Checks if a subscription tier qualifies for priority support."""
    return "Eligible for priority support" if tier.lower() == "premium" else "Not eligible — standard support only"


agent = create_agent(
    model="google_genai:gemini-flash-latest",
    tools=[get_customer_id, get_subscription_tier, check_priority_eligible],
    system_prompt="You are a helpful customer support assistant."
)


def get_answer(result) -> str:
    final_message = result["messages"][-1]
    if isinstance(final_message.content, str):
        return final_message.content
    return final_message.content[0]["text"]


def agent_run(messages: list) -> tuple[str, list]:
    """Runs one agent turn, returns (answer, updated_messages) — or fails gracefully."""
    try:
        result = agent.invoke({"messages": messages})
        return get_answer(result)
    except Exception as e:
        return f"Agent call failed: {e}", messages


# Turn 1 — triggers the full dependency chain: email -> customer ID -> tier -> eligibility
messages = [{"role": "user", "content": "Is priya@mail.com eligible for priority support?"}]
answer= agent_run(messages)
print("Turn 1:", answer)

print("\n" + "="*50 + "\n")

# Turn 2 — only answerable correctly if history genuinely carried over from turn 1
messages = messages + [{"role": "user", "content": "What tier are they on again?"}]
answer = agent_run(messages)
print("Turn 2:", answer)