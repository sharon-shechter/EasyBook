import openai
import os
import json
from fastapi import HTTPException 
from backend.agent.tools import get_tools
from backend.database.database import get_db
from backend.repositories.userRepositorie import get_user_by_id
from sqlalchemy.orm import Session
from backend.schemas.lessonSchema import LessonCreate
from backend.services.Google_apiService import authenticate_google_calendar
from backend.services.lessonService import create_lesson_service

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


local_storage = {}  


def create_lesson_tool(lesson_data: LessonCreate, db: Session, user_id: int):
    try:
        service = authenticate_google_calendar()
        new_lesson = create_lesson_service(db, lesson_data, user_id, 0, service)
        return new_lesson
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create lesson - {e}")


# Chatbot conversation function that continues based on history
def chatbot_conversation(db: Session, user_id: int, user_input: str):
    # Retrieve conversation history or start a new one
    if user_id not in local_storage:
        local_storage[user_id] = []

    conversation_history = local_storage[user_id]

    if not any(msg["role"] == "system" for msg in conversation_history):
        conversation_history.insert(0, {"role": "system", "content": "You are a helpful assistant guiding a user to create a new lesson."})
        print(local_storage)
        conversation_history = local_storage[user_id]

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
                }
            ],
            api_key=OPENAI_API_KEY
        )

        assistant_reply = response["choices"][0]["message"].get("content", "")

        if assistant_reply:
            conversation_history.append({"role": "assistant", "content": assistant_reply})

        # Handle function calls (Lesson Creation)
        if "tool_calls" in response["choices"][0]["message"]:
            for tool_call in response["choices"][0]["message"]["tool_calls"]:
                if tool_call["function"]["name"] == "create_lesson_tool":
                    try:
                        lesson_params = json.loads(tool_call["function"]["arguments"])
                        if not lesson_params:
                            return {"error": "No valid parameters received for lesson creation."}

                        lesson_data = LessonCreate(**lesson_params)
                        created_lesson = create_lesson_tool(lesson_data, db, user_id)

                        if created_lesson:
                            assistant_reply = "Lesson created successfully."
                        else:
                            assistant_reply = "Failed to create the lesson. Please try again."

                    except json.JSONDecodeError:
                        assistant_reply = "Error processing lesson details. Please try again."
                    except Exception:
                        assistant_reply = "An unexpected error occurred. Please try again."

                    # Add response to conversation history
                    conversation_history.append({"role": "assistant", "content": assistant_reply})

        # Update the stored history
        local_storage[user_id] = conversation_history

        return {"response": assistant_reply}