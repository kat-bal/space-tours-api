# 🪐 Space Tours API — Backlog

## 🔴 In Progress
_(nič momentálne)_

## 🟡 Up Next — Validácie (známe bugy, ideálne pre junior testerky)
- [ ] `departure_date` — nemožno zadať dátum v minulosti
- [ ] `passenger_name` — minimálna dĺžka mena (napr. aspoň 2 znaky)
- [ ] `passenger_name` — maximálna dĺžka mena
- [ ] `departure_date` — validácia formátu (teraz prijme akýkoľvek string)
- [ ] Čo sa stane ak pošleš prázdny request body?
- [ ] Čo sa stane ak pošleš neznáme pole (napr. "colour": "red")?
- [ ] PUT — čo ak pošleš neplatný status (napr. "status": "flying")?

## 🟡 Up Next — Funkcionality
- [ ] Úprava objednávky cez FE — editovací formulár (PUT), zmena poľa priamo z tabuľky
- [ ] Jazykové verzie (SK/EN) — Swagger dokumentácia aj Frontend
- [ ] Negative testing scenáre (dokumentácia)

## 🟢 Nápady / Future
- [ ] Rozdeliť `passenger_name` na tri samostatné polia: `first_name`, `middle_name` (voliteľné), `last_name` — úprava DB modelu, API aj FE


- [ ] Autentifikácia (API key alebo JWT token)
- [ ] Pagination (GET /bookings?page=1&limit=10)
- [ ] Sorting (GET /bookings?sort=departure_date)
- [ ] Postman environment variables ({{base_url}}, {{booking_id}})
- [ ] Exportovať Postman kolekciu do repozitára
- [ ] Frontend pre klientov (oddelený od backoffice)

## ✅ Hotovo
- [x] FastAPI projekt — lokálne
- [x] SQLite databáza
- [x] CRUD endpointy (POST, GET, GET by ID, PUT, DELETE)
- [x] Filtrovanie (destination, status)
- [x] Swagger UI dokumentácia
- [x] Postman kolekcia
- [x] GitHub repozitár
- [x] Render.com nasadenie (API)
- [x] CORS middleware
- [x] Frontend — Stellar Command backoffice
- [x] Render.com nasadenie (Frontend)
- [x] Seed data skript (automatické naplnenie DB testovacími dátami)
- [x] PostgreSQL — migrácia na Neon.tech (permanent free tier)
- [x] Vesmírne pozadie na frontende (canvas hviezdy + shooting stars)
