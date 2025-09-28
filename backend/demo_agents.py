#!/usr/bin/env python3

"""
Demo script showing how different agents behave differently in Mailopolis.
Run this to see agent personalities in action!
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.game_engine import GameEngine
from models.game_models import PlayerAction, ActionType

def main():
    print("🏙️  MAILOPOLIS AGENT BEHAVIOR DEMO")
    print("=" * 50)
    
    # Create game engine (this creates all agents)
    game = GameEngine()
    
    print(f"\n📊 Initial Game State:")
    print(f"   City Health: {game.game_state.city_health}")
    print(f"   Budget: ${game.game_state.budget:,}")
    print(f"   Mayor Approval: {game.game_state.approval}%")
    print(f"   Emissions: {game.game_state.sustainability_metrics.emissions} tCO₂e")
    
    print(f"\n👥 Created {len(game.agents)} agents:")
    for agent in game.agents.values():
        trust_emoji = "🟢" if agent.trust_level > 70 else "🟡" if agent.trust_level > 50 else "🔴"
        print(f"   {trust_emoji} {agent.name} ({agent.department.value}) - Trust: {agent.trust_level}%")
        print(f"      Style: {agent.personality.decision_style.value} | Risk Tolerance: {agent.personality.risk_tolerance}%")
    
    # Generate daily scenarios
    print(f"\n📧 Generating daily email scenarios...")
    digest = game.get_daily_digest()
    
    print(f"\n📬 Today's Top {len(digest)} Email Threads:")
    for i, thread in enumerate(digest, 1):
        crisis_emoji = {
            "critical": "🚨", "high": "⚠️", "medium": "⚡", "low": "📝", None: "📄"
        }
        print(f"\n   {i}. {crisis_emoji.get(thread.crisis_level, '📄')} {thread.subject}")
        print(f"      Priority: {thread.priority}/100 | Crisis: {thread.crisis_level or 'none'}")
        print(f"      Participants: {len(thread.participants)} agents")
        
        if thread.messages:
            latest_msg = thread.messages[-1]
            sender = next((a.name for a in game.agents.values() if a.id == latest_msg.from_agent), "Unknown")
            print(f"      Latest from {sender}: {latest_msg.content[:80]}...")
    
    # Test different agents' reactions to the same advice
    if digest:
        test_thread = digest[0]  # Use first thread for testing
        print(f"\n🧪 TESTING: How different agents react to the same advice")
        print(f"Thread: {test_thread.subject}")
        
        # Create an advice action
        advice_action = PlayerAction(
            type=ActionType.ADVISE,
            thread_id=test_thread.id,
            content="We should prioritize this and allocate emergency budget to resolve it quickly."
        )
        
        print(f"\nAdvice: '{advice_action.content}'\n")
        
        # Test each agent's likely response
        for agent in game.agents.values():
            if agent.department.value in ['Citizens', 'Media']:  # Skip these for this test
                continue
                
            accepted, confidence = game.decision_engine.evaluate_player_action(
                agent, advice_action, test_thread, game.game_state
            )
            
            response = game.response_generator.generate_response(
                agent, advice_action, accepted, test_thread
            )
            
            decision_emoji = "✅" if accepted else "❌"
            confidence_bar = "█" * int(confidence * 10) + "░" * (10 - int(confidence * 10))
            
            print(f"{decision_emoji} {agent.name} ({agent.personality.decision_style.value})")
            print(f"   Acceptance: {confidence:.1%} [{confidence_bar}]")
            print(f"   Response: \"{response}\"")
            print()
    
    # Simulate taking an action
    if digest:
        print("🎮 SIMULATING PLAYER ACTION")
        print("-" * 30)
        
        # Let's try asking for information first (good strategy)
        power_agent = next((a for a in game.agents.values() 
                          if a.department.value == "PowerGrid"), None)
        
        if power_agent:
            ask_action = PlayerAction(
                type=ActionType.ASK,
                thread_id=digest[0].id,
                target_agent=power_agent.id
            )
            
            print(f"Action: ASK {power_agent.name} for more information")
            outcome = game.process_player_action(ask_action)
            
            print(f"Result: {'✅ Success' if outcome.success else '❌ Failed'}")
            print(f"Message: {outcome.message}")
            
            if outcome.effects:
                print("Effects:")
                for effect in outcome.effects:
                    effect_emoji = "📈" if effect.delta > 0 else "📉"
                    if effect.agent_id:
                        agent_name = next((a.name for a in game.agents.values() 
                                         if a.id == effect.agent_id), "Unknown")
                        print(f"   {effect_emoji} {agent_name} {effect.metric}: {effect.delta:+}")
                    else:
                        print(f"   {effect_emoji} {effect.metric}: {effect.delta:+}")
    
    print(f"\n🎯 Key Takeaways:")
    print("   • Each agent has distinct personality traits affecting decisions")
    print("   • Cautious agents prefer being asked before being advised")  
    print("   • Trust levels and mayor approval affect acceptance rates")
    print("   • Department priorities influence agent responses")
    print("   • Agent-to-agent collaboration creates synergy bonuses")
    
    print(f"\n🔧 This is just the foundation - agents will get smarter!")

if __name__ == "__main__":
    main()