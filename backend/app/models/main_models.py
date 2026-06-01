"""Models"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from app.core.database import Base
from app.models.user import User

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    room_no = Column(String(20), unique=True, nullable=False)
    room_type = Column(String(50))
    floor = Column(Integer)
    price = Column(Integer)
    status = Column(String(20), default="available")
    description = Column(Text, default="")

class Guest(Base):
    __tablename__ = "guests"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    id_card = Column(String(20))
    phone = Column(String(20))
    email = Column(String(100))
    vip_level = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    guest_id = Column(Integer, ForeignKey("guests.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    check_in = Column(DateTime)
    check_out = Column(DateTime)
    status = Column(String(20), default="reserved")
    total_price = Column(Integer)
    remark = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
