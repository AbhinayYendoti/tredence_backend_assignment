import json
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from database import SessionLocal
from services.room_service import get_room, update_room_code

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)
        print(f"[WS] Client connected to room {room_id}. Total connections: {len(self.active_connections[room_id])}")
    
    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.active_connections:
            if websocket in self.active_connections[room_id]:
                self.active_connections[room_id].remove(websocket)
                print(f"[WS] Client disconnected from room {room_id}. Remaining connections: {len(self.active_connections[room_id])}")
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]
                print(f"[WS] Room {room_id} is now empty, removing from active connections")
    
    async def broadcast_to_room(self, room_id: str, message: dict, exclude_websocket: WebSocket = None):
        """
        Broadcast message to all clients in a room.
        If exclude_websocket is provided, don't send the message back to that client.
        """
        if room_id not in self.active_connections:
            print(f"[WS] Warning: No active connections in room {room_id}")
            return
        
        connections = self.active_connections[room_id].copy()  # Copy to avoid modification during iteration
        disconnected = []
        
        print(f"[WS] Broadcasting to room {room_id} - {len(connections)} connection(s)")
        
        for connection in connections:
            # Skip sending to the sender if exclude_websocket is provided
            if exclude_websocket and connection == exclude_websocket:
                continue
                
            try:
                await connection.send_json(message)
                print(f"[WS] Message sent successfully to connection in room {room_id}")
            except Exception as e:
                print(f"[WS] Error sending message to connection in room {room_id}: {e}")
                disconnected.append(connection)
        
        # Remove disconnected connections
        if disconnected:
            for conn in disconnected:
                if room_id in self.active_connections and conn in self.active_connections[room_id]:
                    self.active_connections[room_id].remove(conn)
            print(f"[WS] Removed {len(disconnected)} disconnected connection(s) from room {room_id}")

manager = ConnectionManager()

async def websocket_endpoint(websocket: WebSocket, room_id: str):
    """Handle WebSocket connections for real-time collaboration"""
    print(f"[WS] New connection attempt to room: {room_id}")
    
    await manager.connect(websocket, room_id)
    
    # Send current room state to newly connected client
    db = SessionLocal()
    try:
        room = get_room(db, room_id)
        if room:
            init_message = {
                "type": "init",
                "code": room.code_content,
                "language": room.language
            }
            await websocket.send_json(init_message)
            print(f"[WS] Sent init message to room {room_id} with code length: {len(room.code_content)}")
        else:
            # Room doesn't exist yet, send empty state
            await websocket.send_json({
                "type": "init",
                "code": "",
                "language": "python"
            })
            print(f"[WS] Room {room_id} not found in database, sent empty state")
    except Exception as e:
        print(f"[WS] Error loading room state for {room_id}: {e}")
        # Send empty state on error
        try:
            await websocket.send_json({
                "type": "init",
                "code": "",
                "language": "python"
            })
        except:
            pass
    finally:
        db.close()
    
    try:
        while True:
            data = await websocket.receive_text()
            print(f"[WS] Received message from room {room_id}: {data[:100]}...")  # Log first 100 chars
            
            try:
                message = json.loads(data)
            except json.JSONDecodeError as e:
                print(f"[WS] Invalid JSON received in room {room_id}: {e}")
                continue
            
            message_type = message.get("type")
            
            if message_type == "code_update":
                # Update code in database
                code_content = message.get("code", "")
                print(f"[WS] Code update in room {room_id}: {len(code_content)} characters")
                
                db = SessionLocal()
                try:
                    update_room_code(db, room_id, code_content)
                    print(f"[WS] Database updated for room {room_id}")
                except Exception as e:
                    print(f"[WS] Error updating database for room {room_id}: {e}")
                    # Continue anyway - we can still broadcast even if DB update fails
                finally:
                    db.close()
                
                # Broadcast to all OTHER clients in the room (exclude sender)
                broadcast_message = {
                    "type": "code_update",
                    "code": code_content,
                    "cursor_position": message.get("cursor_position"),
                    "sender_id": message.get("sender_id", "unknown")
                }
                await manager.broadcast_to_room(room_id, broadcast_message, exclude_websocket=websocket)
                print(f"[WS] Broadcasted code_update to other clients in room {room_id}")
            
            elif message_type == "cursor_update":
                # Broadcast cursor position (optional, for showing where others are typing)
                broadcast_message = {
                    "type": "cursor_update",
                    "cursor_position": message.get("cursor_position"),
                    "sender_id": message.get("sender_id", "unknown")
                }
                await manager.broadcast_to_room(room_id, broadcast_message, exclude_websocket=websocket)
                print(f"[WS] Broadcasted cursor_update to other clients in room {room_id}")
            
            else:
                print(f"[WS] Unknown message type in room {room_id}: {message_type}")
                
    except WebSocketDisconnect:
        print(f"[WS] WebSocket disconnected for room {room_id}")
        manager.disconnect(websocket, room_id)
        # Notify others that user left (only if there are other users)
        try:
            await manager.broadcast_to_room(room_id, {
                "type": "user_left",
                "message": "A user disconnected"
            })
        except Exception as e:
            print(f"[WS] Error broadcasting user_left message: {e}")
    except Exception as e:
        print(f"[WS] Unexpected error in room {room_id}: {e}")
        import traceback
        traceback.print_exc()
        manager.disconnect(websocket, room_id)

