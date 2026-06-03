from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from database import engine, get_db, Base
from models import BookingDB, BookingCreate, BookingUpdate, BookingResponse

Base.metadata.create_all(bind=engine)

from seed import seed
seed()

app = FastAPI(
    title="🪐 Space Tours API — BUGGY",
    description="""
## Vesmírny objednávkový systém — výukový REST API sandbox

Pomocou tohto API môžeš:
- **Vytvoriť** objednávku miesta na vesmírnej lodi (POST)
- **Zobraziť** zoznam všetkých cestujúcich (GET)
- **Zobraziť** detail jednej objednávky (GET)
- **Zmeniť** existujúcu objednávku (PUT)
- **Zrušiť** objednávku (DELETE)

### Dostupné destinácie
`Mercury` | `Venus` | `Mars` | `Jupiter` | `Saturn` | `Uranus` | `Neptune`

### Triedy sedenia
`economy` | `business` | `vip`

### Stavy objednávky
`pending` → `confirmed` → `cancelled`
    """,
    version="1.0.0-buggy",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Destinácie (statický zoznam, nie DB) ─────────────────────────────────────

DESTINATIONS = [
    {"id": 1, "name": "Mercury", "distance_km": 77_000_000,  "duration_days": 105, "price_usd": 180_000},
    {"id": 2, "name": "Venus",   "distance_km": 38_000_000,  "duration_days": 97,  "price_usd": 210_000},
    {"id": 3, "name": "Mars",    "distance_km": 54_600_000,  "duration_days": 259, "price_usd": 450_000},
    {"id": 4, "name": "Jupiter", "distance_km": 588_000_000, "duration_days": 600, "price_usd": 1_200_000},
    {"id": 5, "name": "Saturn",  "distance_km": 1_200_000_000,"duration_days":1180,"price_usd": 2_800_000},
    {"id": 6, "name": "Uranus",  "distance_km": 2_600_000_000,"duration_days":1700,"price_usd": 4_500_000},
    {"id": 7, "name": "Neptune", "distance_km": 4_400_000_000,"duration_days":2100,"price_usd": 6_000_000},
]


# ── ENDPOINTS ─────────────────────────────────────────────────────────────────


# GET /destinations — zoznam všetkých planét
@app.get(
    "/destinations",
    tags=["Destinations"],
    summary="Zoznam dostupných destinácií",
    response_description="Pole planét s ich parametrami",
)
def list_destinations():
    """
    Vráti zoznam všetkých planét, na ktoré je možné cestovať.
    Obsahuje vzdialenosť, dĺžku letu a cenu.
    """
    return destinations


# POST /bookings — nová objednávka
# 🐛 BUG-01: Vracia status 200 namiesto správneho 201 Created
# 🐛 BUG-02: departure_date akceptuje ľubovoľný string (napr. "banán")
# 🐛 BUG-03: departure_date akceptuje dátumy v minulosti
# 🐛 BUG-04: passenger_name bez min/max dĺžky (prázdny string je OK)
# 🐛 BUG-05: Duplikátné objednávky — rovnaký cestujúci+destinácia+dátum možno vytvoriť opakovane
@app.post(
    "/bookings",
    response_model=BookingResponse,
    status_code=200,  # 🐛 BUG-01: malo by byť 201
    tags=["Bookings"],
    summary="Vytvor novú objednávku",
    response_description="Vytvorená objednávka vrátane prideleného ID",
)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    """
    Vytvorí novú objednávku miesta na vesmírnej lodi.

    - **passenger_name**: meno a priezvisko cestujúceho
    - **destination**: cieľová planéta (napr. Mars)
    - **departure_date**: dátum odletu vo formáte YYYY-MM-DD
    - **seat_class**: trieda sedenia (economy / business / vip)

    Objednávka bude mať automaticky status **pending**.
    """
    # 🐛 BUG-02 + BUG-03: Chýba validácia departure_date (formát aj minulosť)
    # 🐛 BUG-04: Chýba validácia dĺžky passenger_name
    # 🐛 BUG-05: Chýba kontrola duplicít

    valid_destinations = [d["name"] for d in DESTINATIONS]
    if booking.destination not in valid_destinations:
        raise HTTPException(
            status_code=422,
            detail=f"Neplatná destinácia. Dostupné: {valid_destinations}"
        )
    if booking.seat_class not in ["economy", "business", "vip"]:
        raise HTTPException(
            status_code=422,
            detail="Neplatná trieda sedenia. Dostupné: economy, business, vip"
        )

    db_booking = BookingDB(**booking.model_dump())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


# GET /bookings — zoznam všetkých objednávok
# 🐛 BUG-06: Filter ?status= je case-sensitive — "Pending" vráti prázdne pole bez chyby
@app.get(
    "/bookings",
    response_model=List[BookingResponse],
    tags=["Bookings"],
    summary="Zoznam všetkých objednávok",
    response_description="Pole objednávok",
)
def list_bookings(
    destination: Optional[str] = Query(None, description="Filtruj podľa planéty, napr. Mars"),
    status:      Optional[str] = Query(None, description="Filtruj podľa stavu: pending, confirmed, cancelled"),
    db: Session = Depends(get_db),
):
    """
    Vráti všetky objednávky. Voliteľne možno filtrovať pomocou query parametrov:

    - **destination**: zobraz len objednávky na konkrétnu planétu
    - **status**: zobraz len objednávky v danom stave
    """
    query = db.query(BookingDB)
    if destination:
        query = query.filter(BookingDB.destination == destination)
    if status:
        # 🐛 BUG-06: case-sensitive filter — "Pending" != "pending", vráti [] bez chyby
        query = query.filter(BookingDB.status == status)
    return query.all()


# GET /bookings/{id} — detail jednej objednávky
# 🐛 BUG-07: Neexistujúce ID vráti 200 s null hodnotami namiesto 404
@app.get(
    "/bookings/{booking_id}",
    tags=["Bookings"],
    summary="Detail objednávky",
    response_description="Jedna objednávka podľa ID",
)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    """
    Vráti detail konkrétnej objednávky podľa jej **ID**.

    Ak objednávka neexistuje, vráti **404 Not Found**.
    """
    booking = db.query(BookingDB).filter(BookingDB.id == booking_id).first()
    # 🐛 BUG-07: Chýba 404 — funkcia vráti None → FastAPI serializuje ako null
    if not booking:
        return None
    return booking


# Povolené prechody medzi stavmi objednávky
# 🐛 BUG-08: VALID_STATUS_TRANSITIONS sa vôbec nepoužíva — akýkoľvek status prejde
VALID_STATUS_TRANSITIONS = {
    "pending":   ["confirmed", "cancelled"],
    "confirmed": ["cancelled"],
    "cancelled": [],
}


# PUT /bookings/{id} — úprava objednávky
# 🐛 BUG-08: Chýba validácia prechodu stavu (napr. "flying" je platný status)
# 🐛 BUG-09: Cancelled objednávku možno znovu otvoriť späť na "pending"
@app.put(
    "/bookings/{booking_id}",
    response_model=BookingResponse,
    tags=["Bookings"],
    summary="Uprav objednávku",
    response_description="Aktualizovaná objednávka",
)
def update_booking(booking_id: int, updates: BookingUpdate, db: Session = Depends(get_db)):
    """
    Aktualizuje existujúcu objednávku. Môžeš zmeniť ľubovoľné pole.

    Príklady použitia:
    - Potvrdenie objednávky: `{"status": "confirmed"}`
    - Zrušenie objednávky: `{"status": "cancelled"}`
    - Zmena destinácie: `{"destination": "Saturn"}`
    """
    booking = db.query(BookingDB).filter(BookingDB.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail=f"Objednávka s ID {booking_id} neexistuje")

    update_data = updates.model_dump(exclude_unset=True)

    # 🐛 BUG-08: Validácia stavu úplne chýba — akýkoľvek string prejde
    # 🐛 BUG-09: Cancelled → pending prechod nie je blokovaný

    for field, value in update_data.items():
        setattr(booking, field, value)

    db.commit()
    db.refresh(booking)
    return booking


# DELETE /bookings/{id} — zmazanie objednávky
# 🐛 BUG-10: Maže akúkoľvek objednávku bez ohľadu na stav (aj confirmed!)
@app.delete(
    "/bookings/{booking_id}",
    status_code=200,
    tags=["Bookings"],
    summary="Zmaž objednávku",
    response_description="Potvrdenie zmazania",
)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    """
    Natrvalo vymaže objednávku z databázy.

    Ak objednávka neexistuje, vráti **404 Not Found**.
    """
    booking = db.query(BookingDB).filter(BookingDB.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail=f"Objednávka s ID {booking_id} neexistuje")

    # 🐛 BUG-10: Chýba kontrola stavu — maže aj pending a confirmed objednávky!

    db.delete(booking)
    db.commit()
    return {"message": f"Objednávka {booking_id} bola úspešne zmazaná", "deleted_id": booking_id}


# GET / — health check
@app.get("/", tags=["Health"], summary="Health check")
def root():
    return {
        "status": "online",
        "message": "🪐 Space Tours API beží. Choď na /docs pre Swagger dokumentáciu.",
        "docs": "/docs",
        "version": "1.0.0-buggy"
    }


destinations = DESTINATIONS
