import asyncio
import random
from typing import Dict, List, Any, Optional, TYPE_CHECKING, Tuple
from dataclasses import dataclass
from datetime import datetime

from agents.conversation_memory import ConversationMemory, ConversationMessage
from models.game_models import PolicyProposal, Department
from service.async_logger import AsyncLogger

if TYPE_CHECKING:
    from agents.langchain_agents import LangChainAgent

@dataclass
class PrivateConversation:
    participants: List[str]  # Agent names
    messages: List[ConversationMessage]
    purpose: str  # "coalition_building", "information_sharing", "lobbying"
    
@dataclass
class MayorLobby:
    agent_name: str
    department: str
    message: ConversationMessage
    influence_attempt: str  # "support", "oppose", "modify"

@dataclass
class PoliticalDiscussion:
    proposal_id: str
    private_conversations: List[PrivateConversation]
    mayor_lobbying: List[MayorLobby]
    coalitions_formed: List[List[str]]
    final_positions: Dict[str, str]

class MultiAgentChatSystem:
    """Orchestrates independent agent conversations and political maneuvering"""
    
    def __init__(self, agents: Dict[Department, 'LangChainAgent'], logger: AsyncLogger = None):
        self.agents = agents
        self.memory = ConversationMemory()
        self.max_conversations = 8  # Maximum private conversations to simulate
        self.logger = logger or AsyncLogger()

    def _log(self, msg: str):
        self.logger.log(msg)
        
    async def discuss_proposal(self, proposal: PolicyProposal, 
                             game_context: Dict[str, Any]) -> PoliticalDiscussion:
        """Simulate independent political discussions and lobbying"""
        self._log(f"🏛️  Starting political maneuvering for: {proposal.title}")
        # Exclude mayor from initial discussions - they're the decision maker
        discussing_agents = {dept: agent for dept, agent in self.agents.items() 
                           if dept != Department.MAYOR}
        try:
            # Phase 1: Independent private conversations
            self._log("🤝 Phase 1: Private conversations and coalition building...")
            private_conversations = await self._simulate_private_conversations(
                proposal, game_context, discussing_agents
            )
            # Phase 2: Determine coalitions based on conversations
            self._log("🤝 Phase 2: Coalition formation...")
            coalitions = self._analyze_coalitions(private_conversations)
            # Phase 3: Agents decide whether to lobby the mayor
            self._log("👑 Phase 3: Mayor lobbying attempts...")
            mayor_lobbying = await self._simulate_mayor_lobbying(
                proposal, game_context, discussing_agents, private_conversations
            )
            # Phase 4: Collect final positions
            final_positions = self._determine_final_positions(private_conversations, coalitions)
            # Save the entire political discussion
            all_messages = []
            for conv in private_conversations:
                all_messages.extend(conv.messages)
            for lobby in mayor_lobbying:
                all_messages.append(lobby.message)
            proposal_id = proposal.title.replace(" ", "_").replace("/", "-").replace(":", "")
            self.memory.save_conversation(proposal_id, all_messages)
            return PoliticalDiscussion(
                proposal_id=proposal_id,
                private_conversations=private_conversations,
                mayor_lobbying=mayor_lobbying,
                coalitions_formed=coalitions,
                final_positions=final_positions
            )
        except Exception as e:
            self._log(f"❌ Error during political discussion: {e}")
            return PoliticalDiscussion(
                proposal_id=proposal.title,
                private_conversations=[],
                mayor_lobbying=[],
                coalitions_formed=[],
                final_positions={}
            )
    
    async def _simulate_private_conversations(self, proposal: PolicyProposal,
                                            game_context: Dict[str, Any],
                                            discussing_agents: Dict[Department, 'LangChainAgent']) -> List[PrivateConversation]:
        """Simulate independent private conversations between agents"""
        conversations = []
        agent_list = list(discussing_agents.values())
        # Create conversation pairs based on agent personalities and interests
        conversation_pairs = self._generate_conversation_pairs(agent_list, proposal)
        for i, (agent1, agent2, purpose) in enumerate(conversation_pairs):
            try:
                self._log(f"  💬 {agent1.personality.name} speaking privately with {agent2.personality.name} about {purpose}...")
                # Agent 1 initiates conversation
                message1 = await self._generate_private_message(agent1, agent2, proposal, game_context, purpose, is_initiator=True)
                # Agent 2 responds
                message2 = await self._generate_private_message(agent2, agent1, proposal, game_context, purpose, is_initiator=False, previous_message=message1)
                conversation = PrivateConversation(
                    participants=[agent1.personality.name, agent2.personality.name],
                    messages=[
                        ConversationMessage(
                            speaker=agent1.personality.name,
                            department=agent1.personality.department.value,
                            content=message1,
                            timestamp=datetime.now(),
                            message_type=f"private_{purpose}",
                            references=[agent2.personality.name]
                        ),
                        ConversationMessage(
                            speaker=agent2.personality.name,
                            department=agent2.personality.department.value,
                            content=message2,
                            timestamp=datetime.now(),
                            message_type=f"private_{purpose}_response",
                            references=[agent1.personality.name]
                        )
                    ],
                    purpose=purpose
                )
                conversations.append(conversation)
            except Exception as e:
                self._log(f"❌ Error in private conversation: {e}")
        return conversations
    
    def _generate_conversation_pairs(self, agents: List['LangChainAgent'], 
                                   proposal: PolicyProposal) -> List[Tuple['LangChainAgent', 'LangChainAgent', str]]:
        """Generate pairs of agents likely to have private conversations"""
        pairs = []
        
        # Strategy 1: Agents with similar values (coalition building)
        for i in range(len(agents)):
            for j in range(i + 1, len(agents)):
                agent1, agent2 = agents[i], agents[j]
                
                # Check if they share core values
                shared_values = set(agent1.personality.core_values) & set(agent2.personality.core_values)
                
                if len(shared_values) >= 2:
                    pairs.append((agent1, agent2, "coalition_building"))
                elif self._are_departments_related(agent1.personality.department, agent2.personality.department):
                    pairs.append((agent1, agent2, "information_sharing"))
                elif random.random() < 0.3:  # Some random conversations
                    pairs.append((agent1, agent2, "general_discussion"))
        
        # Limit to reasonable number of conversations
        return pairs[:self.max_conversations//2]
    
    def _are_departments_related(self, dept1: Department, dept2: Department) -> bool:
        """Check if two departments typically collaborate"""
        related_pairs = {
            (Department.ENERGY, Department.TRANSPORTATION),
            (Department.HOUSING, Department.WATER),
            (Department.WASTE, Department.WATER),
            (Department.ECONOMIC_DEV, Department.ENERGY),
            (Department.CITIZENS, Department.HOUSING),
        }
        return (dept1, dept2) in related_pairs or (dept2, dept1) in related_pairs
    
    async def _simulate_mayor_lobbying(self, proposal: PolicyProposal,
                                      game_context: Dict[str, Any],
                                      discussing_agents: Dict[Department, 'LangChainAgent'],
                                      conversations: List[PrivateConversation]) -> List[MayorLobby]:
        """Simulate agents deciding whether to lobby the mayor"""
        lobbying_attempts = []
        
        for dept, agent in discussing_agents.items():
            # Agent decides if they want to lobby the mayor
            should_lobby = await self._agent_decides_to_lobby(agent, proposal, conversations)
            
            if should_lobby:
                try:
                    self._log(f"  👑 {agent.personality.name} lobbying the mayor...")
                    
                    # Generate lobbying message
                    lobby_message, influence_type = await self._generate_lobby_message(
                        agent, proposal, game_context, conversations
                    )
                    
                    lobbying_attempts.append(MayorLobby(
                        agent_name=agent.personality.name,
                        department=dept.value,
                        message=ConversationMessage(
                            speaker=agent.personality.name,
                            department=dept.value,
                            content=lobby_message,
                            timestamp=datetime.now(),
                            message_type="mayor_lobbying",
                            references=["Mayor"]
                        ),
                        influence_attempt=influence_type
                    ))
                    
                except Exception as e:
                    self._log(f"❌ Error in mayor lobbying from {agent.personality.name}: {e}")
        
        return lobbying_attempts
    
    async def _generate_private_message(self, agent: 'LangChainAgent',
                                       other_agent: 'LangChainAgent',
                                       proposal: PolicyProposal,
                                       game_context: Dict[str, Any],
                                       purpose: str,
                                       is_initiator: bool = False,
                                       previous_message: str = None) -> str:
        """Generate a private conversation message between two agents"""
        
        # Get personalities for context
        personality_context = self._format_personality_context(agent.personality)
        other_personality = f"SPEAKING WITH: {other_agent.personality.name} ({other_agent.personality.department.value})"
        
        if is_initiator:
            user_input = f"""PRIVATE CONVERSATION - YOU ARE INITIATING:

PROPOSAL: {proposal.title}
DESCRIPTION: {proposal.description}

{personality_context}

{other_personality}

PURPOSE: {purpose.replace('_', ' ').title()}

You want to speak privately with {other_agent.personality.name} about this proposal. Based on your personality and the purpose of this conversation:

- If COALITION_BUILDING: Try to find common ground and see if you can work together
- If INFORMATION_SHARING: Share your department's expertise and learn from theirs
- If GENERAL_DISCUSSION: Express your views and gauge their position

Keep it conversational and authentic to your personality. 2-3 sentences max."""

        else:
            user_input = f"""PRIVATE CONVERSATION - RESPONDING:

PROPOSAL: {proposal.title}

{personality_context}

{other_personality}

{other_agent.personality.name} just said to you:
"{previous_message}"

Respond authentically based on your personality and department interests. You can:
- Agree and build on their points
- Express concerns or disagreements
- Propose alternatives or modifications
- Share your department's perspective

Keep it conversational. 2-3 sentences max."""

        if agent.llm:
            try:
                messages = agent.prompt_template.format_messages(user_input=user_input)
                response = await agent.llm.ainvoke(messages)
                return response.content.strip()
            except Exception as e:
                self._log(f"❌ Error generating private message: {e}")
                return f"I'd like to discuss this proposal with you from my department's perspective."
        else:
            return f"Let me share {agent.personality.department.value}'s view on this proposal with you."

    async def _agent_decides_to_lobby(self, agent: 'LangChainAgent',
                                    proposal: PolicyProposal,
                                    conversations: List[PrivateConversation]) -> bool:
        """Agent decides whether they want to lobby the mayor based on their personality and conversations"""
        
        # High political awareness agents more likely to lobby
        lobby_probability = agent.personality.political_awareness / 100
        
        # Agents with strong positions more likely to lobby
        if agent.personality.sustainability_focus > 70 and proposal.sustainability_impact > 30:
            lobby_probability += 0.3
        
        # If they're in conversations that went well, more likely to lobby
        agent_conversations = [c for c in conversations if agent.personality.name in c.participants]
        if len(agent_conversations) >= 2:
            lobby_probability += 0.2
            
        return random.random() < min(0.8, lobby_probability)

    async def _generate_lobby_message(self, agent: 'LangChainAgent',
                                    proposal: PolicyProposal,
                                    game_context: Dict[str, Any],
                                    conversations: List[PrivateConversation]) -> Tuple[str, str]:
        """Generate message for lobbying the mayor"""
        
        personality_context = self._format_personality_context(agent.personality)
        
        # Summarize relevant conversations
        conversation_context = ""
        agent_conversations = [c for c in conversations if agent.personality.name in c.participants]
        if agent_conversations:
            conversation_context = f"\nRECENT DISCUSSIONS:\n"
            for conv in agent_conversations[:2]:
                other_participant = [p for p in conv.participants if p != agent.personality.name][0]
                conversation_context += f"- Spoke with {other_participant} about {conv.purpose}\n"
        
        user_input = f"""LOBBYING THE MAYOR - PRIVATE MEETING:

PROPOSAL: {proposal.title}
DESCRIPTION: {proposal.description}

{personality_context}

{conversation_context}

You have requested a private meeting with the Mayor to influence their decision on this proposal. Based on your personality, department expertise, and recent conversations:

Choose your influence strategy:
- SUPPORT: Advocate for approval with strong arguments
- OPPOSE: Argue against approval with your concerns  
- MODIFY: Suggest specific changes to make it acceptable

Provide compelling arguments based on your expertise and values. Be persuasive but stay in character.

Format your response as:
STRATEGY: [SUPPORT/OPPOSE/MODIFY]
MESSAGE: [Your persuasive argument in 3-4 sentences as {agent.personality.name}]"""

        if agent.llm:
            try:
                messages = agent.prompt_template.format_messages(user_input=user_input)
                response = await agent.llm.ainvoke(messages)
                
                lines = response.content.split('\n')
                strategy = "support"  # default
                message = response.content
                
                for line in lines:
                    if line.startswith('STRATEGY:'):
                        strategy = line.replace('STRATEGY:', '').strip().lower()
                    elif line.startswith('MESSAGE:'):
                        message = line.replace('MESSAGE:', '').strip()
                
                return message, strategy
                
            except Exception as e:
                self._log(f"❌ Error generating lobby message: {e}")
                return f"I wanted to share my department's perspective on this proposal with you.", "support"
        else:
            return f"As {agent.personality.name}, I believe this proposal needs careful consideration.", "support"

    def _analyze_coalitions(self, conversations: List[PrivateConversation]) -> List[List[str]]:
        """Analyze conversations to identify formed coalitions"""
        coalitions = []
        
        # Simple coalition detection based on agreement patterns
        potential_coalitions = {}
        
        for conv in conversations:
            if conv.purpose == "coalition_building" and len(conv.messages) >= 2:
                # Check if both agents seem to agree (simple text analysis)
                message1 = conv.messages[0].content.lower()
                message2 = conv.messages[1].content.lower()
                
                agreement_words = ["agree", "support", "together", "coalition", "alliance", "work with"]
                
                if any(word in message1 + " " + message2 for word in agreement_words):
                    participants = tuple(sorted(conv.participants))
                    potential_coalitions[participants] = True
        
        # Convert to list format
        for participants in potential_coalitions.keys():
            coalitions.append(list(participants))
        
        return coalitions

    def _determine_final_positions(self, conversations: List[PrivateConversation],
                                 coalitions: List[List[str]]) -> Dict[str, str]:
        """Determine each agent's final position based on conversations"""
        positions = {}
        
        # Analyze each agent's stance from their conversations
        all_agents = set()
        for conv in conversations:
            all_agents.update(conv.participants)
        
        for agent_name in all_agents:
            agent_conversations = [c for c in conversations if agent_name in c.participants]
            
            # Simple sentiment analysis based on conversation content
            total_sentiment = 0
            for conv in agent_conversations:
                agent_messages = [m for m in conv.messages if m.speaker == agent_name]
                for message in agent_messages:
                    content = message.content.lower()
                    if any(word in content for word in ["support", "good", "agree", "beneficial"]):
                        total_sentiment += 1
                    elif any(word in content for word in ["oppose", "bad", "disagree", "harmful"]):
                        total_sentiment -= 1
            
            if total_sentiment > 0:
                positions[agent_name] = "SUPPORT"
            elif total_sentiment < 0:
                positions[agent_name] = "OPPOSE"
            else:
                positions[agent_name] = "NEUTRAL"
        
        return positions

    async def _generate_initial_reaction(self, agent: 'LangChainAgent', 
                                       proposal: PolicyProposal,
                                       game_context: Dict[str, Any]) -> str:
        """Generate agent's initial reaction to proposal"""
        
        # Get agent's conversation history for context
        past_conversations = self.memory.get_recent_conversations(agent.personality.name, limit=3)
        history_context = self._format_conversation_history(past_conversations, agent.personality.name)
        
        # Get agent personality details
        personality_context = self._format_personality_context(agent.personality)
        
        user_input = f"""POLICY PROPOSAL FOR DISCUSSION:

PROPOSAL: {proposal.title}
DESCRIPTION: {proposal.description}
TARGET DEPARTMENT: {proposal.target_department.value}
SUSTAINABILITY IMPACT: {proposal.sustainability_impact:+d}
ECONOMIC IMPACT: {proposal.economic_impact:+d}
POLITICAL IMPACT: {proposal.political_impact:+d}

{personality_context}

{history_context}

This is the beginning of a multi-agent discussion about this proposal. Give your initial reaction as {agent.personality.name}. Other department heads will also share their views, then you'll have a chance to respond.

Respond according to your personality traits and department priorities. Keep your response to 2-3 sentences and stay in character."""

        if agent.llm:
            try:
                messages = agent.prompt_template.format_messages(user_input=user_input)
                response = await agent.llm.ainvoke(messages)
                return response.content.strip()
            except Exception as e:
                print(f"❌ Error generating initial reaction for {agent.personality.name}: {e}")
                return f"I need to review this proposal more carefully from my department's perspective. [{agent.personality.name}]"
        else:
            return f"As {agent.personality.name}, I need to consider how this proposal impacts {agent.personality.department.value}."

    async def _generate_negotiation_response(self, agent: 'LangChainAgent',
                                           proposal: PolicyProposal,
                                           game_context: Dict[str, Any],
                                           others_context: str) -> str:
        """Generate agent's response to others' positions"""
        
        # Get agent personality details for negotiation context
        personality_context = self._format_personality_context(agent.personality)
        
        # Get past relationship context with other agents
        relationship_context = self._build_relationship_context(agent, others_context)
        
        user_input = f"""CONTINUING DISCUSSION - RESPOND TO COLLEAGUES:

ORIGINAL PROPOSAL: {proposal.title}

{personality_context}

{relationship_context}

WHAT YOUR COLLEAGUES HAVE SAID:
{others_context}

Now respond to your colleagues' points based on your personality and department priorities. You can:
- Address specific concerns they raised (consider your communication style)
- Propose modifications or compromises (based on your risk tolerance and collaboration style)
- Build coalitions by agreeing with others (consider your political awareness)
- Stand firm on your position if needed (based on your core values)
- Suggest alternative approaches (consider your sustainability focus and department expertise)

Respond authentically as {agent.personality.name} according to your personality traits. Keep response to 2-3 sentences."""

        if agent.llm:
            try:
                messages = agent.prompt_template.format_messages(user_input=user_input)
                response = await agent.llm.ainvoke(messages)
                return response.content.strip()
            except Exception as e:
                print(f"❌ Error generating negotiation response for {agent.personality.name}: {e}")
                return f"I understand my colleagues' concerns and am willing to find common ground."
        else:
            return f"Let me work with my colleagues to find a solution that works for everyone."

    async def _generate_final_position(self, agent: 'LangChainAgent',
                                     proposal: PolicyProposal, 
                                     game_context: Dict[str, Any],
                                     full_context: str) -> str:
        """Generate agent's final position after full discussion"""
        
        # Get agent personality details for final decision
        personality_context = self._format_personality_context(agent.personality)
        
        user_input = f"""FINAL POSITION - FULL DISCUSSION SUMMARY:

PROPOSAL: {proposal.title}

{personality_context}

FULL DISCUSSION SO FAR:
{full_context}

Based on this complete discussion and your personality traits, state your final position on the proposal. This will go to the Mayor for final decision.

Consider:
- Your core values and decision factors (in order of importance)
- Your department's specific needs and expertise
- Your risk tolerance and political awareness
- What your colleagues have said and any coalitions formed
- Your corruption resistance and sustainability focus

Format your response as:
POSITION: [SUPPORT/OPPOSE/CONDITIONAL_SUPPORT]  
REASONING: [Your final reasoning in 2-3 sentences as {agent.personality.name}, reflecting your communication style]
CONDITIONS: [Any conditions for support based on your priorities, or "None"]"""

        if agent.llm:
            try:
                messages = agent.prompt_template.format_messages(user_input=user_input)  
                response = await agent.llm.ainvoke(messages)
                return response.content.strip()
            except Exception as e:
                print(f"❌ Error generating final position for {agent.personality.name}: {e}")
                return f"POSITION: NEUTRAL\nREASONING: I need more information to make a final decision.\nCONDITIONS: None"
        else:
            return f"POSITION: NEUTRAL\nREASONING: After discussion, I maintain a neutral stance.\nCONDITIONS: None"

    def _build_others_context(self, current_agent: 'LangChainAgent', 
                            messages: List[ConversationMessage]) -> str:
        """Build context string of what other agents said"""
        others_messages = [msg for msg in messages if msg.speaker != current_agent.personality.name]
        
        if not others_messages:
            return "No other agents have spoken yet."
            
        context_parts = []
        for msg in others_messages:
            context_parts.append(f"{msg.speaker} ({msg.department}): {msg.content}")
            
        return "\n\n".join(context_parts)
    
    def _build_full_discussion_context(self, all_messages: List[ConversationMessage]) -> str:
        """Build context string of entire discussion"""
        if not all_messages:
            return "No discussion has occurred yet."
            
        context_parts = []
        for msg in all_messages:
            context_parts.append(f"[{msg.message_type.upper()}] {msg.speaker}: {msg.content}")
            
        return "\n\n".join(context_parts)
    
    def _format_conversation_history(self, past_conversations: List[Dict], agent_name: str) -> str:
        """Format agent's conversation history for context"""
        if not past_conversations:
            return "CONVERSATION HISTORY: This is your first major proposal discussion."
            
        history_parts = ["RECENT CONVERSATION HISTORY:"]
        
        for i, convo in enumerate(past_conversations[:2]):  # Limit to 2 recent conversations
            history_parts.append(f"Previous Proposal: {convo.get('proposal_id', 'Unknown')}")
            # Find this agent's messages in the conversation
            agent_messages = [msg for msg in convo.get('messages', []) if msg['speaker'] == agent_name]
            if agent_messages:
                # Get their last message in that conversation
                last_msg = agent_messages[-1]['content'][:100]
                history_parts.append(f"Your position: {last_msg}...")
        
        return "\n".join(history_parts)

    def _format_personality_context(self, personality) -> str:
        """Format agent personality information for context"""
        return f"""YOUR PERSONALITY PROFILE:
- Name: {personality.name}
- Role: {personality.role}
- Department: {personality.department.value}
- Core Values: {', '.join(personality.core_values)}
- Communication Style: {personality.communication_style}
- Decision Factors (priority order): {'; '.join(personality.decision_factors)}
- Corruption Resistance: {personality.corruption_resistance}%
- Sustainability Focus: {personality.sustainability_focus}%
- Political Awareness: {personality.political_awareness}%
- Risk Tolerance: {personality.risk_tolerance}%"""
    
    def _build_relationship_context(self, current_agent: 'LangChainAgent', others_context: str) -> str:
        """Build context about relationships with other agents based on past interactions"""
        # Extract other agent names from the context
        relationship_parts = []
        
        # Simple extraction of agent names from others_context
        lines = others_context.split('\n')
        other_agents = []
        for line in lines:
            if ':' in line:
                agent_name = line.split(':')[0].split('(')[0].strip()
                if agent_name != current_agent.personality.name:
                    other_agents.append(agent_name)
        
        if other_agents:
            relationship_parts.append("RELATIONSHIP CONTEXT:")
            for other_agent in other_agents[:3]:  # Limit to first 3 to avoid too much context
                relationship_info = self.memory.get_agent_relationship_context(
                    current_agent.personality.name, other_agent
                )
                if "No significant" not in relationship_info:
                    relationship_parts.append(f"With {other_agent}: {relationship_info[:150]}...")
        
        return '\n'.join(relationship_parts) if relationship_parts else "RELATIONSHIP CONTEXT: First-time discussion with these colleagues."

    def get_discussion_stats(self) -> Dict[str, Any]:
        """Get statistics about discussions"""
        return self.memory.get_conversation_stats()