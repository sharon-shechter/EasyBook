import openai
import os
import json
from fastapi import HTTPException
from backend.database.database import get_db
from backend.repositories.userRepositorie import get_user_by_id
from sqlalchemy.orm import Session
from backend.schemas.lessonSchema import LessonCreate
from backend.repositories.lessonRepositorie import get_all_user_lessons
from backend.services.Google_apiService import authenticate_google_calendar 
from backend.services.lessonService import create_lesson_service, delete_lesson_service, get_possible_time_slots


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# In-memory storage for conversation history
local_storage = {}  # { user_id: conversation_history }


# Tool function for lesson creation
def create_lesson_tool(lesson_data: LessonCreate, db: Session, user_id: int):
    try:
        service = authenticate_google_calendar()
        new_lesson = create_lesson_service(db, lesson_data, user_id, 0, service)
        return new_lesson
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create lesson - {e}")


# Tool function for deleting a lesson
def delete_lesson_tool(lesson_id: int, db: Session, user_id: int):
    try:
        service = authenticate_google_calendar()
        delete_lesson_service(lesson_id, user_id, service, db)
        return {"status": "success", "message": "Lesson deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete lesson - {e}")


# Tool function for fetching all lessons
def get_lessons_tool(db: Session, user_id: int ):
    try:
        lessons = get_all_user_lessons(db, user_id)
        return lessons
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch lessons - {e}")


# Chatbot conversation function that continues based on history
def chatbot_conversation(db: Session, user_id: int, user_input: str):
    # Retrieve conversation history or start a new one
    if user_id not in local_storage:
        local_storage[user_id] = []

    conversation_history = local_storage[user_id]

    # ✅ Ensure system message is only added once
    if not any(msg["role"] == "system" for msg in conversation_history):
        conversation_history.insert(0, {"role": "system", "content": "You are a helpful assistant guiding a user to manage their lessons."})

    # Add user input to conversation history
    conversation_history.append({"role": "user", "content": user_input})

    # Generate response from OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=conversation_history,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "create_lesson_tool",
                    "description": "Creates a new lesson given the required details.",
                    "parameters": json.loads(LessonCreate.schema_json())  
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_lesson_tool",
                    "description": "Deletes a lesson by ID.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "lesson_id": {"type": "integer", "description": "The ID of the lesson to delete"}
                        },
                        "required": ["lesson_id"]
                    }
                }
            },
                    {
                "type": "function",
                "function": {
                    "name": "get_lessons_tool",
                    "description": "Fetches all lessons for a specific user.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "integer",
                                "description": "The ID of the user whose lessons should be retrieved."
                            }
                        },
                        "required": ["user_id"]
                    }
                }
            },  
         
    ]
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
                
                elif function_name == "get_lessons_tool":
                    result = get_lessons_tool(db, user_id)
                    assistant_reply = f"Here are your lessons: {result}" if result else "No lessons found."

                # Store function response in history
                conversation_history.append({"role": "assistant", "content": assistant_reply})

            except Exception:
                assistant_reply = "An error occurred while processing your request."

    # Update the stored history
    local_storage[user_id] = conversation_history

    return {"response": assistant_reply}


# 