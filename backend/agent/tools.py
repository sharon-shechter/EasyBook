from backend.schemas.lessonSchema import LessonCreate
from backend.schemas.userSchema import UserCreate, LoginRequest
import json

def get_tools():
    return (
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
        {
            "type": "function",
            "function": {
                "name": "possible_time_slots_tool",
                "description": "Finds possible time slots for scheduling a new lesson.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "lesson_date": {
                            "type": "string",
                            "format": "date",
                            "description": "The date of the lesson (YYYY-MM-DD)."
                        },
                        "lesson_address": {
                            "type": "string",
                            "description": "The location of the lesson."
                        },
                        "lesson_duration": {
                            "type": "integer",
                            "description": "Duration of the lesson in minutes."
                        }
                    },
                    "required": ["lesson_date", "lesson_address", "lesson_duration"]
                }
            }
        },
                        {
                    "type": "function",
                    "function": {
                        "name": "signup_tool",
                        "description": "Registers a new user with the provided details.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "email": {
                                    "type": "string",
                                    "format": "email",
                                    "description": "The user's email address."
                                },
                                "password": {
                                    "type": "string",
                                    "description": "The user's password."
                                },
                                "first_name": {
                                    "type": "string",
                                    "description": "The user's first name."
                                },
                                "last_name": {
                                    "type": "string",
                                    "description": "The user's last name."
                                },
                                "phone_number": {
                                    "type": "string",
                                    "description": "The user's phone number (optional)."
                                },
                                "address": {
                                    "type": "string",
                                    "description": "The user's address (optional)."
                                }
                            },
                            "required": ["email", "password", "first_name", "last_name"]
                        }
                    }
                }, 
        {
            "type": "function",
            "function": {
                "name": "login_tool",
                "description": "Authenticates a user and returns a JWT token.",
                "parameters": json.loads(LoginRequest.schema_json())
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_user_tool",
                "description": "Deletes a user by ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "The ID of the user to delete"}
                    },
                    "required": ["user_id"]
                }
            }
        }
    )
