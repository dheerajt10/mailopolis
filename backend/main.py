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

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React/Vite common ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to Mailopolis! 🏙️"}

# Add LangChain-powered game endpoints 
from langchain_api import add_langchain_endpoints
add_langchain_endpoints(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)