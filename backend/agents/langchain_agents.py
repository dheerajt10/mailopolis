"""
LangChain-powered agent personalities for Mailopolis sustai        # Initialize LangChain LLM
        self.llm = None
        if use_openai and os.getenv("OPENAI_API_KEY"):
            try:
                self.llm = ChatOpenAI(
                    model="gpt-4o-mini",  # More cost-effective
                    temperature=temperature,
                    max_tokens=500
                )
                self.provider_name = "OpenAI GPT-4o-mini"
                print("✅ Initialized OpenAI GPT-4o-mini")
            except Exception as e:
                print(f"❌ Failed to initialize OpenAI: {e}")
        
        if not self.llm and os.getenv("ANTHROPIC_API_KEY"):
            try:
                self.llm = ChatAnthropic(
                    model="claude-3-haiku-20240307",  # Fast and cost-effective
                    temperature=temperature,
                    max_tokens=500
                )
                self.provider_name = "Anthropic Claude-3 Haiku"
                print("✅ Initialized Anthropic Claude")
            except Exception as e:
                print(f"❌ Failed to initialize Anthropic: {e}")
        
        if not self.llm:
            # Fallback to mock provider for testing
            self.provider_name = "Mock LLM (No API keys or initialization failed)"
            print("⚠️ Using Mock LLM - no working providers") cleaner and more robust than custom LLM integration.
"""

import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

from models.game_models import PolicyProposal, SustainabilityGameState, Department

@dataclass
class ProposalEvaluation:
    """Response from LangChain agent evaluation of a proposal"""
    accept: bool
    reasoning: str
    confidence: int  # 0-100
    concerns: List[str]
    alternative_suggestions: List[str] = None

# Import the AgentPersonality from existing file
from agents.agent_personalities import AgentPersonality

# Add method to existing AgentPersonality class
def get_system_prompt(self) -> str:
    """Generate LangChain system prompt from personality"""
    return f"""You are {self.name}, {self.role} in Mailopolis.

PERSONALITY & VALUES:
- Core Values: {', '.join(self.core_values)}
- Communication Style: {self.communication_style}
- Corruption Resistance: {self.corruption_resistance}% (how likely you are to resist bribes/influence)
- Sustainability Focus: {self.sustainability_focus}% (how much you prioritize environmental issues)
- Political Awareness: {self.political_awareness}% (how much you consider political implications)
- Risk Tolerance: {self.risk_tolerance}% (willingness to try new/experimental approaches)

DECISION FACTORS (in order of importance):
{chr(10).join(f"• {factor}" for factor in self.decision_factors)}

You always respond authentically according to your personality. Your communication style should reflect your background and values. When evaluating proposals, consider them through the lens of your department's needs and your personal values.

RESPONSE FORMAT (use this EXACT format):
Decision: [SUPPORT/OPPOSE/NEUTRAL]
Reasoning: [2-3 sentences explaining your position in your communication style]
Confidence: [Rate 1-10]
Concerns: [Any concerns, or "None" if no concerns]"""

# Monkey patch the method to the existing class
AgentPersonality.get_system_prompt = get_system_prompt

class LangChainAgentManager:
    """Manages LangChain-powered agents for the sustainability game"""
    
    def __init__(self, use_openai: bool = True, temperature: float = 0.7):
        self.temperature = temperature
        
        # Initialize LangChain LLM
        if use_openai and os.getenv("OPENAI_API_KEY"):
            self.llm = ChatOpenAI(
                model="gpt-4o-mini",  # More cost-effective
                temperature=temperature,
                max_tokens=500
            )
            self.provider_name = "OpenAI GPT-4o-mini"
        elif os.getenv("ANTHROPIC_API_KEY"):
            self.llm = ChatAnthropic(
                model="claude-3-haiku-20240307",  # Fast and cost-effective
                temperature=temperature,
                max_tokens=500
            )
            self.provider_name = "Anthropic Claude-3 Haiku"
        else:
            # Fallback to mock responses
            self.llm = None
            self.provider_name = "Mock LLM (No API keys)"
            
        # Create agents for each department
        from agents.agent_personalities import AgentPersonalities
        personalities = AgentPersonalities.get_all_personalities()
        
        self.agents: Dict[Department, 'LangChainAgent'] = {}
        for dept, personality in personalities.items():
            self.agents[dept] = LangChainAgent(personality, self.llm)
    
    async def evaluate_proposal_by_department(self, proposal: PolicyProposal, 
                                            department: Department,
                                            game_context: Dict[str, Any]) -> ProposalEvaluation:
        """Get evaluation from specific department"""
        if department in self.agents:
            return await self.agents[department].evaluate_proposal(proposal, game_context)
        else:
            # Fallback for unknown department
            return ProposalEvaluation(
                accept=False,
                reasoning="Department not found for evaluation",
                confidence=0,
                concerns=["Unknown department"],
                alternative_suggestions=[]
            )
    
    async def get_all_reactions(self, proposal: PolicyProposal, 
                              game_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get reactions from all department agents"""
        reactions = []
        
        for dept, agent in self.agents.items():
            if dept == Department.MAYOR:
                continue  # Mayor decides, others advise
                
            try:
                evaluation = await agent.evaluate_proposal(proposal, game_context)
                reactions.append({
                    "from": agent.personality.name,
                    "department": dept.value,
                    "message": evaluation.reasoning,
                    "support_level": evaluation.confidence,
                    "concerns": evaluation.concerns,
                    "decision": "SUPPORT" if evaluation.accept else "OPPOSE"
                })
            except Exception as e:
                reactions.append({
                    "from": f"Error from {dept.value}",
                    "department": dept.value,
                    "message": f"Unable to evaluate proposal: {str(e)}",
                    "support_level": 50,
                    "concerns": ["Technical error"],
                    "decision": "NEUTRAL"
                })
                
        return reactions
    
    async def mayor_decide(self, proposal: PolicyProposal, 
                          game_context: Dict[str, Any]) -> ProposalEvaluation:
        """Mayor makes final decision on proposal"""
        return await self.agents[Department.MAYOR].evaluate_proposal(proposal, game_context)
    
    async def generate_counter_proposal(self, rejected_proposal: PolicyProposal,
                                      department: Department,
                                      game_context: Dict[str, Any]) -> Optional[PolicyProposal]:
        """Generate counter-proposal from specific department"""
        if department in self.agents:
            return await self.agents[department].generate_counter_proposal(rejected_proposal, game_context)
        return None

class LangChainAgent:
    """Individual agent powered by LangChain"""
    
    def __init__(self, personality: AgentPersonality, llm):
        self.personality = personality
        self.llm = llm
        self.conversation_history: List[Dict] = []
        
        # Create LangChain prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(personality.get_system_prompt()),
            HumanMessagePromptTemplate.from_template("{user_input}")
        ])
    
    async def evaluate_proposal(self, proposal: PolicyProposal, 
                               game_context: Dict[str, Any]) -> ProposalEvaluation:
        """Evaluate a policy proposal using LangChain"""
        
        # Build context string
        context_info = self._build_context_string(proposal, game_context)
        
        user_input = f"""POLICY PROPOSAL EVALUATION:

{context_info}

PROPOSAL DETAILS:
- Title: {proposal.title}
- Description: {proposal.description}
- Target Department: {proposal.target_department.value}
- Proposed by: {proposal.proposed_by}
- Potential Sustainability Impact: {proposal.sustainability_impact:+d}
- Economic Impact: {proposal.economic_impact:+d}
- Political Impact: {proposal.political_impact:+d}
{'- Bribe Amount: $' + f'{proposal.bribe_amount:,}' if proposal.bribe_amount > 0 else ''}

Please evaluate this proposal considering your role, values, and decision factors. 

Respond with:
1. Decision (SUPPORT/OPPOSE/NEUTRAL)
2. Reasoning (2-3 sentences in your authentic voice)
3. Confidence level (1-10)
4. Any concerns or suggestions"""
        
        if self.llm:
            try:
                # Use LangChain to generate response
                messages = self.prompt_template.format_messages(user_input=user_input)
                print(f"🤖 {self.personality.name}: Making LLM call...")
                response = await self.llm.ainvoke(messages)
                response_text = response.content
                print(f"📥 {self.personality.name}: Received LLM response: {response_text[:100]}...")
                
                # Parse the structured response
                return self._parse_evaluation_response(response_text, proposal)
                
            except Exception as e:
                print(f"❌ {self.personality.name}: LLM call failed: {e}")
                # Fallback to mock response
                return self._generate_mock_evaluation(proposal, game_context)
        else:
            print(f"⚠️ {self.personality.name}: Using mock LLM (no provider)")
            # Mock LLM fallback
            return self._generate_mock_evaluation(proposal, game_context)
    
    async def generate_counter_proposal(self, original_proposal: PolicyProposal,
                                      game_context: Dict[str, Any]) -> Optional[PolicyProposal]:
        """Generate counter-proposal using LangChain"""
        
        user_input = f"""The following proposal was rejected:

ORIGINAL PROPOSAL:
- Title: {original_proposal.title}
- Description: {original_proposal.description}
- Target Department: {original_proposal.target_department.value}
- Sustainability Impact: {original_proposal.sustainability_impact:+d}

Given your expertise and values, suggest a counter-proposal that addresses the same issue but might be more acceptable.

Format your response as:
TITLE: [new title]
DESCRIPTION: [modified description]
SUSTAINABILITY_IMPACT: [number between -20 and +20]
EXPLANATION: [why this version might work better]"""

        if self.llm:
            try:
                messages = self.prompt_template.format_messages(user_input=user_input)
                response = await self.llm.ainvoke(messages)
                return self._parse_counter_proposal(response.content, original_proposal)
            except Exception:
                return None
        else:
            # Mock counter-proposal
            return PolicyProposal(
                title=f"Modified {original_proposal.title}",
                description=f"A more politically feasible version of: {original_proposal.description}",
                target_department=original_proposal.target_department,
                sustainability_impact=max(1, original_proposal.sustainability_impact // 2),
                economic_impact=original_proposal.economic_impact + 2,
                political_impact=original_proposal.political_impact + 3,
                proposed_by=f"{self.personality.department.value}_counter"
            )
    
    def _build_context_string(self, proposal: PolicyProposal, game_context: Dict[str, Any]) -> str:
        """Build context string for LangChain agent"""
        return f"""CURRENT CITY CONTEXT:
- Overall Sustainability Index: {game_context.get('sustainability_index', 50)}/100
- Your Department Score: {game_context.get('department_scores', {}).get(self.personality.department, 50)}/100
- Mayor Trust in Player: {game_context.get('trust_in_player', 50)}/100
- Bad Actor Influence: {game_context.get('bad_actor_influence', 0)}/100
- Round: {game_context.get('round_number', 1)}"""
    
    def _parse_evaluation_response(self, response: str, proposal: PolicyProposal) -> ProposalEvaluation:
        """Parse LangChain response into structured evaluation"""
        response_lower = response.lower()
        
        # Extract decision - look for "Decision:" line first
        accept = False
        lines = [line.strip() for line in response.split('\n') if line.strip()]
        
        for line in lines:
            if line.startswith('Decision:'):
                decision_text = line.replace('Decision:', '').strip().upper()
                if decision_text == 'SUPPORT':
                    accept = True
                elif decision_text == 'OPPOSE':
                    accept = False
                break
        else:
            # Fallback to searching for keywords in entire response
            if any(word in response_lower for word in ['support', 'approve', 'accept', 'favor', 'yes']):
                accept = True
            elif any(word in response_lower for word in ['oppose', 'reject', 'against', 'decline', 'no']):
                accept = False
        
        # Extract confidence (look for numbers 1-10 or percentages)
        confidence = 70  # Default reasonable confidence
        import re
        
        # Look for "Confidence: X" pattern first
        for line in lines:
            if line.startswith('Confidence:'):
                conf_str = line.replace('Confidence:', '').strip()
                try:
                    confidence = int(conf_str) * 10
                    break
                except ValueError:
                    continue
        
        # Fallback patterns if direct "Confidence:" not found
        if confidence == 70:  # Still default
            confidence_patterns = [
                r'confidence[:\s]*([1-9]|10)',  # "confidence: 8"
                r'([1-9]|10)[/\s]*10',          # "8/10" or "8 out of 10"
                r'([1-9]|10)\s*confidence',     # "8 confidence"
            ]
            
            for pattern in confidence_patterns:
                matches = re.findall(pattern, response, re.IGNORECASE)
                if matches:
                    try:
                        confidence = int(matches[0]) * 10
                        break
                    except (ValueError, IndexError):
                        continue
        
        # Extract reasoning - look for "Reasoning:" line specifically
        lines = [line.strip() for line in response.split('\n') if line.strip()]
        reasoning = "Based on my analysis, this proposal requires careful consideration."
        
        # Look for "Reasoning:" line first
        for line in lines:
            if line.startswith('Reasoning:'):
                reasoning = line.replace('Reasoning:', '').strip()
                break
            elif line.startswith('2. Reasoning:'):
                reasoning = line.replace('2. Reasoning:', '').strip()
                break
        
        # If no "Reasoning:" found, look for substantial text
        if reasoning == "Based on my analysis, this proposal requires careful consideration.":
            for line in lines:
                if (len(line) > 30 and 
                    not line.startswith(('Decision:', 'Confidence:', 'Concerns:', 'Suggestions:', '1.', '2.', '3.', '4.')) and
                    not line.upper() in ['SUPPORT', 'OPPOSE', 'NEUTRAL']):
                    reasoning = line.strip()
                    break
        
        # Extract concerns
        concerns = []
        in_concerns = False
        for line in lines:
            if 'concerns:' in line.lower() or 'concern:' in line.lower():
                in_concerns = True
                # Extract concern from same line
                concern_text = line.split(':', 1)[-1].strip()
                if concern_text and len(concern_text) > 5:
                    concerns.append(concern_text)
            elif in_concerns and line.startswith('-'):
                concerns.append(line[1:].strip())
            elif in_concerns and not line.startswith(('Suggestions:', 'Decision:')):
                if len(line) > 10:
                    concerns.append(line)
            else:
                in_concerns = False
        
        return ProposalEvaluation(
            accept=accept,
            reasoning=reasoning,
            confidence=confidence,
            concerns=concerns[:3],  # Limit to 3 concerns
            alternative_suggestions=[]
        )
    
    def _parse_counter_proposal(self, response: str, original: PolicyProposal) -> Optional[PolicyProposal]:
        """Parse counter-proposal from LangChain response"""
        try:
            lines = response.strip().split('\n')
            title = description = explanation = ""
            sustainability_impact = 0
            
            for line in lines:
                line = line.strip()
                if line.upper().startswith("TITLE:"):
                    title = line[6:].strip()
                elif line.upper().startswith("DESCRIPTION:"):
                    description = line[12:].strip()
                elif line.upper().startswith("SUSTAINABILITY_IMPACT:"):
                    impact_str = line[22:].strip()
                    try:
                        sustainability_impact = int(impact_str.replace('+', '').replace('-', ''))
                        if impact_str.startswith('-'):
                            sustainability_impact = -sustainability_impact
                    except ValueError:
                        sustainability_impact = original.sustainability_impact // 2
                elif line.upper().startswith("EXPLANATION:"):
                    explanation = line[12:].strip()
            
            if title and description:
                return PolicyProposal(
                    title=title,
                    description=f"{description}\n\nDepartment rationale: {explanation}",
                    target_department=original.target_department,
                    sustainability_impact=sustainability_impact,
                    economic_impact=original.economic_impact + 1,  # Slightly more appealing
                    political_impact=original.political_impact + 2,  # More politically feasible
                    proposed_by=f"{self.personality.department.value}_counter"
                )
        except Exception:
            pass
            
        return None
    
    def _generate_mock_evaluation(self, proposal: PolicyProposal, 
                                 game_context: Dict[str, Any]) -> ProposalEvaluation:
        """Generate mock evaluation when LLM is not available"""
        # Simple heuristic based on personality
        sustainability_alignment = min(100, abs(proposal.sustainability_impact) * 2)
        personality_match = self.personality.sustainability_focus
        
        # Decision logic based on personality
        score = (sustainability_alignment + personality_match) / 2
        
        if self.personality.department == proposal.target_department:
            score += 20  # Boost for own department
            
        accept = score > 60
        confidence = min(90, max(30, int(score)))
        
        # Generate reasoning based on personality
        reasoning_templates = {
            Department.MAYOR: "I need to balance multiple interests and consider the political implications.",
            Department.ENERGY: "This aligns with our carbon neutrality goals and technical requirements.",
            Department.TRANSPORTATION: "We must consider equity and accessibility for all community members.",
            Department.HOUSING: "Housing as a human right must be our primary consideration.",
            Department.WASTE: "We need to focus on circular economy principles and operational efficiency.",
            Department.WATER: "Water security and ecosystem health are our top priorities.",
            Department.ECONOMIC_DEV: "We must balance environmental goals with economic opportunity.",
            Department.CITIZENS: "This proposal must serve the people and protect future generations."
        }
        
        reasoning = reasoning_templates.get(
            self.personality.department, 
            "I need to evaluate this based on our department's priorities."
        )
        
        return ProposalEvaluation(
            accept=accept,
            reasoning=reasoning,
            confidence=confidence,
            concerns=[],
            alternative_suggestions=[]
        )