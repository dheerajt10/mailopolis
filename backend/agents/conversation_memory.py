import json
import os
from typing import Dict, List, Any
from datetime import datetime
from dataclasses import dataclass

@dataclass
class ConversationMessage:
    speaker: str  # Agent name
    department: str
    content: str
    timestamp: datetime
    message_type: str  # "initial_reaction", "negotiation", "final_position"
    references: List[str] = None  # What/who they're responding to

class ConversationMemory:
    """Manages agent conversation history and retrieval"""
    
    def __init__(self, storage_dir: str = "data/conversations"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        
    def save_conversation(self, proposal_id: str, messages: List[ConversationMessage]):
        """Save conversation to file"""
        filename = f"{proposal_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.storage_dir, filename)
        
        conversation_data = {
            "proposal_id": proposal_id,
            "timestamp": datetime.now().isoformat(),
            "messages": [
                {
                    "speaker": msg.speaker,
                    "department": msg.department,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat(),
                    "message_type": msg.message_type,
                    "references": msg.references or []
                }
                for msg in messages
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(conversation_data, f, indent=2)
        
        print(f"💾 Saved conversation: {filename}")
    
    def get_recent_conversations(self, agent_name: str, limit: int = 5) -> List[Dict]:
        """Get recent conversations involving this agent"""
        conversations = []
        
        if not os.path.exists(self.storage_dir):
            return conversations
            
        try:
            files = [f for f in os.listdir(self.storage_dir) if f.endswith('.json')]
            files.sort(reverse=True)  # Most recent first
            
            for filename in files[:limit*2]:  # Check more files to find agent participation
                filepath = os.path.join(self.storage_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    
                    # Check if agent participated
                    agent_messages = [msg for msg in data['messages'] if msg['speaker'] == agent_name]
                    if agent_messages:
                        conversations.append(data)
                        
                    if len(conversations) >= limit:
                        break
                        
                except Exception as e:
                    print(f"Error reading conversation file {filename}: {e}")
        except Exception as e:
            print(f"Error accessing conversation directory: {e}")
                    
        return conversations
    
    def get_agent_relationship_context(self, agent1: str, agent2: str) -> str:
        """Get context about relationship between two agents based on past conversations"""
        interactions = []
        
        if not os.path.exists(self.storage_dir):
            return f"No significant past interactions between {agent1} and {agent2}."
        
        try:
            # Look through recent conversations for interactions between these two agents
            files = [f for f in os.listdir(self.storage_dir) if f.endswith('.json')]
            
            for filename in files:
                filepath = os.path.join(self.storage_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    
                    # Find messages where these two agents interacted
                    agent1_messages = [msg for msg in data['messages'] if msg['speaker'] == agent1]
                    agent2_messages = [msg for msg in data['messages'] if msg['speaker'] == agent2]
                    
                    if agent1_messages and agent2_messages:
                        interactions.extend([
                            f"{msg['speaker']}: {msg['content'][:100]}..." 
                            for msg in data['messages'] 
                            if msg['speaker'] in [agent1, agent2]
                        ])
                        
                except Exception:
                    continue
        except Exception as e:
            print(f"Error building relationship context: {e}")
        
        if interactions:
            return f"Past interactions between {agent1} and {agent2}:\n" + "\n".join(interactions[-3:])
        else:
            return f"No significant past interactions between {agent1} and {agent2}."
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get statistics about stored conversations"""
        if not os.path.exists(self.storage_dir):
            return {"total_conversations": 0, "total_messages": 0}
        
        try:
            files = [f for f in os.listdir(self.storage_dir) if f.endswith('.json')]
            total_conversations = len(files)
            total_messages = 0
            
            for filename in files:
                filepath = os.path.join(self.storage_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    total_messages += len(data.get('messages', []))
                except Exception:
                    continue
                    
            return {
                "total_conversations": total_conversations,
                "total_messages": total_messages,
                "storage_directory": self.storage_dir
            }
        except Exception as e:
            print(f"Error getting conversation stats: {e}")
            return {"total_conversations": 0, "total_messages": 0, "error": str(e)}