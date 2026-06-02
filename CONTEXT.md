# 🪐 Space Tours API — Project Context

Tento súbor slúži ako rýchly onboarding dokument pre nové konverzácie, spolupracovníkov, alebo študentov.

---

## Čo je tento projekt

Výukový REST API sandbox na výuku základov práce s HTTP metódami pre QA začiatočníkov.
Téma: objednávkový systém zájazdov na planéty slnečnej sústavy.

**Publikum:** QA začiatočníci bez programátorskej skúsenosti  
**Vyučujúca:** Senior QA s presahom do developmentu

---

## Živé URL

| Služba | URL |
|--------|-----|
| API (Swagger UI) | https://space-tours-api.onrender.com/docs |
| API (base URL) | https://space-tours-api.onrender.com |
| Frontend (backoffice) | https://stellar-command.onrender.com |
| GitHub | https://github.com/kat-bal/space-tours-api |
| Databáza (Neon) | https://console.neon.tech |

> ⚠️ Render free tier uspí server po 15 minútach nečinnosti. Prvý request po spánku trvá 30-60 sekúnd.

---

## Stack

| Vrstva | Technológia |
|--------|-------------|
| Backend | Python 3.12 + FastAPI |
| Databáza | PostgreSQL 16 cez Neon.tech (lokálne: SQLite fallback) |
| ORM | SQLAlchemy |
| Frontend | Vanilla HTML/CSS/JS |
| Hosting | Render.com (free tier) |
| Verziovanie | GitHub |

---

## Štruktúra projektu

```
space-tours-api/
├── main.py           # FastAPI aplikácia, všetky endpointy
├── database.py       # Pripojenie k DB (Neon/PostgreSQL v produkcii, SQLite lokálne)
├── models.py         # Databázové modely + Pydantic schémy
├── seed.py           # Seed skript — naplní DB testovacími dátami
├── requirements.txt  # Python závislosti
├── .env              # Lokálne env premenné — nie je v gite!
├── frontend/
│   └── index.html    # Stellar Command backoffice UI
├── BACKLOG.md        # Backlog projektu
├── CONTEXT.md        # Tento súbor
└── README.md         # Inštrukcie pre spustenie
```

---

## Endpointy

| Metóda | Endpoint | Popis |
|--------|----------|-------|
| GET | `/` | Health check |
| GET | `/destinations` | Zoznam planét |
| POST | `/bookings` | Nová objednávka |
| GET | `/bookings` | Všetky objednávky (+ filtre) |
| GET | `/bookings/{id}` | Detail objednávky |
| PUT | `/bookings/{id}` | Úprava objednávky |
| DELETE | `/bookings/{id}` | Zmazanie objednávky |

### Query parametre pre GET /bookings
- `destination` — napr. `?destination=Mars`
- `status` — napr. `?status=pending`
- Kombinovateľné: `?destination=Mars&status=confirmed`

---

## Dátový model — Booking

| Pole | Typ | Povinné | Default | Možné hodnoty |
|------|-----|---------|---------|---------------|
| `passenger_name` | string | áno | — | ľubovoľný text |
| `destination` | string | áno | — | Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune |
| `departure_date` | string | áno | — | YYYY-MM-DD |
| `seat_class` | string | nie | economy | economy, business, vip |
| `status` | string | nie | pending | pending, confirmed, cancelled |

---

## Lokálne spustenie

```bash
# 1. Aktivuj venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

# 2. Nainštaluj závislosti (len prvýkrát)
pip install -r requirements.txt

# 3. Vytvor .env súbor s connection stringom (len prvýkrát)
# DATABASE_URL=postgresql://...  ← z Neon dashboardu
# Bez .env súboru sa použije SQLite ako fallback

# 4. Spusti server
uvicorn main:app --reload

# 5. Voliteľne — naplň DB testovacími dátami
python3 seed.py
```

Server beží na: http://localhost:8000  
Swagger: http://localhost:8000/docs

---

## Databáza

- **Produkcia:** PostgreSQL 16 na [Neon.tech](https://console.neon.tech) — permanent free tier, 0.5 GB
- **Lokálne:** SQLite fallback (ak nie je nastavená `DATABASE_URL` v `.env`)
- **Seed:** 10 testovacích objednávok, spustí sa automaticky pri štarte ak je DB prázdna
- **Štruktúra:** jedna tabuľka `bookings` — definovaná v `models.py` (trieda `BookingDB`)
- **SQL Editor:** dostupný priamo v Neon dashboarde

---

## Nástroje

- **Swagger UI** — interaktívna dokumentácia, ideálna pre začiatočníkov
- **Postman** — kolekcia uložená lokálne (TODO: exportovať do repozitára)
- **Neon SQL Editor** — priamy prístup do databázy cez browser

---

## Known bugs / validácie (zámerné, pre výuku)

Toto sú známe nedostatky ktoré slúžia ako cvičné nálezy pre junior testerky:

- `departure_date` — možno zadať dátum v minulosti
- `passenger_name` — žiadna minimálna ani maximálna dĺžka
- `departure_date` — akceptuje ľubovoľný string (napr. "banán")
- Prázdny request body nevráti zmysluplnú chybu
- Neznáme polia v request body sa ticho ignorujú
- `status` cez PUT — možno nastaviť neplatnú hodnotu

---

## Ďalšie plány

Pozri `BACKLOG.md` pre úplný zoznam. Hlavné priority:
1. Validácie (oprava known bugs)
2. Jazykové verzie (SK/EN)
3. Frontend pre klientov (oddelený od backoffice)
