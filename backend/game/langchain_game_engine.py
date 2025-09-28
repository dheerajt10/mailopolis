"""
LangChain-powered Game Engine for Mailopolis
Manages the city simulation loop with political maneuvering and consequences
"""

import asyncio
import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum

from agents.langchain_agents import LangChainAgentManager
from models.game_models import (
    PolicyProposal, Department, SustainabilityGameState, 
    SustainabilityMetrics, EnergyMix, GameState
)

class EventType(Enum):
    CRISIS = "crisis"
    OPPORTUNITY = "opportunity"
    EXTERNAL_PRESSURE = "external_pressure"
    BUDGET_CHANGE = "budget_change"
    PUBLIC_REACTION = "public_reaction"

@dataclass
class GameEvent:
    event_type: EventType
    title: str
    description: str
    impacts: Dict[str, int]  # What stats this affects
    urgency: int  # 1-10, how quickly it must be addressed
    duration: int  # How many turns this event lasts

@dataclass
class CityStats:
    sustainability_score: int = 45  # 0-100
    budget: int = 1000000  # Starting budget
    public_approval: int = 65  # 0-100
    economic_growth: int = 50  # 0-100
    infrastructure_health: int = 70  # 0-100
    population_happiness: int = 60  # 0-100
    corruption_level: int = 20  # 0-100 (lower is better)
    
    def to_dict(self) -> Dict[str, int]:
        return asdict(self)
    
    def apply_impacts(self, impacts: Dict[str, int]):
        """Apply impacts from decisions or events"""
        for stat, change in impacts.items():
            if hasattr(self, stat):
                current_value = getattr(self, stat)
                new_value = max(0, min(100 if stat != 'budget' else float('inf'), current_value + change))
                setattr(self, stat, int(new_value))

@dataclass
class Turn:
    turn_number: int
    city_stats: CityStats
    active_events: List[GameEvent]
    proposals_this_turn: List[PolicyProposal]
    decisions_made: List[Dict[str, Any]]
    political_consequences: Dict[str, Any]

class MaylopolisGameEngine:
    """Main game engine that runs the city simulation"""
    
    def __init__(self, agent_manager: LangChainAgentManager):
        self.agent_manager = agent_manager
        self.city_stats = CityStats()
        self.turn_number = 0
        self.active_events: List[GameEvent] = []
        self.game_history: List[Turn] = []
        self.max_turns = 50  # Game length
        self.is_game_over = False
        
        # Game balance parameters
        self.event_probability = 0.3  # 30% chance of random event each turn
        self.crisis_threshold = 30  # If any stat drops below this, crisis occurs
        self.win_conditions = {
            'sustainability_score': 85,
            'public_approval': 80,
            'population_happiness': 80
        }
        
    async def start_new_game(self) -> Dict[str, Any]:
        """Initialize a new game"""
        print("🏛️  Starting new Mailopolis game...")
        print(f"Initial city stats: {self.city_stats.to_dict()}")
        
        self.turn_number = 0
        self.active_events = []
        self.game_history = []
        self.is_game_over = False
        
        # Generate initial scenario
        initial_events = await self._generate_initial_events()
        self.active_events.extend(initial_events)
        
        return {
            'status': 'started',
            'turn': self.turn_number,
            'city_stats': self.city_stats.to_dict(),
            'active_events': [asdict(event) for event in self.active_events],
            'message': 'Welcome to Mailopolis! Your city needs strong leadership.'
        }
    
    async def play_turn(self, player_proposals: List[PolicyProposal]) -> Dict[str, Any]:
        """Play one turn of the game with player-submitted proposals"""
        if self.is_game_over:
            return {'status': 'game_over', 'message': 'Game has ended'}
        
        if not player_proposals:
            return {
                'status': 'waiting_for_proposals',
                'message': 'Please submit at least one policy proposal to proceed.',
                'turn': self.turn_number,
                'city_stats': self.city_stats.to_dict(),
                'active_events': [asdict(event) for event in self.active_events]
            }
        
        self.turn_number += 1
        print(f"\n🗓️  TURN {self.turn_number}")
        print("=" * 50)
        print(f"Processing {len(player_proposals)} player proposals...")
        
        # Phase 1: Handle ongoing events and generate new ones
        await self._process_events()
        
        # Phase 2: Use player's proposals
        proposals = player_proposals
        
        # Phase 3: Political maneuvering and decisions
        decisions = []
        political_consequences = {}
        
        for proposal in proposals:
            print(f"\n📋 Processing proposal: {proposal.title}")
            
            # Run the political discussion system
            discussion_result = await self.agent_manager.discuss_and_evaluate_proposal(
                proposal, self._get_game_context()
            )
            
            mayor_decision = discussion_result['mayor_decision']
            
            # Apply consequences of the decision
            consequences = self._calculate_decision_consequences(
                proposal, mayor_decision, discussion_result
            )
            
            decisions.append({
                'proposal': proposal.dict() if hasattr(proposal, 'dict') else proposal.__dict__,
                'mayor_decision': mayor_decision.dict() if hasattr(mayor_decision, 'dict') else mayor_decision.__dict__,
                'political_discussion': discussion_result,
                'consequences': consequences
            })
            
            # Apply stat changes
            self.city_stats.apply_impacts(consequences['stat_changes'])
            
            # Track political consequences
            political_consequences.update(consequences['political_effects'])
            
        # Phase 4: End of turn processing
        end_of_turn_effects = await self._process_end_of_turn()
        
        # Phase 5: Check win/lose conditions
        game_status = self._check_game_status()
        
        # Create turn record
        turn_record = Turn(
            turn_number=self.turn_number,
            city_stats=CityStats(**self.city_stats.to_dict()),
            active_events=self.active_events.copy(),
            proposals_this_turn=proposals,
            decisions_made=decisions,
            political_consequences=political_consequences
        )
        self.game_history.append(turn_record)
        
        return {
            'status': game_status['status'],
            'turn': self.turn_number,
            'city_stats': self.city_stats.to_dict(),
            'decisions_made': decisions,
            'active_events': [asdict(event) for event in self.active_events],
            'political_consequences': political_consequences,
            'end_of_turn_effects': end_of_turn_effects,
            'game_message': game_status['message'],
            'is_game_over': self.is_game_over
        }
    
    async def _process_events(self):
        """Process ongoing events and generate new ones"""
        # Process existing events
        events_to_remove = []
        for event in self.active_events:
            event.duration -= 1
            if event.duration <= 0:
                events_to_remove.append(event)
                print(f"⏰ Event concluded: {event.title}")
        
        # Remove expired events
        for event in events_to_remove:
            self.active_events.remove(event)
        
        # Generate new random events
        if random.random() < self.event_probability:
            new_event = await self._generate_random_event()
            if new_event:
                self.active_events.append(new_event)
                print(f"🚨 New event: {new_event.title}")
        
        # Check for crisis events based on low stats
        crisis_event = await self._check_for_crisis()
        if crisis_event:
            self.active_events.append(crisis_event)
            print(f"💥 CRISIS: {crisis_event.title}")
    
    async def get_suggested_proposals(self) -> List[PolicyProposal]:
        """Generate suggested proposals for the player based on current game state"""
        proposals = []
        
        # Generate 2-4 suggested proposals per turn based on city needs
        num_suggestions = random.randint(2, 4)
        
        for i in range(num_suggestions):
            # Choose departments that have the most relevant expertise for current issues
            relevant_dept = self._get_most_relevant_department()
            
            proposal = await self._generate_contextual_proposal(relevant_dept)
            if proposal:
                proposals.append(proposal)
        
        return proposals
    
    def _get_most_relevant_department(self) -> Department:
        """Get the department most relevant to current city issues"""
        
        if self.city_stats.sustainability_score < 50:
            return random.choice([Department.ENERGY, Department.TRANSPORTATION])
        elif self.city_stats.public_approval < 50:
            return random.choice([Department.HOUSING, Department.CITIZENS])
        elif self.city_stats.infrastructure_health < 50:
            return random.choice([Department.WATER, Department.WASTE])
        elif self.city_stats.economic_growth < 50:
            return Department.ECONOMIC_DEV
        else:
            # Random department when things are going well
            return random.choice([dept for dept in Department if dept != Department.MAYOR])
    
    async def _generate_contextual_proposal(self, department: Department) -> Optional[PolicyProposal]:
        """Generate a proposal that makes sense given current game state"""
        
        # Base proposals based on department and current city needs
        proposal_templates = {
            Department.ENERGY: {
                'low_sustainability': {
                    'title': 'Emergency Renewable Energy Initiative',
                    'description': 'Fast-track solar panel installation on all public buildings within 6 months.',
                    'sustainability_impact': 25, 'economic_impact': -20, 'political_impact': 15
                },
                'low_budget': {
                    'title': 'Energy Efficiency Retrofits', 
                    'description': 'Low-cost energy efficiency improvements to reduce city utility costs.',
                    'sustainability_impact': 15, 'economic_impact': 10, 'political_impact': 5
                },
                'normal': {
                    'title': 'Smart Grid Modernization',
                    'description': 'Upgrade city electrical grid with smart monitoring and renewable integration.',
                    'sustainability_impact': 20, 'economic_impact': -15, 'political_impact': 10
                }
            },
            Department.TRANSPORTATION: {
                'low_sustainability': {
                    'title': 'Electric Bus Fleet Conversion',
                    'description': 'Replace all diesel buses with electric vehicles over 18 months.',
                    'sustainability_impact': 30, 'economic_impact': -25, 'political_impact': 20
                },
                'low_approval': {
                    'title': 'Free Public Transit Month',
                    'description': 'Provide free public transportation for one month to boost ridership.',
                    'sustainability_impact': 10, 'economic_impact': -15, 'political_impact': 25
                },
                'normal': {
                    'title': 'Bike Lane Expansion Project',
                    'description': 'Add 20 miles of protected bike lanes throughout the city.',
                    'sustainability_impact': 15, 'economic_impact': -10, 'political_impact': 5
                }
            },
            Department.HOUSING: {
                'low_approval': {
                    'title': 'Affordable Housing Guarantee',
                    'description': 'Mandate that 30% of all new developments include affordable units.',
                    'sustainability_impact': 5, 'economic_impact': -10, 'political_impact': 30
                },
                'low_happiness': {
                    'title': 'First-Time Homebuyer Program',
                    'description': 'Provide down payment assistance for first-time homebuyers.',
                    'sustainability_impact': 0, 'economic_impact': -20, 'political_impact': 25
                },
                'normal': {
                    'title': 'Green Building Standards',
                    'description': 'Require all new construction to meet LEED certification standards.',
                    'sustainability_impact': 25, 'economic_impact': -15, 'political_impact': 10
                }
            }
            # Add more departments as needed
        }
        
        # Determine current city situation
        situation = self._assess_city_situation()
        
        # Select appropriate proposal template
        dept_proposals = proposal_templates.get(department, {})
        if situation in dept_proposals:
            template = dept_proposals[situation]
        else:
            template = dept_proposals.get('normal', dept_proposals[next(iter(dept_proposals))])
        
        return PolicyProposal(
            title=template['title'],
            description=template['description'],
            proposed_by=f"ai_department_{department.value}",
            target_department=department,
            sustainability_impact=template['sustainability_impact'],
            economic_impact=template['economic_impact'],
            political_impact=template['political_impact']
        )
    
    def _assess_city_situation(self) -> str:
        """Assess the current city situation to guide proposal generation"""
        if self.city_stats.sustainability_score < 40:
            return 'low_sustainability'
        elif self.city_stats.public_approval < 50:
            return 'low_approval'
        elif self.city_stats.population_happiness < 50:
            return 'low_happiness'
        elif self.city_stats.budget < 500000:
            return 'low_budget'
        else:
            return 'normal'
    
    def _calculate_decision_consequences(self, proposal: PolicyProposal, 
                                       mayor_decision, discussion_result) -> Dict[str, Any]:
        """Calculate the consequences of a mayoral decision"""
        
        if not mayor_decision.accept:
            # Rejection consequences
            stat_changes = {
                'public_approval': -5,  # People don't like inaction
                'corruption_level': 2   # Slight increase in perceived corruption
            }
            
            # Department that proposed might lose trust
            political_effects = {
                f"{proposal.target_department.value}_relationship": -10
            }
            
        else:
            # Approval consequences - apply the proposal's intended effects
            stat_changes = {
                'sustainability_score': proposal.sustainability_impact,
                'budget': proposal.economic_impact * 10000,  # Scale economic impact
                'public_approval': proposal.political_impact,
            }
            
            # Additional effects based on proposal type and city readiness
            if proposal.sustainability_impact > 20:
                stat_changes['infrastructure_health'] = 5
            
            if proposal.economic_impact < -20:
                stat_changes['economic_growth'] = -5
            
            # Political effects based on how much support the proposal had
            political_effects = {}
            
            # Count supporting agents from discussion
            if 'department_positions' in discussion_result:
                support_count = sum(1 for pos in discussion_result['department_positions'].values() 
                                  if 'SUPPORT' in pos.get('position', '').upper())
                total_depts = len(discussion_result['department_positions'])
                
                if support_count > total_depts * 0.7:  # Strong support
                    stat_changes['public_approval'] += 10
                    political_effects['strong_consensus'] = True
                elif support_count < total_depts * 0.3:  # Weak support
                    stat_changes['public_approval'] -= 5
                    political_effects['controversial_decision'] = True
            
            # Coalition effects
            if 'coalitions_formed' in discussion_result and discussion_result['coalitions_formed']:
                political_effects['coalitions_active'] = discussion_result['coalitions_formed']
                stat_changes['infrastructure_health'] += 3  # Cooperation improves implementation
        
        # Random variance (-20% to +20% of intended effects)
        for stat in stat_changes:
            if stat != 'budget':  # Don't apply variance to budget
                variance = random.uniform(-0.2, 0.2)
                stat_changes[stat] = int(stat_changes[stat] * (1 + variance))
        
        return {
            'stat_changes': stat_changes,
            'political_effects': political_effects
        }
    
    async def _generate_random_event(self) -> Optional[GameEvent]:
        """Generate a random event based on current city state"""
        
        events = [
            GameEvent(
                event_type=EventType.CRISIS,
                title="Infrastructure Failure",
                description="A major water main burst affects 30% of the city. Immediate action required.",
                impacts={'budget': -50000, 'infrastructure_health': -15, 'public_approval': -10},
                urgency=9,
                duration=2
            ),
            GameEvent(
                event_type=EventType.OPPORTUNITY,
                title="Federal Green Grant Available",
                description="$2M federal grant available for renewable energy projects.",
                impacts={'budget': 200000, 'sustainability_score': 10},
                urgency=3,
                duration=3
            ),
            GameEvent(
                event_type=EventType.EXTERNAL_PRESSURE,
                title="Climate Activists Rally", 
                description="Large environmental rally demanding immediate climate action.",
                impacts={'public_approval': -5, 'sustainability_score': 5},
                urgency=5,
                duration=1
            ),
            GameEvent(
                event_type=EventType.BUDGET_CHANGE,
                title="Unexpected Tax Revenue",
                description="Higher than expected tax collection this quarter.",
                impacts={'budget': 150000, 'economic_growth': 5},
                urgency=1,
                duration=1
            )
        ]
        
        return random.choice(events)
    
    async def _check_for_crisis(self) -> Optional[GameEvent]:
        """Check if low stats should trigger a crisis event"""
        
        if self.city_stats.sustainability_score < self.crisis_threshold:
            return GameEvent(
                event_type=EventType.CRISIS,
                title="Environmental Crisis",
                description="Air quality has reached dangerous levels. Federal oversight threatened.",
                impacts={'public_approval': -20, 'population_happiness': -15},
                urgency=10,
                duration=4
            )
        
        if self.city_stats.public_approval < self.crisis_threshold:
            return GameEvent(
                event_type=EventType.CRISIS,
                title="Public Confidence Crisis",
                description="Citizens are calling for leadership change. Emergency town halls demanded.",
                impacts={'corruption_level': 10, 'economic_growth': -10},
                urgency=8,
                duration=3
            )
        
        return None
    
    async def _generate_initial_events(self) -> List[GameEvent]:
        """Generate initial events for game start"""
        return [
            GameEvent(
                event_type=EventType.OPPORTUNITY,
                title="New Administration Honeymoon",
                description="Citizens are optimistic about new leadership and ready for change.",
                impacts={'public_approval': 5, 'population_happiness': 5},
                urgency=1,
                duration=5
            )
        ]
    
    async def _process_end_of_turn(self) -> Dict[str, Any]:
        """Process end-of-turn effects like budget maintenance, population growth, etc."""
        
        effects = {}
        
        # Monthly budget costs
        monthly_costs = {
            'infrastructure_maintenance': -20000,
            'staff_salaries': -50000,
            'utilities': -15000
        }
        
        total_costs = sum(monthly_costs.values())
        self.city_stats.budget += total_costs
        effects['monthly_costs'] = monthly_costs
        
        # Natural stat degradation/improvement
        natural_changes = {}
        
        # Infrastructure naturally degrades
        if self.city_stats.infrastructure_health > 0:
            degradation = random.randint(1, 3)
            self.city_stats.infrastructure_health -= degradation
            natural_changes['infrastructure_degradation'] = -degradation
        
        # Economic growth affects budget
        if self.city_stats.economic_growth > 60:
            tax_bonus = random.randint(10000, 30000)
            self.city_stats.budget += tax_bonus
            effects['economic_bonus'] = tax_bonus
        
        effects['natural_changes'] = natural_changes
        
        return effects
    
    def _check_game_status(self) -> Dict[str, str]:
        """Check if game has been won, lost, or continues"""
        
        # Check win conditions
        win_conditions_met = 0
        for stat, threshold in self.win_conditions.items():
            if getattr(self.city_stats, stat) >= threshold:
                win_conditions_met += 1
        
        if win_conditions_met >= 2:  # Need to meet at least 2 win conditions
            self.is_game_over = True
            return {
                'status': 'victory',
                'message': f'🎉 Congratulations! You have successfully transformed Mailopolis into a model sustainable city!'
            }
        
        # Check lose conditions
        critical_failures = 0
        if self.city_stats.sustainability_score < 20:
            critical_failures += 1
        if self.city_stats.public_approval < 20:
            critical_failures += 1
        if self.city_stats.population_happiness < 20:
            critical_failures += 1
        if self.city_stats.budget < -500000:  # Bankruptcy
            critical_failures += 1
        
        if critical_failures >= 2:
            self.is_game_over = True
            return {
                'status': 'defeat',
                'message': '💥 Game Over! Multiple critical failures have made your position as mayor untenable.'
            }
        
        # Check turn limit
        if self.turn_number >= self.max_turns:
            self.is_game_over = True
            # Determine ending based on final stats
            avg_score = (self.city_stats.sustainability_score + 
                        self.city_stats.public_approval + 
                        self.city_stats.population_happiness) / 3
            
            if avg_score >= 70:
                return {
                    'status': 'good_ending',
                    'message': '🏛️ Your term ended with the city in good condition. A solid legacy!'
                }
            else:
                return {
                    'status': 'mixed_ending', 
                    'message': '📊 Your term ended with mixed results. Some progress made, but challenges remain.'
                }
        
        return {
            'status': 'ongoing',
            'message': f'Turn {self.turn_number} of {self.max_turns} completed. The city continues to evolve...'
        }
    
    def _get_game_context(self) -> Dict[str, Any]:
        """Get current game context for agent decision making"""
        return {
            'current_sustainability_score': self.city_stats.sustainability_score,
            'budget_remaining': self.city_stats.budget,
            'public_approval': self.city_stats.public_approval,
            'population_happiness': self.city_stats.population_happiness,
            'infrastructure_health': self.city_stats.infrastructure_health,
            'turn_number': self.turn_number,
            'active_events': [event.title for event in self.active_events],
            'crisis_level': 'high' if any(event.urgency > 7 for event in self.active_events) else 'moderate'
        }
    
    def get_game_summary(self) -> Dict[str, Any]:
        """Get a summary of the current game state"""
        return {
            'turn': self.turn_number,
            'city_stats': self.city_stats.to_dict(),
            'active_events': [asdict(event) for event in self.active_events],
            'is_game_over': self.is_game_over,
            'turns_remaining': self.max_turns - self.turn_number,
            'game_history_length': len(self.game_history)
        }
