from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base
from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
from datetime import datetime


# ── Databázová tabuľka ────────────────────────────────────────────────────────

class BookingDB(Base):
    __tablename__ = "bookings"

    id                   = Column(Integer, primary_key=True, index=True)
    passenger_first_name = Column(String, nullable=False)
    passenger_last_name  = Column(String, nullable=False)
    destination          = Column(String, nullable=False)
    departure_date       = Column(String, nullable=False)
    seat_class           = Column(String, default="economy")   # economy | business | vip
    status               = Column(String, default="pending")   # pending | confirmed | cancelled
    created_at           = Column(DateTime(timezone=True), server_default=func.now())


# ── Pydantic schémy (validácia requestov a formát response) ───────────────────

class Passenger(BaseModel):
    first_name: str = Field(..., example="Jozef")
    last_name:  str = Field(..., example="Novák")


class BookingCreate(BaseModel):
    """Čo musí obsahovať POST request body"""
    passenger:      Passenger = Field(...)
    destination:    str       = Field(..., example="Mars")
    departure_date: str       = Field(..., example="2026-07-20")
    seat_class:     str       = Field("economy", example="business")

    class Config:
        json_schema_extra = {
            "example": {
                "passenger": {"first_name": "Jozef", "last_name": "Novák"},
                "destination": "Mars",
                "departure_date": "2026-07-20",
                "seat_class": "economy"
            }
        }


class BookingUpdate(BaseModel):
    """Čo možno zmeniť cez PUT request — všetky polia sú voliteľné"""
    passenger:      Optional[Passenger] = None
    destination:    Optional[str]       = None
    departure_date: Optional[str]       = None
    seat_class:     Optional[str]       = None
    status:         Optional[str]       = None


class BookingStats(BaseModel):
    """Štatistiky objednávok podľa stavu"""
    total:     int
    pending:   int
    confirmed: int
    cancelled: int


class PaginatedBookings(BaseModel):
    """Stránkovaný zoznam objednávok"""
    items: List['BookingResponse']
    total: int
    page:  int
    pages: int


class BookingResponse(BaseModel):
    """Čo vráti API v response"""
    id:             int
    passenger:      Passenger
    destination:    str
    departure_date: str
    seat_class:     str
    status:         str
    created_at:     datetime

    @model_validator(mode='before')
    @classmethod
    def build_passenger(cls, data):
        if hasattr(data, 'passenger_first_name'):
            return {
                'id':             data.id,
                'passenger':      {'first_name': data.passenger_first_name, 'last_name': data.passenger_last_name},
                'destination':    data.destination,
                'departure_date': data.departure_date,
                'seat_class':     data.seat_class,
                'status':         data.status,
                'created_at':     data.created_at,
            }
        return data

    class Config:
        from_attributes = True
