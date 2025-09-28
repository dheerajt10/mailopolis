"""
AgentMail integration service for Mailopolis
Manages email inboxes for each agent and sends action notifications
"""

import asyncio
import aiohttp
import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path

from models.game_models import Department, Agent
from agents.agent_personalities import AgentPersonalities
from load_env import get_api_key


@dataclass
class AgentInbox:
    """Represents an agent's email inbox"""
    inbox_id: str
    agent_name: str
    department: Department
    display_name: str
    created_at: datetime


@dataclass
class ActionNotification:
    """Represents an action that should trigger email notifications"""
    action_type: str
    action_maker: str
    action_maker_inbox: str
    recipients: List[str]
    subject: str
    message_text: str
    message_html: Optional[str] = None


class AgentMailService:
    """Service for managing agent email communications via AgentMail API"""
    
    def __init__(self):
        # Ensure environment variables are loaded
        from load_env import load_environment_variables
        load_environment_variables()
        
        self.api_key = os.getenv('AGENTMAIL_API_KEY')
        self.base_url = "https://api.agentmail.to"
        self.created_inboxes: Dict[str, AgentInbox] = {}
        self.inbox_cache_file = Path(__file__).parent.parent / "data" / "agent_inboxes.json"
        
        # Debug: Check if API key is loaded
        if not self.api_key:
            print("⚠️ Warning: AGENTMAIL_API_KEY not found in environment variables")
            print("Please set AGENTMAIL_API_KEY in your .env file")
        else:
            print(f"✅ AgentMail API key loaded: {self.api_key[:10]}...{self.api_key[-4:]}")
        
        # Load existing inboxes from cache
        self._load_inbox_cache()
    
    def _get_agent_email_username(self, agent_name: str) -> str:
        """Convert agent name to email username format"""
        # Convert "Mayor Patricia Williams" -> "mayor-patricia-williams-mailopolis"
        username = agent_name.lower().replace(" ", "-").replace(".", "")
        return f"{username}-mailopolis"
    
    def _load_inbox_cache(self):
        """Load previously created inboxes from cache file"""
        if self.inbox_cache_file.exists():
            try:
                with open(self.inbox_cache_file, 'r') as f:
                    data = json.load(f)
                    for inbox_data in data.get('inboxes', []):
                        inbox = AgentInbox(
                            inbox_id=inbox_data['inbox_id'],
                            agent_name=inbox_data['agent_name'],
                            department=Department(inbox_data['department']),
                            display_name=inbox_data['display_name'],
                            created_at=datetime.fromisoformat(inbox_data['created_at'])
                        )
                        self.created_inboxes[inbox.agent_name] = inbox
                print(f"📧 Loaded {len(self.created_inboxes)} existing agent inboxes from cache")
            except Exception as e:
                print(f"⚠️ Warning: Could not load inbox cache: {e}")
    
    def _save_inbox_cache(self):
        """Save created inboxes to cache file"""
        try:
            # Ensure data directory exists
            self.inbox_cache_file.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                'inboxes': [
                    {
                        'inbox_id': inbox.inbox_id,
                        'agent_name': inbox.agent_name,
                        'department': inbox.department.value,
                        'display_name': inbox.display_name,
                        'created_at': inbox.created_at.isoformat()
                    }
                    for inbox in self.created_inboxes.values()
                ],
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.inbox_cache_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"⚠️ Warning: Could not save inbox cache: {e}")
    
    async def _make_api_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make authenticated request to AgentMail API"""
        if not self.api_key:
            raise ValueError("AGENTMAIL_API_KEY environment variable not set")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.base_url}{endpoint}"
        
        async with aiohttp.ClientSession() as session:
            if method.upper() == "GET":
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        raise Exception(f"AgentMail API error {response.status}: {error_text}")
            elif method.upper() == "POST":
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status in [200, 201]:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        raise Exception(f"AgentMail API error {response.status}: {error_text}")
    
    async def create_agent_inbox(self, agent_name: str, department: Department) -> AgentInbox:
        """Create an inbox for an agent if it doesn't already exist"""
        
        # Check if inbox already exists
        if agent_name in self.created_inboxes:
            print(f"📧 Using existing inbox for {agent_name}: {self.created_inboxes[agent_name].inbox_id}")
            return self.created_inboxes[agent_name]
        
        try:
            username = self._get_agent_email_username(agent_name)
            display_name = f"{agent_name} - Mailopolis {department.value}"
            
            # Create inbox via AgentMail API
            response = await self._make_api_request("POST", "/v0/inboxes", {
                "username": username,
                "display_name": display_name
            })
            
            # Create inbox object
            inbox = AgentInbox(
                inbox_id=response['inbox_id'],
                agent_name=agent_name,
                department=department,
                display_name=response['display_name'],
                created_at=datetime.fromisoformat(response['created_at'])
            )
            
            # Cache the inbox
            self.created_inboxes[agent_name] = inbox
            self._save_inbox_cache()
            
            print(f"✅ Created inbox for {agent_name}: {inbox.inbox_id}")
            return inbox
            
        except Exception as e:
            print(f"❌ Failed to create inbox for {agent_name}: {e}")
            raise
    
    async def initialize_all_agent_inboxes(self) -> Dict[str, AgentInbox]:
        """Initialize inboxes for all agents in the game"""
        personalities = AgentPersonalities.get_all_personalities()
        
        tasks = []
        for department, personality in personalities.items():
            task = self.create_agent_inbox(personality.name, department)
            tasks.append(task)
        
        # Create all inboxes concurrently
        inboxes = await asyncio.gather(*tasks, return_exceptions=True)
        
        result = {}
        for i, inbox in enumerate(inboxes):
            personality = list(personalities.values())[i]
            if isinstance(inbox, Exception):
                print(f"❌ Failed to create inbox for {personality.name}: {inbox}")
            else:
                result[personality.name] = inbox
        
        return result
    
    def get_agent_inbox(self, agent_name: str) -> Optional[AgentInbox]:
        """Get an agent's inbox if it exists"""
        return self.created_inboxes.get(agent_name)
    
    def get_all_agent_emails(self) -> List[str]:
        """Get all agent email addresses"""
        return [inbox.inbox_id for inbox in self.created_inboxes.values()]
    
    async def get_inbox_messages(self, agent_name: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get messages from an agent's inbox"""
        inbox = self.get_agent_inbox(agent_name)
        if not inbox:
            raise ValueError(f"No inbox found for agent: {agent_name}")
        
        try:
            response = await self._make_api_request(
                "GET", 
                f"/v0/inboxes/{inbox.inbox_id}/messages"
            )
            
            messages = []
            if isinstance(response, dict):
                # Handle different response formats
                message_list = response.get('messages', response.get('data', []))
                if isinstance(message_list, list):
                    for msg in message_list[:limit]:
                        messages.append({
                            "message_id": msg.get('message_id'),
                            "subject": msg.get('subject'),
                            "from": msg.get('from'),
                            "to": msg.get('to', []),
                            "cc": msg.get('cc', []),
                            "bcc": msg.get('bcc', []),
                            "text_content": msg.get('text', ''),
                            "html_content": msg.get('html', ''),
                            "received_at": msg.get('created_at'),
                            "thread_id": msg.get('thread_id'),
                            "labels": msg.get('labels', []),
                            "attachments": msg.get('attachments', [])
                        })
            
            return messages
            
        except Exception as e:
            print(f"❌ Failed to fetch messages for {agent_name}: {e}")
            return []
    
    async def get_specific_message(self, agent_name: str, message_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific message from an agent's inbox"""
        inbox = self.get_agent_inbox(agent_name)
        if not inbox:
            raise ValueError(f"No inbox found for agent: {agent_name}")
        
        try:
            response = await self._make_api_request(
                "GET", 
                f"/v0/inboxes/{inbox.inbox_id}/messages/{message_id}"
            )
            
            return {
                "message_id": response.get('message_id'),
                "subject": response.get('subject'),
                "from": response.get('from'),
                "to": response.get('to', []),
                "cc": response.get('cc', []),
                "bcc": response.get('bcc', []),
                "text_content": response.get('text', ''),
                "html_content": response.get('html', ''),
                "received_at": response.get('created_at'),
                "thread_id": response.get('thread_id'),
                "labels": response.get('labels', []),
                "attachments": response.get('attachments', [])
            }
            
        except Exception as e:
            print(f"❌ Failed to fetch message {message_id} for {agent_name}: {e}")
            return None
    
    async def send_action_notification(self, action: ActionNotification) -> bool:
        """Send email notification about a game action"""
        try:
            # Verify the sender inbox exists
            sender_inbox = None
            for inbox in self.created_inboxes.values():
                if inbox.inbox_id == action.action_maker_inbox:
                    sender_inbox = inbox
                    break
            
            if not sender_inbox:
                print(f"❌ Sender inbox not found: {action.action_maker_inbox}")
                return False
            
            # Send the email via AgentMail API - try different endpoint formats
            message_data = {
                "to": action.recipients,
                "subject": action.subject,
                "text": action.message_text
            }
            
            if action.message_html:
                message_data["html"] = action.message_html
            
            # Use the correct AgentMail API endpoint format
            response = await self._make_api_request(
                "POST", 
                f"/v0/inboxes/{action.action_maker_inbox}/messages/send", 
                message_data
            )
            
            print(f"📧 Email sent from {action.action_maker} to {len(action.recipients)} recipients")
            print(f"   Subject: {action.subject}")
            print(f"   Message ID: {response.get('message_id', 'Unknown')}")
            print(f"   From inbox: {action.action_maker_inbox}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email notification: {e}")
            # Print debug info
            print(f"   Attempted to send from: {action.action_maker_inbox}")
            print(f"   To recipients: {action.recipients}")
            print(f"   Available inboxes: {list(self.created_inboxes.keys())}")
            return False
    
    async def notify_proposal_submission(self, proposal_title: str, submitter: str, description: str) -> bool:
        """Send notification when a user submits a proposal"""
        submitter_inbox = self.get_agent_inbox(submitter)
        if not submitter_inbox:
            print(f"⚠️ No inbox found for {submitter}")
            return False
        
        # Get all other agent emails as recipients
        recipients = [inbox.inbox_id for name, inbox in self.created_inboxes.items() if name != submitter]
        
        action = ActionNotification(
            action_type="proposal_submission",
            action_maker=submitter,
            action_maker_inbox=submitter_inbox.inbox_id,
            recipients=recipients,
            subject=f"🏛️ New Proposal: {proposal_title}",
            message_text=f"""
A new proposal has been submitted to Mailopolis:

Title: {proposal_title}
Submitted by: {submitter}

Description:
{description}

Please review and provide your department's perspective on this proposal.

---
Mailopolis Automated Notification System
            """.strip(),
            message_html=self._create_proposal_html(proposal_title, submitter, description)
        )
        
        return await self.send_action_notification(action)
    
    async def notify_voting_decision(self, proposal_title: str, voter: str, decision: str, reasoning: str) -> bool:
        """Send notification when an agent makes a voting decision"""
        voter_inbox = self.get_agent_inbox(voter)
        if not voter_inbox:
            print(f"⚠️ No inbox found for {voter}")
            return False
        
        # Send to all other agents
        recipients = [inbox.inbox_id for name, inbox in self.created_inboxes.items() if name != voter]
        
        decision_emoji = "✅" if decision.lower() in ["approve", "support", "yes"] else "❌"
        
        action = ActionNotification(
            action_type="voting_decision",
            action_maker=voter,
            action_maker_inbox=voter_inbox.inbox_id,
            recipients=recipients,
            subject=f"{decision_emoji} Vote on {proposal_title}",
            message_text=f"""
{voter} has voted on the proposal "{proposal_title}":

Decision: {decision}

Reasoning:
{reasoning}

---
Mailopolis Automated Notification System
            """.strip(),
            message_html=self._create_vote_html(proposal_title, voter, decision, reasoning)
        )
        
        return await self.send_action_notification(action)
    
    async def notify_mayor_final_decision(self, proposal_title: str, decision: str, reasoning: str) -> bool:
        """Send notification when the mayor makes a final decision"""
        mayor_name = "Mayor Patricia Williams"
        mayor_inbox = self.get_agent_inbox(mayor_name)
        if not mayor_inbox:
            print(f"⚠️ No inbox found for {mayor_name}")
            return False
        
        # Send to all other agents
        recipients = [inbox.inbox_id for name, inbox in self.created_inboxes.items() if name != mayor_name]
        
        decision_emoji = "👑✅" if decision.lower() in ["approve", "support", "yes"] else "👑❌"
        
        action = ActionNotification(
            action_type="mayor_decision",
            action_maker=mayor_name,
            action_maker_inbox=mayor_inbox.inbox_id,
            recipients=recipients,
            subject=f"{decision_emoji} FINAL DECISION: {proposal_title}",
            message_text=f"""
The Mayor has made the final decision on "{proposal_title}":

FINAL DECISION: {decision.upper()}

Mayor's Statement:
{reasoning}

This decision is now official and will be implemented.

---
Office of the Mayor - Mailopolis
            """.strip(),
            message_html=self._create_mayor_decision_html(proposal_title, decision, reasoning)
        )
        
        return await self.send_action_notification(action)
    
    def _create_proposal_html(self, title: str, submitter: str, description: str) -> str:
        """Create HTML email for proposal submission"""
        return f"""
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .email-header {{
            background-color: #1e40af;
            color: #ffffff;
            padding: 20px;
            text-align: center;
            border-radius: 8px 8px 0 0;
        }}
        .email-content {{
            background-color: #ffffff;
            padding: 20px;
            border: 1px solid #e5e7eb;
            border-radius: 0 0 8px 8px;
        }}
        .proposal-title {{
            font-size: 20px;
            font-weight: bold;
            color: #1e40af;
            margin-bottom: 10px;
        }}
        .submitter {{
            font-weight: bold;
            color: #059669;
        }}
        .description {{
            background-color: #f3f4f6;
            padding: 15px;
            border-left: 4px solid #1e40af;
            margin: 15px 0;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            font-size: 12px;
            color: #6b7280;
        }}
    </style>
</head>
<body>
    <div class="email-header">
        <h1>🏛️ New Proposal Submitted</h1>
    </div>
    <div class="email-content">
        <div class="proposal-title">{title}</div>
        <p><strong>Submitted by:</strong> <span class="submitter">{submitter}</span></p>
        
        <div class="description">
            <strong>Description:</strong><br>
            {description.replace(chr(10), '<br>')}
        </div>
        
        <p>Please review this proposal and provide your department's perspective.</p>
    </div>
    <div class="footer">
        Mailopolis Automated Notification System
    </div>
</body>
</html>
        """.strip()
    
    def _create_vote_html(self, title: str, voter: str, decision: str, reasoning: str) -> str:
        """Create HTML email for voting decision"""
        decision_color = "#059669" if decision.lower() in ["approve", "support", "yes"] else "#dc2626"
        decision_emoji = "✅" if decision.lower() in ["approve", "support", "yes"] else "❌"
        
        return f"""
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .email-header {{
            background-color: {decision_color};
            color: #ffffff;
            padding: 20px;
            text-align: center;
            border-radius: 8px 8px 0 0;
        }}
        .email-content {{
            background-color: #ffffff;
            padding: 20px;
            border: 1px solid #e5e7eb;
            border-radius: 0 0 8px 8px;
        }}
        .proposal-title {{
            font-size: 18px;
            font-weight: bold;
            color: #1f2937;
            margin-bottom: 10px;
        }}
        .voter {{
            font-weight: bold;
            color: #1e40af;
        }}
        .decision {{
            font-size: 18px;
            font-weight: bold;
            color: {decision_color};
            margin: 15px 0;
        }}
        .reasoning {{
            background-color: #f3f4f6;
            padding: 15px;
            border-left: 4px solid {decision_color};
            margin: 15px 0;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            font-size: 12px;
            color: #6b7280;
        }}
    </style>
</head>
<body>
    <div class="email-header">
        <h1>{decision_emoji} Vote Recorded</h1>
    </div>
    <div class="email-content">
        <div class="proposal-title">{title}</div>
        <p><strong>Voter:</strong> <span class="voter">{voter}</span></p>
        
        <div class="decision">Decision: {decision.upper()}</div>
        
        <div class="reasoning">
            <strong>Reasoning:</strong><br>
            {reasoning.replace(chr(10), '<br>')}
        </div>
    </div>
    <div class="footer">
        Mailopolis Automated Notification System
    </div>
</body>
</html>
        """.strip()
    
    def _create_mayor_decision_html(self, title: str, decision: str, reasoning: str) -> str:
        """Create HTML email for mayor's final decision"""
        decision_color = "#059669" if decision.lower() in ["approve", "support", "yes"] else "#dc2626"
        decision_emoji = "👑✅" if decision.lower() in ["approve", "support", "yes"] else "👑❌"
        
        return f"""
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .email-header {{
            background-color: #7c2d12;
            color: #ffffff;
            padding: 20px;
            text-align: center;
            border-radius: 8px 8px 0 0;
        }}
        .email-content {{
            background-color: #ffffff;
            padding: 20px;
            border: 1px solid #e5e7eb;
            border-radius: 0 0 8px 8px;
        }}
        .proposal-title {{
            font-size: 18px;
            font-weight: bold;
            color: #1f2937;
            margin-bottom: 10px;
        }}
        .final-decision {{
            font-size: 24px;
            font-weight: bold;
            color: {decision_color};
            text-align: center;
            margin: 20px 0;
            padding: 15px;
            border: 3px solid {decision_color};
            border-radius: 8px;
        }}
        .reasoning {{
            background-color: #fef7ff;
            padding: 15px;
            border-left: 4px solid #7c2d12;
            margin: 15px 0;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            font-size: 12px;
            color: #6b7280;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="email-header">
        <h1>{decision_emoji} MAYORAL DECISION</h1>
    </div>
    <div class="email-content">
        <div class="proposal-title">{title}</div>
        
        <div class="final-decision">
            FINAL DECISION: {decision.upper()}
        </div>
        
        <div class="reasoning">
            <strong>Mayor's Statement:</strong><br>
            {reasoning.replace(chr(10), '<br>')}
        </div>
        
        <p><strong>This decision is now official and will be implemented.</strong></p>
    </div>
    <div class="footer">
        Office of the Mayor - Mailopolis
    </div>
</body>
</html>
        """.strip()


# Global instance
agent_mail_service = AgentMailService()


async def initialize_agent_inboxes():
    """Initialize all agent inboxes - call this on startup"""
    return await agent_mail_service.initialize_all_agent_inboxes()


async def send_proposal_notification(proposal_title: str, submitter: str, description: str):
    """Send notification when a proposal is submitted"""
    return await agent_mail_service.notify_proposal_submission(proposal_title, submitter, description)


async def send_vote_notification(proposal_title: str, voter: str, decision: str, reasoning: str):
    """Send notification when an agent votes"""
    return await agent_mail_service.notify_voting_decision(proposal_title, voter, decision, reasoning)


async def send_mayor_decision_notification(proposal_title: str, decision: str, reasoning: str):
    """Send notification when the mayor makes a final decision"""
    return await agent_mail_service.notify_mayor_final_decision(proposal_title, decision, reasoning)


if __name__ == "__main__":
    """Test the AgentMail service"""
    import asyncio
    
    async def test_service():
        print("🧪 Testing AgentMail Service")
        print("=" * 50)
        
        # Initialize inboxes
        inboxes = await initialize_agent_inboxes()
        print(f"✅ Initialized {len(inboxes)} agent inboxes")
        
        # Test sending a proposal notification
        await send_proposal_notification(
            "Test Renewable Energy Initiative",
            "Dr. Marcus Chen",
            "This is a test proposal to implement solar panels on all municipal buildings."
        )
        
        print("🧪 Test completed!")
    
    asyncio.run(test_service())
