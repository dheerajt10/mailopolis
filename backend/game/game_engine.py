from typing import Dict, List, Optional, Tuple
import random
from datetime import datetime, timedelta
from models.game_models import (
    GameState, Agent, EmailThread, Message, PlayerAction, 
    ActionOutcome, Crisis, StateEffect, OutcomeType, Department
)
from agents.agent_factory import AgentFactory
from agents.decision_engine import AgentDecisionEngine, AgentResponseGenerator

class GameEngine:
    """
    Core game engine that manages state, agents, and email threads.
    This is where all the agent interactions happen.
    """
    
    def __init__(self):
        self.game_state = GameState()
        self.agents = AgentFactory.create_all_agents()
        self.email_threads: Dict[str, EmailThread] = {}
        self.active_crises: Dict[str, Crisis] = {}
        
        # Agent behavior systems
        self.decision_engine = AgentDecisionEngine()
        self.response_generator = AgentResponseGenerator()
        
        # Game progression tracking
        self.actions_taken_today = 0
        self.max_actions_per_day = 3
        
    def get_daily_digest(self) -> List[EmailThread]:
        """
        Get the top 3 most important email threads for the day.
        This is what the player sees each morning.
        """
        
        # Generate new threads if needed
        if len(self.email_threads) < 3:
            self._generate_daily_scenarios()
        
        # Sort threads by priority and return top 3
        all_threads = list(self.email_threads.values())
        active_threads = [t for t in all_threads if t.status == "active"]
        
        # Sort by priority (crisis level + priority score)
        def thread_importance(thread: EmailThread) -> float:
            base_priority = thread.priority
            crisis_bonus = {
                "critical": 50,
                "high": 30, 
                "medium": 15,
                "low": 5,
                None: 0
            }
            return base_priority + crisis_bonus.get(thread.crisis_level, 0)
        
        sorted_threads = sorted(active_threads, key=thread_importance, reverse=True)
        return sorted_threads[:3]
    
    def process_player_action(self, action: PlayerAction) -> ActionOutcome:
        """
        Process a player action and return the outcome.
        This is where agent decision-making happens.
        """
        
        if self.actions_taken_today >= self.max_actions_per_day:
            return ActionOutcome(
                success=False,
                type=OutcomeType.NEGATIVE,
                effects=[],
                message="You've reached your daily action limit (3 actions per day)."
            )
        
        # Get the thread and relevant agents
        thread = self.email_threads.get(action.thread_id)
        if not thread:
            return ActionOutcome(
                success=False,
                type=OutcomeType.NEGATIVE, 
                effects=[],
                message="Thread not found."
            )
        
        # Process the action based on type
        if action.type.value == "ask":
            return self._process_ask_action(action, thread)
        elif action.type.value == "advise":
            return self._process_advise_action(action, thread)
        elif action.type.value == "forward":
            return self._process_forward_action(action, thread)
        
        return ActionOutcome(
            success=False,
            type=OutcomeType.NEGATIVE,
            effects=[],
            message="Unknown action type."
        )
    
    def _process_ask_action(self, action: PlayerAction, thread: EmailThread) -> ActionOutcome:
        """
        Process an ASK action - requesting information from an agent.
        Different agents respond differently based on personality.
        """
        
        target_agent = self.agents.get(action.target_agent)
        if not target_agent:
            return ActionOutcome(
                success=False,
                type=OutcomeType.NEGATIVE,
                effects=[],
                message="Target agent not found."
            )
        
        # Evaluate if agent will respond positively
        accepted, confidence = self.decision_engine.evaluate_player_action(
            target_agent, action, thread, self.game_state
        )
        
        # Generate agent response
        response_text = self.response_generator.generate_response(
            target_agent, action, accepted, thread
        )
        
        # Create response message
        response_message = Message(
            thread_id=thread.id,
            from_agent=target_agent.id,
            to_agents=["shadow_mayor"],  # Player
            content=response_text
        )
        
        thread.messages.append(response_message)
        thread.last_activity = datetime.now()
        
        # Calculate outcome effects
        effects = []
        
        if accepted:
            # Successful ask reduces risk of bad advice later
            effects.append(StateEffect(
                metric="trust_level",
                agent_id=target_agent.id,
                delta=2,
                reason="Appreciated being consulted"
            ))
            
            outcome_type = OutcomeType.POSITIVE
            message = f"{target_agent.name} provided helpful information."
            
        else:
            # Failed ask might indicate strained relationship
            effects.append(StateEffect(
                metric="trust_level", 
                agent_id=target_agent.id,
                delta=-1,
                reason="Too busy to respond properly"
            ))
            
            outcome_type = OutcomeType.NEUTRAL
            message = f"{target_agent.name} was too busy to provide detailed information."
        
        self.actions_taken_today += 1
        return ActionOutcome(
            success=accepted,
            type=outcome_type,
            effects=effects,
            message=message
        )
    
    def _process_advise_action(self, action: PlayerAction, thread: EmailThread) -> ActionOutcome:
        """
        Process an ADVISE action - suggesting a course of action.
        This is where major game state changes happen.
        """
        
        # Find the decision-maker for this thread (usually mayor or department head)
        decision_maker = self._get_thread_decision_maker(thread)
        
        # Evaluate if they accept the advice
        accepted, confidence = self.decision_engine.evaluate_player_action(
            decision_maker, action, thread, self.game_state
        )
        
        # Generate response
        response_text = self.response_generator.generate_response(
            decision_maker, action, accepted, thread
        )
        
        response_message = Message(
            thread_id=thread.id,
            from_agent=decision_maker.id,
            to_agents=["shadow_mayor"],
            content=response_text
        )
        
        thread.messages.append(response_message)
        
        # Calculate major outcome effects
        effects = self._calculate_advice_effects(action, thread, accepted, decision_maker)
        
        # Update trust based on outcome
        trust_delta = 5 if accepted else -3
        effects.append(StateEffect(
            metric="trust_level",
            agent_id=decision_maker.id,
            delta=trust_delta,
            reason="Advice outcome"
        ))
        
        # Apply effects to game state
        self._apply_effects(effects)
        
        outcome_type = OutcomeType.POSITIVE if accepted else OutcomeType.NEGATIVE
        message = f"Advice {'accepted' if accepted else 'declined'} by {decision_maker.name}."
        
        # Mark thread as resolved if advice was accepted
        if accepted:
            thread.status = "resolved"
        
        self.actions_taken_today += 1
        return ActionOutcome(
            success=accepted,
            type=outcome_type,
            effects=effects,
            message=message
        )
    
    def _process_forward_action(self, action: PlayerAction, thread: EmailThread) -> ActionOutcome:
        """
        Process a FORWARD action - bringing new agents into the conversation.
        This enables agent-to-agent collaboration.
        """
        
        if not action.new_participants:
            return ActionOutcome(
                success=False,
                type=OutcomeType.NEGATIVE,
                effects=[],
                message="No new participants specified for forwarding."
            )
        
        # Add new participants to thread
        for agent_id in action.new_participants:
            if agent_id not in thread.participants:
                thread.participants.append(agent_id)
        
        # Generate collaborative response
        effects = []
        collaborative_bonus = len(action.new_participants) * 2
        
        # Different departments working together can solve problems better
        dept_synergy = self._calculate_department_synergy(thread)
        
        effects.extend([
            StateEffect(
                metric="city_health",
                delta=collaborative_bonus + dept_synergy,
                reason="Inter-department collaboration"
            ),
            StateEffect(
                metric="crisis_speed", 
                delta=1,  # Faster resolution
                reason="More resources applied"
            )
        ])
        
        # Trust bonus for good routing
        for agent_id in thread.participants:
            if agent_id in self.agents:
                effects.append(StateEffect(
                    metric="trust_level",
                    agent_id=agent_id,
                    delta=1,
                    reason="Effective collaboration"
                ))
        
        self._apply_effects(effects)
        
        message = f"Successfully involved {len(action.new_participants)} additional departments."
        
        self.actions_taken_today += 1
        return ActionOutcome(
            success=True,
            type=OutcomeType.POSITIVE,
            effects=effects,
            message=message
        )
    
    def _get_thread_decision_maker(self, thread: EmailThread) -> Agent:
        """Find who makes final decisions for this thread"""
        
        # Mayor makes final calls on high-priority items
        if thread.priority > 70 or thread.crisis_level in ["high", "critical"]:
            mayor_id = next((id for id, agent in self.agents.items() 
                           if agent.department == Department.MAYOR), None)
            if mayor_id:
                return self.agents[mayor_id]
        
        # Otherwise, department head decides
        for agent_id in thread.participants:
            agent = self.agents.get(agent_id)
            if agent and agent.department != Department.CITIZENS:
                return agent
        
        # Fallback to mayor
        mayor_id = next((id for id, agent in self.agents.items() 
                       if agent.department == Department.MAYOR), None)
        return self.agents[mayor_id]
    
    def _calculate_advice_effects(
        self, 
        action: PlayerAction, 
        thread: EmailThread, 
        accepted: bool, 
        decision_maker: Agent
    ) -> List[StateEffect]:
        """Calculate how advice affects game metrics"""
        
        effects = []
        
        if not accepted:
            return effects
        
        # Base effects depend on thread type and content
        if "power" in thread.subject.lower():
            effects.extend(self._power_grid_effects(action, decision_maker))
        elif "hospital" in thread.subject.lower():
            effects.extend(self._hospital_effects(action, decision_maker))
        elif "transit" in thread.subject.lower():
            effects.extend(self._transit_effects(action, decision_maker))
        elif "budget" in thread.subject.lower():
            effects.extend(self._finance_effects(action, decision_maker))
        
        return effects
    
    def _power_grid_effects(self, action: PlayerAction, agent: Agent) -> List[StateEffect]:
        """Effects specific to power grid decisions"""
        
        effects = []
        
        # Sustainability-focused agent makes greener choices
        if agent.personality.sustainability_focus > 70:
            effects.extend([
                StateEffect(
                    metric="emissions",
                    delta=-random.randint(10, 30),
                    reason="Green energy prioritization"
                ),
                StateEffect(
                    metric="city_health",
                    delta=random.randint(2, 6),
                    reason="Cleaner air quality"
                )
            ])
        
        # Always costs money but improves reliability
        effects.extend([
            StateEffect(
                metric="budget",
                delta=-random.randint(15000, 45000),
                reason="Infrastructure maintenance"
            ),
            StateEffect(
                metric="city_health",
                delta=random.randint(3, 8),
                reason="Reliable power supply"
            )
        ])
        
        return effects
    
    def _hospital_effects(self, action: PlayerAction, agent: Agent) -> List[StateEffect]:
        """Effects specific to hospital decisions"""
        
        return [
            StateEffect(
                metric="city_health",
                delta=random.randint(5, 12),
                reason="Healthcare improvements"
            ),
            StateEffect(
                metric="approval",
                delta=random.randint(2, 5),
                reason="Visible health improvements"
            ),
            StateEffect(
                metric="budget",
                delta=-random.randint(20000, 60000),
                reason="Medical equipment/staffing"
            )
        ]
    
    def _transit_effects(self, action: PlayerAction, agent: Agent) -> List[StateEffect]:
        """Effects specific to transit decisions"""
        
        return [
            StateEffect(
                metric="city_health",
                delta=random.randint(2, 6),
                reason="Reduced traffic pollution"
            ),
            StateEffect(
                metric="approval",
                delta=random.randint(3, 7),
                reason="Better public transit"
            ),
            StateEffect(
                metric="emissions",
                delta=-random.randint(5, 15),
                reason="More public transit usage"
            )
        ]
    
    def _finance_effects(self, action: PlayerAction, agent: Agent) -> List[StateEffect]:
        """Effects specific to finance decisions"""
        
        # Finance decisions usually save money but might impact services
        return [
            StateEffect(
                metric="budget",
                delta=random.randint(25000, 75000),
                reason="Cost optimization"
            ),
            StateEffect(
                metric="city_health",
                delta=random.randint(-3, 1),
                reason="Service adjustments"
            )
        ]
    
    def _calculate_department_synergy(self, thread: EmailThread) -> int:
        """Bonus effects when departments work together effectively"""
        
        departments = set()
        for agent_id in thread.participants:
            agent = self.agents.get(agent_id)
            if agent:
                departments.add(agent.department)
        
        # Certain department combinations are particularly effective
        synergy_bonuses = {
            frozenset([Department.POWER_GRID, Department.FINANCE]): 5,  # Cost-effective energy
            frozenset([Department.HOSPITAL, Department.TRANSIT]): 4,    # Health accessibility
            frozenset([Department.POWER_GRID, Department.HOSPITAL]): 6, # Critical infrastructure
        }
        
        for combo, bonus in synergy_bonuses.items():
            if combo.issubset(departments):
                return bonus
        
        return max(0, len(departments) - 2)  # General collaboration bonus
    
    def _apply_effects(self, effects: List[StateEffect]) -> None:
        """Apply state effects to the game state"""
        
        for effect in effects:
            if effect.metric == "trust_level" and effect.agent_id:
                # Update agent trust
                agent = self.agents.get(effect.agent_id)
                if agent:
                    agent.trust_level = max(0, min(100, agent.trust_level + effect.delta))
            
            elif hasattr(self.game_state, effect.metric):
                # Update game state metric
                current_value = getattr(self.game_state, effect.metric)
                if isinstance(current_value, (int, float)):
                    new_value = current_value + effect.delta
                    
                    # Clamp values to reasonable ranges
                    if effect.metric in ["city_health", "approval"]:
                        new_value = max(0, min(100, new_value))
                    
                    setattr(self.game_state, effect.metric, new_value)
    
    def _generate_daily_scenarios(self) -> None:
        """Generate interesting email scenarios for the day"""
        
        scenarios = [
            self._create_power_crisis_thread(),
            self._create_hospital_capacity_thread(), 
            self._create_transit_complaint_thread(),
            self._create_budget_concern_thread(),
            self._create_sustainability_opportunity_thread()
        ]
        
        # Select 2-3 random scenarios
        selected = random.sample(scenarios, random.randint(2, 3))
        
        for thread in selected:
            self.email_threads[thread.id] = thread
    
    def _create_power_crisis_thread(self) -> EmailThread:
        """Create a power grid related crisis"""
        
        power_agent = next((agent for agent in self.agents.values() 
                          if agent.department == Department.POWER_GRID), None)
        
        return EmailThread(
            subject="Solar Feeder Station Offline - Gas Peaker Activated",
            participants=[power_agent.id] if power_agent else [],
            priority=85,
            crisis_level="high",
            tags=["power", "crisis", "sustainability"],
            messages=[
                Message(
                    thread_id="",  # Will be set when added to thread
                    from_agent=power_agent.id if power_agent else "",
                    to_agents=["shadow_mayor"],
                    content="Major solar array offline due to equipment failure. Had to activate gas peaker plant. Repair estimate: $30k, 4 hours. Current emissions spike: +2.8 tCO2e/hour.",
                    message_type="initial"
                )
            ]
        )
    
    def _create_hospital_capacity_thread(self) -> EmailThread:
        """Create a hospital capacity issue"""
        
        hospital_agent = next((agent for agent in self.agents.values()
                             if agent.department == Department.HOSPITAL), None)
        
        return EmailThread(
            subject="ICU Cooling System Strain - Summer Heat Wave",
            participants=[hospital_agent.id] if hospital_agent else [],
            priority=75,
            crisis_level="medium",
            tags=["health", "crisis"],
            messages=[
                Message(
                    thread_id="",
                    from_agent=hospital_agent.id if hospital_agent else "",
                    to_agents=["shadow_mayor"],
                    content="Heat wave pushing our ICU cooling systems to limit. Running at 98% capacity. Can pre-cool overnight but need to delay non-critical imaging to reduce power load.",
                    message_type="initial"
                )
            ]
        )
    
    def _create_transit_complaint_thread(self) -> EmailThread:
        """Create a transit service complaint"""
        
        transit_agent = next((agent for agent in self.agents.values()
                            if agent.department == Department.TRANSIT), None)
        citizen_agent = next((agent for agent in self.agents.values()
                            if agent.department == Department.CITIZENS), None)
        
        participants = []
        if transit_agent:
            participants.append(transit_agent.id)
        if citizen_agent:
            participants.append(citizen_agent.id)
        
        return EmailThread(
            subject="Bus Route 15 Frequency Complaints Rising",
            participants=participants,
            priority=60,
            crisis_level="low",
            tags=["transit", "approval"],
            messages=[
                Message(
                    thread_id="",
                    from_agent=citizen_agent.id if citizen_agent else "",
                    to_agents=["shadow_mayor"],
                    content="Route 15 buses are 20+ minutes late consistently. People are driving instead. We need more frequent service during rush hour.",
                    message_type="initial"
                )
            ]
        )
    
    def _create_budget_concern_thread(self) -> EmailThread:
        """Create a budget-related concern"""
        
        finance_agent = next((agent for agent in self.agents.values()
                            if agent.department == Department.FINANCE), None)
        
        return EmailThread(
            subject="Q3 Budget Review - Infrastructure Overspend",
            participants=[finance_agent.id] if finance_agent else [],
            priority=70,
            tags=["finance", "budget"],
            messages=[
                Message(
                    thread_id="",
                    from_agent=finance_agent.id if finance_agent else "",
                    to_agents=["shadow_mayor"],
                    content="Infrastructure spending is 18% over Q3 budget. Need to either cut services or find additional revenue. Bond issuance possible but affects credit rating.",
                    message_type="initial"
                )
            ]
        )
    
    def _create_sustainability_opportunity_thread(self) -> EmailThread:
        """Create a sustainability opportunity"""
        
        power_agent = next((agent for agent in self.agents.values()
                          if agent.department == Department.POWER_GRID), None)
        
        return EmailThread(
            subject="Federal Green Energy Grant Available - $2M",
            participants=[power_agent.id] if power_agent else [],
            priority=65,
            tags=["sustainability", "finance", "opportunity"],
            messages=[
                Message(
                    thread_id="",
                    from_agent=power_agent.id if power_agent else "",
                    to_agents=["shadow_mayor"],
                    content="DOE offering $2M grant for smart grid upgrades. 60-day application window. Would reduce emissions by 15% but requires 50% city matching funds.",
                    message_type="initial"
                )
            ]
        )
    
    def advance_day(self) -> None:
        """Move to the next day, reset actions, update state"""
        
        self.game_state.day += 1
        self.actions_taken_today = 0
        
        # Clear old threads, generate new ones
        self.email_threads.clear()
        
        # Update influence tier based on performance
        self._update_influence_tier()
        
        # Random events and natural changes
        self._apply_daily_changes()
    
    def _update_influence_tier(self) -> None:
        """Update player's influence tier based on success"""
        
        # Calculate average trust across all agents
        total_trust = sum(agent.trust_level for agent in self.agents.values())
        avg_trust = total_trust / len(self.agents)
        
        if avg_trust >= 90:
            self.game_state.influence_tier = "Diamond"
        elif avg_trust >= 80:
            self.game_state.influence_tier = "Platinum"
        elif avg_trust >= 70:
            self.game_state.influence_tier = "Gold"
        elif avg_trust >= 60:
            self.game_state.influence_tier = "Silver"
        else:
            self.game_state.influence_tier = "Bronze"
    
    def _apply_daily_changes(self) -> None:
        """Apply natural daily changes to city metrics"""
        
        # Small random fluctuations
        self.game_state.city_health += random.randint(-2, 2)
        self.game_state.approval += random.randint(-3, 3)
        
        # Budget changes (operating costs)
        daily_costs = random.randint(15000, 25000)
        self.game_state.budget -= daily_costs
        
        # Emissions changes
        base_emissions = random.randint(-5, 10)
        self.game_state.sustainability_metrics.emissions += base_emissions
        
        # Clamp values
        self.game_state.city_health = max(0, min(100, self.game_state.city_health))
        self.game_state.approval = max(0, min(100, self.game_state.approval))