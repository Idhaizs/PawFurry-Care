# 🐾 PawFurry Care Malaysia

> **Platform Telekesihatan Veterinar & Triage Kecemasan Kucing & Anjing Malaysia 24/7**  
> *Bilingual (Bahasa Melayu & English) • Deterministic Clinical Triage • 24H Emergency Clinics GPS • Real-Time Seasonal Poison Guide • Verified Pet Health News*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)]()

---

## 🌟 Gambaran Keseluruhan (Overview)

**PawFurry Care** ialah platform digital komprehensif yang dibina khusus untuk pemilik **kucing (*cats*)** dan **anjing (*dogs*)** di Malaysia. Platform ini menggabungkan kecerdasan buatan, enjin triage kecemasan deterministik, dan direktori hospital veterinar 24 jam dengan integrasi GPS dan kesesakan jalan raya tempatan.

---

## 🚀 Ciri-Ciri Utama (Core Features)

### 1. 🤖 AI Pet Care Chatbot (Khusus Kucing & Anjing Sahaja)
* **Pengawal Sempadan Domain Ketat (*Strict Cat & Dog Guardrail*):**
  * Hanya melayan pertanyaan kesihatan, pemakanan, vaksinasi, dan tingkah laku bagi **kucing dan anjing**.
  * Soalan luar topik (seperti *"nasi lemak sedap kat mana"*, resepi manusia, pengaturcaraan, politik) ditolak secara sopan.
  * **Kecerdasan Klinikal:** Jika ditanya *"Boleh ke kucing makan nasi lemak?"*, sistem menerangkan secara terperinci bahaya santan (*pancreatitis*), sambal (*capsaicin*), dan bawang (*Heinz body hemolytic anemia*).
* **Dwi-Bahasa (*Dual Language*):** Sokongan penuh dalam **Bahasa Melayu (BM)** dan **English (EN)**.
* **Penyegerakan Musim Tropika (*Live Seasonal Advisory*):** Memasukkan amaran cuaca semasa (kurap & sporo semasa monsun, strok haba semasa musim panas) ke dalam nasihat bot.

### 2. 🚨 Enjin Triage Kecemasan Veterinar (*Zero-Delay Triage Engine*)
* **Pengesanan Simptom Bahaya Deterministik (*Red Alert*):**
  * Saluran kencing tersumbat (*Urinary Blockage / FLUTD* pada kucing jantan).
  * Keracunan ubat manusia (*Panadol / Paracetamol / Tylenol*).
  * Keracunan bunga lili (*Lilies*).
  * Perut kembung berpusing (*Bloat / GDV* pada anjing).
  * Sesak nafas, sawan berterusan, atau pendarahan aktif.
* **Protokol Pertolongan Cemas:** Panduan segera apa yang patut dibuat (**DOs**) dan dilarang (**DONTs**), serta pautan panggilan terus ke **Pusat Racun Negara (1-800-88-8099)** dan BOMBA (**999**).

### 3. 🏥 Direktori Vet 24 Jam Malaysia & GPS Geolocation
* Meliputi pusat rujukan kecemasan veterinar di Selangor, Kuala Lumpur, Pulau Pinang, Johor, Perak, Melaka, Pahang, Sarawak, dan Sabah.
* **Status Operasi Waktu Sebenar (*Live Operating Hours*):** Mengira status buka/tutup klinik berdasarkan jam tempatan Malaysia (*DIBUKA SEKARANG 24 JAM* vs *TUTUP ON-CALL KECEMASAN*).
* **Kiraan Trafik Waktu Puncak (*Peak-Hour Traffic Multiplier*):** Mengira anggaran masa pemanduan (ETA) mengikut waktu puncak jalan raya Malaysia (+40% hingga +45% masa perjalanan).
* Pautan pantas navigasi ke **Google Maps** dan **Waze**.

### 4. ⚠️ Panduan Toksin & Racun Haiwan Semasa
* Ensiklopedia bahan kimia dan makanan toksik lazim (coklat, bawang, anggur/kismis, ubat gegat).
* **Amaran Toksin Musiman Aktif (*Seasonal Hazard Spotlight*):** Amaran bahaya katak puru beracun (*Bufo*) dan asap ubat nyamuk lingkaran (*Pyrethroids*) pada musim hujan lebat/monsun.

### 5. 📰 Berita & Panduan Penjagaan Malaysia (PawNews)
* Artikel panduan penjagaan iklim tropika, amaran strok haba MetMalaysia, Akta Kebajikan Haiwan 2015 (Akta 772), dan pencegahan wabak Sporotrichosis (Sporo) & Rabies.

### 6. 🛡️ Sistem Keselamatan Berlapis (*Enterprise Security*)
* Penyulitan kata laluan menggunakan `bcrypt` dengan 12 *salt rounds*.
* Pengesahan token stateless `PyJWT` (HS256).
* *In-Memory Sliding Window Rate Limiting* untuk mencegah serangan *brute force* dan DDoS.
* Pembersihan input (*HTML sanitization* / XSS prevention) dan *HTTP Security Headers* (`nosniff`, `DENY`, `CSP`).

---

## 📂 Struktur Projek (Project Structure)

```text
mypet-care-malaysia/
├── app.py                 # Pelayan Flask, API endpoints & router utama
├── chat_service.py        # Enjin perbualan AI, penapis domain kucing/anjing & buletin musim
├── config.py              # Konfigurasi sistem, secret keys & had kadar (rate limits)
├── database.py            # Skema pangkalan data SQLite & fungsi CRUD
├── emergency_data.py      # Direktori vet Malaysia, formula Haversine & kalkulator trafik
├── news_data.py           # Pangkalan data berita dwi-bahasa & amaran cuaca
├── security.py            # Keselamatan JWT, bcrypt, XSS sanitization & headers
├── test_system.py         # 12 kes ujian unit & integrasi automatik
├── triage_engine.py       # Enjin triage kecemasan & ensiklopedia toksin musiman
├── requirements.txt       # Senarai kebergantungan (dependencies) Python
├── .env.example           # Contoh pembolehubah persekitaran (environment variables)
├── .gitignore             # Fail pengecualian Git (database, secrets, cache)
├── templates/
│   └── index.html         # Antaramuka web responsif (TailwindCSS + FontAwesome)
└── static/
    ├── css/
    │   └── custom.css     # Gaya CSS khas
    └── js/
        └── app.js         # Pengawal logik frontend, dwi-bahasa i18n & auto-sync senyap
```

---

## 🛠️ Cara Pemasangan & Menjalankan Sistem (Getting Started)

### 1. Klon Repositori
```bash
git clone https://github.com/Idhaizs/PawFurry-Care.git
cd PawFurry-Care
```

### 2. Pasang Kebergantungan (Dependencies)
Disarankan menggunakan persekitaran maya (*virtual environment*):
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Konfigurasi Fail `.env` (Pilihan)
Salin fail contoh `.env.example` kepada `.env`:
```bash
cp .env.example .env
```

### 4. Jalankan Ujian Automatik
Pastikan semua modul berfungsi dengan baik:
```bash
python test_system.py
```
*(Keputusan yang dijangka: 12 tests OK)*

### 5. Mulakan Pelayan Web
```bash
python app.py
```
Buka pelayar web di:
👉 **`http://127.0.0.1:5000`**

---

## 🔒 Privasi & Keselamatan Data

* **Tiada Data Sensitif Dikongsi:** Fail pangkalan data tempatan (`petcare.db`) dan kunci rahsia (`.env`) dikecualikan secara ketat melalui `.gitignore`.
* **Pematuhan Perubatan:** Nasihat sistem berfungsi sebagai triage maklumat am dan sentiasa mengutamakan rujukan kepada doktor veterinar bertauliah berdaftar.

---

## 👨‍💻 Pengarang & Hak Cipta
Dibangunkan untuk komuniti pencinta haiwan di Malaysia.  
Hak Cipta © 2026 **PawFurry Care Malaysia**.
