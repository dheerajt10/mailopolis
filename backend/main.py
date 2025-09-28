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

# Add AgentMail endpoints
from agentmail_api import add_agentmail_endpoints
add_agentmail_endpoints(app)

# Add LangChain-powered game endpoints (main game)
from langchain_api import add_langchain_endpoints
add_langchain_endpoints(app)

if __name__ == "__main__":
    # Run the FastAPI app directly 
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)