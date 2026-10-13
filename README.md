# 🐾 PawFurry Care

> **24/7 AI-Powered Veterinary Telehealth, Emergency Triage & 24-Hour Hospital GPS Directory**  
> *Dedicated Exclusively to Cats & Dogs in Malaysia • Dual-Language (English & Bahasa Melayu) • Zero-Delay Deterministic Triage • Real-Time Seasonal Poison & Toxin Advisory*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-12%2F12%20Passing-brightgreen.svg)]()
[![Security](https://img.shields.io/badge/Security-JWT%20%7C%20Bcrypt%20%7C%20Rate%20Limited-blue.svg)]()

---

## 🌟 Executive Summary

**PawFurry Care** is an enterprise-grade veterinary assistant and emergency triage web application engineered specifically for pet parents in Malaysia. Built on a modular Python (Flask) backend and lightweight reactive frontend, PawFurry Care delivers real-time clinical guidance, life-saving triage protocols, GPS routing to verified 24-hour veterinary emergency centres, and tropical climate hazard updates.

---

## 🚀 Key Platform Capabilities

### 1. 🤖 AI Pet Care Chatbot (Strict Cat & Dog Scope Guardrail)
* **Exclusive Feline & Canine Scope:** Engineered specifically for cats (*kucing*) and dogs (*anjing*).
* **Strict Out-of-Domain Interceptor:** Non-pet inquiries (such as human cooking/recipes like *"nasi lemak"*, human weather, coding, politics, or non-canine/feline species) are politely declined.
* **Clinical Nuance Detection:** If a user asks whether a pet can consume human food (e.g., *"Can cats eat nasi lemak?"*), the engine provides an in-depth clinical analysis explaining the physiological dangers of coconut milk (*pancreatitis*), chili/sambal (*capsaicin gastric erosion*), onions/garlic (*Heinz body hemolytic anemia*), and salted anchovies (*FLUTD urinary obstruction*).
* **Bilingual Support (i18n):** Native support for **English (EN)** and **Bahasa Melayu (BM)**.
* **Tropical Weather & Seasonal Advisory:** Seamlessly injects Malaysian seasonal warnings (e.g., high humidity ringworm & sporotrichosis risks, heatwave hyperthermia) into conversation contexts.

### 2. 🚨 Deterministic Emergency Triage Engine (Zero-Delay)
* **Instant Red-Flag Detection:** Eliminates AI hallucination latency during acute emergencies:
  * Male cat urinary obstruction (*FLUTD / Blocked Bladder*).
  * Human medication toxicity (*Paracetamol / Panadol / Tylenol / NSAIDs*).
  * True lily ingestion (*Lilium & Hemerocallis* in cats).
  * Gastric Dilatation-Volvulus (*GDV / Bloat* in dogs).
  * Acute respiratory distress, refractory status epilepticus, or massive hemorrhage.
* **Actionable First-Aid Guidance:** Provides immediate bulleted **DOs** and **DONTs**, paired with instant 1-tap dialers for the **National Poison Centre (1-800-88-8099)** and **BOMBA (999)**.

### 3. 🏥 Verified 24-Hour Emergency Clinics & GPS Geolocation
* Comprehensive coverage across Selangor, Kuala Lumpur, Penang, Johor, Perak, Melaka, Pahang, Sarawak, and Sabah.
* **Real-Time Operational Status:** Evaluates active opening hours against local Malaysian time (`OPEN NOW (24 HOURS)` vs `CLOSED (EMERGENCY ON-CALL ACTIVE)`).
* **Rush-Hour Traffic ETA Multiplier:** Automatically recalculates estimated driving times based on Malaysian rush-hour traffic conditions (+40% to +45% during morning & evening commutes).
* Direct turn-by-turn routing via **Google Maps** and **Waze**.

### 4. ⚠️ Household & Seasonal Poison Encyclopedia
* Comprehensive catalog of toxic substances, mechanism of toxicity, and specific clinical signs.
* **Live Seasonal Hazard Spotlight:** Dynamically updates hazards according to Malaysian weather patterns (e.g., toxic *Asian Common Toads (Bufo)* emerging after tropical rains, and mosquito coil pyrethroid toxicity in felines).

### 5. 📰 Malaysian Pet Care News & Official Advisories
* Localized articles on heatstroke prevention, Malaysian Animal Welfare Act 2015 (Act 772), regional outbreaks (Rabies surveillance zones, Sporotrichosis), and nutritional myths.

### 6. 🛡️ Multi-Layered Security Architecture
* Password hashing using `bcrypt` with 12 algorithmic salt rounds.
* Stateless `PyJWT` authentication with configurable token expiration.
* In-memory sliding window rate limiting across authentication and chat endpoints.
* Strict XSS sanitization and HTTP Security Headers (`X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `X-XSS-Protection: 1; mode=block`).

---

## 🏗️ Architecture & Project Structure

```text
PawFurry-Care/
├── app.py                 # Core Flask application, RESTful APIs & security middleware
├── chat_service.py        # Bilingual AI assistant, domain guardrail & seasonal logic
├── config.py              # Environment configuration & rate limit definitions
├── database.py            # SQLite schema initialisation & CRUD queries
├── emergency_data.py      # Malaysian vet clinic directory, Haversine formula & traffic engine
├── news_data.py           # Bilingual pet healthcare advisories & weather alerts
├── security.py            # JWT token engine, bcrypt hashing & input sanitizers
├── test_system.py         # Automated test suite (12/12 unit & integration tests)
├── triage_engine.py       # Deterministic clinical triage & seasonal poison encyclopedia
├── requirements.txt       # Production Python dependencies
├── Procfile               # Cloud deployment process file (Gunicorn)
├── .env.example           # Environment variable template
├── .gitignore             # Git exclusions (database, local secrets, bytecode)
├── templates/
│   └── index.html         # Responsive frontend application (TailwindCSS + FontAwesome)
└── static/
    ├── css/
    │   └── custom.css     # Bespoke UI styles
    └── js/
        └── app.js         # Reactive client controller, i18n & silent auto-sync
```

---

## ⚙️ Quickstart & Local Installation

### Prerequisites
* **Python 3.10+** (Tested on Python 3.11)
* **Git**

### 1. Clone Repository
```bash
git clone https://github.com/Idhaizs/PawFurry-Care.git
cd PawFurry-Care
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Activate on macOS / Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(Optional: Add your `GEMINI_API_KEY` to enable Google Gemini AI fallback. If omitted, the platform uses its built-in deterministic veterinary knowledge base.)*

### 5. Execute Test Suite
Verify that all 12 automated unit and integration tests pass:
```bash
python test_system.py
```
```text
Ran 12 tests in 0.063s
OK
[PASS] Health Check Endpoint (PawFurry Care v1.2)
[PASS] Dual-Language (BM & EN) News Listing
[PASS] Live News Auto-Update Sync Endpoint
[PASS] Emergency Triage in English (Paracetamol Toxicity): CRITICAL Red Alert
[PASS] Emergency Triage in Bahasa Melayu (Urinary Blockage): CRITICAL Red Alert
[PASS] Bilingual Chat for Cats and Dogs (English & Bahasa Melayu)
[PASS] Malaysia 24H Emergency Clinics & GPS Haversine Sort
[PASS] Production HTTP Security Headers
[PASS] Strict Chat Guardrail: Successfully intercepted off-topic queries
[PASS] Chat Knowledge: 'Can cats eat nasi lemak?' clinical explanation
[PASS] Master System Auto-Sync Endpoint: Synchronized all 4 pillars
[PASS] Live Seasonal Toxin Guide: Active Monsoon Hazard Spotlight
```

### 6. Run Application
```bash
python app.py
```
Open your browser and navigate to:  
👉 **`http://127.0.0.1:5000`**

---

## 🌐 Cloud Deployment Guide

Because **PawFurry Care** incorporates a full Python backend, SQLite database, and deterministic API services, it requires a Python host rather than static-only hosting.

### Option A: Deploy on Render (Recommended - Free Tier)
1. Sign up / Log in to [Render](https://render.com/).
2. Click **New +** → Select **Web Service**.
3. Connect your GitHub repository: `Idhaizs/PawFurry-Care`.
4. Configure settings:
   * **Runtime:** `Python 3`
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `gunicorn app:app`
5. Click **Create Web Service**. Your app will be live with a free HTTPS URL in 2 minutes!

### Option B: Deploy on Railway
1. Sign up on [Railway.app](https://railway.app/).
2. Select **New Project** → **Deploy from GitHub repo**.
3. Select `PawFurry-Care`. Railway will automatically detect the Python environment and `Procfile`, deploying the live application automatically.

### Option C: Deploy on PythonAnywhere
1. Create a free account on [PythonAnywhere](https://www.pythonanywhere.com/).
2. In the **Web** tab, select **Add a new web app** → **Flask** → **Python 3.10+**.
3. Clone the repository into your home directory and set the WSGI configuration to point to `app:app`.

---

## 🔒 Security & Privacy Notice

* **Data Protection:** Local databases (`petcare.db`) and secret tokens (`.env`) are strictly excluded from version control via `.gitignore`.
* **Clinical Disclaimer:** PawFurry Care serves as a digital veterinary triage and health education platform. In persistent or life-threatening clinical circumstances, pet owners must seek examination from a certified, registered veterinarian immediately.

---

## 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Developed with ❤️ for the Malaysian pet parent community.  
Copyright © 2026 **PawFurry Care Malaysia**.
