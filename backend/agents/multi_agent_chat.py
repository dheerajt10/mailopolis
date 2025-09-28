import asyncio
from typing import Dict, List, Any, Optional, TYPE_CHECKING
from dataclasses import dataclass
from datetime import datetime

from agents.conversation_memory import ConversationMemory, ConversationMessage
from models.game_models import PolicyProposal, Department

if TYPE_CHECKING:
    from agents.langchain_agents import LangChainAgent

@dataclass
class ChatRound:
    round_number: int
    messages: List[ConversationMessage]
    coalitions_formed: List[List[str]] = None

class MultiAgentChatSystem:
    """Orchestrates multi-agent discussions with memory"""
    
    def __init__(self, agents: Dict[Department, 'LangChainAgent']):
        self.agents = agents
        self.memory = ConversationMemory()
        self.max_rounds = 3  # Limit conversation rounds
        
    async def discuss_proposal(self, proposal: PolicyProposal, 
                             game_context: Dict[str, Any]) -> List[ChatRound]:
        """Run multi-round discussion between agents"""
        print(f"🗣️  Starting {self.max_rounds}-round discussion for: {proposal.title}")
        chat_rounds = []
        
        try:
            # Round 1: Initial Reactions
            print("📢 Round 1: Initial department reactions...")
            round1 = await self._initial_reactions_round(proposal, game_context)
            chat_rounds.append(round1)
            
            # Round 2: Responses and Negotiations  
            print("🤝 Round 2: Inter-department negotiations...")
            round2 = await self._negotiation_round(proposal, game_context, round1.messages)
            chat_rounds.append(round2)
            
            # Round 3: Final Positions
            print("⚖️  Round 3: Final positions before mayor decision...")
            round3 = await self._final_positions_round(proposal, game_context, 
                                                     round1.messages + round2.messages)
            chat_rounds.append(round3)
            
            # Save entire conversation
            all_messages = []
            for round_data in chat_rounds:
                all_messages.extend(round_data.messages)
            
            proposal_id = proposal.title.replace(" ", "_").replace("/", "-").replace(":", "")
            self.memory.save_conversation(proposal_id, all_messages)
            
        except Exception as e:
            print(f"❌ Error during discussion: {e}")
            # Return at least empty rounds to prevent crashes
            if not chat_rounds:
                chat_rounds = [ChatRound(round_number=1, messages=[])]
        
        return chat_rounds
    
    async def _initial_reactions_round(self, proposal: PolicyProposal, 
                                     game_context: Dict[str, Any]) -> ChatRound:
        """Round 1: Each agent gives initial reaction"""
        messages = []
        
        # Exclude mayor from initial discussion - they decide after hearing others
        discussing_agents = {dept: agent for dept, agent in self.agents.items() 
                           if dept != Department.MAYOR}
        
        for dept, agent in discussing_agents.items():
            try:
                print(f"  🎤 Getting initial reaction from {agent.personality.name}...")
                message_content = await self._generate_initial_reaction(agent, proposal, game_context)
                
                messages.append(ConversationMessage(
                    speaker=agent.personality.name,
                    department=dept.value,
                    content=message_content,
                    timestamp=datetime.now(),
                    message_type="initial_reaction"
                ))
            except Exception as e:
                print(f"❌ Error getting reaction from {agent.personality.name}: {e}")
                # Add fallback message
                messages.append(ConversationMessage(
                    speaker=agent.personality.name,
                    department=dept.value,
                    content=f"I need to review this proposal more carefully from my department's perspective.",
                    timestamp=datetime.now(),
                    message_type="initial_reaction"
                ))
            
        return ChatRound(round_number=1, messages=messages)
    
    async def _negotiation_round(self, proposal: PolicyProposal, 
                               game_context: Dict[str, Any],
                               previous_messages: List[ConversationMessage]) -> ChatRound:
        """Round 2: Agents respond to each other and negotiate"""
        messages = []
        
        discussing_agents = {dept: agent for dept, agent in self.agents.items() 
                           if dept != Department.MAYOR}
        
        for dept, agent in discussing_agents.items():
            try:
                print(f"  🔄 {agent.personality.name} responding to colleagues...")
                # Get context about what others said
                others_context = self._build_others_context(agent, previous_messages)
                
                message_content = await self._generate_negotiation_response(
                    agent, proposal, game_context, others_context
                )
                
                messages.append(ConversationMessage(
                    speaker=agent.personality.name,
                    department=dept.value, 
                    content=message_content,
                    timestamp=datetime.now(),
                    message_type="negotiation",
                    references=[msg.speaker for msg in previous_messages]
                ))
            except Exception as e:
                print(f"❌ Error getting negotiation response from {agent.personality.name}: {e}")
                messages.append(ConversationMessage(
                    speaker=agent.personality.name,
                    department=dept.value,
                    content="I understand my colleagues' concerns and am willing to find common ground.",
                    timestamp=datetime.now(),
                    message_type="negotiation",
                    references=[msg.speaker for msg in previous_messages]
                ))
            
        return ChatRound(round_number=2, messages=messages)
    
    async def _final_positions_round(self, proposal: PolicyProposal,
                                   game_context: Dict[str, Any],
                                   all_previous_messages: List[ConversationMessage]) -> ChatRound:
        """Round 3: Final positions after hearing full discussion"""
        messages = []
        
        discussing_agents = {dept: agent for dept, agent in self.agents.items() 
                           if dept != Department.MAYOR}
        
        for dept, agent in discussing_agents.items():
            try:
                print(f"  ✋ {agent.personality.name} stating final position...")
                # Get full discussion context
                full_context = self._build_full_discussion_context(all_previous_messages)
                
                message_content = await self._generate_final_position(
                    agent, proposal, game_context, full_context
                )
                
                messages.append(ConversationMessage(
                    speaker=agent.personality.name,
                    department=dept.value,
                    content=message_content, 
                    timestamp=datetime.now(),
                    message_type="final_position"
                ))
            except Exception as e:
                print(f"❌ Error getting final position from {agent.personality.name}: {e}")
                messages.append(ConversationMessage(
                    speaker=agent.personality.name,
                    department=dept.value,
                    content="POSITION: NEUTRAL\nREASONING: I need more information to make a final decision.\nCONDITIONS: None",
                    timestamp=datetime.now(),
                    message_type="final_position"
                ))
            
        return ChatRound(round_number=3, messages=messages)
    
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