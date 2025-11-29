from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import RoomCreate, RoomResponse
from services.room_service import create_room, get_room

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.post("", response_model=RoomResponse)
def create_new_room(room_data: RoomCreate, db: Session = Depends(get_db)):
    """Create a new collaboration room"""
    try:
        result = create_room(db, room_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create room: {str(e)}")

@router.get("/{room_id}")
def get_room_info(room_id: str, db: Session = Depends(get_db)):
    """Get room information"""
    room = get_room(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {
        "room_id": room.room_id,
        "code_content": room.code_content,
        "language": room.language
    }


