# 🪐 Space Tours API — Backlog

## 🔴 In Progress
- [ ] Negative tests in Postman
- [ ] Pytest
- [ ] GitHub Actions CI

## 🟡 Up Next — Validations (known bugs, ideal for QA students)
- [ ] `departure_date` — past dates should not be accepted
- [ ] `passenger_name` — minimum name length (e.g. at least 2 characters)
- [ ] `passenger_name` — maximum name length
- [ ] `departure_date` — format validation (currently accepts any string)
- [ ] What happens if you send an empty request body?
- [ ] What happens if you send an unknown field (e.g. `"colour": "red"`)?
- [ ] PUT — what if you send an invalid status (e.g. `"status": "flying"`)?

## 🟡 Up Next — Features
- [ ] Mark some planets in the destination selector as `disabled` with a "Tour coming soon" note
- [ ] Show travel time to planet — calculate and display trip duration when selecting a destination (FE and API `/destinations`)
- [ ] Meal selection and other add-ons when creating a booking
- [ ] Language versions — Swagger documentation and Frontend
  - SK / EN as a base
  - invented space language (e.g. Galactic Standard, Martian Creole...) — for fun and branding
- [ ] Document generation for the client
  - Booking confirmation — PDF or HTML
  - Optionally other documents (boarding pass, trip itinerary...)
- [ ] Client-facing FE — public page for customers (separate from Stellar Command backoffice)
  - `source` field on booking (`"backoffice"` / `"web"` / etc.) — non-breaking, scales to any channel
  - **Leads** tab in Stellar Command — incoming bookings from client FE, until processed by backoffice
- [ ] Design Doc — feature description with screenshots, serves as a basis for development and testing

## 🟢 Ideas / Future
- [ ] Add optional `middle_name` field to `passenger_name` — update DB model, API, and FE

## 🧪 QA / Learning

## 🧊 Icebox / Future Scope
_Long-term ideas — interesting but without a concrete timeline. May become a priority or stay here forever._

### Backend / API
- [ ] Authentication — API key (simpler) or JWT tokens (more realistic auth flow, Bearer tokens, protected endpoints)
- [ ] Payments integration — Stripe, webhooks, idempotency
- [ ] Rate limiting — protect API from spam
- [ ] Background tasks — e.g. confirmation email after booking creation (FastAPI has this built in)
- [ ] Email notifications — SendGrid or Resend

### Testing / QA
- [ ] Pytest — automated tests for FastAPI endpoints
- [ ] GitHub Actions CI — automatically run tests on every push
- [ ] Playwright — end-to-end tests for Stellar Command FE (Python library, Page Object Model)
- [ ] Postman / Newman — automated Postman collection runs in CI
- [ ] Load testing — Locust (Python), simulate load on endpoints
- [ ] Contract testing — Pact, verify that FE and API agree on data format

### Messaging / Event-Driven
- [ ] RabbitMQ integration — event-driven notifications on booking status change (e.g. `booking.confirmed`, `booking.cancelled`)
- [ ] Producer in API — publish event to queue on PUT /bookings
- [ ] Consumer worker — separate Python process that reads and processes messages (email, stats, payments)
- [ ] Local setup via Docker, production via CloudAMQP (free tier)
- [ ] Kafka as an alternative for more advanced use cases (high message volume, event log)

### DevOps / Infrastructure
- [ ] Docker — containerise the app
- [ ] Environment management — `.env`, secrets, dev/staging/prod differences
- [ ] Monitoring — Sentry for error tracking and alerting
- [ ] Semantic versioning — `MAJOR.MINOR.PATCH`, GitHub releases for larger deployments

### Frontend
- [ ] Client-facing frontend — public page separate from backoffice (Stellar Command)
- [ ] Destinations page — list of planets with description (distance, flight duration, price)
- [ ] Booking detail page — click on passenger name opens `/#/bookings/{id}` with read-only info, actions (Confirm/Cancel/Delete), and edit form (PUT)

## ✅ Done
- [x] Split `passenger_name` into two separate fields: `first_name`, `last_name` — update DB model, API, and FE
- [x] Pagination and server-side sorting (GET /bookings?page=1&limit=10&sort_by=id&sort_dir=asc)
- [x] Booking statistics — GET /bookings/stats (total, pending, confirmed, cancelled)
- [x] Filtering by seat_class (FE and API)
- [x] Staging environment — `-x` Render services switched to feature branch staging (prod + staging simultaneously)
- [x] Postman environments — prod and staging ({{base_url}} differs by env)
- [x] Tooltips on action buttons — custom CSS (consistent, without native browser delay)
- [x] Edit booking via FE — edit form (PUT), change field directly from the table
- [x] Postman environment variables ({{base_url}}, {{booking_id}})
- [x] Export Postman collection to repository
- [x] `buggy` branch with intentional bugs — for learning testing
- [x] Buggy version deployed on a separate environment (Render) — two versions simultaneously (stable + buggy)
- [x] Staging environment — second branch (`develop`) deployed on separate Render services (2× BE, 2× FE, 2× DB)
  - prod: https://space-tours-api.onrender.com / https://stellar-command.onrender.com
  - staging: https://space-tours-api-x.onrender.com / https://stellar-command-x.onrender.com
- [x] FastAPI project — local
- [x] SQLite database
- [x] CRUD endpoints (POST, GET, GET by ID, PUT, DELETE)
- [x] Filtering (destination, status)
- [x] Swagger UI documentation
- [x] Postman collection
- [x] GitHub repository
- [x] Render.com deployment (API)
- [x] CORS middleware
- [x] Frontend — Stellar Command backoffice
- [x] Render.com deployment (Frontend)
- [x] Seed data script (automatic DB population with test data)
- [x] PostgreSQL — migration to Neon.tech (permanent free tier)
- [x] Space background on frontend (canvas stars + shooting stars)
