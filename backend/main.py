from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn

from models.game_models import (
    GameState, EmailThread, PlayerAction, ActionOutcome, 
    SustainabilityGameState, PolicyProposal, Department
)
from game.game_engine import SustainabilityGameEngine

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

# Global game instance (in production, this would be per-session)
game_engine = SustainabilityGameEngine()

@app.get("/")
async def root():
    return {"message": "Welcome to Mailopolis! 🏙️"}

@app.get("/api/game/state")
async def get_game_state():
    """Get current sustainability game state and metrics"""
    return game_engine.get_game_status()

@app.get("/api/departments")
async def get_departments():
    """Get all city departments with their current sustainability scores"""
    return {
        "departments": [
            {
                "name": dept.value,
                "sustainability_score": game_engine.game_state.department_scores.get(dept, 50)
            }
            for dept in [Department.ENERGY, Department.TRANSPORTATION, Department.HOUSING, 
                        Department.WASTE, Department.WATER, Department.ECONOMIC_DEV]
        ],
        "overall_index": game_engine.game_state.sustainability_index
    }

@app.get("/api/round/start")
async def start_new_round():
    """Start a new round of the adversarial sustainability game"""
    return game_engine.start_new_round()

@app.get("/api/blockchain/analysis")
async def get_blockchain_analysis():
    """Get blockchain transaction analysis for player intelligence gathering"""
    return game_engine.get_blockchain_analysis()

@app.get("/api/bad-actors")
async def get_bad_actors():
    """Get information about active bad actors and their recent activities"""
    return {
        "active_bad_actors": {
            actor.id: {
                "name": actor.name,
                "type": actor.type.value,
                "influence_power": actor.influence_power,
                "remaining_budget": actor.corruption_budget,
                "target_departments": [dept.value for dept in actor.target_departments],
                "active": actor.active
            }
            for actor in game_engine.game_state.active_bad_actors.values()
        }
    }

@app.post("/api/proposals/submit")
async def submit_policy_proposal(
    title: str,
    description: str, 
    target_department: str
):
    """Submit a sustainability policy proposal as a player"""
    try:
        dept = Department(target_department)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid department: {target_department}")
    
    proposal = game_engine.submit_player_proposal(title, description, dept)
    return {
        "success": True,
        "proposal_id": proposal.id,
        "message": f"Policy proposal '{title}' submitted to {dept.value} department"
    }

@app.post("/api/mayor/decide")
async def mayor_decide_on_proposals():
    """Trigger mayor to make decisions on all pending proposals"""
    decisions = game_engine.mayor_decide_on_proposals()
    return {
        "decisions": decisions,
        "new_sustainability_index": game_engine.game_state.sustainability_index,
        "round_number": game_engine.game_state.round_number
    }

@app.get("/api/proposals/pending")
async def get_pending_proposals():
    """Get all pending policy proposals"""
    return {
        "proposals": [
            {
                "id": prop.id,
                "title": prop.title,
                "description": prop.description,
                "proposed_by": prop.proposed_by,
                "target_department": prop.target_department.value,
                "bribe_amount": prop.bribe_amount,
                "created_at": prop.created_at.isoformat()
            }
            for prop in game_engine.game_state.pending_proposals
        ]
    }

@app.post("/api/game/advance-day")
async def advance_day():
    """Advance to the next day"""
    game_engine.advance_day()
    return {
        "success": True,
        "new_day": game_engine.game_state.day,
        "message": f"Advanced to day {game_engine.game_state.day}"
    }

@app.get("/api/game/actions-remaining")
async def get_actions_remaining():
    """Get remaining actions for today"""
    remaining = game_engine.max_actions_per_day - game_engine.actions_taken_today
    return {
        "actions_taken": game_engine.actions_taken_today,
        "actions_remaining": remaining,
        "max_per_day": game_engine.max_actions_per_day
    }

@app.post("/api/game/reset")
async def reset_game():
    """Reset the sustainability game to initial state"""
    global game_engine
    game_engine = SustainabilityGameEngine()
    return {"success": True, "message": "Sustainability game reset successfully"}

# Development and gameplay endpoints
@app.get("/api/win-conditions")
async def check_win_conditions():
    """Check current win and loss condition status"""
    win_conditions = game_engine._check_win_conditions()
    loss_conditions = game_engine._check_loss_conditions()
    
    return {
        "win_conditions": win_conditions,
        "loss_conditions": loss_conditions,
        "game_over": any(loss_conditions.values()),
        "victory": any(win_conditions.values()),
        "round_number": game_engine.game_state.round_number,
        "max_rounds": game_engine.max_rounds
    }

@app.get("/api/player-stats")
async def get_player_stats():
    """Get player performance statistics"""
    return {
        "mayor_trust": game_engine.game_state.mayor_trust_in_player,
        "consecutive_rejections": game_engine.player_consecutive_rejections,
        "max_consecutive_rejections": game_engine.max_consecutive_rejections,
        "sustainability_index": game_engine.game_state.sustainability_index,
        "bad_actor_influence": game_engine.game_state.bad_actor_influence,
        "round_number": game_engine.game_state.round_number
    }

# Add LangChain-powered game endpoints 
from langchain_api import add_langchain_endpoints
add_langchain_endpoints(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)