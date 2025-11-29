from pydantic import BaseModel
from typing import Optional

class RoomCreate(BaseModel):
    language: Optional[str] = "python"

class RoomResponse(BaseModel):
    room_id: str
    
    class Config:
        from_attributes = True

class AutocompleteRequest(BaseModel):
    code: str
    cursorPosition: int
    language: str = "python"

class AutocompleteResponse(BaseModel):
    suggestion: str
    start_position: int
    end_position: int


