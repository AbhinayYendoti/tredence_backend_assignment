import uuid
from sqlalchemy.orm import Session
from models import Room
from schemas import RoomCreate, RoomResponse

def create_room(db: Session, room_data: RoomCreate) -> RoomResponse:
    """Create a new room with unique ID"""
    room_id = str(uuid.uuid4())[:8]  # Short ID for easier sharing
    
    new_room = Room(
        room_id=room_id,
        code_content="",
        language=room_data.language
    )
    
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    
    return RoomResponse(room_id=room_id)

def get_room(db: Session, room_id: str) -> Room:
    """Get room by ID"""
    return db.query(Room).filter(Room.room_id == room_id).first()

def update_room_code(db: Session, room_id: str, code: str):
    """Update the code content for a room"""
    room = db.query(Room).filter(Room.room_id == room_id).first()
    if room:
        room.code_content = code
        db.commit()
        db.refresh(room)
    return room


