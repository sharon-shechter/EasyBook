import openai
import os
import json
from datetime import date
from fastapi import HTTPException
from backend.database.database import get_db
from backend.schemas.userSchema import UserCreate
from backend.services.agentService import user_signup_tool
from backend.repositories.userRepositorie import get_user_by_id
from sqlalchemy.orm import Session
from backend.agent.tools import get_tools
from backend.schemas.lessonSchema import LessonCreate
from backend.services.agentService import create_lesson_tool, delete_lesson_tool, get_lessons_tool,possible_time_slots_tool , user_login_tool


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TODAY = date.today()

# In-memory storage for conversation history
local_storage = {}  



def chatbot_conversation(db: Session, user_id: int, user_input: str):
    # Retrieve conversation history or start a new one
    if user_id not in local_storage:
        local_storage[user_id] = []

    conversation_history = local_storage[user_id]
    if not any(msg["role"] == "system" for msg in conversation_history):
        conversation_history.insert(0, {"role": "system", "content": f'You are a helpful assistant guiding a user to manage their lessons. To day is {str(TODAY)}.'})

    # Add user input to conversation history
    conversation_history.append({"role": "user", "content": user_input})

    # Generate response from OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4",
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

                elif function_name == "user_signup_tool":
                    user_data = UserCreate(**function_args)
                    result = user_signup_tool(user_data, db)
                    assistant_reply = result if result else "User signup failed."

                

                # Store function response in history
                conversation_history.append({"role": "assistant", "content": assistant_reply})

            except Exception as e:
                assistant_reply = f"Error executing function: {str(e)}"
    # Update the stored history
    local_storage[user_id] = conversation_history

    return {"response": assistant_reply}


# 