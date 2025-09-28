"""
Game API endpoints for Mailopolis
Provides HTTP access to the game engine functionality
"""

from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import json

from agents.langchain_agents import LangChainAgentManager
from game.langchain_game_engine import MaylopolisGameEngine
from models.game_models import PolicyProposal, Department, ProposalCategory


class ProposalRequest(BaseModel):
    """Request model for submitting proposals"""
    title: str
    description: str
    proposing_department: Department
    category: ProposalCategory
    estimated_cost: float
    estimated_timeline_months: int
    expected_impact_description: str


class GameStateResponse(BaseModel):
    """Response model for game state"""
    current_turn: int
    city_stats: Dict[str, Any]
    game_status: str
    events: List[Dict[str, Any]]


class TurnRequest(BaseModel):
    """Request model for playing a turn"""
    proposals: List[ProposalRequest]


# Global game instance - in production, this would be per-session
game_engine: Optional[MaylopolisGameEngine] = None
agent_manager: Optional[LangChainAgentManager] = None


async def get_game_engine() -> MaylopolisGameEngine:
    """Get or create the game engine instance"""
    global game_engine, agent_manager
    
    if game_engine is None:
        agent_manager = LangChainAgentManager()
        game_engine = MaylopolisGameEngine(
            agent_manager=agent_manager,
            max_turns=20,
            target_sustainability=80,
            min_approval=30
        )
    
    return game_engine


def create_game_api() -> FastAPI:
    """Create the FastAPI game application"""
    
    app = FastAPI(
        title="Mailopolis Game API",
        description="Political maneuvering game where agents negotiate and mayors decide",
        version="1.0.0"
    )
    
    @app.post("/game/start", response_model=GameStateResponse)
    async def start_game():
        """Start a new game session"""
        try:
            engine = await get_game_engine()
            game_state = await engine.start_game()
            
            return GameStateResponse(
                current_turn=game_state['current_turn'],
                city_stats=game_state['city_stats'],
                game_status=game_state['game_status'],
                events=game_state.get('events', [])
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to start game: {str(e)}")
    
    
    @app.get("/game/state", response_model=GameStateResponse)
    async def get_game_state():
        """Get current game state"""
        try:
            engine = await get_game_engine()
            
            # Return current state
            return GameStateResponse(
                current_turn=engine.current_turn,
                city_stats=engine.city_stats.__dict__,
                game_status=engine.game_status,
                events=[]
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get game state: {str(e)}")
    
    
    @app.post("/game/suggestions")
    async def get_proposal_suggestions():
        """Get suggested proposals for the current turn"""
        try:
            engine = await get_game_engine()
            suggestions = await engine.get_suggested_proposals()
            
            # Convert to dict format
            suggestion_dicts = []
            for suggestion in suggestions:
                suggestion_dicts.append({
                    'title': suggestion.title,
                    'description': suggestion.description,
                    'proposing_department': suggestion.proposing_department.value,
                    'category': suggestion.category.value,
                    'estimated_cost': suggestion.estimated_cost,
                    'estimated_timeline_months': suggestion.estimated_timeline_months,
                    'expected_impact_description': suggestion.expected_impact_description
                })
            
            return {
                'suggestions': suggestion_dicts,
                'count': len(suggestion_dicts)
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get suggestions: {str(e)}")
    
    
    @app.post("/game/turn")
    async def play_turn(turn_request: TurnRequest):
        """Play a turn with the provided proposals"""
        try:
            engine = await get_game_engine()
            
            # Convert request proposals to PolicyProposal objects
            proposals = []
            for prop_req in turn_request.proposals:
                proposal = PolicyProposal(
                    title=prop_req.title,
                    description=prop_req.description,
                    proposing_department=prop_req.proposing_department,
                    category=prop_req.category,
                    estimated_cost=prop_req.estimated_cost,
                    estimated_timeline_months=prop_req.estimated_timeline_months,
                    expected_impact_description=prop_req.expected_impact_description
                )
                proposals.append(proposal)
            
            # Play the turn
            turn_result = await engine.play_turn(player_proposals=proposals)
            
            return {
                'turn_result': turn_result,
                'success': True
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to play turn: {str(e)}")
    
    
    @app.get("/game/conversation-history")
    async def get_conversation_history():
        """Get recent conversation history"""
        try:
            engine = await get_game_engine()
            
            # Get conversation memory
            from agents.conversation_memory import ConversationMemory
            memory = ConversationMemory()
            
            # Get recent conversations (last 10)
            recent_convos = memory.get_recent_conversations(limit=10)
            
            return {
                'conversations': recent_convos,
                'count': len(recent_convos)
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get conversation history: {str(e)}")
    
    
    @app.get("/game/departments")
    async def get_departments():
        """Get list of available departments"""
        return {
            'departments': [dept.value for dept in Department if dept != Department.MAYOR],
            'all_departments': [dept.value for dept in Department]
        }
    
    
    @app.get("/game/categories")
    async def get_proposal_categories():
        """Get list of available proposal categories"""
        return {
            'categories': [cat.value for cat in ProposalCategory]
        }
    
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {"status": "healthy", "service": "mailopolis-game-api"}
    
    
    return app


# Create the app instance
app = create_game_api()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("game_api:app", host="0.0.0.0", port=8001, reload=True)