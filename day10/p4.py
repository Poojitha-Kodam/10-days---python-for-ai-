import json
import os

from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv(override=True)


# ============================================================
# CONFIGURATION
# ============================================================

HISTORY_FILE = "library_history.json"


# ============================================================
# DAY 10 — LOAD HISTORY
# ============================================================

def load_history():

    if os.path.exists(HISTORY_FILE):

        try:

            with open(HISTORY_FILE, "r") as file:

                return json.load(file)

        except json.JSONDecodeError:

            print(
                "History file is corrupted."
            )

            return []

        except Exception as e:

            print(
                f"Could not load history: {e}"
            )

            return []

    return []


# ============================================================
# DAY 10 — SAVE HISTORY
# ============================================================

def save_history(messages):

    try:

        with open(HISTORY_FILE, "w") as file:

            json.dump(
                messages,
                file,
                indent=2
            )

    except Exception as e:

        print(
            f"Could not save history: {e}"
        )


# ============================================================
# TOOL 1
# ============================================================

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


# ============================================================
# DAY 9 — CREATE AGENT
# ============================================================

agent = create_agent(

    model="google_genai:gemini-flash-latest",

    tools=[
        find_book_id,
        check_book_availability,
        get_due_date
    ],

    system_prompt="""
    You are a helpful library assistant.

    When the user asks about a book:

    1. Find its book ID.
    2. Check whether it is available.
    3. If it is checked out, use the due-date tool.
    4. Never invent library information.

    Explain the result clearly.
    """
)


# ============================================================
# DAY 9 — GET ANSWER
# ============================================================

def get_answer(result):

    final_message = result["messages"][-1]

    if isinstance(
        final_message.content,
        str
    ):

        return final_message.content

    return final_message.content[0]["text"]


# ============================================================
# DAY 5 — ERROR HANDLING
# ============================================================

def run_agent(messages):

    try:

        result = agent.invoke(
            {
                "messages": messages
            }
        )

        return get_answer(result)

    except Exception as e:

        return f"Agent failed: {e}"


# ============================================================
# MESSAGE HELPER
# ============================================================

def add_message(
    messages,
    role,
    content
):

    messages.append(
        {
            "role": role,
            "content": content
        }
    )


# ============================================================
# DAY 3 — MENU
# ============================================================

def main():

    messages = load_history()

    print("=" * 60)
    print("             LIBRARY AI ASSISTANT")
    print("=" * 60)

    if messages:

        print(
            "Previous conversation loaded."
        )

    else:

        print(
            "Starting a new conversation."
        )

    while True:

        print("\n")
        print("1. Ask about a book")
        print("2. View conversation")
        print("3. Clear history")
        print("4. Exit")

        choice = input(
            "\nChoose: "
        )

        # ----------------------------------------------------
        # ASK
        # ----------------------------------------------------

        if choice == "1":

            question = input(
                "\nYou: "
            )

            if not question.strip():

                print(
                    "Please enter a question."
                )

                continue

            add_message(
                messages,
                "user",
                question
            )

            answer = run_agent(
                messages
            )

            print(
                f"\nAgent: {answer}"
            )

            add_message(
                messages,
                "assistant",
                answer
            )

            save_history(
                messages
            )

        # ----------------------------------------------------
        # VIEW
        # ----------------------------------------------------

        elif choice == "2":

            print(
                "\nConversation:"
            )

            print("-" * 50)

            if not messages:

                print(
                    "No conversation yet."
                )

            else:

                for message in messages:

                    print(
                        f"{message['role'].upper()}: "
                        f"{message['content']}"
                    )

        # ----------------------------------------------------
        # CLEAR
        # ----------------------------------------------------

        elif choice == "3":

            messages = []

            save_history(
                messages
            )

            print(
                "History cleared."
            )

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        elif choice == "4":

            save_history(
                messages
            )

            print(
                "Conversation saved."
            )

            break

        else:

            print(
                "Invalid option."
            )


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":

    main()