# 🐛 Buggy Branch — Setup & Bug Register

Tento dokument opisuje ako vytvoriť `buggy` branch a zoznam všetkých zámerných chýb.

---

## Git príkazy — krok za krokom

```bash
# 1. Prepni sa do repozitára
cd ~/space-tours-api

# 2. Uisti sa, že si na main a máš všetko aktuálne
git checkout main
git pull origin main

# 3. Vytvor novú buggy branch
git checkout -b buggy

# 4. Nahraď main.py buggy verziou
cp /cesta/k/main_buggy.py main.py

# 5. Nahraď frontend buggy verziou
cp /cesta/k/index_buggy.html frontend/index.html

# 6. Commitni zmeny
git add main.py frontend/index.html
git commit -m "feat: add intentional bugs for QA training (buggy branch)"

# 7. Push na GitHub
git push origin buggy
```

---

## Render.com — nasadenie buggy verzie

1. Choď na https://render.com → **New Web Service**
2. Pripoj rovnaký GitHub repozitár
3. V nastaveniach nastav **Branch: buggy**
4. Service name: napr. `space-tours-api-buggy`
5. Rovnaké environment variables ako stable (DATABASE_URL z Neon — môžeš použiť separátnu DB!)
6. Pre frontend: **New Static Site** → branch: buggy → publish dir: `frontend`

> ⚠️ Odporúča sa použiť **separátnu Neon databázu** pre buggy env,
> aby testeri nemohli rozbiť produkčné dáta.

---

## 🐛 Bug Register — Zoznam zámerných chýb

### Bugy zdedené zo stable (neopravené)

| # | ID | Endpoint | Popis |
|---|-----|----------|-------|
| 1 | STABLE-01 | POST /bookings | `departure_date` akceptuje dátumy v minulosti |
| 2 | STABLE-02 | POST /bookings | `departure_date` akceptuje ľubovoľný string (napr. "banán") |
| 3 | STABLE-03 | POST /bookings | `passenger_name` bez minimálnej ani maximálnej dĺžky |
| 4 | STABLE-04 | POST /bookings | Prázdny request body nevráti zmysluplnú chybu |
| 5 | STABLE-05 | všetky | Neznáme polia v request body sa ticho ignorujú |
| 6 | STABLE-06 | PUT /bookings/{id} | `status` bez validácie povolených hodnôt (na stable bol opravený, tu nie) |

### Nové bugy pridané na buggy branchi

| # | ID | Endpoint | Popis | Očakávané | Skutočné |
|---|-----|----------|-------|-----------|---------|
| 7 | BUG-01 | POST /bookings | Nesprávny HTTP status kód | `201 Created` | `200 OK` |
| 8 | BUG-05 | POST /bookings | Duplikátné objednávky povolené | Chyba alebo upozornenie | Rovnaký cestujúci+destinácia+dátum možno vytvoriť opakovane bez obmedzenia |
| 9 | BUG-06 | GET /bookings | Filter `?status=` je case-sensitive | `Pending` aj `pending` nájdu výsledky | `?status=Pending` vráti prázdne pole `[]` bez chyby |
| 10 | BUG-07 | GET /bookings/{id} | Neexistujúce ID nevráti 404 | `404 Not Found` | `200 OK` s `null` hodnotami |
| 11 | BUG-08 | PUT /bookings/{id} | Akceptuje neplatné hodnoty stavu | Chyba 422 pre `"flying"` | `200 OK`, stav sa uloží |
| 12 | BUG-09 | PUT /bookings/{id} | Zrušenú objednávku možno znovu otvoriť | `cancelled` je finálny stav | `cancelled → pending` prechod prejde |
| 13 | BUG-10 | DELETE /bookings/{id} | Maže akúkoľvek objednávku | Len `cancelled` možno zmazať | `confirmed` aj `pending` sa dajú zmazať |

---

## Frontend rozdiely

| Vlastnosť | Stable (stellar-command) | Buggy (void-terminal) |
|-----------|-------------------------|----------------------|
| Názov | Stellar Command | VOID//TERMINAL |
| Farebnú schéma | Modrá / cyan / zelená | Fialová / pink / glitch |
| Branding | Seriózny backoffice | Cyberpunk, glitch efekty |
| Bug banner | Nie | Áno — upozorňuje na buggy env |
| Delete tlačidlo | Len pre `cancelled` | Pre všetky záznamy (odráža BUG-10) |

---

## Poznámky pre inštruktorku

- Bugy sú označené komentármi `# 🐛 BUG-XX:` priamo v `main.py`
- Každý bug je dobre izolovaný — oprava jedného neovplyvní ostatné
- Odporúčané poradie objavovania pre študentov: BUG-01 → BUG-06 → BUG-07 → BUG-10 → BUG-08 → BUG-09 → BUG-05
- BUG-05 (duplikáty) je najťažší na odhalenie bez systematického testovania
