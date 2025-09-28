from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn

from models.game_models import (
    GameState, EmailThread, PlayerAction, ActionOutcome, 
    SustainabilityGameState, PolicyProposal, Department
)
from agents.agent_personalities import AgentPersonalities, AgentPersonality


app = FastAPI(
    title="Mailopolis - Adversarial Sustainability Game",
    description="Compete against bad actors to maximize city sustainability",
    version="2.0.0"
)

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