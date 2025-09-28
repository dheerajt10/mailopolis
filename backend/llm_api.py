"""
API endpoints for LLM-powered sustainability game
"""

import asyncio
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from game.llm_game_engine import EnhancedSustainabilityGameEngine
from models.game_models import PolicyProposal, Department
from agents.llm_agents import OpenAIProvider, AnthropicProvider

# Initialize LLM-powered game engine
try:
    llm_provider = OpenAIProvider()
except:
    try:
        llm_provider = AnthropicProvider()
    except:
        from agents.llm_agents import MockLLMProvider
        llm_provider = MockLLMProvider()

llm_game_engine = EnhancedSustainabilityGameEngine(llm_provider=llm_provider)

class LLMPolicyProposal(BaseModel):
    title: str
    description: str
    target_department: str  # Will be converted to Department enum
    sustainability_impact: int
    economic_impact: int = 0
    political_impact: int = 0

class LLMGameAPI:
    """LLM-powered game API endpoints"""
    
    @staticmethod
    async def submit_llm_proposal(proposal_data: LLMPolicyProposal) -> Dict:
        """Submit a proposal to be evaluated by LLM agents"""
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
        
        # Add to pending proposals
        llm_game_engine.game_state.pending_proposals.append(proposal)
        
        # Get immediate reactions from all department agents
        agent_messages = await llm_game_engine.get_agent_messages(proposal)
        
        return {
            "proposal_id": proposal.id,
            "status": "submitted",
            "agent_reactions": agent_messages,
            "message": f"Proposal '{proposal.title}' submitted for mayor's review"
        }
    
    @staticmethod
    async def llm_mayor_decide() -> Dict:
        """Have the LLM-powered mayor decide on all pending proposals"""
        if not llm_game_engine.game_state.pending_proposals:
            raise HTTPException(status_code=400, detail="No pending proposals to decide on")
        
        # Mayor makes decisions using LLM
        decisions = await llm_game_engine.mayor_decide_on_proposals_llm()
        
        # Generate counter-proposals for rejected proposals
        counter_proposals = []
        for decision in decisions:
            if not decision["accepted"]:
                # Find the original proposal
                for proposal in llm_game_engine.game_state.pending_proposals:
                    if proposal.id == decision["proposal_id"]:
                        counters = await llm_game_engine.generate_counter_proposals(proposal)
                        counter_proposals.extend(counters)
                        break
        
        return {
            "decisions": decisions,
            "counter_proposals": [
                {
                    "title": cp.title,
                    "description": cp.description,
                    "department": cp.target_department.value,
                    "sustainability_impact": cp.sustainability_impact
                } for cp in counter_proposals
            ],
            "game_state": {
                "sustainability_index": llm_game_engine.game_state.sustainability_index,
                "department_scores": dict(llm_game_engine.game_state.department_scores),
                "mayor_trust": llm_game_engine.game_state.mayor_trust_in_player,
                "round_number": llm_game_engine.game_state.round_number
            }
        }
    
    @staticmethod
    async def get_agent_perspectives(proposal_data: LLMPolicyProposal) -> Dict:
        """Get all agent perspectives on a hypothetical proposal"""
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
        
        # Get all agent perspectives
        agent_messages = await llm_game_engine.get_agent_messages(proposal)
        
        # Also get mayor's perspective
        mayor_agent = llm_game_engine.llm_agents[Department.MAYOR]
        mayor_eval = await mayor_agent.evaluate_proposal(
            proposal=proposal,
            game_context={
                "sustainability_index": llm_game_engine.game_state.sustainability_index,
                "department_scores": dict(llm_game_engine.game_state.department_scores),
                "trust_in_player": llm_game_engine.game_state.mayor_trust_in_player,
                "preview_mode": True
            }
        )
        
        agent_messages.append({
            "from": mayor_agent.personality.name,
            "department": "MAYOR",
            "message": mayor_eval.reasoning,
            "likely_decision": "ACCEPT" if mayor_eval.accept else "REJECT",
            "confidence": mayor_eval.confidence,
            "concerns": mayor_eval.concerns
        })
        
        return {
            "proposal": {
                "title": proposal.title,
                "description": proposal.description,
                "department": proposal.target_department.value
            },
            "agent_perspectives": agent_messages,
            "game_context": {
                "sustainability_index": llm_game_engine.game_state.sustainability_index,
                "department_scores": dict(llm_game_engine.game_state.department_scores),
                "mayor_trust": llm_game_engine.game_state.mayor_trust_in_player
            }
        }
    
    @staticmethod
    def get_llm_game_status() -> Dict:
        """Get current LLM game status and agent information"""
        agent_info = {}
        
        for dept, agent in llm_game_engine.llm_agents.items():
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
        
        return {
            "game_state": {
                "sustainability_index": llm_game_engine.game_state.sustainability_index,
                "department_scores": dict(llm_game_engine.game_state.department_scores),
                "mayor_trust": llm_game_engine.game_state.mayor_trust_in_player,
                "bad_actor_influence": llm_game_engine.game_state.bad_actor_influence,
                "round_number": llm_game_engine.game_state.round_number
            },
            "agents": agent_info,
            "llm_provider": type(llm_provider).__name__,
            "pending_proposals": len(llm_game_engine.game_state.pending_proposals)
        }

# FastAPI endpoint integration
def add_llm_endpoints(app: FastAPI):
    """Add LLM game endpoints to FastAPI app"""
    
    @app.post("/api/llm/proposals/submit")
    async def submit_llm_proposal(proposal: LLMPolicyProposal):
        return await LLMGameAPI.submit_llm_proposal(proposal)
    
    @app.post("/api/llm/mayor/decide")
    async def llm_mayor_decide():
        return await LLMGameAPI.llm_mayor_decide()
    
    @app.post("/api/llm/proposals/preview")
    async def get_agent_perspectives(proposal: LLMPolicyProposal):
        return await LLMGameAPI.get_agent_perspectives(proposal)
    
    @app.get("/api/llm/game/status")
    def get_llm_game_status():
        return LLMGameAPI.get_llm_game_status()
    
    @app.get("/api/llm/agents")
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