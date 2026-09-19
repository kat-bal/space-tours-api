# 🪐 Space Tours API — Project Context

This file serves as a quick onboarding document for new conversations, collaborators, or students.

---

## What this project is

A REST API sandbox for learning the basics of HTTP methods.  
Theme: a booking system for space travel to planets of the Solar System.

**Audience:** QA beginners and anyone learning API testing  
**Author:** Senior QA with a development background

---

## Live URLs

### Stable (main branch)

| Service | URL |
|---------|-----|
| API (Swagger UI) | https://space-tours-api.onrender.com/docs |
| API (base URL) | https://space-tours-api.onrender.com |
| Frontend (backoffice) | https://stellar-command.onrender.com |
| Database (Neon) — project `space-tours-api` | https://console.neon.tech |

### Staging / Buggy (buggy-void-terminal branch)

| Service | URL |
|---------|-----|
| API (Swagger UI) | https://space-tours-api-x.onrender.com/docs |
| API (base URL) | https://space-tours-api-x.onrender.com |
| Frontend (backoffice) | https://stellar-command-x.onrender.com |
| Database (Neon) — project `space-tours-api-x` | https://console.neon.tech |

### Other

| Service | URL |
|---------|-----|
| GitHub | https://github.com/kat-bal/space-tours-api |

> ⚠️ Render free tier puts the server to sleep after 15 minutes of inactivity. The first request after sleep may take 30–60 seconds.

---

## Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.12 + FastAPI |
| Database | PostgreSQL 16 via Neon.tech (local: SQLite fallback) |
| ORM | SQLAlchemy |
| Frontend | Vanilla HTML/CSS/JS |
| Hosting | Render.com (free tier) |
| Version control | GitHub |

---

## Project structure

```
space-tours-api/
├── main.py           # FastAPI app, all endpoints
├── database.py       # DB connection (Neon/PostgreSQL in production, SQLite locally)
├── models.py         # Database models + Pydantic schemas
├── seed.py           # Seed script — populates DB with test data
├── requirements.txt  # Python dependencies
├── .env              # Local env variables — not in git!
├── frontend/
│   ├── index.html    # Stellar Command backoffice UI
│   ├── favicon16.png
│   ├── favicon32.png
│   ├── favicon180.png
│   └── favicon512.png
├── BACKLOG.md        # Project backlog
├── CONTEXT.md        # This file
└── README.md         # Setup instructions
```

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/destinations` | List of planets |
| POST | `/bookings` | Create a new booking |
| GET | `/bookings` | All bookings (+ filters) |
| GET | `/bookings/stats` | Statistics (total, pending, confirmed, cancelled) |
| GET | `/bookings/{id}` | Booking detail |
| PUT | `/bookings/{id}` | Update a booking |
| DELETE | `/bookings/{id}` | Delete a booking |

### Query parameters for GET /bookings

| Parameter | Description | Example |
|-----------|-------------|---------|
| `destination` | Filter by planet | `?destination=Mars` |
| `status` | Filter by status | `?status=pending` |
| `seat_class` | Filter by seat class | `?seat_class=vip` |
| `page` | Page number (default: 1) | `?page=2` |
| `limit` | Items per page (default: 10) | `?limit=5` |
| `sort_by` | Field to sort by | `?sort_by=departure_date` |
| `sort_dir` | Sort direction: `asc` / `desc` | `?sort_dir=desc` |

---

## Data model — Booking

| Field | Type | Required | Default | Allowed values |
|-------|------|----------|---------|----------------|
| `passenger.first_name` | string | yes | — | any text |
| `passenger.last_name` | string | yes | — | any text |
| `destination` | string | yes | — | Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune |
| `departure_date` | string | yes | — | YYYY-MM-DD |
| `seat_class` | string | no | economy | economy, business, vip |
| `status` | string | no | pending | pending, confirmed, cancelled |

---

## Local setup

```bash
# 1. Activate venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

# 2. Install dependencies (first time only)
pip install -r requirements.txt

# 3. Create .env file with connection string (first time only)
# DATABASE_URL=postgresql://...  ← from Neon dashboard
# Without .env, SQLite is used as a fallback

# 4. Start the server
uvicorn main:app --reload

# 5. Optionally — seed the DB with test data
python3 seed.py
```

Server running at: http://localhost:8000  
Swagger: http://localhost:8000/docs

---

## Database

- **Production:** PostgreSQL 16 on [Neon.tech](https://console.neon.tech) — permanent free tier, 0.5 GB
- **Local:** SQLite fallback (if `DATABASE_URL` is not set in `.env`)
- **Seed:** 10 test bookings, runs automatically on startup if DB is empty
- **Schema:** single `bookings` table — defined in `models.py` (`BookingDB` class)
- **SQL Editor:** available directly in the Neon dashboard

---

## Tools

- **Swagger UI** — interactive documentation, ideal for beginners
- **Postman** — collection stored in the repository (`Space-Tours-API.postman_collection.json`); two environments: `Space-Tours-API-prod` and `Space-Tours-API-staging` (switch `{{base_url}}`)
- **Neon SQL Editor** — direct database access via browser
- **DBeaver Community** — free database editor; works with both SQLite and PostgreSQL

### Connecting via DBeaver

**SQLite (local):**
1. **Database → New Database Connection → SQLite**
2. In the **Path** field, enter the path to `space_tours.db` in the project folder
3. Click **Finish**

**PostgreSQL — Neon (production):**
1. In the [Neon console](https://console.neon.tech) open the project → **Connection Details**
2. **Database → New Database Connection → PostgreSQL**
3. Fill in the parameters (Host, Port, Database, Username, Password) from the Neon console
4. Click **Test Connection** → **Finish**

---

## Known intentional bugs (for learning)

These are known issues that serve as practice findings for QA students:

- `departure_date` — past dates are accepted
- `passenger_name` — no minimum or maximum length
- `departure_date` — accepts any string (e.g. "banana")
- Empty request body does not return a meaningful error
- Unknown fields in request body are silently ignored
- `status` via PUT — invalid values can be set

---

## Further plans

See `BACKLOG.md` for the full list. Main priorities:
1. Validations (fixing known bugs)
2. Language versions (SK/EN)
3. Client-facing frontend (separate from backoffice)

---

## Working with Claude

### Option A — Claude Code (recommended)

Claude Code is a CLI tool that runs directly in the terminal with access to local files and GitHub.

**Prerequisites:**
- Claude Code installed (`npm install -g @anthropic-ai/claude-code`)
- `gh` CLI installed and authenticated (`brew install gh && gh auth login`)

**Workflow:**
1. Open a terminal in the `space-tours-api` folder
2. Run `claude`
3. Describe the task — Claude will edit files, commit, and push directly

**What Claude Code can do autonomously:**
- Read and edit all project files
- Generate new features, validations, endpoints
- Update documentation
- `git add`, `git commit`, `git push` — including commit messages

---

### Option B — Claude Desktop (no terminal access)

The GitHub repository is public — Claude can download the current state directly:

```bash
git clone https://github.com/kat-bal/space-tours-api.git
```

**Workflow:**
1. Claude downloads the repository from GitHub and reads the current file state
2. Edits files according to the task
3. Generates the edited files for download
4. You copy them into the repository, commit, and push

**What you need to do yourself:**
- `git add`, `git commit`, `git push` — Claude Desktop does not have access to credentials
