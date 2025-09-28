#!/usr/bin/env python3
"""
Demo of LangChain-powered Mailopolis with sophisticated AI agents
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from game.langchain_game_engine import LangChainGameEngine
from models.game_models import PolicyProposal, Department

async def demo_langchain_game():
    """Demonstrate the LangChain-powered sustainability game"""
    
    print("🏙️  MAILOPOLIS - LANGCHAIN-POWERED SUSTAINABILITY GAME")
    print("=" * 65)
    print()
    
    # Check API keys
    has_openai = bool(os.getenv("OPENAI_API_KEY"))
    has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))
    
    if has_openai:
        print("✅ OpenAI API key found - Using GPT-4o-mini")
        use_openai = True
    elif has_anthropic:
        print("✅ Anthropic API key found - Using Claude-3 Haiku")
        use_openai = False
    else:
        print("⚠️  No API keys found - Using mock LLM responses")
        use_openai = True  # Will fallback to mock
    print()
    
    # Initialize LangChain-powered game
    game = LangChainGameEngine(use_openai=use_openai)
    
    print("🎮 INITIAL GAME STATE")
    status = game.get_game_status()
    print(f"   Sustainability Index: {status['sustainability_index']}")
    print(f"   Mayor Trust: {status['mayor_trust']}")
    print(f"   LLM Provider: {status['llm_provider']}")
    print(f"   Department Scores:")
    for dept, score in status['department_scores'].items():
        print(f"     {dept.value}: {score}")
    print()
    
    # Show available agents
    print("🤖 LANGCHAIN AGENTS")
    for dept, agent in game.agent_manager.agents.items():
        personality = agent.personality
        print(f"   {personality.name}")
        print(f"     Department: {dept.value}")
        print(f"     Sustainability Focus: {personality.sustainability_focus}%")
        print(f"     Corruption Resistance: {personality.corruption_resistance}%")
        print(f"     Communication: {personality.communication_style[:80]}...")
        print()
    
    # Create a player proposal
    print("📋 TESTING PROPOSAL PREVIEW")
    test_proposal = PolicyProposal(
        title="Green Building Retrofit Program",
        description="Provide incentives and technical assistance to retrofit existing buildings with energy-efficient systems, solar panels, and green roofs to reduce citywide emissions.",
        target_department=Department.HOUSING,
        sustainability_impact=15,
        economic_impact=8,
        political_impact=6,
        proposed_by="player"
    )
    
    print(f"   Title: {test_proposal.title}")
    print(f"   Target: {test_proposal.target_department.value}")
    print(f"   Sustainability Impact: +{test_proposal.sustainability_impact}")
    print()
    
    # Get agent preview (doesn't submit the proposal)
    print("🔮 AGENT PREVIEW (Before Submission)")
    try:
        preview = await game.get_agent_preview(test_proposal)
        
        print("   Agent Reactions:")
        for reaction in preview['agent_reactions']:
            print(f"     {reaction['from']} ({reaction['department']}): {reaction['decision']}")
            print(f"       \"{reaction['message'][:100]}...\"")
            print(f"       Support Level: {reaction['support_level']}%")
            print()
        
        print("   Mayor Preview:")
        mayor_preview = preview['mayor_preview']
        print(f"     Likely Decision: {mayor_preview['likely_decision']}")
        print(f"     \"{mayor_preview['reasoning']}\"")
        print(f"     Confidence: {mayor_preview['confidence']}%")
        print()
        
    except Exception as e:
        print(f"❌ Preview failed: {e}")
        print()
    
    # Now actually submit the proposal
    print("📤 SUBMITTING PROPOSAL")
    try:
        submission_result = await game.submit_player_proposal(test_proposal)
        
        print(f"   Status: {submission_result['status']}")
        print(f"   Message: {submission_result['message']}")
        print()
        
        print("   Live Agent Reactions:")
        for reaction in submission_result['agent_reactions']:
            print(f"     {reaction['from']} ({reaction['department']}): {reaction['decision']}")
            print(f"       \"{reaction['message']}\"")
            print(f"       Support Level: {reaction['support_level']}%")
            if reaction.get('concerns'):
                print(f"       Concerns: {', '.join(reaction['concerns'])}")
            print()
            
    except Exception as e:
        print(f"❌ Submission failed: {e}")
        print()
    
    # Mayor decision
    print("🏛️  MAYOR DECISION")
    try:
        decisions = await game.mayor_decide_on_proposals()
        
        for decision in decisions:
            print(f"   Proposal: {decision['title']}")
            print(f"   Decision: {'✅ ACCEPTED' if decision['accepted'] else '❌ REJECTED'}")
            print(f"   Mayor's Reasoning:")
            print(f"     \"{decision['reasoning']}\"")
            print(f"   Confidence: {decision['confidence']}%")
            
            if decision.get('concerns'):
                print(f"   Concerns: {', '.join(decision['concerns'])}")
            
            if decision['accepted']:
                print(f"   Sustainability Impact: +{decision['sustainability_impact']}")
            print()
            
            # Generate counter-proposals for rejected proposals
            if not decision['accepted']:
                print("🔄 GENERATING COUNTER-PROPOSAL")
                try:
                    # Find the original proposal
                    original = None
                    for prop in [test_proposal]:  # In real game, would check pending proposals
                        if prop.id == decision['proposal_id']:
                            original = prop
                            break
                    
                    if original:
                        counter_proposals = await game.generate_counter_proposals(original)
                        for counter in counter_proposals:
                            print(f"   Counter-proposal: {counter.title}")
                            print(f"   Description: {counter.description[:150]}...")
                            print(f"   Revised Sustainability Impact: +{counter.sustainability_impact}")
                            print(f"   Proposed by: {counter.proposed_by}")
                            print()
                        
                        if not counter_proposals:
                            print("   No counter-proposals generated")
                            print()
                            
                except Exception as e:
                    print(f"❌ Counter-proposal generation failed: {e}")
                    print()
            
    except Exception as e:
        print(f"❌ Mayor decision failed: {e}")
        print()
    
    # Show updated game state
    print("📊 FINAL GAME STATE")
    final_status = game.get_game_status()
    print(f"   Sustainability Index: {final_status['sustainability_index']}")
    print(f"   Mayor Trust: {final_status['mayor_trust']}")
    print(f"   Round: {final_status['round_number']}")
    print(f"   Department Scores:")
    for dept, score in final_status['department_scores'].items():
        print(f"     {dept.value}: {score}")
    print()
    
    # Show blockchain transparency
    print("⛓️  BLOCKCHAIN TRANSPARENCY")
    recent_transactions = game.game_state.blockchain_transactions[-5:]
    for tx in recent_transactions:
        print(f"   {tx.timestamp.strftime('%H:%M:%S')} - {tx.from_agent} → {tx.to_agent}")
        print(f"     Type: {tx.transaction_type}")
        if tx.amount:
            print(f"     Amount: ${tx.amount:,}")
        print(f"     Data: {str(tx.data)[:100]}...")
        print()
    
    print("🎯 LANGCHAIN DEMO COMPLETE")
    print(f"   Total Transactions: {len(game.game_state.blockchain_transactions)}")
    print(f"   LLM Provider: {final_status['llm_provider']}")
    print("   🚀 LangChain Integration Successful! 🤖✨")

if __name__ == "__main__":
    # Run the LangChain demo
    asyncio.run(demo_langchain_game())