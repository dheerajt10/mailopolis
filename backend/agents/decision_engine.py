from typing import Dict, List, Optional, Tuple
import random
import numpy as np
from models.game_models import (
    Agent, PlayerAction, ActionOutcome, GameState, 
    EmailThread, Message, StateEffect, OutcomeType,
    Department, DecisionStyle, PriorityType
)

class AgentDecisionEngine:
    """
    Core system for how agents make decisions.
    Each agent has different personalities that affect their choices.
    """
    
    def __init__(self):
        self.decision_history: Dict[str, List[PlayerAction]] = {}
        
    def evaluate_player_action(
        self, 
        agent: Agent, 
        action: PlayerAction, 
        thread: EmailThread,
        game_state: GameState
    ) -> Tuple[bool, float]:
        """
        Determines if an agent accepts/follows player advice.
        Returns (accepted, confidence_score)
        """
        
        # Base acceptance based on trust level
        base_acceptance = agent.trust_level / 100.0
        
        # Personality modifiers
        personality_modifier = self._get_personality_modifier(agent, action, game_state)
        
        # Context modifiers (crisis, budget, etc.)
        context_modifier = self._get_context_modifier(agent, thread, game_state)
        
        # Mayor approval effect (if approval is low, agents are more resistant)
        approval_modifier = self._get_approval_modifier(agent, game_state)
        
        # Calculate final acceptance probability
        final_probability = base_acceptance + personality_modifier + context_modifier + approval_modifier
        final_probability = max(0.05, min(0.95, final_probability))  # Clamp between 5-95%
        
        accepted = random.random() < final_probability
        
        return accepted, final_probability
    
    def _get_personality_modifier(self, agent: Agent, action: PlayerAction, game_state: GameState) -> float:
        """Different personalities react differently to different action types"""
        
        personality = agent.personality
        modifier = 0.0
        
        # Decision style effects
        if personality.decision_style == DecisionStyle.CAUTIOUS:
            if action.type.value == "ask":  # Cautious agents like when you ask first
                modifier += 0.15
            elif action.type.value == "advise" and not action.content:
                modifier -= 0.1  # Don't like vague advice
                
        elif personality.decision_style == DecisionStyle.AGGRESSIVE:
            if action.type.value == "advise":
                modifier += 0.1  # Like decisive action
            elif action.type.value == "ask":
                modifier -= 0.05  # Impatient with questions
                
        elif personality.decision_style == DecisionStyle.COLLABORATIVE:
            if action.type.value == "forward":
                modifier += 0.2  # Love involving others
            
        elif personality.decision_style == DecisionStyle.BUREAUCRATIC:
            if action.type.value == "ask":
                modifier += 0.1  # Want proper procedure
            if game_state.budget < 500000:  # Worried about budget
                modifier -= 0.15
        
        # Priority-based modifiers
        for priority in personality.priorities:
            if priority.type == PriorityType.BUDGET and game_state.budget < 750000:
                modifier -= 0.1 * priority.weight
            elif priority.type == PriorityType.APPROVAL and game_state.approval < 60:
                modifier -= 0.15 * priority.weight
            elif priority.type == PriorityType.HEALTH and game_state.city_health < 70:
                modifier += 0.1 * priority.weight
        
        return modifier
    
    def _get_context_modifier(self, agent: Agent, thread: EmailThread, game_state: GameState) -> float:
        """Context like crises, thread priority affects acceptance"""
        
        modifier = 0.0
        
        # Crisis urgency
        if thread.crisis_level == "critical":
            modifier += 0.2  # More likely to accept help during crisis
        elif thread.crisis_level == "high":
            modifier += 0.1
            
        # Thread priority
        if thread.priority > 80:
            modifier += 0.1
        elif thread.priority < 30:
            modifier -= 0.05
            
        # Department-specific logic
        if agent.department == Department.FINANCE:
            # Finance is always worried about budget
            if game_state.budget < 600000:
                modifier -= 0.2
        
        elif agent.department == Department.HOSPITAL:
            # Hospital prioritizes health metrics
            if game_state.city_health < 60:
                modifier += 0.15
                
        elif agent.department == Department.POWER_GRID:
            # PowerGrid cares about sustainability
            if game_state.sustainability_metrics.emissions > 900:
                modifier += 0.1
        
        return modifier
    
    def _get_approval_modifier(self, agent: Agent, game_state: GameState) -> float:
        """When mayor approval is low, agents become resistant"""
        
        if game_state.approval < 50:
            # Agents start to doubt the Shadow Mayor
            resistance = (50 - game_state.approval) / 100.0
            return -resistance * 0.3  # Up to -30% acceptance
        
        elif game_state.approval > 80:
            # High approval gives bonus acceptance
            bonus = (game_state.approval - 80) / 100.0
            return bonus * 0.2  # Up to +20% acceptance
            
        return 0.0

class AgentResponseGenerator:
    """
    Generates realistic email responses from agents based on their personalities
    """
    
    def __init__(self):
        self.response_templates = self._load_response_templates()
    
    def generate_response(
        self, 
        agent: Agent, 
        action: PlayerAction, 
        accepted: bool,
        thread: EmailThread
    ) -> str:
        """Generate a response email from an agent"""
        
        # Select template based on action type and acceptance
        template_key = f"{action.type.value}_{accepted}"
        templates = self.response_templates.get(template_key, [])
        
        if not templates:
            return "I'll look into this."
        
        # Pick template based on personality
        template = self._select_template_by_personality(agent, templates)
        
        # Fill in template with agent-specific details
        return self._fill_template(template, agent, action, thread)
    
    def _load_response_templates(self) -> Dict[str, List[Dict]]:
        """Load email response templates for different scenarios"""
        return {
            "ask_True": [
                {
                    "template": "Good question. Let me check our {metric} data and get back to you within {time_estimate}.",
                    "personality_match": ["cautious", "collaborative"]
                },
                {
                    "template": "I'll pull those numbers right now. Expect a full report in {time_estimate}.",
                    "personality_match": ["aggressive", "technical"]
                }
            ],
            "ask_False": [
                {
                    "template": "I'm swamped with the {current_crisis} situation. Can this wait?", 
                    "personality_match": ["aggressive"]
                },
                {
                    "template": "I'd need to go through proper channels for that information. Maybe try the Mayor's office?",
                    "personality_match": ["bureaucratic", "cautious"]
                }
            ],
            "advise_True": [
                {
                    "template": "That's a solid approach. I'll implement {action_summary} immediately.",
                    "personality_match": ["collaborative", "aggressive"]
                },
                {
                    "template": "After reviewing the proposal, I agree. Moving forward with {action_summary}.",
                    "personality_match": ["cautious", "bureaucratic"]
                }
            ],
            "advise_False": [
                {
                    "template": "I appreciate the input, but I think we need a different approach here.",
                    "personality_match": ["cautious", "collaborative"]
                },
                {
                    "template": "That won't work with our current budget constraints. We need to be more realistic.",
                    "personality_match": ["bureaucratic"]
                }
            ],
            "forward_True": [
                {
                    "template": "Great idea to loop in {new_participants}. They'll have the expertise we need.",
                    "personality_match": ["collaborative"]
                }
            ],
            "forward_False": [
                {
                    "template": "I think we can handle this internally. No need to involve more departments right now.",
                    "personality_match": ["bureaucratic", "cautious"]
                }
            ]
        }
    
    def _select_template_by_personality(self, agent: Agent, templates: List[Dict]) -> Dict:
        """Pick the best template for this agent's personality"""
        
        personality_style = agent.personality.decision_style.value
        
        # Find templates that match personality
        matching = [t for t in templates if personality_style in t.get("personality_match", [])]
        
        if matching:
            return random.choice(matching)
        else:
            return random.choice(templates)
    
    def _fill_template(self, template: Dict, agent: Agent, action: PlayerAction, thread: EmailThread) -> str:
        """Fill in template variables with context"""
        
        response = template["template"]
        
        # Replace common variables
        replacements = {
            "time_estimate": f"{agent.get_response_time()} minutes",
            "metric": self._infer_metric_from_thread(thread),
            "current_crisis": thread.crisis_level or "ongoing",
            "action_summary": action.content[:50] + "..." if action.content else "the suggested changes",
            "new_participants": ", ".join(action.new_participants or [])
        }
        
        for key, value in replacements.items():
            response = response.replace(f"{{{key}}}", str(value))
        
        return response
    
    def _infer_metric_from_thread(self, thread: EmailThread) -> str:
        """Guess what metric they're asking about from thread context"""
        
        if "power" in thread.subject.lower():
            return "energy consumption"
        elif "hospital" in thread.subject.lower():
            return "capacity utilization" 
        elif "transit" in thread.subject.lower():
            return "ridership"
        elif "budget" in thread.subject.lower():
            return "expenditure"
        else:
            return "performance"