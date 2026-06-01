from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.core.deps import get_admin_user
from app.models.room import Room

router = APIRouter(prefix="/api/rooms", tags=["Rooms"])

class RoomCreate(BaseModel):
    room_number: str
    room_type: str
    price: float
    capacity: int = 2
    floor: int = 1

@router.get("")
async def list_rooms(room_type: Optional[str] = None, available: Optional[bool] = None, db: Session = Depends(get_db)):
    q = db.query(Room)
    if room_type: q = q.filter(Room.room_type == room_type)
    if available is not None: q = q.filter(Room.is_available == available)
    return {"items": [{"id": r.id, "room_number": r.room_number, "room_type": r.room_type, "price": r.price, "capacity": r.capacity, "is_available": r.is_available} for r in q.all()]}

@router.post("")
async def create_room(req: RoomCreate, db: Session = Depends(get_db), admin = Depends(get_admin_user)):
    r = Room(**req.dict()); db.add(r); db.commit(); db.refresh(r)
    return {"id": r.id, "room_number": r.room_number}

@router.get("/{rid}")
async def get_room(rid: int, db: Session = Depends(get_db)):
    r = db.query(Room).filter(Room.id == rid).first()
    if not r: raise HTTPException(404, "Not found")
    return {"id": r.id, "room_number": r.room_number, "room_type": r.room_type, "price": r.price, "is_available": r.is_available}

@router.delete("/{rid}")
async def delete_room(rid: int, db: Session = Depends(get_db), admin = Depends(get_admin_user)):
    r = db.query(Room).filter(Room.id == rid).first()
    if not r: raise HTTPException(404, "Not found")
    db.delete(r); db.commit()
    return {"message": "Deleted"}
