# 🪐 Space Tours API — REST API Sandbox

A simple REST API sandbox for practising HTTP methods.  
Theme: a booking system for space travel to planets of the Solar System.

---

## ⚡ Quick start

```bash
# 1. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 2. Install dependencies (first time only)
pip install -r requirements.txt

# 3. Start the server
uvicorn main:app --reload
```

Server running at: **http://localhost:8000**  
Swagger documentation: **http://localhost:8000/docs**

---

## 📋 Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | Health check |
| GET | `/destinations` | List of planets |
| POST | `/bookings` | Create a new booking |
| GET | `/bookings` | All bookings |
| GET | `/bookings/stats` | Statistics |
| GET | `/bookings/{id}` | Booking detail |
| PUT | `/bookings/{id}` | Update a booking |
| DELETE | `/bookings/{id}` | Delete a booking |

---

## 🧪 Request examples

### POST — Create a booking
```
POST http://localhost:8000/bookings
Content-Type: application/json

{
  "passenger": {
    "first_name": "Jane",
    "last_name": "Doe"
  },
  "destination": "Mars",
  "departure_date": "2026-07-20",
  "seat_class": "economy"
}
```

### GET — All bookings to Mars
```
GET http://localhost:8000/bookings?destination=Mars
```

### PUT — Confirm a booking
```
PUT http://localhost:8000/bookings/1
Content-Type: application/json

{
  "status": "confirmed"
}
```

### DELETE — Delete a booking
```
DELETE http://localhost:8000/bookings/1
```

---

## 🪐 Available destinations
Mercury | Venus | Mars | Jupiter | Saturn | Uranus | Neptune

## 💺 Seat classes
economy | business | vip

## 📊 Booking status flow
pending → confirmed → cancelled
