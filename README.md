# AutoVault — A Secure and Personalized Vehicle Management System

> **B.Tech Computer Science & Engineering (Cyber Security) — Academic Capstone Platform**

---

## 1. Project Overview

AutoVault is an all-in-one, personalized vehicle management and telemetry security platform. It replaces scattered glovebox paper bills, forgotten renewal deadlines, and unstructured spreadsheets with a centralized, cryptographically secured digital system.

The system delivers:
$$\text{Vehicle Profiles} + \text{Fuel Telemetry \& Mileage Math} + \text{Service Ledger} + \text{Predictive Reminders} + \text{Quarantined Document Vault} + \text{Chart.js Analytics} + \text{Cyber Security Hardening}$$

---

## 2. Technology Stack

| Layer | Technology | Rationale |
| :--- | :--- | :--- |
| **Backend** | Python 3 + Flask 3.x | Lightweight, modular routing via blueprints, high viva explainability |
| **Database** | SQLite + SQLAlchemy ORM | Zero-configuration serverless file database with foreign-key relationships and parameterized queries (PostgreSQL ready via `DATABASE_URL`) |
| **Authentication** | Werkzeug Security | Salted key derivation (PBKDF2/scrypt) cryptographic password hashing with resilient serverless session persistence |
| **Frontend** | HTML5, CSS3, JavaScript | Executive automotive theme (Black & Gold Royale Cockpit: Deep Onyx `#07080A`, Royal Gold `#D4AF37`, Champagne `#F3D079`, Orange warnings, Green optimal, Red critical), Plus Jakarta Sans typography, Lucide Icons |
| **Analytics** | Chart.js 4.x | Dynamic multi-dimensional charts (monthly spending, cost distribution, mileage trends, category breakdowns) |
| **Cloud Deployment** | Vercel Serverless / Render | Configured with `vercel.json` and WSGI serverless entrypoint (`api/index.py`) |

---

## 3. Implemented Modules & Functional Capabilities

### 1. Vehicle Garage (`/vehicle`)
* Multi-vehicle registration and profile management.
* Telemetry attributes: Manufacturer, Model, Variant, Registration Number, Fuel Type, Transmission, Manufacturing Year, Current Odometer, Color, Insurance Expiry, PUCC Expiry.
* Automatic odometer updates when new fuel fills or service records log higher mileage.

### 2. Fuel & Mileage Tracking (`/fuel`)
* Detailed fuel refill logging: Date, Odometer reading, Litres, Price per Litre, Total Cost, Fuel Station brand, and Notes.
* **Interval Mileage Math**: Automatically sorts refills by odometer to calculate exact distance between consecutive fills:
  $$\text{Interval Mileage (km/L)} = \frac{\text{Odometer}_{i} - \text{Odometer}_{i-1}}{\text{Litres}_{i}}$$
* Rolling metrics: Lifetime fuel spend, total litres, average cost per litre, and weighted average fuel efficiency.

### 3. Service & Maintenance Ledger (`/maintenance`)
* Chronological digital workshop book: Service Date, Service Category, Workshop Name, Incurred Cost, Odometer at service, Work Summary, and Part Invoices.
* Service categories: General Periodic Service, Engine Oil & Filter, Brake Service, Tyre Replacement, Battery Replacement, AC Servicing, Wheel Alignment, etc.
* Real-time expenditure totals and category distribution summaries.

### 4. Smart Reminders & Deadlines (`/reminders`)
* **Dual-Trigger Alerts**:
  * *Calendar Trigger*: Alerts based on target expiry dates (e.g. Insurance policy or PUCC renewal).
  * *Odometer Trigger*: Alerts based on target mileage milestones (e.g. 20,000 km major service).
* Dynamic status calculation: **Upcoming**, **Due Soon** ($\le$ 7 days or $\le$ 500 km), **Overdue**, and **Completed**.
* One-click task completion toggling with full historical audit log.

### 5. Quarantined Document Vault (`/documents`)
* Secure storage for high-value ownership paperwork: RC, Insurance Schedules, PUCC Certificates, and Workshop Invoices.
* **Security Controls**:
  * Strict file extension whitelisting (`.pdf`, `.png`, `.jpg`, `.jpeg`, `.webp`).
  * Cryptographic UUID renaming to prevent directory traversal and file collisions.
  * Stored in dedicated `instance/uploads/documents/` outside public web directories.
  * In-app secure viewing and authenticated file download with strict IDOR verification.

### 6. Interactive Analytics & Intelligence (`/analytics`)
* **Monthly Spending Progression**: Side-by-side comparative bar chart tracking Monthly Fuel vs Monthly Maintenance costs.
* **Cost Distribution**: Doughnut ratio of operational fuel consumption vs maintenance servicing.
* **Mileage Telemetry Trend**: Line progression of km/L efficiency across refills over time.
* **Maintenance by Category**: Horizontal distribution of servicing expenditures.

### 7. User Profile & Security Settings (`/profile`)
* Profile management, account creation timestamps, and secure password modification requiring verification of current credentials.

---

## 4. Cyber Security Architecture (Viva Highlights)

1. **Defense Against Insecure Direct Object References (IDOR)**:
   Every query for a vehicle, fuel entry, service record, reminder, or uploaded document verifies ownership against `session['user_id']`:
   ```python
   if object.vehicle.user_id != session['user_id']:
       abort(403)  # HTTP 403 Forbidden
   ```
2. **Cryptographic Password Digesting**:
   Plaintext passwords never touch database storage. Passwords are salted and hashed using Werkzeug key derivation (`generate_password_hash` / `check_password_hash`).
3. **Anti-Enumeration Handlers**:
   Authentication endpoints return uniform generic responses (`"Invalid username/email or password."`) to defeat user enumeration.
4. **SQL Injection (SQLi) Immunity**:
   All database operations run through SQLAlchemy ORM using parameterized query construction.
5. **Cross-Site Scripting (XSS) Mitigation**:
   Jinja2 auto-escaping sanitizes user-supplied input across all templates.
6. **File Ingestion Security**:
   Uploaded files are quarantined with randomized UUID identifiers outside the static root and served only via authenticated gateway routes (`/documents/view/<id>`).

---

## 5. Installation & Execution (Windows)

```powershell
# 1. Navigate to project root
cd d:\SHUB\AutoVault

# 2. Run the application
python app.py
```
Open your browser at:
```
http://127.0.0.1:5000
```

### Optional: Pre-populate Realistic Demo Data
To immediately demonstrate the platform with populated vehicles, fuel logs, service history, and reminders:
```powershell
python seed.py
```
Log in with:
* **Username**: `demo_driver`
* **Password**: `AutoVault@2026`

### Run Automated Security & Functional Tests
```powershell
# Run all feature verification tests
python -m unittest tests/test_all_features.py

# Run Phase 1 regression tests
python -m unittest tests/test_phase1.py
```
*(All 10 tests pass 100%.)*
