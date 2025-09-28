#!/usr/bin/env python3
"""
Demo script for multi-agent discussion system
Demonstrates how agents discuss proposals with conversation memory
"""

import asyncio
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ["OPENAI_API_KEY"] = "sk-proj-lP8RgBe1BkZstd5h1rNcT3BlbkFJirH5YElfKbMTNZgMreZE"

from agents.langchain_agents import LangChainAgentManager
from models.game_models import PolicyProposal, Department, SustainabilityGameState

async def demo_agent_discussion():
    """Demonstrate multi-agent discussion with conversation memory"""
    
    print("🏛️  Mailopolis Multi-Agent Discussion Demo")
    print("=" * 50)
    
    # Initialize the agent manager
    print("🤖 Initializing LangChain Agent Manager...")
    agent_manager = LangChainAgentManager(use_openai=True, temperature=0.8)
    
    print(f"✅ Initialized with provider: {agent_manager.provider_name}")
    print(f"👥 Created {len(agent_manager.agents)} department agents")
    print(f"💾 Conversation memory system ready")
    print()
    
    # Create a sample policy proposal
    sample_proposal = PolicyProposal(
        title="Green Energy Transition Initiative",
        description="Mandate all city buildings to use 50% renewable energy within 2 years. Provides tax incentives for early adopters and penalties for non-compliance.",
        proposed_by="player_mayor",  # Required field
        target_department=Department.ENERGY,
        sustainability_impact=40,  # Must be between -50 and 50
        economic_impact=-30,
        political_impact=25,  # Required field, between -50 and 50
        bribe_amount=0  # Default value for transparency
    )
    
    print(f"📋 Sample Proposal: {sample_proposal.title}")
    print(f"🎯 Target Department: {sample_proposal.target_department.value}")
    print(f"🌱 Sustainability Impact: +{sample_proposal.sustainability_impact}")
    print(f"💰 Economic Impact: {sample_proposal.economic_impact}")
    print(f"🏛️ Political Impact: +{sample_proposal.political_impact}")
    print()
    
    # Create game context
    game_context = {
        "current_sustainability_score": 45,
        "budget_remaining": 250000,
        "public_approval": 65,
        "crisis_level": "moderate"
    }
    
    print("🎮 Current Game State:")
    for key, value in game_context.items():
        print(f"  {key}: {value}")
    print()
    
    # Run the multi-agent discussion
    print("🗣️  STARTING MULTI-AGENT DISCUSSION")
    print("-" * 40)
    
    try:
        discussion_result = await agent_manager.discuss_and_evaluate_proposal(
            sample_proposal, 
            game_context
        )
        
        # Display results
        print("\n📊 DISCUSSION RESULTS")
        print("=" * 30)
        
        print(f"\n🏛️  Chat Rounds: {len(discussion_result['chat_rounds'])}")
        
        # Show each round's messages
        for i, round_data in enumerate(discussion_result['chat_rounds']):
            print(f"\n📢 ROUND {round_data.round_number}: {round_data.messages[0].message_type.upper()}")
            print("-" * 25)
            
            for message in round_data.messages:
                print(f"🎤 {message.speaker} ({message.department}):")
                print(f"   {message.content}")
                print()
        
        # Show final department positions
        print("\n🏛️  FINAL DEPARTMENT POSITIONS")
        print("-" * 35)
        for dept, info in discussion_result['department_positions'].items():
            print(f"🏢 {dept}:")
            print(f"   Agent: {info['agent_name']}")
            print(f"   Position: {info['position']}")
            print(f"   Reasoning: {info['reasoning']}")
            if info['conditions'] != "None":
                print(f"   Conditions: {info['conditions']}")
            print()
        
        # Show mayor's final decision
        mayor_decision = discussion_result['mayor_decision']
        print("👑 MAYOR'S FINAL DECISION")
        print("-" * 25)
        print(f"Decision: {'✅ APPROVED' if mayor_decision.accept else '❌ REJECTED'}")
        print(f"Reasoning: {mayor_decision.reasoning}")
        print(f"Confidence: {mayor_decision.confidence}/100")
        if mayor_decision.concerns:
            print(f"Concerns: {', '.join(mayor_decision.concerns)}")
        print()
        
        # Show discussion summary
        print("📋 DISCUSSION SUMMARY")
        print("-" * 20)
        print(discussion_result['discussion_summary'])
        print()
        
        # Show conversation memory stats
        stats = agent_manager.chat_system.get_discussion_stats()
        print("💾 CONVERSATION MEMORY STATS")
        print("-" * 30)
        print(f"Total Conversations Stored: {stats['total_conversations']}")
        print(f"Total Messages Stored: {stats['total_messages']}")
        print(f"Storage Directory: {stats['storage_directory']}")
        
    except Exception as e:
        print(f"❌ Error during discussion: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🎉 Demo completed!")

def main():
    """Run the demo"""
    print("Starting Mailopolis Multi-Agent Discussion Demo...")
    
    # Check for API keys
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  Warning: No OpenAI or Anthropic API key found.")
        print("   The demo will run with mock responses.")
        print("   Set OPENAI_API_KEY or ANTHROPIC_API_KEY for full functionality.")
        print()
    
    # Run the async demo
    asyncio.run(demo_agent_discussion())

if __name__ == "__main__":
    main()