from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from database import engine, get_db, Base
from models import BookingDB, BookingCreate, BookingUpdate, BookingResponse, BookingStats, PaginatedBookings

Base.metadata.create_all(bind=engine)

from seed import seed
seed()

app = FastAPI(
    title="🪐 Space Tours API",
    description="""
## Space booking system — REST API sandbox

Using this API you can:
- **Create** a seat booking on a spacecraft (POST)
- **List** all bookings (GET)
- **Retrieve** a single booking (GET)
- **Update** an existing booking (PUT)
- **Delete** a booking (DELETE)

### Available destinations
`Mercury` | `Venus` | `Mars` | `Jupiter` | `Saturn` | `Uranus` | `Neptune`

### Seat classes
`economy` | `business` | `vip`

### Booking status flow
`pending` → `confirmed` → `cancelled`
    """,
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://stellar-command.onrender.com",
        "https://stellar-command-x.onrender.com",
    ],
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
    summary="List available destinations",
    response_description="Array of planets with their parameters",
)
def list_destinations():
    """
    Returns a list of all planets available for travel.
    Includes distance, flight duration, and price.
    """
    return destinations


# POST /bookings — nová objednávka
@app.post(
    "/bookings",
    response_model=BookingResponse,
    status_code=201,
    tags=["Bookings"],
    summary="Create a new booking",
    response_description="Created booking including the assigned ID",
    responses={
        422: {"description": "Invalid destination or seat class"},
    },
)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    """
    Creates a new seat booking on a spacecraft.

    - **passenger.first_name**: passenger's first name
    - **passenger.last_name**: passenger's last name
    - **destination**: target planet (e.g. Mars)
    - **departure_date**: departure date in YYYY-MM-DD format
    - **seat_class**: seat class (economy / business / vip)

    The booking will automatically have status **pending**.
    """
    valid_destinations = [d["name"] for d in DESTINATIONS]
    if booking.destination not in valid_destinations:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid destination. Available: {valid_destinations}"
        )
    if booking.seat_class not in ["economy", "business", "vip"]:
        raise HTTPException(
            status_code=422,
            detail="Invalid seat class. Available: economy, business, vip"
        )

    db_booking = BookingDB(
        passenger_first_name=booking.passenger.first_name,
        passenger_last_name=booking.passenger.last_name,
        destination=booking.destination,
        departure_date=booking.departure_date,
        seat_class=booking.seat_class,
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


# GET /bookings/stats — štatistiky objednávok
@app.get(
    "/bookings/stats",
    response_model=BookingStats,
    tags=["Bookings"],
    summary="Booking statistics",
    response_description="Booking counts by status",
)
def get_booking_stats(db: Session = Depends(get_db)):
    """Returns the total number of bookings broken down by status."""
    total     = db.query(BookingDB).count()
    pending   = db.query(BookingDB).filter(BookingDB.status == "pending").count()
    confirmed = db.query(BookingDB).filter(BookingDB.status == "confirmed").count()
    cancelled = db.query(BookingDB).filter(BookingDB.status == "cancelled").count()
    return BookingStats(total=total, pending=pending, confirmed=confirmed, cancelled=cancelled)


# GET /bookings — stránkovaný zoznam objednávok
@app.get(
    "/bookings",
    response_model=PaginatedBookings,
    tags=["Bookings"],
    summary="List bookings",
    response_description="Paginated list of bookings",
)
def list_bookings(
    destination: Optional[str] = Query(None, description="Filter by planet, e.g. Mars"),
    status:      Optional[str] = Query(None, description="Filter by status: pending, confirmed, cancelled"),
    seat_class:  Optional[str] = Query(None, description="Filter by seat class: economy, business, vip"),
    page:        int           = Query(1,    ge=1, description="Page number"),
    limit:       int           = Query(10,   ge=1, le=100, description="Items per page"),
    sort_by:     Optional[str] = Query("id", description="Sort by: id, passenger_first_name, passenger_last_name, destination, departure_date, seat_class, status, created_at"),
    sort_dir:    Optional[str] = Query("asc", description="Sort direction: asc, desc"),
    db: Session = Depends(get_db),
):
    """
    Returns a paginated list of bookings. Optional filters:

    - **destination**: show only bookings for a specific planet
    - **status**: show only bookings with the given status
    - **seat_class**: show only bookings in the given seat class
    - **page**: page number (default: 1)
    - **limit**: items per page (default: 10, max: 100)
    - **sort_by**: sort column (default: id)
    - **sort_dir**: sort direction asc/desc (default: asc)
    """
    SORTABLE = {"id", "passenger_first_name", "passenger_last_name", "destination", "departure_date", "seat_class", "status", "created_at"}
    sort_column = getattr(BookingDB, sort_by if sort_by in SORTABLE else "id")

    query = db.query(BookingDB)
    if destination:
        query = query.filter(BookingDB.destination == destination)
    if status:
        query = query.filter(BookingDB.status == status)
    if seat_class:
        query = query.filter(BookingDB.seat_class == seat_class)

    query = query.order_by(sort_column.desc() if sort_dir == "desc" else sort_column.asc())

    total = query.count()
    pages = max(1, -(-total // limit))
    items = query.offset((page - 1) * limit).limit(limit).all()

    return PaginatedBookings(items=items, total=total, page=page, pages=pages)


# GET /bookings/{id} — detail jednej objednávky
@app.get(
    "/bookings/{booking_id}",
    response_model=BookingResponse,
    tags=["Bookings"],
    summary="Get booking by ID",
    response_description="A single booking by ID",
    responses={
        404: {"description": "Booking not found"},
    },
)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    """
    Returns the details of a specific booking by its **ID**.

    If the booking does not exist, returns **404 Not Found**.
    """
    booking = db.query(BookingDB).filter(BookingDB.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail=f"Booking with ID {booking_id} not found")
    return booking


# Povolené prechody medzi stavmi objednávky
VALID_STATUS_TRANSITIONS = {
    "pending":   ["confirmed", "cancelled"],
    "confirmed": ["cancelled"],
    "cancelled": [],  # finálny stav — žiadne ďalšie prechody
}


# PUT /bookings/{id} — úprava objednávky
@app.put(
    "/bookings/{booking_id}",
    response_model=BookingResponse,
    tags=["Bookings"],
    summary="Update a booking",
    response_description="Updated booking",
    responses={
        404: {"description": "Booking not found"},
        422: {"description": "Invalid status transition"},
    },
)
def update_booking(booking_id: int, updates: BookingUpdate, db: Session = Depends(get_db)):
    """
    Updates an existing booking. Any field can be changed.

    ### Allowed status transitions:
    - `pending` → `confirmed`
    - `pending` → `cancelled`
    - `confirmed` → `cancelled`
    - `cancelled` → *(no further transitions allowed)*

    Usage examples:
    - Confirm a booking: `{"status": "confirmed"}`
    - Cancel a booking: `{"status": "cancelled"}`
    - Change destination: `{"destination": "Saturn"}`
    """
    booking = db.query(BookingDB).filter(BookingDB.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail=f"Booking with ID {booking_id} not found")

    update_data = updates.model_dump(exclude_unset=True)  # len polia ktoré prišli v requeste

    # Rozlož nested passenger objekt na flat DB stĺpce
    if "passenger" in update_data:
        passenger = update_data.pop("passenger")
        update_data["passenger_first_name"] = passenger["first_name"]
        update_data["passenger_last_name"]  = passenger["last_name"]

    # Validácia prechodu stavu
    if "status" in update_data:
        new_status = update_data["status"]
        current_status = booking.status
        allowed = VALID_STATUS_TRANSITIONS.get(current_status, [])
        if new_status not in allowed:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid status transition: '{current_status}' → '{new_status}'. "
                       f"Allowed transitions from '{current_status}': {allowed if allowed else 'none'}"
            )

    for field, value in update_data.items():
        setattr(booking, field, value)

    db.commit()
    db.refresh(booking)
    return booking


# DELETE /bookings/{id} — zmazanie objednávky
@app.delete(
    "/bookings/{booking_id}",
    status_code=200,
    tags=["Bookings"],
    summary="Delete a booking",
    response_description="Deletion confirmation",
    responses={
        404: {"description": "Booking not found"},
        422: {"description": "Booking is not in cancelled status"},
    },
)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    """
    Permanently deletes a booking from the database.

    Condition: the booking must have status **cancelled**.
    If the booking does not exist, returns **404 Not Found**.
    If the booking is not cancelled, returns **422 Unprocessable Entity**.
    """
    booking = db.query(BookingDB).filter(BookingDB.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail=f"Booking with ID {booking_id} not found")

    if booking.status != "cancelled":
        raise HTTPException(
            status_code=422,
            detail=f"Booking can only be deleted when status is 'cancelled'. "
                   f"Current status: '{booking.status}'"
        )

    db.delete(booking)
    db.commit()
    return {"message": f"Booking {booking_id} has been successfully deleted", "deleted_id": booking_id}


# GET / — health check
@app.get("/", tags=["Health"], summary="Health check")
def root():
    return {
        "status": "online",
        "message": "🪐 Space Tours API is running. Go to /docs for Swagger documentation.",
        "docs": "/docs",
        "version": "1.0.0"
    }


# Oprava - destinations premenná musí byť definovaná
destinations = DESTINATIONS
