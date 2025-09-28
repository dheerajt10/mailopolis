"""
LangChain-powered game engine for Mailopolis
"""

from typing import Dict, List, Optional
import random
from datetime import datetime

from models.game_models import (
    SustainabilityGameState, BadActor, BadActorType, PolicyProposal,
    Department, BlockchainTransaction
)
from agents.langchain_agents import LangChainAgentManager, ProposalEvaluation

class LangChainGameEngine:
    """
    LangChain-powered sustainability game engine with sophisticated AI agents
    """
    
    def __init__(self, use_openai: bool = True):
        self.game_state = SustainabilityGameState()
        
        # Initialize LangChain agent manager
        self.agent_manager = LangChainAgentManager(use_openai=use_openai)
        
        # Initialize game components
        self._initialize_departments()
        self._initialize_bad_actors()
        
        # Game progression tracking
        self.round_number = 1
        self.max_rounds = 25
        self.player_consecutive_rejections = 0
        self.max_consecutive_rejections = 8
        
    def _initialize_departments(self):
        """Initialize all city departments with starting sustainability scores"""
        departments = [
            Department.ENERGY, Department.TRANSPORTATION, Department.HOUSING,
            Department.WASTE, Department.WATER, Department.ECONOMIC_DEV
        ]
        
        for dept in departments:
            # Random starting scores between 40-60
            score = random.randint(40, 60)
            self.game_state.department_scores[dept] = score
            
        # Calculate initial sustainability index
        self.game_state.sustainability_index = self.game_state.calculate_sustainability_index()
        
    def _initialize_bad_actors(self):
        """Create bad actors that will compete against the player"""
        bad_actors = [
            BadActor(
                name="Sprawl Development Corp",
                type=BadActorType.DEVELOPER_GROUP,
                influence_power=75,
                corruption_budget=500000,
                target_departments=[Department.HOUSING, Department.TRANSPORTATION]
            ),
            BadActor(
                name="Carbon Industries Lobby",
                type=BadActorType.FOSSIL_FUEL_COMPANY,
                influence_power=85,
                corruption_budget=750000,
                target_departments=[Department.ENERGY, Department.TRANSPORTATION]
            ),
            BadActor(
                name="Waste Management Cartel",
                type=BadActorType.CORPORATE_LOBBY,
                influence_power=60,
                corruption_budget=300000,
                target_departments=[Department.WASTE, Department.WATER]
            )
        ]
        
        for actor in bad_actors:
            self.game_state.active_bad_actors[actor.id] = actor
    
    def get_game_status(self) -> Dict:
        """Get current game status with LangChain agent info"""
        return {
            "sustainability_index": self.game_state.sustainability_index,
            "department_scores": dict(self.game_state.department_scores),
            "mayor_trust": self.game_state.mayor_trust_in_player,
            "bad_actor_influence": self.game_state.bad_actor_influence,
            "round_number": self.game_state.round_number,
            "llm_provider": self.agent_manager.provider_name,
            "pending_proposals": len(self.game_state.pending_proposals),
            "blockchain_transactions": len(self.game_state.blockchain_transactions)
        }
    
    async def submit_player_proposal(self, proposal: PolicyProposal) -> Dict:
        """Submit player proposal and get agent reactions"""
        
        # Add to pending proposals
        self.game_state.pending_proposals.append(proposal)
        
        # Get context for agents
        game_context = {
            "sustainability_index": self.game_state.sustainability_index,
            "department_scores": dict(self.game_state.department_scores),
            "trust_in_player": self.game_state.mayor_trust_in_player,
            "bad_actor_influence": self.game_state.bad_actor_influence,
            "round_number": self.game_state.round_number
        }
        
        # Get reactions from all department agents
        agent_reactions = await self.agent_manager.get_all_reactions(proposal, game_context)
        
        # Record submission on blockchain
        self.game_state.add_blockchain_transaction(
            from_agent="player",
            to_agent="mayor",
            transaction_type="proposal_submission",
            data={
                "proposal_id": proposal.id,
                "title": proposal.title,
                "target_department": proposal.target_department.value
            }
        )
        
        return {
            "proposal_id": proposal.id,
            "status": "submitted",
            "agent_reactions": agent_reactions,
            "message": f"Proposal '{proposal.title}' submitted for mayor's review"
        }
    
    async def mayor_decide_on_proposals(self) -> List[Dict]:
        """LangChain-powered mayor makes decisions on all pending proposals"""
        decisions = []
        
        game_context = {
            "sustainability_index": self.game_state.sustainability_index,
            "department_scores": dict(self.game_state.department_scores),
            "trust_in_player": self.game_state.mayor_trust_in_player,
            "bad_actor_influence": self.game_state.bad_actor_influence,
            "round_number": self.game_state.round_number
        }
        
        for proposal in self.game_state.pending_proposals:
            try:
                # Get LangChain-powered mayor decision
                evaluation = await self.agent_manager.mayor_decide(proposal, game_context)
                
                decision = {
                    "proposal_id": proposal.id,
                    "title": proposal.title,
                    "proposed_by": proposal.proposed_by,
                    "accepted": evaluation.accept,
                    "reasoning": evaluation.reasoning,
                    "confidence": evaluation.confidence,
                    "concerns": evaluation.concerns,
                    "sustainability_impact": proposal.sustainability_impact if evaluation.accept else 0
                }
                
                decisions.append(decision)
                
                # Implement policy if accepted
                if evaluation.accept:
                    await self._implement_policy(proposal, game_context)
                    
                    # Update mayor trust for player proposals
                    if proposal.proposed_by == "player":
                        self.game_state.mayor_trust_in_player = min(100, self.game_state.mayor_trust_in_player + 3)
                        self.player_consecutive_rejections = 0
                else:
                    if proposal.proposed_by == "player":
                        self.game_state.mayor_trust_in_player = max(0, self.game_state.mayor_trust_in_player - 5)
                        self.player_consecutive_rejections += 1
                
                # Record decision on blockchain
                self.game_state.add_blockchain_transaction(
                    from_agent="mayor",
                    to_agent=proposal.proposed_by,
                    transaction_type="policy_decision",
                    data={
                        "proposal_id": proposal.id,
                        "accepted": evaluation.accept,
                        "reasoning": evaluation.reasoning,
                        "confidence": evaluation.confidence
                    }
                )
                
            except Exception as e:
                # Fallback decision
                decision = {
                    "proposal_id": proposal.id,
                    "title": proposal.title,
                    "proposed_by": proposal.proposed_by,
                    "accepted": False,
                    "reasoning": f"Technical error in evaluation: {str(e)}",
                    "confidence": 0,
                    "concerns": ["Technical error"],
                    "sustainability_impact": 0
                }
                decisions.append(decision)
        
        # Clear pending proposals
        self.game_state.pending_proposals = []
        
        # Update round number
        self.game_state.round_number += 1
        
        return decisions
    
    async def _implement_policy(self, proposal: PolicyProposal, game_context: Dict):
        """Implement accepted policy and get department reactions"""
        target_dept = proposal.target_department
        
        # Update department scores
        if target_dept in self.game_state.department_scores:
            current_score = self.game_state.department_scores[target_dept]
            new_score = max(0, min(100, current_score + proposal.sustainability_impact))
            self.game_state.department_scores[target_dept] = new_score
            
            # Get department reaction using LangChain
            try:
                dept_context = {**game_context, "implementation_phase": True, "score_change": proposal.sustainability_impact}
                evaluation = await self.agent_manager.evaluate_proposal_by_department(
                    proposal, target_dept, dept_context
                )
                
                # Record department reaction on blockchain
                self.game_state.add_blockchain_transaction(
                    from_agent=target_dept.value,
                    to_agent="mayor",
                    transaction_type="department_reaction",
                    data={
                        "proposal_id": proposal.id,
                        "reaction": evaluation.reasoning,
                        "satisfaction": evaluation.confidence
                    }
                )
                
            except Exception as e:
                print(f"Failed to get department reaction: {e}")
            
            # Record score update on blockchain
            self.game_state.add_blockchain_transaction(
                from_agent="system",
                to_agent=target_dept.value,
                transaction_type="department_score_update",
                data={
                    "old_score": current_score,
                    "new_score": new_score,
                    "change": proposal.sustainability_impact,
                    "policy": proposal.title
                }
            )
        
        # Update overall sustainability index
        self.game_state.sustainability_index = self.game_state.calculate_sustainability_index()
        
        # Handle bribe payments for bad actors
        if proposal.bribe_amount > 0:
            for actor in self.game_state.active_bad_actors.values():
                if actor.id == proposal.proposed_by:
                    actor.corruption_budget -= proposal.bribe_amount
                    self.game_state.bad_actor_influence = min(100, self.game_state.bad_actor_influence + 2)
                    break
    
    async def generate_counter_proposals(self, rejected_proposal: PolicyProposal) -> List[PolicyProposal]:
        """Generate counter-proposals using LangChain agents"""
        counter_proposals = []
        
        game_context = {
            "sustainability_index": self.game_state.sustainability_index,
            "department_scores": dict(self.game_state.department_scores),
            "trust_in_player": self.game_state.mayor_trust_in_player,
            "bad_actor_influence": self.game_state.bad_actor_influence,
            "round_number": self.game_state.round_number
        }
        
        # Get counter-proposal from target department
        target_dept = rejected_proposal.target_department
        counter_proposal = await self.agent_manager.generate_counter_proposal(
            rejected_proposal, target_dept, game_context
        )
        
        if counter_proposal:
            counter_proposals.append(counter_proposal)
            
            # Record counter-proposal generation on blockchain
            self.game_state.add_blockchain_transaction(
                from_agent=target_dept.value,
                to_agent="player",
                transaction_type="counter_proposal",
                data={
                    "original_proposal_id": rejected_proposal.id,
                    "counter_proposal_title": counter_proposal.title,
                    "reasoning": "Department suggested alternative approach"
                }
            )
        
        return counter_proposals
    
    async def get_agent_preview(self, proposal: PolicyProposal) -> Dict:
        """Get preview of how agents would react to a proposal without submitting it"""
        
        game_context = {
            "sustainability_index": self.game_state.sustainability_index,
            "department_scores": dict(self.game_state.department_scores),
            "trust_in_player": self.game_state.mayor_trust_in_player,
            "bad_actor_influence": self.game_state.bad_actor_influence,
            "round_number": self.game_state.round_number,
            "preview_mode": True
        }
        
        # Get all agent reactions
        agent_reactions = await self.agent_manager.get_all_reactions(proposal, game_context)
        
        # Get mayor's likely decision
        mayor_evaluation = await self.agent_manager.mayor_decide(proposal, game_context)
        
        return {
            "proposal": {
                "title": proposal.title,
                "description": proposal.description,
                "department": proposal.target_department.value,
                "sustainability_impact": proposal.sustainability_impact
            },
            "agent_reactions": agent_reactions,
            "mayor_preview": {
                "likely_decision": "ACCEPT" if mayor_evaluation.accept else "REJECT",
                "reasoning": mayor_evaluation.reasoning,
                "confidence": mayor_evaluation.confidence,
                "concerns": mayor_evaluation.concerns
            },
            "game_context": game_context
        }