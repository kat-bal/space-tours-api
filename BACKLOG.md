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
- [ ] Stránka Destinations — zoznam planét s popisom (vzdialenosť, dĺžka letu, cena)
- [ ] V destination selectione označiť niektorú planétu ako `disabled` s poznámkou "Tour coming soon"
- [ ] Zobraziť čas doletu na planétu — vypočítať a zobraziť dĺžku cesty pri výbere destinácie (FE aj API `/destinations`)
- [ ] Filtrovanie na FE podľa travel class (seat_class)
- [ ] Výber stravovania a ďalších doplnkov (addons) pri vytváraní objednávky
- [ ] Jazykové verzie — Swagger dokumentácia aj Frontend
  - SK / EN ako základ
  - vymyslený vesmírny jazyk (napr. Galactic Standard, Martian Creole...) — pre zábavu a branding
- [ ] Generovanie dokumentov pre klienta
  - Potvrdenie objednávky (booking confirmation) — PDF alebo HTML
  - Prípadne ďalšie doklady (palubný lístok, itinerár cesty...)
- [ ] Negative testing scenáre (dokumentácia) - aktuálne jeden negative test v Postman kolekcii
- [ ] Design Doc — popis funkcionality appky so screenshotmi, slúži ako podklad pre vývoj aj testovanie

## 🟢 Nápady / Future
- [ ] Rozdeliť `passenger_name` na tri samostatné polia: `first_name`, `middle_name` (voliteľné), `last_name` — úprava DB modelu, API aj FE
- [ ] Pagination (GET /bookings?page=1&limit=10)
- [ ] Sorting (GET /bookings?sort=departure_date)

## 🧪 QA / Výuka

## 🧊 Icebox / Future Scope
_Dlhodobé nápady — zaujímavé, ale bez konkrétneho termínu. Môžu sa stať prioritou alebo zostať tu navždy._

### Backend / API
- [ ] Autentifikácia — API key (jednoduchšie) alebo JWT tokeny (reálnejší auth flow, Bearer tokeny, chránené endpointy)
- [ ] Payments integrácia — Stripe, webhooky, idempotency
- [ ] Rate limiting — ochrana API pred spamom
- [ ] Background tasks — napr. confirmation email po vytvorení objednávky (FastAPI má zabudované)
- [ ] Email notifikácie — SendGrid alebo Resend

### Testing / QA
- [ ] Pytest — automatizované testy pre FastAPI endpointy
- [ ] GitHub Actions CI — automatické spúšťanie testov pri každom push
- [ ] Playwright — end-to-end testy pre Stellar Command FE (Python knižnica, Page Object Model)
- [ ] Postman / Newman — automatizované spúšťanie Postman kolekcií v CI
- [ ] Load testing — Locust (Python), simulácia záťaže na endpointy
- [ ] Contract testing — Pact, overenie že FE a API sa zhodujú na formáte dát

### Messaging / Event-Driven
- [ ] RabbitMQ integrácia — event-driven notifikácie pri zmene stavu objednávky (napr. `booking.confirmed`, `booking.cancelled`)
- [ ] Producer v API — pri PUT /bookings publishnúť event do fronty
- [ ] Consumer worker — samostatný Python proces ktorý správy číta a spracováva (email, štatistiky, payments)
- [ ] Lokálny setup cez Docker, produkcia cez CloudAMQP (free tier)
- [ ] Kafka ako alternatíva pre pokročilejší use case (vysoký objem správ, event log)

### DevOps / Infraštruktúra
- [ ] Docker — zabaliť appku do kontajnera
- [ ] Environment management — `.env`, secrets, dev/staging/prod rozdiel
- [ ] Monitoring — Sentry pre error tracking a alerting
- [ ] Staging prostredie — druhý branch (`develop`) nasadený na samostatných Render službách (2× BE, 2× FE, 2× DB)
- [ ] Semantic versioning — `MAJOR.MINOR.PATCH`, GitHub releases pri väčších nasadeniach

### Frontend
- [ ] Frontend pre klientov — verejná stránka oddelená od backoffice (Stellar Command)

## ✅ Hotovo
- [x] Tooltips na akčných buttonoch — custom CSS (konzistentné, bez natívneho browser delay)
- [x] Úprava objednávky cez FE — editovací formulár (PUT), zmena poľa priamo z tabuľky
- [x] Postman environment variables ({{base_url}}, {{booking_id}})
- [x] Exportovať Postman kolekciu do repozitára
- [x] `buggy` branch s úmyselnými bugmi — na výuku testovania
- [x] Buggy verzia nasadená na samostatnom prostredí (Render) — dve verzie naraz (stable + buggy)
  - stable: https://space-tours-api.onrender.com / https://stellar-command.onrender.com
  - buggy: https://space-tours-api-x.onrender.com / https://stellar-command-x.onrender.com
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
