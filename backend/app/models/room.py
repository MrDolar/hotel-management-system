from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from app.core.database import Base

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(20), unique=True, nullable=False)
    room_type = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    capacity = Column(Integer, default=2)
    floor = Column(Integer, default=1)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, nullable=False)
    guest_name = Column(String(100), nullable=False)
    guest_phone = Column(String(20), default="")
    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=False)
    total_price = Column(Float, default=0)
    status = Column(String(20), default="confirmed")
    created_at = Column(DateTime, default=datetime.utcnow)
