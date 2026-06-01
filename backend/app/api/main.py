"""API Routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user, get_admin_user
from app.models.main_models import *

router = APIRouter(prefix="/api", tags=["Main"])

@router.get("/rooms")
async def list_rooms(status: str = None, room_type: str = None, db = Depends(get_db)):
    query = db.query(Room)
    if status: query = query.filter(Room.status == status)
    if room_type: query = query.filter(Room.room_type == room_type)
    return query.all()

@router.post("/rooms", status_code=201)
async def create_room(room_no: str, room_type: str, price: int, db = Depends(get_db)):
    r = Room(room_no=room_no, room_type=room_type, price=price)
    db.add(r); db.commit(); db.refresh(r)
    return r

@router.post("/reservations", status_code=201)
async def create_reservation(guest_id: int, room_id: int, check_in: str, check_out: str, db = Depends(get_db)):
    r = Reservation(guest_id=guest_id, room_id=room_id, check_in=check_in, check_out=check_out)
    db.add(r); db.commit(); db.refresh(r)
    return r

@router.post("/checkin/{id}")
async def checkin(id: int, db = Depends(get_db)):
    r = db.query(Reservation).filter(Reservation.id == id).first()
    if not r: raise HTTPException(404)
    room = db.query(Room).filter(Room.id == r.room_id).first()
    room.status = "occupied"; r.status = "checked_in"
    db.commit()
    return {"message": "checked in"}

@router.post("/checkout/{id}")
async def checkout(id: int, db = Depends(get_db)):
    r = db.query(Reservation).filter(Reservation.id == id).first()
    if not r: raise HTTPException(404)
    room = db.query(Room).filter(Room.id == r.room_id).first()
    room.status = "cleaning"; r.status = "completed"
    db.commit()
    return {"message": "checked out", "total": r.total_price}
