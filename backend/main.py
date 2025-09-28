from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn

from models.game_models import (
    GameState, EmailThread, PlayerAction, ActionOutcome, 
    SustainabilityGameState, PolicyProposal, Department
)

app = FastAPI(
    title="Mailopolis - Adversarial Sustainability Game",
    description="Compete against bad actors to maximize city sustainability",
    version="2.0.0"
)

# Initialize agent email system on startup
@app.on_event("startup")
async def startup_event():
    """Initialize the agent email system"""
    try:
        from service.agent_mail import initialize_agent_inboxes
        from load_env import load_environment_variables
        
        # Load environment variables
        load_environment_variables()
        
        # Initialize agent inboxes
        inboxes = await initialize_agent_inboxes()
        print(f"📧 Initialized {len(inboxes)} agent email inboxes")
        
    except Exception as e:
        print(f"⚠️ Warning: Could not initialize agent emails: {e}")
        print("Email notifications will be disabled")

# Enable CORS for frontend - Allow everything
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
async def root():
    return {"message": "Welcome to Mailopolis! 🏙️"}


# Include the Maylopolis router (if available) under /maylopolis
try:
    from maylopolis_api import router as maylopolis_router
    app.include_router(maylopolis_router)
except Exception:
    # If the module isn't importable (e.g., missing deps during static analysis),
    # we silently skip including the router so the main app still runs.
    pass


if __name__ == "__main__":
    # Run the FastAPI app directly 
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)