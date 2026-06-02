from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ── Databázová tabuľka ────────────────────────────────────────────────────────
# Toto je mapa toho, ako vyzerá záznam v SQLite databáze

class BookingDB(Base):
    __tablename__ = "bookings"

    id              = Column(Integer, primary_key=True, index=True)
    passenger_name  = Column(String, nullable=False)
    destination     = Column(String, nullable=False)
    departure_date  = Column(String, nullable=False)
    seat_class      = Column(String, default="economy")   # economy | business | vip
    status          = Column(String, default="pending")   # pending | confirmed | cancelled
    created_at      = Column(DateTime(timezone=True), server_default=func.now())


# ── Pydantic schémy (validácia requestov a formát response) ───────────────────
# FastAPI tieto schémy automaticky zobrazí v Swagger dokumentácii

class BookingCreate(BaseModel):
    """Čo musí obsahovať POST request body"""
    passenger_name: str  = Field(..., example="Jozef Novák")
    destination:    str  = Field(..., example="Mars")
    departure_date: str  = Field(..., example="2026-07-20")
    seat_class:     str  = Field("economy", example="business")

    class Config:
        json_schema_extra = {
            "example": {
                "passenger_name": "Jozef Novák",
                "destination": "Mars",
                "departure_date": "2026-07-20",
                "seat_class": "economy"
            }
        }


class BookingUpdate(BaseModel):
    """Čo možno zmeniť cez PUT request — všetky polia sú voliteľné"""
    passenger_name: Optional[str] = None
    destination:    Optional[str] = None
    departure_date: Optional[str] = None
    seat_class:     Optional[str] = None
    status:         Optional[str] = None


class BookingResponse(BaseModel):
    """Čo vráti API v response"""
    id:             int
    passenger_name: str
    destination:    str
    departure_date: str
    seat_class:     str
    status:         str
    created_at:     datetime

    class Config:
        from_attributes = True  # povolí konverziu SQLAlchemy objektu na JSON
