#!/usr/bin/env python3
"""
Demo script for the new Adversarial Sustainability Game
Shows how the game mechanics work with player vs bad actors
"""

from game.game_engine import SustainabilityGameEngine
from models.game_models import Department

def main():
    print("🏙️ Welcome to Mailopolis - Adversarial Sustainability Game! 🌱")
    print("=" * 60)
    
    # Initialize game
    game = SustainabilityGameEngine()
    
    print(f"\n📊 INITIAL GAME STATE")
    print(f"Overall Sustainability Index: {game.game_state.sustainability_index}/100")
    print(f"Mayor Trust in Player: {game.game_state.mayor_trust_in_player}/100")
    print(f"Bad Actor Influence: {game.game_state.bad_actor_influence}/100")
    
    print(f"\n🏢 DEPARTMENT SCORES:")
    for dept, score in game.game_state.department_scores.items():
        print(f"  {dept.value}: {score}/100")
    
    print(f"\n💀 BAD ACTORS:")
    for actor in game.game_state.active_bad_actors.values():
        print(f"  {actor.name} ({actor.type.value})")
        print(f"    Influence: {actor.influence_power}/100")
        print(f"    Budget: ${actor.corruption_budget:,}")
        print(f"    Targets: {[d.value for d in actor.target_departments]}")
    
    # Start first round
    print(f"\n🎮 STARTING ROUND 1...")
    round_data = game.start_new_round()
    
    print(f"\n💰 BAD ACTOR PROPOSALS THIS ROUND:")
    for proposal_data in round_data["bad_actor_proposals"]:
        print(f"  {proposal_data['actor']}: {proposal_data['proposal'].title}")
        print(f"    Target: {proposal_data['target_department']}")
        print(f"    Bribe: ${proposal_data['bribe_amount']:,}")
        print(f"    Sustainability Impact: {proposal_data['proposal'].sustainability_impact}")
    
    # Player submits counter-proposal
    print(f"\n🌱 PLAYER SUBMITS SUSTAINABILITY PROPOSAL...")
    player_proposal = game.submit_player_proposal(
        title="Solar Panel Incentive Program",
        description="Provide tax incentives for residential and commercial solar installations",
        target_department=Department.ENERGY
    )
    
    print(f"  Submitted: {player_proposal.title}")
    print(f"  Target: {player_proposal.target_department.value}")
    print(f"  Sustainability Impact: {player_proposal.sustainability_impact}")
    
    # Mayor makes decisions
    print(f"\n👨‍💼 MAYOR EVALUATES ALL PROPOSALS...")
    decisions = game.mayor_decide_on_proposals()
    
    print(f"\n📋 MAYOR'S DECISIONS:")
    for decision in decisions:
        status = "✅ ACCEPTED" if decision["accepted"] else "❌ REJECTED"
        proposer = "Player" if decision["proposed_by"] == "player" else "Bad Actor"
        print(f"  {status}: {decision['title']} (by {proposer})")
        print(f"    Score: {decision['total_score']:.1f} (needed {decision['threshold']:.1f})")
        print(f"    Reasoning: {decision['reasoning']}")
        if decision["accepted"] and decision["sustainability_impact"] != 0:
            print(f"    Sustainability Impact: {decision['sustainability_impact']:+d}")
    
    # Show updated state
    print(f"\n📊 UPDATED GAME STATE")
    print(f"Overall Sustainability Index: {game.game_state.sustainability_index}/100")
    print(f"Mayor Trust in Player: {game.game_state.mayor_trust_in_player}/100")
    print(f"Bad Actor Influence: {game.game_state.bad_actor_influence}/100")
    
    print(f"\n🏢 UPDATED DEPARTMENT SCORES:")
    for dept, score in game.game_state.department_scores.items():
        print(f"  {dept.value}: {score}/100")
    
    # Show blockchain activity
    print(f"\n🔗 BLOCKCHAIN ACTIVITY:")
    blockchain_analysis = game.get_blockchain_analysis()
    print(f"  Total Transactions: {blockchain_analysis['total_transactions']}")
    print(f"  Bribe Attempts: {blockchain_analysis['total_bribe_attempts']}")
    print(f"  Total Bribe Amount: ${blockchain_analysis['total_bribe_amount']:,}")
    
    # Check win/loss conditions
    win_conditions = game._check_win_conditions()
    loss_conditions = game._check_loss_conditions()
    
    print(f"\n🎯 WIN/LOSS CONDITIONS:")
    print(f"  Sustainability Dominance: {win_conditions['sustainability_dominance']}")
    print(f"  Corruption Takeover: {loss_conditions['corruption_takeover']}")
    print(f"  Trust Collapse: {loss_conditions['trust_collapse']}")
    print(f"  Department Rebellion: {loss_conditions['department_rebellion']}")
    
    print(f"\n🎮 Round {game.game_state.round_number} complete!")
    print("Game continues with new bad actor moves each round...")
    
    print(f"\n" + "=" * 60)
    print("Demo complete! The player successfully competed against bad actors")
    print("and influenced the mayor toward more sustainable policies! 🌱")

if __name__ == "__main__":
    main()