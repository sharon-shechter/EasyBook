import threading
import time
from fastapi import FastAPI
from backend.database.database import engine, Base
from backend.api.routes import userRoutes, lessonRoutes, agentRoutes
from backend.agent.chat_agent import cleanup_old_sessions  # Import cleanup function

app = FastAPI(title="EasyBook API", version="1.0")

# Create database tables (if they don't exist)
Base.metadata.create_all(bind=engine)

# Include API routes
app.include_router(userRoutes.router, prefix="/users", tags=["Users"])
app.include_router(lessonRoutes.router, prefix="/lessons", tags=["Lessons"]) 
app.include_router(agentRoutes.router, prefix="/agent")

@app.get("/")
def home():
    return {"message": "Welcome to EasyBook API!"}

# Start the cleanup thread once when the application starts
cleanup_thread = threading.Thread(target=cleanup_old_sessions, daemon=True)
cleanup_thread.start()
