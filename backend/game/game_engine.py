from typing import Dict, List, Optional, Tuple
import random
from datetime import datetime, timedelta
from models.game_models import (
    GameState, Agent, EmailThread, Message, PlayerAction, 
    ActionOutcome, Crisis, StateEffect, OutcomeType, Department,
    SustainabilityGameState, BadActor, BadActorType, PolicyProposal,
    BlockchainTransaction, DepartmentSustainabilityScore
)
from agents.agent_factory import AgentFactory
from agents.decision_engine import AgentDecisionEngine, AgentResponseGenerator

class SustainabilityGameEngine:
    """
    Adversarial sustainability game engine where player competes against bad actors
    to influence the mayor and maximize city sustainability index.
    """
    
    def __init__(self):
        self.game_state = SustainabilityGameState()
        self.agents = AgentFactory.create_all_agents()
        self.email_threads: Dict[str, EmailThread] = {}
        
        # Agent behavior systems
        self.decision_engine = AgentDecisionEngine()
        self.response_generator = AgentResponseGenerator()
        
        # Initialize sustainability game components
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
    
    def start_new_round(self) -> Dict:
        """Start a new round of the adversarial sustainability game"""
        self.round_number = self.game_state.round_number
        
        # Generate bad actor moves for this round
        bad_actor_proposals = self._generate_bad_actor_proposals()
        
        # Update blockchain with round start
        self.game_state.add_blockchain_transaction(
            from_agent="system",
            to_agent="all",
            transaction_type="round_start",
            data={"round": self.round_number}
        )
        
        return {
            "round_number": self.round_number,
            "sustainability_index": self.game_state.sustainability_index,
            "department_scores": dict(self.game_state.department_scores),
            "mayor_trust": self.game_state.mayor_trust_in_player,
            "bad_actor_influence": self.game_state.bad_actor_influence,
            "bad_actor_proposals": bad_actor_proposals,
            "blockchain_transactions_count": len(self.game_state.blockchain_transactions)
        }
    
    def _generate_bad_actor_proposals(self) -> List[Dict]:
        """Generate policy proposals from bad actors for this round"""
        proposals = []
        
        for actor in self.game_state.active_bad_actors.values():
            if not actor.active or actor.corruption_budget <= 0:
                continue
                
            # Each bad actor has a chance to make a proposal this round
            if random.random() < 0.7:  # 70% chance to act each round
                proposal = self._create_bad_actor_proposal(actor)
                proposals.append({
                    "proposal": proposal,
                    "actor": actor.name,
                    "bribe_amount": proposal.bribe_amount,
                    "target_department": proposal.target_department.value
                })
                
                # Add to game state
                self.game_state.pending_proposals.append(proposal)
                
                # Record on blockchain
                self.game_state.add_blockchain_transaction(
                    from_agent=actor.id,
                    to_agent="mayor",
                    transaction_type="bribe_attempt",
                    amount=proposal.bribe_amount,
                    data={
                        "proposal_id": proposal.id,
                        "description": proposal.description
                    }
                )
                
        return proposals
    
    def _create_bad_actor_proposal(self, actor: BadActor) -> PolicyProposal:
        """Create a specific unsustainable policy proposal from a bad actor"""
        target_dept = random.choice(actor.target_departments)
        bribe_amount = random.randint(10000, min(100000, actor.corruption_budget))
        
        proposals_by_type = {
            BadActorType.DEVELOPER_GROUP: {
                Department.HOUSING: [
                    ("Relax Building Codes", "Reduce environmental standards for faster construction", -15, 20, 10),
                    ("Suburban Expansion", "Approve low-density sprawl development project", -20, 15, 15),
                ],
                Department.TRANSPORTATION: [
                    ("Highway Expansion", "Build new car-centric infrastructure", -10, 25, 5),
                    ("Parking Minimums", "Require more parking spaces in developments", -8, 12, 8),
                ]
            },
            BadActorType.FOSSIL_FUEL_COMPANY: {
                Department.ENERGY: [
                    ("Gas Plant Extension", "Extend natural gas power plant operations", -25, 30, 20),
                    ("Renewable Delays", "Postpone solar farm construction permits", -15, 10, 15),
                ],
                Department.TRANSPORTATION: [
                    ("EV Tax Rollback", "Eliminate electric vehicle incentives", -12, 18, 12),
                    ("Fuel Subsidies", "Increase gasoline subsidies for 'economic relief'", -18, 22, 25),
                ]
            },
            BadActorType.CORPORATE_LOBBY: {
                Department.WASTE: [
                    ("Landfill Expansion", "Increase landfill capacity instead of recycling", -20, 15, 8),
                    ("Recycling Cuts", "Reduce municipal recycling program funding", -15, 25, 10),
                ],
                Department.WATER: [
                    ("Regulation Rollback", "Reduce water quality monitoring requirements", -18, 20, 12),
                    ("Private Contracts", "Privatize water treatment facilities", -10, 30, 15),
                ]
            }
        }
        
        proposal_options = proposals_by_type.get(actor.type, {}).get(target_dept, [])
        if not proposal_options:
            # Fallback generic proposal
            title = f"Deregulation Initiative"
            description = f"Reduce regulatory burden on {target_dept.value} sector"
            sustainability_impact = -10
            economic_impact = 15
            political_impact = 8
        else:
            title, description, sustainability_impact, economic_impact, political_impact = random.choice(proposal_options)
        
        return PolicyProposal(
            title=title,
            description=description,
            proposed_by=actor.id,
            target_department=target_dept,
            sustainability_impact=sustainability_impact,
            economic_impact=economic_impact,
            political_impact=political_impact,
            bribe_amount=bribe_amount
        )

    def submit_player_proposal(self, title: str, description: str, 
                             target_department: Department) -> PolicyProposal:
        """Player submits a sustainability-focused policy proposal"""
        
        # Player proposals are designed to be sustainable (positive impact)
        sustainability_impact = random.randint(8, 25)  # Always positive for player
        economic_impact = random.randint(-5, 20)  # Can vary
        political_impact = random.randint(-10, 15)  # Depends on political climate
        
        proposal = PolicyProposal(
            title=title,
            description=description,
            proposed_by="player",
            target_department=target_department,
            sustainability_impact=sustainability_impact,
            economic_impact=economic_impact,
            political_impact=political_impact,
            bribe_amount=0  # Player doesn't bribe
        )
        
        self.game_state.pending_proposals.append(proposal)
        
        # Record on blockchain
        self.game_state.add_blockchain_transaction(
            from_agent="player",
            to_agent="mayor",
            transaction_type="policy_proposal",
            data={
                "proposal_id": proposal.id,
                "title": title,
                "sustainability_impact": sustainability_impact
            }
        )
        
        return proposal

    def get_daily_digest(self) -> Dict:
        """Get summary of current game state and blockchain activity"""
        
        recent_transactions = self.game_state.blockchain_transactions[-10:]  # Last 10 transactions
        pending_proposals = len(self.game_state.pending_proposals)
        
        return {
            "round_number": self.game_state.round_number,
            "sustainability_index": self.game_state.sustainability_index,
            "department_scores": dict(self.game_state.department_scores),
            "mayor_trust": self.game_state.mayor_trust_in_player,
            "bad_actor_influence": self.game_state.bad_actor_influence,
            "pending_proposals": pending_proposals,
            "recent_blockchain_activity": len(recent_transactions),
            "win_conditions_check": self._check_win_conditions(),
            "loss_conditions_check": self._check_loss_conditions()
        }
    
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
    
    # New methods for sustainability game
    def _check_win_conditions(self) -> Dict:
        """Check if any win conditions have been met"""
        conditions = {
            "sustainability_dominance": False,
            "corruption_exposure": False, 
            "rapid_transformation": False
        }
        
        # Check sustainability dominance (85+ for 10 rounds)
        if self.game_state.sustainability_index >= 85:
            # This would need tracking over multiple rounds - simplified for now
            conditions["sustainability_dominance"] = True
        
        # Check corruption exposure (simplified - track successful counters)
        # This would need more complex tracking in real implementation
        
        # Check rapid transformation (30+ point increase in 5 rounds)
        # This would need historical tracking in real implementation
        
        return conditions
    
    def _check_loss_conditions(self) -> Dict:
        """Check if any loss conditions have been triggered"""
        conditions = {
            "corruption_takeover": self.game_state.sustainability_index < 40,
            "trust_collapse": self.player_consecutive_rejections >= self.max_consecutive_rejections,
            "department_rebellion": self._check_department_rebellion(),
            "time_limit": self.game_state.round_number >= self.max_rounds
        }
        
        return conditions
    
    def _check_department_rebellion(self) -> bool:
        """Check if 4+ departments have scores below 30"""
        low_scoring_depts = sum(1 for score in self.game_state.department_scores.values() if score < 30)
        return low_scoring_depts >= 4
    
    def get_blockchain_analysis(self) -> Dict:
        """Provide blockchain transaction analysis for player intelligence gathering"""
        transactions = self.game_state.blockchain_transactions
        
        # Analyze bribe patterns
        bribe_transactions = [t for t in transactions if t.transaction_type == "bribe_attempt"]
        total_bribes = sum(t.amount or 0 for t in bribe_transactions)
        
        # Analyze policy impacts
        policy_transactions = [t for t in transactions if t.transaction_type == "department_score_update"]
        
        # Recent bad actor activity
        recent_bad_actor_activity = [
            t for t in transactions[-20:] 
            if t.from_agent in self.game_state.active_bad_actors.keys()
        ]
        
        return {
            "total_transactions": len(transactions),
            "total_bribe_attempts": len(bribe_transactions),
            "total_bribe_amount": total_bribes,
            "policy_implementations": len(policy_transactions),
            "recent_bad_actor_moves": len(recent_bad_actor_activity),
            "corruption_evidence": [
                {
                    "transaction_id": t.id,
                    "from": t.from_agent,
                    "type": t.transaction_type,
                    "amount": t.amount,
                    "timestamp": t.timestamp.isoformat()
                }
                for t in bribe_transactions[-5:]  # Last 5 bribe attempts
            ]
        }
    
    def get_game_status(self) -> Dict:
        """Get complete game status for UI display"""
        return {
            **self.get_daily_digest(),
            "blockchain_analysis": self.get_blockchain_analysis(),
            "active_bad_actors": {
                actor.id: {
                    "name": actor.name,
                    "type": actor.type.value,
                    "influence_power": actor.influence_power,
                    "remaining_budget": actor.corruption_budget,
                    "active": actor.active
                }
                for actor in self.game_state.active_bad_actors.values()
            }
        }