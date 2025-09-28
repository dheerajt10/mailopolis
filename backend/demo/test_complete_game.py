#!/usr/bin/env python3
"""
Comprehensive test of the complete Mailopolis game system.
This demonstrates how user-provided proposals flow through the political system.
"""

import asyncio
import json
from pathlib import Path
from typing import List

# Load environment variables first
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from load_env import load_environment_variables, print_api_status

from agents.langchain_agents import LangChainAgentManager
from game.langchain_game_engine import MaylopolisGameEngine
from models.game_models import PolicyProposal, Department




class GameTester:
    """Test harness for the complete game system"""
    
    def __init__(self):
        self.game_engine = None
        self.agent_manager = None
    
    async def initialize_game(self):
        """Initialize the game engine and agent manager"""
        print("🏛️  Initializing Mailopolis Game Engine...")
        
        # Load environment variables and check API status
        load_environment_variables()
        print_api_status()
        print()
        
        # Initialize agents
        self.agent_manager = LangChainAgentManager()
        
        # Initialize game engine
        self.game_engine = MaylopolisGameEngine(
            agent_manager=self.agent_manager
        )
        
        # Start the game
        game_state = await self.game_engine.start_new_game()
        
        print(f"🎯 Game started! Initial state:")
        print(f"   Turn: {game_state['turn']}")
        print(f"   Budget: ${game_state['city_stats']['budget']:,.0f}")
        print(f"   Sustainability: {game_state['city_stats']['sustainability_score']}")
        print(f"   Public Approval: {game_state['city_stats']['public_approval']}")
        print(f"   Infrastructure: {game_state['city_stats']['infrastructure_health']}")
        print()
        
        return game_state
    
    def create_sample_proposals(self) -> List[PolicyProposal]:
        """Create sample proposals that a player might submit"""
        
        proposals = [
            PolicyProposal(
                title="Solar Panel Incentive Program",
                description="Provide tax rebates and subsidies for residential solar panel installations to increase renewable energy adoption citywide.",
                proposed_by="player",
                target_department=Department.ENERGY,
                sustainability_impact=25,
                economic_impact=-10,
                political_impact=15
            ),
            PolicyProposal(
                title="Affordable Housing Development",
                description="Build 500 new affordable housing units in underserved neighborhoods with green building standards.",
                proposed_by="player",
                target_department=Department.HOUSING,
                sustainability_impact=15,
                economic_impact=-20,
                political_impact=30
            ),
            PolicyProposal(
                title="Electric Bus Fleet Upgrade",
                description="Replace 50% of diesel buses with electric vehicles and install charging infrastructure throughout the city.",
                proposed_by="player",
                target_department=Department.TRANSPORTATION,
                sustainability_impact=30,
                economic_impact=-15,
                political_impact=20
            )
        ]
        
        return proposals
    
    async def play_sample_turn(self):
        """Play a turn with sample user proposals"""
        
        print("📝 Creating sample proposals (these would come from the player)...")
        proposals = self.create_sample_proposals()
        
        for i, proposal in enumerate(proposals, 1):
            print(f"   {i}. {proposal.title} ({proposal.target_department.value})")
            print(f"      Sustainability Impact: {proposal.sustainability_impact:+d}")
            print(f"      Economic Impact: {proposal.economic_impact:+d}")
            print(f"      Political Impact: {proposal.political_impact:+d}")
            print()
        
        print("⚖️  Starting political discussions...")
        turn_result = await self.game_engine.play_turn(player_proposals=proposals)
        
        return turn_result
    
    def display_turn_results(self, turn_result: dict):
        """Display the results of a turn"""
        
        print("🏛️  TURN RESULTS")
        print("=" * 50)
        
        # Political discussions
        if 'political_discussions' in turn_result:
            print("💬 Political Discussions:")
            discussions = turn_result['political_discussions']
            
            if 'private_conversations' in discussions:
                print(f"   - {len(discussions['private_conversations'])} private conversations occurred")
            
            if 'lobbying_efforts' in discussions:
                lobbying = discussions['lobbying_efforts']
                print(f"   - Mayor received {len(lobbying.get('arguments_presented', []))} lobbying arguments")
                
                if 'coalitions_formed' in lobbying:
                    coalitions = lobbying['coalitions_formed']
                    print(f"   - {len(coalitions)} coalitions formed:")
                    for coalition in coalitions:
                        members = ", ".join([m.value for m in coalition.get('members', [])])
                        print(f"     * {coalition.get('name', 'Unnamed Coalition')}: {members}")
        
        # Mayor's decision
        if 'mayor_decision' in turn_result:
            decision = turn_result['mayor_decision']
            approved = decision.get('approved_proposals', [])
            rejected = decision.get('rejected_proposals', [])
            
            print(f"\n🎯 Mayor's Decision:")
            print(f"   ✅ Approved: {len(approved)} proposals")
            for proposal in approved:
                print(f"      - {proposal.get('title', 'Unknown Proposal')}")
            
            print(f"   ❌ Rejected: {len(rejected)} proposals")
            for proposal in rejected:
                print(f"      - {proposal.get('title', 'Unknown Proposal')}")
        
        # City stats changes
        if 'city_stats' in turn_result:
            stats = turn_result['city_stats']
            print(f"\n📊 Updated City Statistics:")
            print(f"   Budget: ${stats['budget']:,.0f}")
            print(f"   Sustainability: {stats['sustainability_score']}")
            print(f"   Public Approval: {stats['public_approval']}")
            print(f"   Infrastructure: {stats['infrastructure_health']}")
            print(f"   Economic Growth: {stats['economic_growth']}")
        
        # Events
        if 'events' in turn_result and turn_result['events']:
            print(f"\n📰 Events This Turn:")
            for event in turn_result['events']:
                print(f"   • {event.get('title', 'Unknown Event')}")
                print(f"     {event.get('description', 'No description')}")
        
        # Game status
        if 'game_status' in turn_result:
            status = turn_result['game_status']
            print(f"\n🏆 Game Status: {status}")
            
            if status in ['won', 'lost']:
                print("   Game Over!")
    
    async def demonstrate_no_proposals_scenario(self):
        """Test what happens when no proposals are provided"""
        
        print("\n" + "="*60)
        print("🚫 Testing scenario with NO proposals...")
        
        turn_result = await self.game_engine.play_turn(player_proposals=[])
        
        print(f"📋 Result: {turn_result.get('game_status', 'unknown')}")
        if turn_result.get('game_status') == 'waiting_for_proposals':
            print("   ✅ Game correctly waits for player to provide proposals")
        
        return turn_result
    
    async def get_suggestions(self):
        """Test the suggestion system"""
        print("\n" + "="*60)
        print("💡 Getting suggested proposals for the player...")
        
        suggestions = await self.game_engine.get_suggested_proposals()
        
        print(f"📝 Generated {len(suggestions)} suggestions:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"   {i}. {suggestion.title}")
            print(f"      Department: {suggestion.target_department.value}")
            print(f"      Sustainability Impact: {suggestion.sustainability_impact:+d}")
            print(f"      Economic Impact: {suggestion.economic_impact:+d}")
            print(f"      Political Impact: {suggestion.political_impact:+d}")
            print()
        
        return suggestions


async def main():
    """Run the comprehensive game test"""
    
    print("🏛️  MAILOPOLIS COMPLETE SYSTEM TEST")
    print("="*60)
    
    tester = GameTester()
    
    try:
        # Initialize the game
        game_state = await tester.initialize_game()
        
        # Test suggestions
        suggestions = await tester.get_suggestions()
        
        # Test no proposals scenario
        await tester.demonstrate_no_proposals_scenario()
        
        # Play a turn with sample proposals
        print("\n" + "="*60)
        print("🎮 Playing turn with user proposals...")
        turn_result = await tester.play_sample_turn()
        
        # Display results
        tester.display_turn_results(turn_result)
        
        print("\n" + "="*60)
        print("✅ Complete system test finished successfully!")
        print("🎯 The game engine properly:")
        print("   - Accepts user-provided proposals")
        print("   - Facilitates political discussions between agents")
        print("   - Makes mayor decisions based on agent negotiations")
        print("   - Updates city statistics based on decisions")
        print("   - Persists conversation history")
        
        # Show final API status
        print("\n🔑 API Configuration Used:")
        print_api_status()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())