"""
WebSocket support for real-time game updates
"""

import socketio
from fastapi import FastAPI
import asyncio
import json
from typing import Dict, List
from datetime import datetime

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins="*",  # Allow all origins
    logger=True,
    engineio_logger=True
)

# Track connected clients
connected_clients: Dict[str, Dict] = {}
game_rooms: Dict[str, List[str]] = {}

class WebSocketManager:
    """Manages WebSocket connections and game events"""
    
    @staticmethod
    async def broadcast_game_update(data: Dict):
        """Broadcast game state update to all connected clients"""
        await sio.emit('game_state_update', data)
    
    @staticmethod 
    async def broadcast_new_message(message_data: Dict):
        """Broadcast new AgentMail message to relevant clients"""
        await sio.emit('new_message', message_data)
    
    @staticmethod
    async def broadcast_proposal_decision(decision_data: Dict):
        """Broadcast proposal decision to all clients"""
        await sio.emit('proposal_decision', decision_data)
    
    @staticmethod
    async def broadcast_round_start(round_data: Dict):
        """Broadcast new round start to all clients"""
        await sio.emit('round_started', round_data)
    
    @staticmethod
    async def broadcast_bad_actor_action(action_data: Dict):
        """Broadcast bad actor action to all clients"""
        await sio.emit('bad_actor_action', action_data)
    
    @staticmethod
    async def broadcast_sustainability_change(change_data: Dict):
        """Broadcast sustainability index change"""
        await sio.emit('sustainability_change', change_data)
    
    @staticmethod
    async def broadcast_blockchain_transaction(tx_data: Dict):
        """Broadcast new blockchain transaction"""
        await sio.emit('blockchain_transaction', tx_data)

# WebSocket event handlers
@sio.event
async def connect(sid, environ):
    """Handle client connection"""
    print(f"🔌 Client connected: {sid}")
    
    connected_clients[sid] = {
        'connected_at': datetime.now().isoformat(),
        'game_room': None
    }
    
    # Send connection confirmation
    await sio.emit('connect_confirmation', {
        'status': 'connected',
        'client_id': sid,
        'server_time': datetime.now().isoformat()
    }, room=sid)

@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    print(f"🔌 Client disconnected: {sid}")
    
    # Clean up client data
    if sid in connected_clients:
        game_room = connected_clients[sid].get('game_room')
        if game_room and game_room in game_rooms:
            if sid in game_rooms[game_room]:
                game_rooms[game_room].remove(sid)
            if not game_rooms[game_room]:  # Remove empty room
                del game_rooms[game_room]
        
        del connected_clients[sid]

@sio.event
async def join_game(sid, data):
    """Handle client joining a game room"""
    game_id = data.get('gameId', 'main_game')
    
    # Add client to game room
    if game_id not in game_rooms:
        game_rooms[game_id] = []
    
    game_rooms[game_id].append(sid)
    connected_clients[sid]['game_room'] = game_id
    
    # Join the Socket.IO room
    await sio.enter_room(sid, game_id)
    
    print(f"🎮 Client {sid} joined game room: {game_id}")
    
    # Send join confirmation
    await sio.emit('room_joined', {
        'game_id': game_id,
        'players_in_room': len(game_rooms[game_id])
    }, room=sid)

@sio.event
async def leave_game(sid, data):
    """Handle client leaving a game room"""
    game_id = data.get('gameId', 'main_game')
    
    # Remove from game room
    if game_id in game_rooms and sid in game_rooms[game_id]:
        game_rooms[game_id].remove(sid)
        if not game_rooms[game_id]:
            del game_rooms[game_id]
    
    connected_clients[sid]['game_room'] = None
    
    # Leave the Socket.IO room
    await sio.leave_room(sid, game_id)
    
    print(f"🎮 Client {sid} left game room: {game_id}")

@sio.event
async def player_action(sid, data):
    """Handle player action from client"""
    action = data.get('action')
    action_data = data.get('data', {})
    
    print(f"🎯 Player action from {sid}: {action}")
    
    # Process different action types
    if action == 'submit_proposal':
        # Broadcast that a proposal was submitted
        await sio.emit('proposal_submitted', {
            'player_id': sid,
            'proposal_title': action_data.get('title', 'New Proposal'),
            'timestamp': datetime.now().isoformat()
        }, skip_sid=sid)  # Don't send back to sender
    
    elif action == 'request_mayor_decision':
        # Broadcast that mayor decision was requested
        await sio.emit('mayor_decision_requested', {
            'player_id': sid,
            'timestamp': datetime.now().isoformat()
        }, skip_sid=sid)
    
    # Acknowledge action received
    await sio.emit('action_acknowledged', {
        'action': action,
        'status': 'processed',
        'timestamp': datetime.now().isoformat()
    }, room=sid)

@sio.event
async def request_update(sid, data):
    """Handle client request for game state update"""
    # Import here to avoid circular imports
    from game_api import GameAPI
    
    try:
        # Get current game state
        game_state = GameAPI.get_game_state()
        departments = GameAPI.get_departments()
        
        # Send update to requesting client
        await sio.emit('game_state_update', {
            'game_state': game_state,
            'departments': departments,
            'timestamp': datetime.now().isoformat()
        }, room=sid)
        
    except Exception as e:
        print(f"❌ Error sending game update to {sid}: {e}")
        await sio.emit('update_error', {
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }, room=sid)

@sio.event
async def ping(sid, data):
    """Handle ping from client (for connection testing)"""
    await sio.emit('pong', {
        'timestamp': datetime.now().isoformat(),
        'client_count': len(connected_clients)
    }, room=sid)

# Admin/monitoring events
@sio.event
async def get_server_stats(sid, data):
    """Get server statistics (admin only)"""
    stats = {
        'connected_clients': len(connected_clients),
        'active_rooms': len(game_rooms),
        'server_uptime': datetime.now().isoformat(),
        'rooms_info': {room: len(clients) for room, clients in game_rooms.items()}
    }
    
    await sio.emit('server_stats', stats, room=sid)

def add_websocket_support(app: FastAPI):
    """Add WebSocket support to FastAPI app"""
    
    # Create ASGI app for Socket.IO
    socket_app = socketio.ASGIApp(sio, other_asgi_app=app)
    
    return socket_app

# Utility functions for triggering WebSocket events from other modules
async def notify_game_update(data: Dict):
    """Notify all clients of game state update"""
    await WebSocketManager.broadcast_game_update(data)

async def notify_new_message(message_data: Dict):
    """Notify clients of new AgentMail message"""
    await WebSocketManager.broadcast_new_message(message_data)

async def notify_proposal_decision(decision_data: Dict):
    """Notify clients of proposal decision"""
    await WebSocketManager.broadcast_proposal_decision(decision_data)

async def notify_round_start(round_data: Dict):
    """Notify clients of new round start"""
    await WebSocketManager.broadcast_round_start(round_data)

async def notify_bad_actor_action(action_data: Dict):
    """Notify clients of bad actor action"""
    await WebSocketManager.broadcast_bad_actor_action(action_data)

async def notify_sustainability_change(change_data: Dict):
    """Notify clients of sustainability change"""
    await WebSocketManager.broadcast_sustainability_change(change_data)

async def notify_blockchain_transaction(tx_data: Dict):
    """Notify clients of new blockchain transaction"""
    await WebSocketManager.broadcast_blockchain_transaction(tx_data)