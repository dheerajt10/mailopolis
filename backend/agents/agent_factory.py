from typing import Dict, List
from models.game_models import (
    Agent, AgentPersonality, Department, DecisionStyle, 
    CommunicationStyle, Priority, PriorityType
)

class AgentFactory:
    """
    Creates agents with distinct personalities and behaviors.
    Each department has agents with different characteristics.
    """
    
    @staticmethod
    def create_all_agents() -> Dict[str, Agent]:
        """Create the full roster of city agents"""
        
        agents = {}
        
        # Mayor - Political, approval-focused
        mayor = AgentFactory.create_mayor()
        agents[mayor.id] = mayor
        
        # PowerGrid Department - Technical, sustainability-focused
        power_chief = AgentFactory.create_power_grid_chief()
        agents[power_chief.id] = power_chief
        
        # Hospital Department - Health-focused, collaborative
        hospital_chief = AgentFactory.create_hospital_chief()
        agents[hospital_chief.id] = hospital_chief
        
        # Transit Department - Efficiency-focused, bureaucratic
        transit_chief = AgentFactory.create_transit_chief()
        agents[transit_chief.id] = transit_chief
        
        # Finance Department - Budget-focused, cautious
        finance_chief = AgentFactory.create_finance_chief()
        agents[finance_chief.id] = finance_chief
        
        # Citizens - Emotional, approval-sensitive
        citizen_rep = AgentFactory.create_citizen_representative()
        agents[citizen_rep.id] = citizen_rep
        
        return agents
    
    @staticmethod
    def create_mayor() -> Agent:
        """Mayor prioritizes approval ratings and political optics"""
        return Agent(
            name="Mayor Patricia Williams",
            email="mayor@mailopolis.gov",
            department=Department.MAYOR,
            personality=AgentPersonality(
                decision_style=DecisionStyle.BUREAUCRATIC,
                priorities=[
                    Priority(type=PriorityType.APPROVAL, weight=0.4),
                    Priority(type=PriorityType.BUDGET, weight=0.3),
                    Priority(type=PriorityType.HEALTH, weight=0.3)
                ],
                communication_style=CommunicationStyle.POLITICAL,
                risk_tolerance=30,  # Risk-averse
                budget_sensitivity=80,  # Very budget conscious
                public_opinion_sensitivity=95,  # Extremely sensitive to public opinion
                sustainability_focus=50  # Moderate sustainability focus
            ),
            trust_level=60,  # Starts neutral
            response_time_base=45,  # Slower due to political considerations
            current_workload=70
        )
    
    @staticmethod
    def create_power_grid_chief() -> Agent:
        """PowerGrid Chief is technical, sustainability-focused"""
        return Agent(
            name="Dr. Marcus Chen",
            email="power@mailopolis.gov", 
            department=Department.POWER_GRID,
            personality=AgentPersonality(
                decision_style=DecisionStyle.COLLABORATIVE,
                priorities=[
                    Priority(type=PriorityType.SUSTAINABILITY, weight=0.4),
                    Priority(type=PriorityType.EFFICIENCY, weight=0.3),
                    Priority(type=PriorityType.BUDGET, weight=0.3)
                ],
                communication_style=CommunicationStyle.TECHNICAL,
                risk_tolerance=65,  # Moderate risk tolerance for innovation
                budget_sensitivity=60,
                public_opinion_sensitivity=40,  # Less concerned with optics
                sustainability_focus=90  # Very high sustainability focus
            ),
            trust_level=75,  # Starts trusting
            response_time_base=25,  # Quick technical responses
            current_workload=60
        )
    
    @staticmethod
    def create_hospital_chief() -> Agent:
        """Hospital Chief prioritizes health outcomes above all"""
        return Agent(
            name="Dr. Sarah Rodriguez",
            email="hospital@mailopolis.gov",
            department=Department.HOSPITAL,
            personality=AgentPersonality(
                decision_style=DecisionStyle.AGGRESSIVE,  # Aggressive about health
                priorities=[
                    Priority(type=PriorityType.HEALTH, weight=0.6),
                    Priority(type=PriorityType.BUDGET, weight=0.2),
                    Priority(type=PriorityType.APPROVAL, weight=0.2)
                ],
                communication_style=CommunicationStyle.TECHNICAL,
                risk_tolerance=85,  # Will take risks for health outcomes
                budget_sensitivity=40,  # Less budget sensitive when health at stake
                public_opinion_sensitivity=60,
                sustainability_focus=35  # Lower sustainability focus
            ),
            trust_level=80,  # High trust, medical professional
            response_time_base=20,  # Very quick, emergency-oriented
            current_workload=75  # Always busy
        )
    
    @staticmethod  
    def create_transit_chief() -> Agent:
        """Transit Chief is bureaucratic, process-oriented"""
        return Agent(
            name="James Morrison",
            email="transit@mailopolis.gov",
            department=Department.TRANSIT,
            personality=AgentPersonality(
                decision_style=DecisionStyle.BUREAUCRATIC,
                priorities=[
                    Priority(type=PriorityType.EFFICIENCY, weight=0.4),
                    Priority(type=PriorityType.BUDGET, weight=0.35),
                    Priority(type=PriorityType.APPROVAL, weight=0.25)
                ],
                communication_style=CommunicationStyle.FORMAL,
                risk_tolerance=25,  # Very risk-averse
                budget_sensitivity=85,  # Highly budget sensitive
                public_opinion_sensitivity=70,
                sustainability_focus=55  # Moderate sustainability focus
            ),
            trust_level=65,
            response_time_base=50,  # Slower, needs to check procedures
            current_workload=55
        )
    
    @staticmethod
    def create_finance_chief() -> Agent:
        """Finance Chief is cautious, budget-obsessed"""
        return Agent(
            name="Robert Kim",
            email="finance@mailopolis.gov",
            department=Department.FINANCE,
            personality=AgentPersonality(
                decision_style=DecisionStyle.CAUTIOUS,
                priorities=[
                    Priority(type=PriorityType.BUDGET, weight=0.5),
                    Priority(type=PriorityType.EFFICIENCY, weight=0.3),
                    Priority(type=PriorityType.APPROVAL, weight=0.2)
                ],
                communication_style=CommunicationStyle.FORMAL,
                risk_tolerance=15,  # Extremely risk-averse
                budget_sensitivity=95,  # Maximum budget sensitivity
                public_opinion_sensitivity=45,
                sustainability_focus=40  # Lower sustainability focus
            ),
            trust_level=70,
            response_time_base=35,  # Deliberate, needs to analyze numbers
            current_workload=65
        )
    
    @staticmethod
    def create_citizen_representative() -> Agent:
        """Citizens are emotional, reactive"""
        return Agent(
            name="Citizens Council", 
            email="citizens@mailopolis.gov",
            department=Department.CITIZENS,
            personality=AgentPersonality(
                decision_style=DecisionStyle.AGGRESSIVE,  # Emotional reactions
                priorities=[
                    Priority(type=PriorityType.HEALTH, weight=0.4),
                    Priority(type=PriorityType.APPROVAL, weight=0.3),
                    Priority(type=PriorityType.SUSTAINABILITY, weight=0.3)
                ],
                communication_style=CommunicationStyle.CASUAL,
                risk_tolerance=70,  # Willing to take risks for change
                budget_sensitivity=30,  # Don't fully understand budget constraints
                public_opinion_sensitivity=100,  # Maximum sensitivity - they ARE public opinion
                sustainability_focus=75  # High sustainability concern
            ),
            trust_level=50,  # Starts skeptical
            response_time_base=15,  # Very quick, emotional responses
            current_workload=40
        )

class AgentBehaviorProfiles:
    """
    Defines how different agent personalities behave in specific scenarios.
    This creates the "character" that makes agents feel different.
    """
    
    @staticmethod
    def get_agent_quirks() -> Dict[str, Dict[str, str]]:
        """Personality quirks that make agents feel unique"""
        
        return {
            "mayor": {
                "worried_about_budget": "We need to think about how this looks to taxpayers...",
                "low_approval": "I'm getting heat from the press on this. We need wins.",
                "high_approval": "The people are behind us. Let's be bold.",
                "crisis_response": "How quickly can we contain this? I have a press conference at 3."
            },
            
            "power_chief": {
                "sustainability_focus": "Have we considered the carbon impact of this decision?",
                "technical_solution": "The load balancing algorithm suggests we should...", 
                "innovation_opportunity": "This could be a chance to pilot our new smart grid tech.",
                "efficiency_concern": "We're running at 94% capacity. That's cutting it close."
            },
            
            "hospital_chief": {
                "health_crisis": "Patient safety is non-negotiable. We do whatever it takes.",
                "resource_shortage": "We're already at 105% capacity. This will push us over the edge.",
                "preventive_approach": "If we act now, we can prevent this from becoming an emergency.",
                "data_driven": "The epidemiological data shows a clear trend..."
            },
            
            "transit_chief": {
                "process_concern": "This needs to go through the proper approval channels first.",
                "budget_limitation": "The union contract specifically states we can't...",
                "efficiency_metrics": "Our on-time performance is down 3% this quarter.",
                "regulatory_compliance": "Let me check if this violates any DOT regulations."
            },
            
            "finance_chief": {
                "budget_alarm": "This expenditure puts us 12% over budget for the quarter.",
                "cost_benefit": "What's the ROI timeline on this investment?",
                "fiscal_responsibility": "We have fiduciary duty to the taxpayers.",
                "cash_flow": "Our liquidity position can't support this without bond issuance."
            },
            
            "citizens": {
                "frustrated": "We've been dealing with this for weeks! When will something change?",
                "supportive": "Finally! This is exactly what we've been asking for.",
                "confused": "Why is this taking so long? It seems simple to us.",
                "demanding": "Our taxes pay your salaries. We expect better service."
            }
        }