#!/usr/bin/env python3
"""
Test LangChain API endpoints
"""

import asyncio
import json
from langchain_api import LangChainGameAPI, LangChainPolicyProposal

async def test_langchain_api():
    """Test the LangChain API functionality"""
    print("🚀 Testing LangChain API...")
    
    # Test 1: Get game status
    print("\n📊 Getting game status...")
    status = LangChainGameAPI.get_game_status()
    print(f"   Sustainability Index: {status['sustainability_index']}")
    print(f"   Active Agents: {len(status['agents'])}")
    
    # Test 2: Preview a proposal
    print("\n🔮 Testing proposal preview...")
    test_proposal = LangChainPolicyProposal(
        title="Solar Panel Incentive Program",
        description="Provide tax incentives for residential solar panel installations to reduce carbon footprint",
        target_department="ENERGY",
        sustainability_impact=8
    )
    
    preview = await LangChainGameAPI.preview_proposal(test_proposal)
    print(f"   Preview completed for {len(preview)} agents")
    for dept, response in preview.items():
        print(f"   {dept}: {response.get('stance', 'No stance')}")
    
    # Test 3: Submit and decide on proposal
    print("\n📝 Submitting proposal...")
    result = await LangChainGameAPI.submit_proposal(test_proposal)
    print(f"   Proposal submitted: {result['success']}")
    
    print("\n⚖️  Mayor deciding on proposal...")
    decision = await LangChainGameAPI.mayor_decide()
    print(f"   Decisions made: {len(decision['decisions'])}")
    
    # Show final results
    for dept, decision_info in decision['decisions'].items():
        print(f"   {dept}: {decision_info['decision']} - {decision_info.get('reasoning', '')[:100]}...")

if __name__ == "__main__":
    print("🎮 LangChain API Test Suite")
    print("=" * 50)
    
    # Test basic functionality
    asyncio.run(test_langchain_api())
    
    print("\n✅ All LangChain API tests completed!")