# 🪐 Space Tours API — Backlog

## 🔴 In Progress
- [ ] Seed data skript (automatické naplnenie DB testovacími dátami)

## 🟡 Up Next — Validácie (známe bugy, ideálne pre junior testerky)
- [ ] `departure_date` — nemožno zadať dátum v minulosti
- [ ] `passenger_name` — minimálna dĺžka mena (napr. aspoň 2 znaky)
- [ ] `passenger_name` — maximálna dĺžka mena
- [ ] `departure_date` — validácia formátu (teraz prijme akýkoľvek string)
- [ ] Čo sa stane ak pošleš prázdny request body?
- [ ] Čo sa stane ak pošleš neznáme pole (napr. "colour": "red")?
- [ ] PUT — čo ak pošleš neplatný status (napr. "status": "flying")?

## 🟡 Up Next — Funkcionality
- [ ] Jazykové verzie (SK/EN) — Swagger dokumentácia aj Frontend
- [ ] Negative testing scenáre (dokumentácia)

## 🟢 Nápady / Future
- [ ] FE: pozadie — vesmírna obloha (CSS/canvas hviezdy alebo NASA obrázok) namiesto solid color
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
