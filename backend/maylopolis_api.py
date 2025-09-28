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
        _agent_manager = LangChainAgentManager()
        _engine = MaylopolisGameEngine(agent_manager=_agent_manager)
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

