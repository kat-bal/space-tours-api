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
    {"passenger_first_name": "Aeon",    "passenger_last_name": "Stargazer", "destination": "Mars",    "departure_date": "2026-07-20", "seat_class": "economy",  "status": "confirmed"},
    {"passenger_first_name": "Celeste", "passenger_last_name": "Quasary",   "destination": "Venus",   "departure_date": "2026-08-01", "seat_class": "vip",      "status": "pending"},
    {"passenger_first_name": "Orion",   "passenger_last_name": "Blackwell", "destination": "Jupiter", "departure_date": "2027-01-13", "seat_class": "business", "status": "pending"},
    {"passenger_first_name": "Luna",    "passenger_last_name": "Vega",      "destination": "Saturn",  "departure_date": "2027-03-15", "seat_class": "vip",      "status": "confirmed"},
    {"passenger_first_name": "Rex",     "passenger_last_name": "Cosmov",    "destination": "Mercury", "departure_date": "2026-09-05", "seat_class": "economy",  "status": "cancelled"},
    {"passenger_first_name": "Nova",    "passenger_last_name": "Threlfall", "destination": "Neptune", "departure_date": "2028-06-30", "seat_class": "vip",      "status": "pending"},
    {"passenger_first_name": "Cassidy", "passenger_last_name": "Varn",      "destination": "Uranus",  "departure_date": "2027-11-20", "seat_class": "business", "status": "pending"},
    {"passenger_first_name": "Sirius",  "passenger_last_name": "Holt",      "destination": "Mars",    "departure_date": "2026-07-20", "seat_class": "business", "status": "confirmed"},
    {"passenger_first_name": "Lyra",    "passenger_last_name": "Mendoza",   "destination": "Venus",   "departure_date": "2026-10-10", "seat_class": "economy",  "status": "pending"},
    {"passenger_first_name": "Atlas",   "passenger_last_name": "Brennan",   "destination": "Jupiter", "departure_date": "2027-05-01", "seat_class": "vip",      "status": "cancelled"},
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
