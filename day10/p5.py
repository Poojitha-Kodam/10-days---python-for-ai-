import json
import os

from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv(override=True)


HIST_FILE = "lib.json"

# load_history
def load_history():
    if os.path.exists(HIST_FILE):
        try:
            with open(HIST_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            return f"file not found : {e}"
    return []

# save_history
def save_history(messages):
    try:
        with open(HIST_FILE, "w") as f:
            return json.dump(messages, f, indent=2)
    except Exception as e:
        return f"file not found : {e}"


def find_book_id(title: str) -> str:
    """
    Find book ID from title.
    """

    books = {

        "harry potter": "BOOK001",

        "atomic habits": "BOOK002",

        "python crash course": "BOOK003",

        "the alchemist": "BOOK004"
    }

    return books.get(
        title.lower(),
        "book not found"
    )


# ============================================================
# TOOL 2
# ============================================================

def check_book_availability(book_id: str) -> str:
    """
    DEPENDS ON find_book_id().
    """

    availability = {

        "BOOK001": "checked out",

        "BOOK002": "available",

        "BOOK003": "available",

        "BOOK004": "checked out"
    }

    return availability.get(
        book_id,
        "unknown book"
    )


# ============================================================
# TOOL 3
# ============================================================

def get_due_date(book_id: str) -> str:
    """
    Only useful when the book is checked out.
    """

    due_dates = {

        "BOOK001": "September 5, 2026",

        "BOOK004": "August 28, 2026"
    }

    return due_dates.get(
        book_id,
        "no due date available"
    )

# create_agent

agent = create_agent(
    model="google_genai:gemini-flash-latest",
    tools=[find_book_id, check_book_availability, get_due_date],
    system_prompt = "you are a helpful assistant and based on tools answer the user questions"
)

def get_answer(result):
    final_answer = result["messages"][-1]
    try:
        if isinstance(final_answer.content, str):
            return final_answer.content
        else:
            return final_answer.content[0]["text"]
    except Exception as e:
        return f"exception :{e}"


def add_message(messages, role, content):
    return messages.append({
        "role" : role,
        "content" : content
    })


def run_agent(messages):
    try:
        result = agent.invoke(
            {
                "messages" : messages
            }
        )
        return get_answer(result)
    except Exception as e:
        return f"agent failed : {e}"

def main():
    messages = load_history()

    print("=" * 60)
    print("             LIBRARY AI ASSISTANT")
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

        choice = input("\n Choose:")

        if choice == "1":
            ques = input("\n You :")
            if not ques.strip():
                print("please enter the question")
            
            add_message(messages, "user", ques)

            answer = run_agent(messages)

            print(f"agent answer : {answer}")

            add_message(messages, "assistant", answer)

            save_history(messages)

        elif choice == "2":
            print("\n Conversation")

            if not messages:
                print("no conversation yet")
            else:
                for message in messages:
                    print(
                        f"{message["role"].upper()} : "
                        f"{message["content"]}"
                    )
        
        elif choice == "3":
            messages = []

            save_history(messages)

            print("\n History deleted")

        elif choice == "4":
            save_history(messages)
            print("Conversation saved")

            break
        else:
            print("Invalid choice!!")


if __name__ == "__main__":
    main()
