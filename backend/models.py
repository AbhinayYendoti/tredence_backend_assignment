from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class Room(Base):
    __tablename__ = "rooms"
    
    room_id = Column(String, primary_key=True, index=True)
    code_content = Column(Text, default="")
    language = Column(String, default="python")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


