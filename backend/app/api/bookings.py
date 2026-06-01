from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from app.core.database import get_db
from app.models.room import Booking, Room

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])

class BookingCreate(BaseModel):
    room_id: int
    guest_name: str
    guest_phone: str = ""
    check_in: datetime
    check_out: datetime

@router.get("")
async def list_bookings(status: str = None, db: Session = Depends(get_db)):
    q = db.query(Booking)
    if status: q = q.filter(Booking.status == status)
    return {"items": [{"id": b.id, "room_id": b.room_id, "guest_name": b.guest_name, "check_in": str(b.check_in), "check_out": str(b.check_out), "total_price": b.total_price, "status": b.status} for b in q.order_by(Booking.created_at.desc()).all()]}

@router.post("")
async def create_booking(req: BookingCreate, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == req.room_id).first()
    if not room: raise HTTPException(404, "Room not found")
    if not room.is_available: raise HTTPException(400, "Room not available")
    days = max(1, (req.check_out - req.check_in).days)
    total = room.price * days
    b = Booking(room_id=req.room_id, guest_name=req.guest_name, guest_phone=req.guest_phone, check_in=req.check_in, check_out=req.check_out, total_price=total, status="confirmed")
    room.is_available = False
    db.add(b); db.commit(); db.refresh(b)
    return {"id": b.id, "total_price": total, "message": "Booking confirmed"}

@router.put("/{bid}/checkin")
async def check_in(bid: int, db: Session = Depends(get_db)):
    b = db.query(Booking).filter(Booking.id == bid).first()
    if not b: raise HTTPException(404, "Not found")
    b.status = "checked_in"; db.commit()
    return {"message": "Checked in"}

@router.put("/{bid}/checkout")
async def check_out(bid: int, db: Session = Depends(get_db)):
    b = db.query(Booking).filter(Booking.id == bid).first()
    if not b: raise HTTPException(404, "Not found")
    b.status = "checked_out"
    room = db.query(Room).filter(Room.id == b.room_id).first()
    if room: room.is_available = True
    db.commit()
    return {"message": "Checked out", "total": b.total_price}
