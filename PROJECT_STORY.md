# Mailopolis: Adversarial AI City Sustainability Game

## 🌍 Inspiration

In a world where climate change and urban sustainability challenges grow more pressing each day, we asked ourselves: **How can we make sustainability policy engaging and accessible?** Traditional city simulation games treat sustainability as a simple metric to optimize, but real urban planning involves complex political dynamics, competing interests, and adversarial actors who profit from unsustainable practices.

This realization sparked the creation of **Mailopolis** - an adversarial strategy game where players compete directly against AI-powered bad actors to influence a city's sustainability trajectory. Rather than building yet another city builder, we wanted to simulate the **real political battle** that sustainability advocates face when trying to implement meaningful environmental policies.


## 🎯 What We Built

**Core Concept**: You're a sustainability advisor competing against AI "bad actors" (developers, corporations) who actively lobby to corrupt the city with unsustainable policies for profit.

**Key Features**:
- **Multi-Agent AI System**: Each city department head has unique personalities, corruption resistance, and decision-making patterns powered by LangChain
- **AgentMail Communication**: Real-time messaging system where players and AI agents exchange policy proposals and influence decisions
- **Adversarial Gameplay**: AI opponents actively counter your sustainability efforts with bribes and competing proposals
- **Dynamic City Simulation**: City Sustainability Index (0-100) changes based on political battles and policy outcomes

**Victory Condition**: Maximize the City Sustainability Index while bad actors try to minimize it through political corruption.

## 🏗️ Technical Implementation

### Multi-Agent AI with LangChain
Each AI agent has a distinct personality matrix:
```python
@dataclass
class AgentPersonality:
    corruption_resistance: int  # 0-100, resistance to bribes
    sustainability_focus: int   # 0-100, environmental priority  
    political_awareness: int    # 0-100, considers politics
    decision_factors: List[str] # Priority ordering
```

**Example**: Dr. Marcus Chen (Energy Dept) has 85% sustainability focus but only 70% corruption resistance - he supports green energy but might be swayed by economic arguments.

### Backend Architecture
- **FastAPI + Multi-LLM**: Integrates OpenAI, Anthropic, and Google models for diverse agent behaviors
- **WebSocket Integration**: Live gameplay updates and agent notifications
- **JSON Persistence**: Conversation logs and game state storage
- **AgentMail Communication System**: Innovative email-based interface where players and AI agents communicate through authentic government-style email threads with subjects, formal messaging, and realistic political correspondence

### Frontend
- **React 18 + TypeScript**: Modern cyberpunk-inspired UI with interactive city visualization
- **Real-time Integration**: WebSocket-ready for live agent communications

## 🚧 Key Challenges Solved

**1. AI Agent Consistency**: Ensuring agents maintain believable personalities across conversations
- *Solution*: Sophisticated prompt engineering with personality profiles and decision history

**2. Game Balance**: Making the game winnable through skill while maintaining challenge
- *Solution*: Dynamic difficulty that scales bad actor aggression based on player success

**3. Complex State Management**: City systems with cascading policy effects across departments
- *Solution*: Comprehensive game engine simulating policy delays and unintended consequences

## 📚 What We Learned

- **Advanced AI**: Mastered multi-agent systems with personality persistence
- **Real-time Systems**: Built a WebSocket architecture for responsive multiplayer-style gameplay  
- **Game Design**: Balanced player agency with meaningful AI opposition
- **Urban Policy**: Gained appreciation for the political complexity of sustainability implementation

## 🌟 Impact & Future

**Educational Value**: Makes complex policy topics engaging through strategic gameplay
**Technical Innovation**: Demonstrates cutting-edge AI applications in serious gaming
**Real-world Relevance**: Could be adapted for actual policy simulation and urban planning education

**Next Steps**: Train reinforcement learning models to play the game autonomously, creating AI vs AI policy battles and generating training data for optimal sustainability strategies. Add multiplayer modes, partner with educational institutions for curriculum integration.

---

Mailopolis demonstrates how sophisticated AI can simulate the true complexity of real-world urban policy-making, where decisions depend on multiple interconnected factors, competing stakeholder interests, and cascading effects across city systems - creating an authentic representation of how sustainability policy actually works in practice.