from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn

from models.game_models import GameState, EmailThread, PlayerAction, ActionOutcome
from game.game_engine import GameEngine

app = FastAPI(
    title="Mailopolis Backend",
    description="Email-based city management game backend",
    version="1.0.0"
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
game_engine = GameEngine()

@app.get("/")
async def root():
    return {"message": "Welcome to Mailopolis! 🏙️"}

@app.get("/api/game/state", response_model=GameState)
async def get_game_state():
    """Get current game state and metrics"""
    return game_engine.game_state

@app.get("/api/agents")
async def get_agents():
    """Get all agents with their current trust levels"""
    agents_info = []
    for agent in game_engine.agents.values():
        agents_info.append({
            "id": agent.id,
            "name": agent.name,
            "department": agent.department.value,
            "trust_level": agent.trust_level,
            "personality": {
                "decision_style": agent.personality.decision_style.value,
                "communication_style": agent.personality.communication_style.value,
                "risk_tolerance": agent.personality.risk_tolerance
            }
        })
    return {"agents": agents_info}

@app.get("/api/emails/digest", response_model=List[EmailThread])
async def get_daily_digest():
    """Get the top 3 email threads for the day"""
    return game_engine.get_daily_digest()

@app.get("/api/emails/{thread_id}")
async def get_thread(thread_id: str):
    """Get a specific email thread with all messages"""
    thread = game_engine.email_threads.get(thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    # Include agent names in messages for frontend display
    enriched_messages = []
    for message in thread.messages:
        agent = game_engine.agents.get(message.from_agent)
        enriched_messages.append({
            **message.dict(),
            "from_agent_name": agent.name if agent else "Unknown",
            "from_agent_department": agent.department.value if agent else "Unknown"
        })
    
    return {
        **thread.dict(),
        "messages": enriched_messages
    }

@app.post("/api/actions/ask", response_model=ActionOutcome)
async def process_ask_action(action: PlayerAction):
    """Process an ASK action"""
    if action.type.value != "ask":
        raise HTTPException(status_code=400, detail="Action type must be 'ask'")
    
    return game_engine.process_player_action(action)

@app.post("/api/actions/advise", response_model=ActionOutcome)
async def process_advise_action(action: PlayerAction):
    """Process an ADVISE action"""
    if action.type.value != "advise":
        raise HTTPException(status_code=400, detail="Action type must be 'advise'")
    
    return game_engine.process_player_action(action)

@app.post("/api/actions/forward", response_model=ActionOutcome)
async def process_forward_action(action: PlayerAction):
    """Process a FORWARD action"""
    if action.type.value != "forward":
        raise HTTPException(status_code=400, detail="Action type must be 'forward'")
    
    return game_engine.process_player_action(action)

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
    """Reset the game to initial state"""
    global game_engine
    game_engine = GameEngine()
    return {"success": True, "message": "Game reset successfully"}

# Development endpoint to see agent decision process
@app.post("/api/debug/simulate-action")
async def simulate_action(action: PlayerAction):
    """Debug endpoint to see how agents would react without actually processing"""
    
    thread = game_engine.email_threads.get(action.thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    results = {}
    
    # Show how each relevant agent would react
    for agent_id, agent in game_engine.agents.items():
        if agent.department.value in ['Citizens', 'Media']:
            continue
            
        accepted, confidence = game_engine.decision_engine.evaluate_player_action(
            agent, action, thread, game_engine.game_state
        )
        
        response = game_engine.response_generator.generate_response(
            agent, action, accepted, thread
        )
        
        results[agent_id] = {
            "name": agent.name,
            "department": agent.department.value,
            "would_accept": accepted,
            "confidence": confidence,
            "response": response,
            "trust_level": agent.trust_level,
            "personality": agent.personality.decision_style.value
        }
    
    return results

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)