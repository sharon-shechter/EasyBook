import openai
import os
import json
import time
from datetime import date
from backend.schemas.userSchema import UserCreate
from backend.services.agentService import user_signup_tool
from sqlalchemy.orm import Session
from backend.agent.tools import get_tools
from backend.schemas.lessonSchema import LessonCreate
from backend.services.agentService import create_lesson_tool, delete_lesson_tool, get_lessons_tool,possible_time_slots_tool 

EXPIRATION_TIME = 300

local_storage = {"1": {"messages": [], "timestamp": time.time()}}

def cleanup_old_sessions():
    while True:
        time.sleep(10)  
        current_time = time.time()
        
        for user_id in list(local_storage.keys()):  # Iterate over a copy of keys
            if current_time - local_storage[user_id]["timestamp"] > EXPIRATION_TIME:
                print(f"Deleting conversation history for user {user_id}")
                del local_storage[user_id]  # Remove expired user history




OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TODAY = date.today()

# In-memory storage for conversation history
def print_local_storage():
    print("Local storage:", local_storage)

def chatbot_conversation(db: Session, user_id: int, user_input: str):
    # Retrieve conversation history or start a new one
    if user_id not in local_storage:
        local_storage[user_id] = {
    "messages": [],
    "timestamp": time.time(),
   
}

    local_storage[user_id]["timestamp"] = time.time()  # Update last interaction time
    conversation_history = local_storage[user_id]["messages"]
    if not any(msg["role"] == "system" for msg in conversation_history):
        conversation_history.insert(0, {"role": "system", "content": f'You are a helpful assistant guiding a user to manage their lessons for the privet teacher - Sharon (male)  . To day is {str(TODAY)}. Talk shortly and simply"'})

    # Add user input to conversation history
    conversation_history.append({"role": "user", "content": user_input})

    # Generate response from OpenAI
    response = openai.ChatCompletion.create(
        model="o3-mini",
        messages=conversation_history,
        tools= get_tools()
    )

    assistant_reply = response["choices"][0]["message"].get("content", "")

    if assistant_reply:
        conversation_history.append({"role": "assistant", "content": assistant_reply})

    # Handle function calls
    if "tool_calls" in response["choices"][0]["message"]:
        print(response["choices"][0]["message"]["tool_calls"])
        for tool_call in response["choices"][0]["message"]["tool_calls"]:
            function_name = tool_call["function"]["name"]

            try:
                function_args = json.loads(tool_call["function"]["arguments"])
                
                if function_name == "create_lesson_tool":
                    lesson_data = LessonCreate(**function_args)
                    result = create_lesson_tool(lesson_data, db, user_id)
                    assistant_reply = "Lesson created successfully." 
                
                elif function_name == "delete_lesson_tool":
                    lesson_id = function_args["lesson_id"]
                    result = delete_lesson_tool(lesson_id, db, user_id)
                    assistant_reply = result["message"]
                
                elif function_name == "signup_tool":
                    print("Function detected: signup_tool")  # Debug print
                    user_data = UserCreate(**function_args)
                    print(f"Parsed user data: {user_data}")  # Debug print
                    
                    result = user_signup_tool(user_data, db)
                    print(f"Signup result: {result}")  # Debug print

                    assistant_reply = "User signed up successfully." if result else "Failed to sign up."


                elif function_name == "possible_time_slots_tool":
                    lesson_date = function_args["lesson_date"]
                    lesson_address = function_args["lesson_address"]
                    lesson_duration = function_args["lesson_duration"]
                    result = possible_time_slots_tool(lesson_date, lesson_address, lesson_duration, user_id)
                    assistant_reply = f"Possible time slots: {result}" if result else "No available time slots found."

                elif function_name == "get_lessons_tool":
                    result = get_lessons_tool(db, user_id)
                    if result:
                        lesson_lines = [
                            f"• {lesson['lesson_name'].capitalize()} on {lesson['date']} from {lesson['start_time']} to {lesson['end_time']} at {lesson['lesson_adress']} "  
                            for lesson in result
                        ]
                        assistant_reply = "Your lessons:\n" + "\n".join(lesson_lines)
                    else:
                        assistant_reply = "No lessons found."

                

                # Store function response in history
                conversation_history.append({"role": "assistant", "content": assistant_reply})

            except Exception as e:
                assistant_reply = f"Error executing function: {str(e)}"

    return {"response": assistant_reply}


# 