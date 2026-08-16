from dotenv import load_dotenv
load_dotenv(override=True)
from langchain.agents import create_agent


# Question
# Build a "Library Assistant": 3 tools with genuine dependency —
# find_book_id(title) → check_book_availability(book_id) →
# get_due_date(book_id) (only relevant if unavailable/checked out).
# Use create_agent, your own get_answer extractor, try/except, and
# prove multi-turn memory the same way (turn 1 asks about a book,
# turn 2 references it without restating the title).
# Build it from a blank file, paste code + real output when done.

def find_book(title:str) -> str:
    """gets book id for the title given """
    fake_books = {
        "harry potter" : "1",
        "you and me" : "2",
        "too good to be true" : "3"
    }
    return fake_books.get(title.lower(), "no book found")

def check_book_availability(book_id:str) -> str:
    """gets availability of book for the give book_id"""
    fake_availability = {
        "1": "available", 
        "2": "not available",
        "3": "available"
    }
    return fake_availability.get(book_id.lower(), "no book id found")

def get_due_date(book_id:str):
    """if book is not available then gets the due date of that book"""
    fake_due = {
        "1": "2/12/2026",
        "2": "5/9/2026",
        "3": "20/8/2026"
    }
    return fake_due.get(book_id.lower(), "no data")


agent = create_agent(
    model = "google_genai:gemini-flash-latest",
    tools = [find_book, check_book_availability, get_due_date],
    system_prompt = "you are an helpful library assistant"
)


def get_answer(result):
    final_answer = result["messages"][-1]
    if isinstance(final_answer.content, str):
        return final_answer.content
    return final_answer.content[0]["text"]

def run_agent(messages):
    try:
        result = agent.invoke({
            "messages" : messages
        })
        return get_answer(result)

    except Exception as e:
        return f"Agent call failed, {e}"



messages = [{"role":"user", "content":"what is the book id for 'you and me'?"}]
answer = run_agent(messages)
print(f"turn 1 , {answer}")



messages = messages + [
    {"role":"assistant", "content": answer},
    {"role":"user", "content":"is that book available if not what is the due date?"}
]
answer = run_agent(messages)
print(f"turn 2 , {answer}")