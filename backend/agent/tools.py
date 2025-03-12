from backend.schemas.lessonSchema import LessonCreate
import json

def get_tools():
    return {
        "type": "function",
        "function": {
            "name": "create_lesson_tool",
            "description": "Creates a new lesson given the required details.",
            "parameters": json.loads(LessonCreate.schema_json())
        }
    }
