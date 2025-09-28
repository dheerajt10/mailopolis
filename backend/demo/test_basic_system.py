#!/usr/bin/env python3
"""
Simple test of the Mailopolis game system core functionality.
"""

import asyncio
import sys
import os
from datetime import datetime

# Load environment variables first
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from load_env import load_environment_variables, print_api_status

from models.game_models import PolicyProposal, Department


def test_basic_models():
    """Test that we can create basic game models"""
    print("🧪 Testing basic game models...")
    
    # Test creating a policy proposal
    proposal = PolicyProposal(
        title="Test Solar Panel Program",
        description="A test proposal for solar panels",
        proposed_by="test_player",
        target_department=Department.ENERGY,
        sustainability_impact=20,
        economic_impact=-10,
        political_impact=15
    )
    
    print(f"✅ Created proposal: {proposal.title}")
    print(f"   Target Department: {proposal.target_department.value}")
    print(f"   Sustainability Impact: {proposal.sustainability_impact:+d}")
    print(f"   Economic Impact: {proposal.economic_impact:+d}")
    print(f"   Political Impact: {proposal.political_impact:+d}")
    print()
    
    return proposal


async def test_agent_manager():
    """Test that we can create the agent manager"""
    print("🤖 Testing agent manager...")
    
    try:
        from agents.langchain_agents import LangChainAgentManager
        agent_manager = LangChainAgentManager()
        print("✅ Agent manager created successfully")
        return agent_manager
    except Exception as e:
        print(f"❌ Failed to create agent manager: {e}")
        return None


async def test_conversation_memory():
    """Test the conversation memory system"""
    print("💭 Testing conversation memory...")
    
    try:
        from agents.conversation_memory import ConversationMemory, ConversationMessage
        
        memory = ConversationMemory()
        
        # Create a test message
        test_message = ConversationMessage(
            speaker="Energy",
            department="Energy",
            content="We need more funding for renewable energy projects.",
            timestamp=datetime.now(),
            message_type="lobbying"
        )
        
        # Save to memory
        memory.save_conversation("test_session", [test_message])
        print("✅ Conversation memory working")
        
        # Retrieve from memory
        recent = memory.get_recent_conversations(agent_name="Energy", limit=1)
        print(f"   Retrieved {len(recent)} recent conversations")
        
        return memory
        
    except Exception as e:
        print(f"❌ Failed to test conversation memory: {e}")
        return None


async def main():
    """Run the basic tests"""
    
    print("🏛️  MAILOPOLIS BASIC SYSTEM TEST")
    print("="*50)
    
    # Load environment variables and show API status
    load_environment_variables()
    print_api_status()
    print()
    
    # Test 1: Basic models
    proposal = test_basic_models()
    
    # Test 2: Agent manager
    agent_manager = await test_agent_manager()
    
    # Test 3: Conversation memory
    memory = await test_conversation_memory()
    
    # Test 4: Try importing game engine
    print("🎮 Testing game engine import...")
    try:
        from game.langchain_game_engine import MaylopolisGameEngine
        print("✅ Game engine import successful")
        
        if agent_manager:
            print("🎯 Testing game engine initialization...")
            try:
                game_engine = MaylopolisGameEngine(agent_manager=agent_manager)
                print("✅ Game engine created successfully")
                print(f"   Initial sustainability: {game_engine.city_stats.sustainability_score}")
                print(f"   Initial budget: ${game_engine.city_stats.budget:,.0f}")
                print(f"   Initial approval: {game_engine.city_stats.public_approval}")
            except Exception as e:
                print(f"❌ Failed to create game engine: {e}")
                import traceback
                traceback.print_exc()
        
    except Exception as e:
        print(f"❌ Failed to import game engine: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*50)
    print("🎯 Basic test completed!")
    
    if proposal and agent_manager and memory:
        print("✅ All core components are working!")
        print("🚀 The system is ready for full integration testing.")
    else:
        print("⚠️  Some components had issues. Check the errors above.")


if __name__ == "__main__":
    asyncio.run(main())