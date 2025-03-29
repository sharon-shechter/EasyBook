def get_tools():
    return (
         {
            "type": "function",
            "function": {
                "name": "create_lesson_tool",
                "description": "Creates a new lesson given the required details.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "format": "date",
                            "description": "The date of the lesson in YYYY-MM-DD format"
                        },
                        "start_time": {
                            "type": "string",
                            "format": "time",
                            "description": "The start time of the lesson in HH:MM format"
                        },
                        "end_time": {
                            "type": "string",
                            "format": "time",
                            "description": "The end time of the lesson in HH:MM format"
                        },
                        "duration": {
                            "type": "integer",
                            "description": "Duration of the lesson in minutes"
                        },
                        "lesson_type": {
                            "type": "string",
                            "description": "Home or Zoom"
                        },
                        "lesson_adress": {
                            "type": "string",
                            "description": "Address where the lesson will take place - if applicable"
                        },
                        "lesson_name": {
                            "type": "string",
                            "description": "Name or title of the lesson like math or algebra"
                        },
                        "class_number": {
                            "type": "integer",
                            "description": "Class number or grade of the student"
                        }
                    },
                    "required": [
                        "date", "start_time", "end_time", "duration",
                        "lesson_type", "lesson_name", "class_number"
                    ]
                }
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
            
    )
