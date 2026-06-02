"""
Seed skript — naplní databázu testovacími dátami.
Spusti ručne: python seed.py
Alebo sa volá automaticky pri štarte servera ak je DB prázdna.
"""

from database import engine, SessionLocal, Base
from models import BookingDB
from datetime import date

Base.metadata.create_all(bind=engine)

SEED_BOOKINGS = [
    {"passenger_name": "Aeon Stargazer",   "destination": "Mars",    "departure_date": "2026-07-20", "seat_class": "economy",  "status": "confirmed"},
    {"passenger_name": "Celeste Quasary",  "destination": "Venus",   "departure_date": "2026-08-01", "seat_class": "vip",      "status": "pending"},
    {"passenger_name": "Orion Blackwell",  "destination": "Jupiter", "departure_date": "2027-01-13", "seat_class": "business", "status": "pending"},
    {"passenger_name": "Luna Vega",        "destination": "Saturn",  "departure_date": "2027-03-15", "seat_class": "vip",      "status": "confirmed"},
    {"passenger_name": "Rex Cosmov",       "destination": "Mercury", "departure_date": "2026-09-05", "seat_class": "economy",  "status": "cancelled"},
    {"passenger_name": "Nova Threlfall",   "destination": "Neptune", "departure_date": "2028-06-30", "seat_class": "vip",      "status": "pending"},
    {"passenger_name": "Cassidy Varn",     "destination": "Uranus",  "departure_date": "2027-11-20", "seat_class": "business", "status": "pending"},
    {"passenger_name": "Sirius Holt",      "destination": "Mars",    "departure_date": "2026-07-20", "seat_class": "business", "status": "confirmed"},
    {"passenger_name": "Lyra Mendoza",     "destination": "Venus",   "departure_date": "2026-10-10", "seat_class": "economy",  "status": "pending"},
    {"passenger_name": "Atlas Brennan",    "destination": "Jupiter", "departure_date": "2027-05-01", "seat_class": "vip",      "status": "cancelled"},
]


def seed():
    db = SessionLocal()
    try:
        existing = db.query(BookingDB).count()
        if existing > 0:
            print(f"✋ Databáza už obsahuje {existing} záznamov — seed preskočený.")
            return

        for data in SEED_BOOKINGS:
            db.add(BookingDB(**data))
        db.commit()
        print(f"✅ Seed hotový — pridaných {len(SEED_BOOKINGS)} objednávok.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
