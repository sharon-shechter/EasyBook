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




# Tool function for lesson creation
def create_lesson_tool(lesson_data: LessonCreate, db: Session, user_id: int):
    try:
        service = authenticate_google_calendar()
        new_lesson = create_lesson_service(db, lesson_data, user_id, 0, service)
        return new_lesson
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create lesson - {e}")

# Chatbot conversation loop
def chatbot_conversation(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        print("Chatbot: User not found. Exiting chat.")
        return

    conversation_history = [{"role": "system", "content": "You are a helpful assistant guiding a user to create a new lesson."}]

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break

        conversation_history.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=conversation_history,
            tools=get_tools(),
            api_key=OPENAI_API_KEY
        )
        assistant_reply = response["choices"][0]["message"].get("content")
        if assistant_reply is not None:
            print(f"Chatbot: {assistant_reply}")
            conversation_history.append({"role": "assistant", "content": assistant_reply})

        # Handle function calls
        if "tool_calls" in response["choices"][0]["message"]:
            for tool_call in response["choices"][0]["message"]["tool_calls"]:
                if tool_call["function"]["name"] == "create_lesson_tool":
                    try:
                        lesson_params = json.loads(tool_call["function"]["arguments"])
                        if not lesson_params:
                            print("Chatbot: No valid parameters received for lesson creation.")
                            continue

                        lesson_data = LessonCreate(**lesson_params)
                        created_lesson = create_lesson_tool(lesson_data, db, user_id)

                        if created_lesson:
                            return created_lesson
                        else:
                            print("Chatbot: Failed to create the lesson. Please try again.")

                    except json.JSONDecodeError:
                        print("Chatbot: Error processing lesson details. Please try again.")
                    except Exception:
                        print("Chatbot: An unexpected error occurred. Please try again.")
            
            break
