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

### Stable (main branch)

| Služba | URL |
|--------|-----|
| API (Swagger UI) | https://space-tours-api.onrender.com/docs |
| API (base URL) | https://space-tours-api.onrender.com |
| Frontend (backoffice) | https://stellar-command.onrender.com |
| Databáza (Neon) — projekt `space-tours-api` | https://console.neon.tech |

### Staging / Buggy (buggy-void-terminal branch)

| Služba | URL |
|--------|-----|
| API (Swagger UI) | https://space-tours-api-x.onrender.com/docs |
| API (base URL) | https://space-tours-api-x.onrender.com |
| Frontend (backoffice) | https://stellar-command-x.onrender.com |
| Databáza (Neon) — projekt `space-tours-api-x` | https://console.neon.tech |

### Ostatné

| Služba | URL |
|--------|-----|
| GitHub | https://github.com/kat-bal/space-tours-api |

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
│   ├── index.html    # Stellar Command backoffice UI
│   ├── favicon16.png
│   ├── favicon32.png
│   ├── favicon180.png
│   └── favicon512.png
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
| GET | `/bookings/stats` | Štatistiky (total, pending, confirmed, cancelled) |
| GET | `/bookings/{id}` | Detail objednávky |
| PUT | `/bookings/{id}` | Úprava objednávky |
| DELETE | `/bookings/{id}` | Zmazanie objednávky |

### Query parametre pre GET /bookings

| Parameter | Popis | Príklad |
|-----------|-------|---------|
| `destination` | Filter podľa planéty | `?destination=Mars` |
| `status` | Filter podľa stavu | `?status=pending` |
| `seat_class` | Filter podľa triedy sedenia | `?seat_class=vip` |
| `page` | Číslo stránky (default: 1) | `?page=2` |
| `limit` | Počet výsledkov na stránku (default: 10) | `?limit=5` |
| `sort_by` | Pole na zoradenie | `?sort_by=departure_date` |
| `sort_dir` | Smer zoradenia: `asc` / `desc` | `?sort_dir=desc` |

---

## Dátový model — Booking

| Pole | Typ | Povinné | Default | Možné hodnoty |
|------|-----|---------|---------|---------------|
| `passenger.first_name` | string | áno | — | ľubovoľný text |
| `passenger.last_name` | string | áno | — | ľubovoľný text |
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
- **Postman** — kolekcia uložená v repozitári (`Space-Tours-API.postman_collection.json`); dve environments: `Space-Tours-API-prod` a `Space-Tours-API-staging` (prepínajú `{{base_url}}`)
- **Neon SQL Editor** — priamy prístup do databázy cez browser
- **DBeaver Community** — bezplatný databázový editor; funguje so SQLite aj PostgreSQL

### Pripojenie cez DBeaver

**SQLite (lokálne):**
1. **Database → New Database Connection → SQLite**
2. Do poľa **Path** zadaj cestu k súboru `space_tours.db` v priečinku projektu
3. Klikni **Finish**

**PostgreSQL — Neon (produkčné):**
1. V [Neon konzole](https://console.neon.tech) otvor projekt → **Connection Details**
2. **Database → New Database Connection → PostgreSQL**
3. Vyplň parametre (Host, Port, Database, Username, Password) podľa Neon konzoly
4. Klikni **Test Connection** → **Finish**

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

---

## Práca s Claudom

### Možnosť A — Claude Code (odporúčané)

Claude Code je CLI nástroj, ktorý beží priamo v termináli a má prístup k lokálnym súborom aj GitHubu.

**Predpoklady:**
- Nainštalovaný Claude Code (`npm install -g @anthropic-ai/claude-code`)
- Nainštalovaný a prihlásený `gh` CLI (`brew install gh && gh auth login`)

**Workflow:**
1. Otvor terminál v priečinku `space-tours-api`
2. Spusti `claude`
3. Zadaj úlohu — Claude priamo upraví súbory, commitne a pushne

**Čo Claude Code vie robiť samostatne:**
- Čítať a upravovať všetky projektové súbory
- Generovať nové funkcie, validácie, endpointy
- Aktualizovať dokumentáciu
- `git add`, `git commit`, `git push` — vrátane commit messages

---

### Možnosť B — Claude Desktop (bez prístupu k terminálu)

GitHub repozitár je verejný — Claude si vie stiahnuť aktuálny stav priamo:

```bash
git clone https://github.com/kat-bal/space-tours-api.git
```

**Workflow:**
1. Claude si stiahne repozitár z GitHubu a prečíta aktuálny stav súborov
2. Upraví súbory podľa zadania
3. Vygeneruje upravené súbory na stiahnutie
4. Vyučujúca ich skopíruje do repozitára, commitne a pushne

**Čo musí urobiť vyučujúca:**
- `git add`, `git commit`, `git push` — Claude Desktop nemá prístup k credentials
