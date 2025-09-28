from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal, Union
from datetime import datetime
from enum import Enum
import uuid

class Department(str, Enum):
    POWER_GRID = "PowerGrid"
    HOSPITAL = "Hospital" 
    TRANSIT = "Transit"
    FINANCE = "Finance"
    MAYOR = "Mayor"
    CITIZENS = "Citizens"
    MEDIA = "Media"

class DecisionStyle(str, Enum):
    CAUTIOUS = "cautious"
    AGGRESSIVE = "aggressive"
    COLLABORATIVE = "collaborative"
    BUREAUCRATIC = "bureaucratic"

class CommunicationStyle(str, Enum):
    FORMAL = "formal"
    CASUAL = "casual"
    TECHNICAL = "technical"
    POLITICAL = "political"

class PriorityType(str, Enum):
    BUDGET = "budget"
    HEALTH = "health"
    APPROVAL = "approval"
    SUSTAINABILITY = "sustainability"
    EFFICIENCY = "efficiency"

class Priority(BaseModel):
    type: PriorityType
    weight: float = Field(ge=0, le=1)  # 0-1 scale

class AgentPersonality(BaseModel):
    decision_style: DecisionStyle
    priorities: List[Priority]
    communication_style: CommunicationStyle
    risk_tolerance: int = Field(ge=0, le=100)
    budget_sensitivity: int = Field(ge=0, le=100)
    public_opinion_sensitivity: int = Field(ge=0, le=100)
    sustainability_focus: int = Field(ge=0, le=100)
    
class Agent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    department: Department
    personality: AgentPersonality
    trust_level: int = Field(ge=0, le=100, default=75)
    response_time_base: int = Field(default=30)  # minutes
    current_workload: int = Field(ge=0, le=100, default=50)
    
    def get_response_time(self) -> int:
        """Calculate actual response time based on workload and trust"""
        base_time = self.response_time_base
        workload_multiplier = 1 + (self.current_workload / 100)
        trust_modifier = 1 - (self.trust_level / 200)  # Higher trust = faster response
        return int(base_time * workload_multiplier * (1 + trust_modifier))

class EnergyMix(BaseModel):
    solar: float = Field(ge=0, le=100)
    gas: float = Field(ge=0, le=100)
    wind: float = Field(ge=0, le=100)

class SustainabilityMetrics(BaseModel):
    emissions: float  # tCO2e
    energy_mix: EnergyMix
    water_stress: float = Field(ge=0, le=100)
    waste_diversion: float = Field(ge=0, le=100)

class GameState(BaseModel):
    city_health: int = Field(ge=0, le=100, default=75)
    budget: int = Field(default=1000000)  # in dollars
    approval: int = Field(ge=0, le=100, default=65)  # Mayor's approval
    influence_tier: Literal["Bronze", "Silver", "Gold", "Platinum", "Diamond"] = "Bronze"
    crisis_speed: Literal["Slow", "OK", "Fast"] = "OK"
    day: int = Field(default=1)
    sustainability_metrics: SustainabilityMetrics = Field(
        default_factory=lambda: SustainabilityMetrics(
            emissions=850.0,
            energy_mix=EnergyMix(solar=25, gas=60, wind=15),
            water_stress=45,
            waste_diversion=68
        )
    )

class ThreadTag(str, Enum):
    POWER = "power"
    HEALTH = "health" 
    TRANSIT = "transit"
    FINANCE = "finance"
    CRISIS = "crisis"
    SUSTAINABILITY = "sustainability"
    APPROVAL = "approval"
    BUDGET = "budget"
    OPPORTUNITY = "opportunity"

class MessageType(str, Enum):
    INITIAL = "initial"
    RESPONSE = "response"
    FORWARDED = "forwarded"
    ESCALATION = "escalation"

class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    thread_id: str
    from_agent: str
    to_agents: List[str]
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    message_type: MessageType = MessageType.RESPONSE
    metadata: Optional[Dict] = None

class EmailThread(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    subject: str
    participants: List[str]  # agent IDs
    messages: List[Message] = Field(default_factory=list)
    tags: List[ThreadTag] = Field(default_factory=list)
    priority: int = Field(ge=0, le=100)
    status: Literal["active", "resolved", "escalated", "ignored"] = "active"
    created_at: datetime = Field(default_factory=datetime.now)
    last_activity: datetime = Field(default_factory=datetime.now)
    crisis_level: Optional[Literal["low", "medium", "high", "critical"]] = None

class ActionType(str, Enum):
    ASK = "ask"
    ADVISE = "advise"
    FORWARD = "forward"

class PlayerAction(BaseModel):
    type: ActionType
    thread_id: str
    target_agent: Optional[str] = None  # for ask actions
    content: Optional[str] = None  # for advise actions
    new_participants: Optional[List[str]] = None  # for forward actions
    timestamp: datetime = Field(default_factory=datetime.now)

class OutcomeType(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral" 
    NEGATIVE = "negative"

class StateEffect(BaseModel):
    metric: str  # field name in GameState
    agent_id: Optional[str] = None  # for trust changes
    delta: Union[int, float]
    reason: str

class ActionOutcome(BaseModel):
    success: bool
    type: OutcomeType
    effects: List[StateEffect]
    message: str
    follow_up_threads: List[str] = Field(default_factory=list)

class CrisisType(str, Enum):
    POWER_OUTAGE = "power_outage"
    HOSPITAL_OVERFLOW = "hospital_overflow"
    TRANSIT_BREAKDOWN = "transit_breakdown"
    BUDGET_SHORTFALL = "budget_shortfall"
    PUBLIC_UNREST = "public_unrest"

class Crisis(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: CrisisType
    severity: Literal["minor", "major", "critical"]
    affected_departments: List[Department]
    description: str
    time_to_escalate: int  # minutes
    resolution_requirements: Dict[str, Union[List[Department], int]]