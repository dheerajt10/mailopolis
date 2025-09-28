#!/usr/bin/env python3
"""
AgentMail Integration Demo for Mailopolis
Shows all the email communications happening between agents
"""

import asyncio
from service.agent_mail import agent_mail_service, initialize_agent_inboxes


async def show_agent_emails():
    """Display all agent email addresses"""
    
    print("📧 MAILOPOLIS AGENT EMAIL SYSTEM")
    print("=" * 50)
    
    # Initialize inboxes
    print("🔧 Initializing agent inboxes...")
    inboxes = await initialize_agent_inboxes()
    
    print(f"\n✅ {len(inboxes)} Agent Email Accounts Created:")
    print("-" * 50)
    
    for agent_name, inbox in inboxes.items():
        department = inbox.department.value
        email = inbox.inbox_id
        print(f"🏛️ {agent_name}")
        print(f"   📧 Email: {email}")
        print(f"   🏢 Department: {department}")
        print(f"   📅 Created: {inbox.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    print("📬 EMAIL COMMUNICATION FLOW:")
    print("-" * 50)
    print("1. 📝 When a proposal is submitted:")
    print("   → All agents receive proposal notification email")
    print()
    print("2. 💬 During private conversations:")
    print("   → Agents send private discussion emails to each other")
    print("   → Coalition building happens via email")
    print()
    print("3. 🏛️ During mayor lobbying:")
    print("   → Department heads send lobbying emails to mayor")
    print("   → Mayor receives influence attempts via email")
    print()
    print("4. 🗳️ When agents make voting decisions:")
    print("   → Each agent sends their decision via email")
    print("   → All other agents are notified of the vote")
    print()
    print("5. 👑 When mayor makes final decision:")
    print("   → Mayor sends final decision email to all agents")
    print("   → Implementation status is communicated")
    print()
    
    print("🎯 ALL AGENT COMMUNICATIONS NOW USE AGENTMAIL!")
    print("   Check your AgentMail dashboard to see emails in real-time")


if __name__ == "__main__":
    asyncio.run(show_agent_emails())