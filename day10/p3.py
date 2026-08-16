# Build an agent with 3 dependent tools: 
# get_workout_plan(goal) (e.g. "strength"/"cardio" → returns a workout name)
# → get_exercise_list(workout_name) (returns list of exercises) → 
# estimate_calories_burned(workout_name) (returns a number). 
# Must persist history to a JSON file across runs, use try/except, 
# and prove multi-turn (turn 2 references turn 1 without restating the workout name).


import json
import os
from dotenv import load_dotenv
load_dotenv(override=True)
from langchain.agents import create_agent

HIST_FILE = "workout.json"

def load_history() ->list:  # takes the memory and gives it to llm in form of python pbject
    if os.path.exists(HIST_FILE):
        with open(HIST_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(messages):
    with open(HIST_FILE, "w") as f:
        return json.dump(messages, f, indent=2)

def get_workout_plan(goal):
    """gets workout plan for the user goal"""
    fake_goal = {
        "cardio" : "training",
        "muscles" : "yoga"
    }
    return fake_goal.get(goal.lower(), "no goal")

def get_exercise_list(workout_name):
    """gets list of exercise for the given workout name"""
    fake_list = {
        "training" : ["squats", "pushups"],
        "yoga" : ["vajrasan", "pull-ups"]
    }
    return fake_list.get(workout_name.lower(), "no data")

def estimate_calories_burned(workout_name):
    """gets the number of calories burned for given workout name"""
    fake_calories = {
        "training" : 500,
        "yoga" : 400
    }
    return fake_calories.get(workout_name.lower(), "no data")

agent = create_agent(
    model="google_genai:gemini-flash-latest",
    tools=[get_workout_plan, get_exercise_list, estimate_calories_burned],
    system_prompt="you are an helpful gym assistant"
)

def get_answer(result):
    final_answer = result["messages"][-1]
    if isinstance(final_answer.content, str):
        return final_answer.content
    return final_answer.content[0]["text"]

messages = load_history()
messages.append({
    "role" : "user",
    "content" : "my goal is to do cardio so tell me what exercises do i need to do and how many calories will i burn?"
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
        return f" agent falied : {e}"


messages_to_save = []

for m in result["messages"]:
    if m.type in ["human", "ai"]:
        messages_to_save.append({
            "role" : m.type,
            "content" : m.content
        })

save_history(messages_to_save)

