"""
API endpoints for LangChain-powered sustainability game
"""

import asyncio
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from game.langchain_game_engine import LangChainGameEngine
from models.game_models import PolicyProposal, Department

# Initialize LangChain-powered game engine
langchain_game_engine = LangChainGameEngine(use_openai=True)

class LangChainPolicyProposal(BaseModel):
    title: str
    description: str
    target_department: str  # Will be converted to Department enum
    sustainability_impact: int
    economic_impact: int = 0
    political_impact: int = 0

class LangChainGameAPI:
    """LangChain-powered game API endpoints"""
    
    @staticmethod
    async def submit_proposal(proposal_data: LangChainPolicyProposal) -> Dict:
        """Submit a proposal to be evaluated by LangChain agents"""
        try:
            # Convert string department to enum
            dept_enum = Department(proposal_data.target_department.upper())
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid department: {proposal_data.target_department}")
        
        # Create policy proposal
        proposal = PolicyProposal(
            title=proposal_data.title,
            description=proposal_data.description,
            target_department=dept_enum,
            sustainability_impact=proposal_data.sustainability_impact,
            economic_impact=proposal_data.economic_impact,
            political_impact=proposal_data.political_impact,
            proposed_by="player"
        )
        
        # Submit proposal using LangChain engine
        result = await langchain_game_engine.submit_player_proposal(proposal)
        
        return result
    
    @staticmethod
    async def mayor_decide() -> Dict:
        """Have the LangChain-powered mayor decide on all pending proposals"""
        if not langchain_game_engine.game_state.pending_proposals:
            raise HTTPException(status_code=400, detail="No pending proposals to decide on")
        
        # Mayor makes decisions using LangChain
        decisions = await langchain_game_engine.mayor_decide_on_proposals()
        
        return {
            "decisions": decisions,
            "game_state": langchain_game_engine.get_game_status()
        }
    
    @staticmethod
    async def preview_proposal(proposal_data: LangChainPolicyProposal) -> Dict:
        """Get agent perspectives on a hypothetical proposal without submitting it"""
        try:
            dept_enum = Department(proposal_data.target_department.upper())
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid department: {proposal_data.target_department}")
        
        proposal = PolicyProposal(
            title=proposal_data.title,
            description=proposal_data.description,
            target_department=dept_enum,
            sustainability_impact=proposal_data.sustainability_impact,
            economic_impact=proposal_data.economic_impact,
            political_impact=proposal_data.political_impact,
            proposed_by="player"
        )
        
        # Get preview using LangChain engine
        preview = await langchain_game_engine.get_agent_preview(proposal)
        
        return preview
    
    @staticmethod
    def get_game_status() -> Dict:
        """Get current LangChain game status and agent information"""
        status = langchain_game_engine.get_game_status()
        
        # Add agent personality info
        agent_info = {}
        for dept, agent in langchain_game_engine.agent_manager.agents.items():
            personality = agent.personality
            agent_info[dept.value] = {
                "name": personality.name,
                "role": personality.role,
                "core_values": personality.core_values,
                "communication_style": personality.communication_style,
                "corruption_resistance": personality.corruption_resistance,
                "sustainability_focus": personality.sustainability_focus,
                "political_awareness": personality.political_awareness,
                "risk_tolerance": personality.risk_tolerance
            }
        
        status["agents"] = agent_info
        return status

# FastAPI endpoint integration
def add_langchain_endpoints(app: FastAPI):
    """Add LangChain game endpoints to FastAPI app"""
    
    @app.post("/api/langchain/proposals/submit")
    async def submit_proposal(proposal: LangChainPolicyProposal):
        return await LangChainGameAPI.submit_proposal(proposal)
    
    @app.post("/api/langchain/mayor/decide")
    async def mayor_decide():
        return await LangChainGameAPI.mayor_decide()
    
    @app.post("/api/langchain/proposals/preview")
    async def preview_proposal(proposal: LangChainPolicyProposal):
        return await LangChainGameAPI.preview_proposal(proposal)
    
    @app.get("/api/langchain/game/status")
    def get_game_status():
        return LangChainGameAPI.get_game_status()
    
    @app.get("/api/langchain/agents")
    def get_agent_personalities():
        """Get detailed information about all agent personalities"""
        from agents.agent_personalities import AgentPersonalities
        personalities = AgentPersonalities.get_all_personalities()
        
        return {
            dept.value: {
                "name": personality.name,
                "role": personality.role,
                "department": personality.department.value,
                "core_values": personality.core_values,
                "communication_style": personality.communication_style,
                "decision_factors": personality.decision_factors,
                "corruption_resistance": personality.corruption_resistance,
                "sustainability_focus": personality.sustainability_focus,
                "political_awareness": personality.political_awareness,
                "risk_tolerance": personality.risk_tolerance
            } for dept, personality in personalities.items()
        }
    
    @app.post("/api/langchain/proposals/counter")
    async def generate_counter_proposal(original_proposal: LangChainPolicyProposal):
        """Generate counter-proposals for rejected proposals"""
        try:
            dept_enum = Department(original_proposal.target_department.upper())
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid department: {original_proposal.target_department}")
        
        proposal = PolicyProposal(
            title=original_proposal.title,
            description=original_proposal.description,
            target_department=dept_enum,
            sustainability_impact=original_proposal.sustainability_impact,
            economic_impact=original_proposal.economic_impact,
            political_impact=original_proposal.political_impact,
            proposed_by="player"
        )
        
        counter_proposals = await langchain_game_engine.generate_counter_proposals(proposal)
        
        return {
            "original_proposal": {
                "title": proposal.title,
                "department": proposal.target_department.value
            },
            "counter_proposals": [
                {
                    "title": cp.title,
                    "description": cp.description,
                    "department": cp.target_department.value,
                    "sustainability_impact": cp.sustainability_impact,
                    "proposed_by": cp.proposed_by
                } for cp in counter_proposals
            ]
        }