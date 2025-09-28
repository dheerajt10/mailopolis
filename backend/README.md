# 🏙️ Mailopolis Backend - Agent Decision System

## What We Built

A **sophisticated agent-based decision system** for the Mailopolis city management game. This backend demonstrates how **different agents behave differently** based on their personalities, departments, and current game state.

## 🧠 How Agents Work

### Agent Personalities Drive Decisions

Each agent has a unique personality that affects how they respond to player actions:

```python
# Dr. Sarah Rodriguez (Hospital Chief)
personality = AgentPersonality(
    decision_style="aggressive",      # Takes bold action for health
    priorities=[
        Priority(type="health", weight=0.6),  # 60% health focus
        Priority(type="budget", weight=0.2),  # 20% budget focus  
        Priority(type="approval", weight=0.2) # 20% approval focus
    ],
    risk_tolerance=85,                # High risk tolerance for health outcomes
    budget_sensitivity=40,            # Less worried about costs when health at stake
    sustainability_focus=35           # Lower environmental focus
)
```

### Different Agents, Different Responses

**Same advice, different reactions:**

- **Dr. Sarah Rodriguez (Hospital, Aggressive)**: ✅ 90% acceptance - "That's a solid approach. I'll implement it immediately."
- **Robert Kim (Finance, Cautious)**: ❌ 70% acceptance - "I appreciate the input, but I think we need a different approach here."
- **Dr. Marcus Chen (PowerGrid, Collaborative)**: ✅ 75% acceptance - "Great idea to loop in other departments."

## 🎮 Core Mechanics

### 1. **Trust-Based Decision Making**
- Each agent has a `trust_level` (0-100) toward the Shadow Mayor
- Higher trust = more likely to accept advice
- Trust changes based on action outcomes

### 2. **Context-Aware Responses** 
- Agents consider current game state (budget, health, approval)
- Crisis level affects willingness to cooperate
- Department priorities influence decisions

### 3. **Personality-Driven Behavior**
- **Cautious agents** prefer being asked before being advised
- **Aggressive agents** like decisive action
- **Collaborative agents** love involving other departments
- **Bureaucratic agents** worry about procedures and budgets

### 4. **Mayor Approval Effects**
When Mayor approval < 50%, agents become resistant:
- Advice acceptance drops significantly
- Recovery requires visible wins to rebuild trust

## 🚀 API Endpoints

### Get Game State
```bash
GET http://localhost:8000/api/game/state
```

### Get Daily Email Digest  
```bash
GET http://localhost:8000/api/emails/digest
```

### Process Player Actions
```bash
POST http://localhost:8000/api/actions/ask
POST http://localhost:8000/api/actions/advise  
POST http://localhost:8000/api/actions/forward
```

### Debug Agent Reactions
```bash
POST http://localhost:8000/api/debug/simulate-action
# See how ALL agents would react to an action without executing it
```

## 🧪 Testing the System

### Run the Agent Demo
```bash
cd backend
python demo_agents.py
```

This shows:
- ✅ 6 unique agents with different personalities
- 📧 Realistic email scenarios generated daily
- 🧠 How each agent reacts differently to the same advice
- 📈 Trust levels and acceptance rates in real-time

### Start the API Server
```bash
cd backend  
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🎯 Key Innovations

### 1. **Realistic Agent Personalities**
Each agent feels like a real person with:
- Consistent decision-making patterns
- Department-specific priorities  
- Personality quirks and communication styles

### 2. **Dynamic Trust System**
- Trust affects acceptance rates
- Actions have consequences for future interactions
- Recovery mechanisms when relationships sour

### 3. **Emergent Collaboration**
- Agents can work together when forwarded to each other
- Department synergy bonuses (e.g., PowerGrid + Finance = cost-effective solutions)
- Natural conversation chains

### 4. **Scalable Architecture**
- Easy to add new agent types
- JSON-configurable scenarios  
- Modular personality system

## 🔮 Next Steps

1. **Enhanced AI Responses** - Use LLM integration for more natural dialogue
2. **Learning Agents** - Agents remember past interactions and adapt
3. **Complex Scenarios** - Multi-day crises requiring sustained collaboration
4. **Citizen Sentiment** - Public opinion dynamically affects all decisions
5. **Real-time Events** - External factors (weather, news) impact agent behavior

## 📊 Performance Highlights

From our demo run:
- ✅ **6 distinct agent personalities** working simultaneously
- 🎯 **Different acceptance rates** for the same advice (90% vs 70%)  
- 📧 **Realistic email scenarios** generated dynamically
- ⚡ **Fast response times** - decisions made in milliseconds
- 🔄 **Stateful interactions** - trust persists between actions

This backend proves the core concept: **agents that feel human through personality-driven decision making.**