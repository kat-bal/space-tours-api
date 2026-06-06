# 🪐 Space Tours API — Výukový REST API Sandbox

Jednoduchý REST API sandbox na výuku základov práce s HTTP metódami.  
Téma: objednávkový systém zájazdov na planéty slnečnej sústavy.

---

## ⚡ Rýchly štart

```bash
# 1. Aktivuj virtuálne prostredie
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 2. Nainštaluj závislosti (len prvýkrát)
pip install -r requirements.txt

# 3. Spusti server
uvicorn main:app --reload
```

Server beží na: **http://localhost:8000**  
Swagger dokumentácia: **http://localhost:8000/docs**

---

## 📋 Endpointy

| Metóda | URL | Popis |
|--------|-----|-------|
| GET | `/` | Health check |
| GET | `/destinations` | Zoznam planét |
| POST | `/bookings` | Nová objednávka |
| GET | `/bookings` | Všetky objednávky |
| GET | `/bookings/stats` | Štatistiky (total, pending, confirmed, cancelled) |
| GET | `/bookings/{id}` | Detail objednávky |
| PUT | `/bookings/{id}` | Uprav objednávku |
| DELETE | `/bookings/{id}` | Zmaž objednávku |

---

## 🧪 Príklady requestov

### POST — Nová objednávka
```
POST http://localhost:8000/bookings
Content-Type: application/json

{
  "passenger_name": "Jozef Novák",
  "destination": "Mars",
  "departure_date": "2026-07-20",
  "seat_class": "economy"
}
```

### GET — Všetky objednávky na Mars
```
GET http://localhost:8000/bookings?destination=Mars
```

### PUT — Potvrď objednávku
```
PUT http://localhost:8000/bookings/1
Content-Type: application/json

{
  "status": "confirmed"
}
```

### DELETE — Zmaž objednávku
```
DELETE http://localhost:8000/bookings/1
```

---

## 🪐 Dostupné destinácie
Mercury | Venus | Mars | Jupiter | Saturn | Uranus | Neptune

## 💺 Triedy sedenia
economy | business | vip

## 📊 Stavy objednávky
pending → confirmed → cancelled
