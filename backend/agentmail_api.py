"""
AgentMail API endpoints for Mailopolis
Handles in-game email communication between player and agents
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random
import uuid

from models.game_models import Department

class Message(BaseModel):
    id: str
    from_agent: str
    to_agent: str
    subject: str
    content: str
    timestamp: datetime
    read: bool = False
    priority: str = "medium"  # low, medium, high, urgent
    thread_id: Optional[str] = None

class SendMessageRequest(BaseModel):
    to: str
    subject: str
    content: str
    priority: str = "medium"

# In-memory message storage (could be replaced with database)
message_store: Dict[str, Message] = {}
agent_names = {
    "mayor": "Mayor Sarah Chen",
    "energy": "Dr. Alex Rivera - Energy Director",
    "transportation": "Maria Santos - Transportation Chief",
    "housing": "James Wilson - Housing Director", 
    "waste": "Dr. Priya Patel - Waste Management Director",
    "water": "Michael Chang - Water Systems Director",
    "economic_dev": "Lisa Thompson - Economic Development Director",
    "player": "Player"
}

def initialize_sample_messages():
    """Initialize the system with some sample messages"""
    global message_store
    
    sample_messages = [
        {
            "from": "mayor",
            "to": "player", 
            "subject": "Welcome to Mailopolis - Let's Build a Sustainable Future",
            "content": """Dear Sustainability Advisor,

Welcome to your new role! I'm excited to work with you to transform Mailopolis into a model sustainable city.

Our current sustainability index is at 57/100 - there's significant room for improvement. I've reviewed the department reports and see several areas where your expertise could make a real impact.

Please review the attached department scorecards and submit your initial policy recommendations. I'm particularly interested in quick wins that can demonstrate progress to our citizens while laying groundwork for longer-term transformation.

The city council meeting is next Tuesday, so any proposals you submit by Monday will be considered for immediate implementation.

Looking forward to your insights!

Best regards,
Mayor Sarah Chen""",
            "priority": "high"
        },
        {
            "from": "energy",
            "to": "player",
            "subject": "URGENT: Grid Stability Issues & Renewable Energy Opportunities", 
            "content": """Hi there,

Dr. Alex Rivera from the Energy Department. We've got both challenges and opportunities on our plate:

**IMMEDIATE CONCERNS:**
- Peak demand has increased 12% this quarter
- Two coal plants scheduled for decommission next year
- Grid stability issues during high renewable generation periods

**OPPORTUNITIES:**
- Federal solar incentive program expires in 6 months
- Community solar program proposal ready for approval
- Battery storage pilot project awaiting funding

I've prepared three policy options for your review. The Mayor trusts your judgment on sustainability priorities, and frankly, we need to move fast on the federal incentives.

Would love to discuss strategy over coffee this week.

Best,
Alex""",
            "priority": "high"
        },
        {
            "from": "transportation",
            "to": "player",
            "subject": "Public Transit Ridership Down 23% - Need Strategic Input",
            "content": """Hello,

Maria Santos here, Transportation Chief. I wanted to brief you on our current situation before you meet with the Mayor.

**THE PROBLEM:**
Our public transit ridership has dropped 23% since the pandemic, but car registrations are up 15%. This is moving us backwards on emissions goals.

**WHAT I'M SEEING:**
- Bus routes haven't been optimized for new housing developments
- Electric bus pilot program stalled due to charging infrastructure costs  
- Bike lane network has gaps that make commuting impractical
- Ride-sharing services are cannibalizing short bus trips

**MY RECOMMENDATION:**
We need an integrated mobility strategy that makes sustainable transportation the obvious choice, not just the "right" choice.

I have detailed proposals ready, but I need political backing from the Mayor's office to overcome resistance from car dealerships and parking garage operators.

Can we set up a meeting to discuss strategy?

Regards,
Maria""",
            "priority": "medium"
        }
    ]
    
    for msg_data in sample_messages:
        msg_id = str(uuid.uuid4())
        timestamp = datetime.now() - timedelta(hours=random.randint(1, 48))
        
        message = Message(
            id=msg_id,
            from_agent=msg_data["from"],
            to_agent=msg_data["to"],
            subject=msg_data["subject"],
            content=msg_data["content"],
            timestamp=timestamp,
            priority=msg_data["priority"]
        )
        message_store[msg_id] = message

# Initialize sample messages
initialize_sample_messages()

class AgentMailAPI:
    """AgentMail API for game communication"""
    
    @staticmethod
    def get_messages(recipient: str = "player") -> Dict:
        """Get all messages for a recipient"""
        user_messages = []
        
        for message in message_store.values():
            if message.to_agent == recipient:
                user_messages.append({
                    "id": message.id,
                    "from": agent_names.get(message.from_agent, message.from_agent),
                    "to": agent_names.get(message.to_agent, message.to_agent),
                    "subject": message.subject,
                    "content": message.content,
                    "timestamp": message.timestamp.isoformat(),
                    "read": message.read,
                    "priority": message.priority,
                    "thread_id": message.thread_id
                })
        
        # Sort by timestamp (newest first)
        user_messages.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return {
            "messages": user_messages,
            "total_count": len(user_messages),
            "unread_count": len([m for m in user_messages if not m["read"]])
        }
    
    @staticmethod
    def get_message(message_id: str) -> Dict:
        """Get a specific message and mark it as read"""
        if message_id not in message_store:
            raise HTTPException(status_code=404, detail="Message not found")
        
        message = message_store[message_id]
        message.read = True  # Mark as read when accessed
        
        return {
            "id": message.id,
            "from": agent_names.get(message.from_agent, message.from_agent),
            "to": agent_names.get(message.to_agent, message.to_agent),
            "subject": message.subject,
            "content": message.content,
            "timestamp": message.timestamp.isoformat(),
            "read": message.read,
            "priority": message.priority,
            "thread_id": message.thread_id
        }
    
    @staticmethod 
    def send_message(sender: str, message_data: SendMessageRequest) -> Dict:
        """Send a message to an agent"""
        # Validate recipient
        valid_recipients = list(agent_names.keys())
        if message_data.to not in valid_recipients:
            raise HTTPException(status_code=400, detail=f"Invalid recipient. Valid options: {valid_recipients}")
        
        # Create new message
        message_id = str(uuid.uuid4())
        message = Message(
            id=message_id,
            from_agent=sender,
            to_agent=message_data.to,
            subject=message_data.subject,
            content=message_data.content,
            timestamp=datetime.now(),
            priority=message_data.priority
        )
        
        message_store[message_id] = message
        
        # Generate automatic reply based on recipient (simulate agent behavior)
        AgentMailAPI._generate_auto_reply(message)
        
        # Notify WebSocket clients of new message
        try:
            from websocket_manager import notify_new_message
            import asyncio
            asyncio.create_task(notify_new_message({
                "message_id": message_id,
                "from": agent_names.get(sender, sender),
                "to": agent_names.get(message_data.to, message_data.to),
                "subject": message_data.subject,
                "timestamp": message.timestamp.isoformat()
            }))
        except:
            pass  # WebSocket notification is optional
        
        return {
            "success": True,
            "message_id": message_id,
            "message": f"Message sent to {agent_names.get(message_data.to, message_data.to)}",
            "estimated_response_time": AgentMailAPI._get_response_time(message_data.to)
        }
    
    @staticmethod
    def mark_message_read(message_id: str) -> Dict:
        """Mark a message as read"""
        if message_id not in message_store:
            raise HTTPException(status_code=404, detail="Message not found")
        
        message_store[message_id].read = True
        return {"success": True, "message": "Message marked as read"}
    
    @staticmethod
    def delete_message(message_id: str) -> Dict:
        """Delete a message"""
        if message_id not in message_store:
            raise HTTPException(status_code=404, detail="Message not found")
        
        del message_store[message_id]
        return {"success": True, "message": "Message deleted"}
    
    @staticmethod
    def get_conversation_thread(thread_id: str) -> Dict:
        """Get all messages in a conversation thread"""
        thread_messages = [
            {
                "id": msg.id,
                "from": agent_names.get(msg.from_agent, msg.from_agent),
                "to": agent_names.get(msg.to_agent, msg.to_agent),
                "subject": msg.subject,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "read": msg.read,
                "priority": msg.priority
            }
            for msg in message_store.values()
            if msg.thread_id == thread_id
        ]
        
        thread_messages.sort(key=lambda x: x["timestamp"])
        
        return {
            "thread_id": thread_id,
            "messages": thread_messages,
            "message_count": len(thread_messages)
        }
    
    @staticmethod
    def _generate_auto_reply(original_message: Message):
        """Generate an automatic reply from agents (simulated AI behavior)"""
        # Simple auto-reply logic (can be enhanced with LangChain)
        replies = {
            "mayor": [
                "Thank you for your proposal. I'll review it with my team and get back to you within 48 hours.",
                "Interesting perspective. Let me discuss this with the relevant department heads.",
                "I appreciate your proactive approach. This aligns with our sustainability goals."
            ],
            "energy": [
                "Great points about energy efficiency. I'll run some numbers and feasibility analysis.",
                "This could work well with our renewable energy transition plan. Let me check the budget.",
                "I like the innovative approach. We should schedule a technical review meeting."
            ],
            "transportation": [
                "Thanks for the transportation insights. I'll coordinate with city planning.",
                "This fits our mobility strategy. I'll need to verify integration with existing routes.",
                "Good timing - we're updating our transportation master plan next month."
            ]
        }
        
        recipient = original_message.to_agent
        if recipient in replies and random.random() < 0.7:  # 70% chance of auto-reply
            reply_content = random.choice(replies[recipient])
            
            # Create reply message
            reply_id = str(uuid.uuid4())
            reply = Message(
                id=reply_id,
                from_agent=recipient,
                to_agent=original_message.from_agent,
                subject=f"Re: {original_message.subject}",
                content=reply_content,
                timestamp=datetime.now() + timedelta(minutes=random.randint(5, 120)),
                priority="medium",
                thread_id=original_message.thread_id or original_message.id
            )
            
            message_store[reply_id] = reply
            
            # Notify WebSocket clients of auto-reply
            try:
                from websocket_manager import notify_new_message
                import asyncio
                asyncio.create_task(notify_new_message({
                    "message_id": reply_id,
                    "from": agent_names.get(recipient, recipient),
                    "to": agent_names.get(original_message.from_agent, original_message.from_agent),
                    "subject": reply.subject,
                    "timestamp": reply.timestamp.isoformat(),
                    "is_auto_reply": True
                }))
            except:
                pass  # WebSocket notification is optional
    
    @staticmethod
    def _get_response_time(recipient: str) -> str:
        """Get estimated response time for different agents"""
        response_times = {
            "mayor": "24-48 hours",
            "energy": "4-8 hours",
            "transportation": "2-6 hours", 
            "housing": "8-12 hours",
            "waste": "4-8 hours",
            "water": "6-10 hours",
            "economic_dev": "12-24 hours"
        }
        return response_times.get(recipient, "4-12 hours")

def add_agentmail_endpoints(app: FastAPI):
    """Add AgentMail endpoints to FastAPI app"""
    
    @app.get("/api/agentmail/messages")
    def get_messages(recipient: str = "player"):
        """Get all messages for a recipient"""
        return AgentMailAPI.get_messages(recipient)
    
    @app.get("/api/agentmail/messages/{message_id}")
    def get_message(message_id: str):
        """Get a specific message"""
        return AgentMailAPI.get_message(message_id)
    
    @app.post("/api/agentmail/send")
    def send_message(message_data: SendMessageRequest, sender: str = "player"):
        """Send a message to an agent"""
        return AgentMailAPI.send_message(sender, message_data)
    
    @app.put("/api/agentmail/messages/{message_id}/read")
    def mark_message_read(message_id: str):
        """Mark a message as read"""
        return AgentMailAPI.mark_message_read(message_id)
    
    @app.delete("/api/agentmail/messages/{message_id}")
    def delete_message(message_id: str):
        """Delete a message"""
        return AgentMailAPI.delete_message(message_id)
    
    @app.get("/api/agentmail/threads/{thread_id}")
    def get_conversation_thread(thread_id: str):
        """Get all messages in a conversation thread"""
        return AgentMailAPI.get_conversation_thread(thread_id)
    
    @app.get("/api/agentmail/agents")
    def get_available_agents():
        """Get list of available agents to message"""
        return {
            "agents": [
                {"id": agent_id, "name": name, "department": agent_id.title()}
                for agent_id, name in agent_names.items() 
                if agent_id != "player"
            ]
        }