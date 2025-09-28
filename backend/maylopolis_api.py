"""
Mailopolis (Maylopolis) Game API

Provides HTTP endpoints to interact with the `MaylopolisGameEngine`.

Endpoints:
- POST /maylopolis/start -> start a new game
- GET  /maylopolis/state -> current game state
- GET  /maylopolis/suggestions -> list of suggested proposals
- POST /maylopolis/turn -> play one turn by submitting proposals
"""
import asyncio
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, WebSocket, Query
from pydantic import BaseModel

from agents.langchain_agents import LangChainAgentManager
from game.langchain_game_engine import MaylopolisGameEngine
from models.game_models import PolicyProposal, Department
from service.agent_mail import agent_mail_service


class AskProposalRequest(BaseModel):
    department: Optional[Department] = None


class ProposalInput(BaseModel):
    title: str
    description: str
    target_department: Department
    sustainability_impact: Optional[int] = None
    economic_impact: Optional[int] = None
    political_impact: Optional[int] = None


class SingleProposalRequest(BaseModel):
    proposal: ProposalInput


# Singleton engine for this process (simple in-memory session)
_engine: Optional[MaylopolisGameEngine] = None
_agent_manager: Optional[LangChainAgentManager] = None


async def get_engine() -> MaylopolisGameEngine:
    global _engine, _agent_manager
    if _engine is None:
        # Let the engine create its own agent manager with shared logger
        _engine = MaylopolisGameEngine()
        # start a fresh game on creation
        await _engine.start_new_game()
    return _engine


router = APIRouter(prefix="/maylopolis", tags=["maylopolis"])


@router.post("/start")
async def start_game():
    try:
        engine = await get_engine()
        state = await engine.start_new_game()
        return {"ok": True, "state": state}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/state")
async def get_state():
    try:
        engine = await get_engine()
        return {
            "turn": engine.turn_number,
            "city_stats": engine.city_stats.to_dict(),
            "active_events": [e.__dict__ for e in engine.active_events],
            "is_game_over": engine.is_game_over
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/suggestions")
async def get_suggestions():
    try:
        engine = await get_engine()
        suggestions = await engine.get_suggested_proposals()
        # PolicyProposal is a pydantic model; convert to dict
        return {"count": len(suggestions), "suggestions": [s.dict() for s in suggestions]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/turn")
async def play_turn(req: SingleProposalRequest):
    try:
        engine = await get_engine()
        # Convert single input to PolicyProposal and play one turn
        p = req.proposal
        proposal = PolicyProposal(
            title=p.title,
            description=p.description,
            proposed_by="player",
            target_department=p.target_department,
            sustainability_impact=p.sustainability_impact or 0,
            economic_impact=p.economic_impact or 0,
            political_impact=p.political_impact or 0
        )

        result = await engine.play_turn(proposal)
        return {"ok": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/inboxes")
async def get_agent_inboxes():
    """Get all agent email inboxes and their details"""
    try:
        # Get all created inboxes from the agent mail service
        inboxes = agent_mail_service.created_inboxes
        
        if not inboxes:
            # If no inboxes exist, try to initialize them
            await agent_mail_service.initialize_all_agent_inboxes()
            inboxes = agent_mail_service.created_inboxes
        
        # Convert to API-friendly format
        inbox_data = []
        for agent_name, inbox in inboxes.items():
            inbox_data.append({
                "agent_name": inbox.agent_name,
                "email_address": inbox.inbox_id,
                "department": inbox.department.value,
                "display_name": inbox.display_name,
                "created_at": inbox.created_at.isoformat(),
                "username": agent_mail_service._get_agent_email_username(agent_name)
            })
        
        return {
            "ok": True,
            "count": len(inbox_data),
            "inboxes": inbox_data,
            "api_status": "connected" if agent_mail_service.api_key else "no_api_key"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get agent inboxes: {str(e)}")


@router.get("/inboxes/{agent_name}")
async def get_agent_inbox(agent_name: str):
    """Get specific agent's inbox details"""
    try:
        # Find the inbox for this agent
        inbox = agent_mail_service.get_agent_inbox(agent_name)
        
        if not inbox:
            # Try to find by partial name match (case insensitive)
            for name, inbox_obj in agent_mail_service.created_inboxes.items():
                if agent_name.lower() in name.lower():
                    inbox = inbox_obj
                    break
        
        if not inbox:
            raise HTTPException(
                status_code=404, 
                detail=f"No inbox found for agent '{agent_name}'. Available agents: {list(agent_mail_service.created_inboxes.keys())}"
            )
        
        # Try to get recent messages from this inbox using the service method
        messages = []
        try:
            messages = await agent_mail_service.get_inbox_messages(inbox.agent_name, limit=10)
            # Truncate text content for preview
            for msg in messages:
                if msg.get('text_content'):
                    text = msg['text_content']
                    if len(text) > 200:
                        msg['text_content'] = text[:200] + "..."
        except Exception as e:
            # If we can't fetch messages, that's okay - just return empty list
            print(f"Could not fetch messages for {inbox.agent_name}: {e}")
        
        return {
            "ok": True,
            "agent_name": inbox.agent_name,
            "email_address": inbox.inbox_id,
            "department": inbox.department.value,
            "display_name": inbox.display_name,
            "created_at": inbox.created_at.isoformat(),
            "username": agent_mail_service._get_agent_email_username(inbox.agent_name),
            "recent_messages": messages,
            "message_count": len(messages)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get agent inbox: {str(e)}")


@router.get("/inboxes/{agent_name}/messages")
async def get_agent_messages(
    agent_name: str, 
    limit: int = Query(default=20, description="Number of messages to retrieve"),
    include_content: bool = Query(default=True, description="Include full message content")
):
    """Get messages from a specific agent's inbox"""
    try:
        # Find the inbox for this agent
        inbox = agent_mail_service.get_agent_inbox(agent_name)
        
        if not inbox:
            # Try to find by partial name match (case insensitive)
            for name, inbox_obj in agent_mail_service.created_inboxes.items():
                if agent_name.lower() in name.lower():
                    inbox = inbox_obj
                    break
        
        if not inbox:
            raise HTTPException(
                status_code=404, 
                detail=f"No inbox found for agent '{agent_name}'"
            )
        
        # Fetch messages using the AgentMail service
        try:
            messages = await agent_mail_service.get_inbox_messages(inbox.agent_name, limit=limit)
            
            # Process messages based on include_content flag
            if not include_content:
                for msg in messages:
                    # Replace full content with preview
                    text = msg.get('text_content', '')
                    msg['text_preview'] = text[:200] + "..." if len(text) > 200 else text
                    # Remove full content fields
                    msg.pop('text_content', None)
                    msg.pop('html_content', None)
                    msg.pop('attachments', None)
            
            return {
                "ok": True,
                "agent_name": inbox.agent_name,
                "email_address": inbox.inbox_id,
                "total_messages": len(messages),
                "messages": messages,
                "inbox_info": {
                    "department": inbox.department.value,
                    "display_name": inbox.display_name,
                    "created_at": inbox.created_at.isoformat()
                }
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to fetch messages from AgentMail API: {str(e)}"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get agent messages: {str(e)}")


@router.get("/inboxes/{agent_name}/messages/{message_id}")
async def get_specific_message(agent_name: str, message_id: str):
    """Get a specific message from an agent's inbox"""
    try:
        # Find the inbox for this agent
        inbox = agent_mail_service.get_agent_inbox(agent_name)
        
        if not inbox:
            # Try to find by partial name match (case insensitive)
            for name, inbox_obj in agent_mail_service.created_inboxes.items():
                if agent_name.lower() in name.lower():
                    inbox = inbox_obj
                    break
        
        if not inbox:
            raise HTTPException(
                status_code=404, 
                detail=f"No inbox found for agent '{agent_name}'"
            )
        
        # Fetch specific message using the AgentMail service
        try:
            message_data = await agent_mail_service.get_specific_message(inbox.agent_name, message_id)
            
            if not message_data:
                raise HTTPException(status_code=404, detail=f"Message {message_id} not found")
            
            return {
                "ok": True,
                "agent_name": inbox.agent_name,
                "email_address": inbox.inbox_id,
                "message": message_data
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=404 if "not found" in str(e).lower() else 500,
                detail=f"Message not found or API error: {str(e)}"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get message: {str(e)}")


@router.post("/inboxes/initialize")
async def initialize_agent_inboxes():
    """Initialize or refresh all agent email inboxes"""
    try:
        inboxes = await agent_mail_service.initialize_all_agent_inboxes()
        
        return {
            "ok": True,
            "message": "Agent inboxes initialized successfully",
            "count": len(inboxes),
            "inboxes": [
                {
                    "agent_name": inbox.agent_name,
                    "email_address": inbox.inbox_id,
                    "department": inbox.department.value,
                    "created_at": inbox.created_at.isoformat()
                }
                for inbox in inboxes.values()
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize agent inboxes: {str(e)}")


@router.websocket("/ws/logs")
async def websocket_endpoint(websocket: WebSocket):
    """Simple websocket endpoint that registers the client to receive game logs.

    """
    # Accept the connection
    await websocket.accept()

    # Subscribe to engine logs (if engine available)
    engine = None
    log_queue = None
    try:
        engine = await get_engine()
        log_queue = await engine.subscribe_logs()
    except Exception:
        # If engine or subscription fails, we'll keep the socket open but no logs will be sent
        log_queue = None

    try:
        # Forward logs from engine to client while accepting pings/messages
        while True:
            # Wait for either a log message or an incoming websocket message
            receive_task = asyncio.create_task(websocket.receive_text())
            log_task = asyncio.create_task(log_queue.get()) if log_queue is not None else None

            done, pending = await asyncio.wait(
                [t for t in [receive_task, log_task] if t is not None],
                return_when=asyncio.FIRST_COMPLETED,
            )

            if receive_task in done:
                try:
                    msg = receive_task.result()
                except Exception:
                    break
                # Ignore client messages (or you could implement ping handling)

            if log_task is not None and log_task in done:
                try:
                    log_msg = log_task.result()
                    await websocket.send_text(log_msg)
                except Exception:
                    break

            # Cancel any pending tasks to avoid leaks
            for t in pending:
                t.cancel()
    finally:
        if engine is not None and log_queue is not None:
            try:
                await engine.unsubscribe_logs(log_queue)
            except Exception:
                pass

__all__ = ["router", "get_engine"]

