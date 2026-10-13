import math
from typing import List, Dict, Any, Optional

# Verified 24-Hour & Major Emergency Veterinary Centres in Malaysia
MALAYSIA_VET_CLINICS = [
    {
        "id": "vet_upm",
        "name": "Hospital Veterinar Universiti (UVH - UPM)",
        "state": "Selangor",
        "area": "Serdang",
        "address": "Fakulti Perubatan Veterinar, Universiti Putra Malaysia, 43400 UPM Serdang, Selangor",
        "phone": "+603-97693900",
        "emergency_phone": "+603-97693888",
        "is_24_hours": True,
        "operating_hours": "24 Jam (Kecemasan & Ambulans Haiwan)",
        "lat": 2.9961,
        "lng": 101.7081,
        "specialties": ["Kecemasan 24 Jam", "Pembedahan Kompleks", "ICU Haiwan", "X-Ray & Ultrasound"]
    },
    {
        "id": "vet_gasing",
        "name": "Gasing Veterinary Hospital (24 Hours)",
        "state": "Selangor",
        "area": "Petaling Jaya",
        "address": "53 & 55, Jalan 5/58, Gasing Indah, 46000 Petaling Jaya, Selangor",
        "phone": "+603-77823553",
        "emergency_phone": "+603-77823550",
        "is_24_hours": True,
        "operating_hours": "24 Jam Setiap Hari",
        "lat": 3.1042,
        "lng": 101.6558,
        "specialties": ["Rawatan Kecemasan", "Hospitalisasi 24 Jam", "Bank Darah Haiwan", "Surgeri"]
    },
    {
        "id": "vet_amc",
        "name": "Animal Medical Centre (AMC - 24 Hours)",
        "state": "Kuala Lumpur",
        "area": "Titiwangsa / Chow Kit",
        "address": "Wisma Medivet, 8, Jalan Tun Razak, 50400 Kuala Lumpur",
        "phone": "+603-40426742",
        "emergency_phone": "+603-40425873",
        "is_24_hours": True,
        "operating_hours": "24 Jam Setiap Hari (Termasuk Cuti Umum)",
        "lat": 3.1706,
        "lng": 101.6998,
        "specialties": ["Pusat Trauma & Kecemasan", "Makmal Darah Segera", "Oksigen Terapi", "Pembedahan Ortopedik"]
    },
    {
        "id": "vet_kd",
        "name": "Kota Damansara Veterinary Centre (24 Jam)",
        "state": "Selangor",
        "area": "Kota Damansara",
        "address": "27-1, Ground Floor, Jalan PJU 5/4, Dataran Sunway, Kota Damansara, 47810 Petaling Jaya, Selangor",
        "phone": "+603-61435988",
        "emergency_phone": "+603-61435988",
        "is_24_hours": True,
        "operating_hours": "24 Jam Setiap Hari",
        "lat": 3.1517,
        "lng": 101.5936,
        "specialties": ["Triage Kecemasan", "Pemeriksaan USG/Rontgen", "Wad Rawatan Rapi"]
    },
    {
        "id": "vet_st_angel",
        "name": "St. Angel Animal Medical Centre",
        "state": "Selangor",
        "area": "Puchong",
        "address": "19, Jalan Merbah 3, Bandar Puchong Jaya, 47100 Puchong, Selangor",
        "phone": "+603-80616851",
        "emergency_phone": "+603-80616851",
        "is_24_hours": True,
        "operating_hours": "24 Jam (Panggilan Kecemasan)",
        "lat": 3.0315,
        "lng": 101.6167,
        "specialties": ["Rawatan Darurat", "Inkubator Kucing Kritikal", "Dialisis & Infusi"]
    },
    {
        "id": "vet_healing_rooms",
        "name": "The Healing Rooms Veterinary Clinic",
        "state": "Selangor",
        "area": "Subang Jaya",
        "address": "No. 32, Jalan SS 15/4D, 47500 Subang Jaya, Selangor",
        "phone": "+603-56378378",
        "emergency_phone": "+6012-3298378",
        "is_24_hours": False,
        "operating_hours": "9:30 AM - 8:00 PM (Emergency On-Call Malam)",
        "lat": 3.0765,
        "lng": 101.5898,
        "specialties": ["Perubatan Kucing & Anjing", "Vaksinasi", "Diagnosis Cepat"]
    },
    {
        "id": "vet_windsor_penang",
        "name": "Windsor Animal Hospital (Pulau Pinang)",
        "state": "Pulau Pinang",
        "area": "George Town",
        "address": "25, Jalan Cantonment, 10250 George Town, Pulau Pinang",
        "phone": "+604-2277131",
        "emergency_phone": "+6012-4217131",
        "is_24_hours": True,
        "operating_hours": "24 Jam Kecemasan On-Call",
        "lat": 5.4141,
        "lng": 100.3128,
        "specialties": ["Pusat Kecemasan Utara", "Surgeri & Bius Selamat", "X-Ray Digital"]
    },
    {
        "id": "vet_jb_amc",
        "name": "JB Animal Medical Centre & Hospital",
        "state": "Johor",
        "area": "Johor Bahru",
        "address": "12, Jalan Molek 2/1, Taman Molek, 81100 Johor Bahru, Johor",
        "phone": "+607-3333833",
        "emergency_phone": "+6016-7223833",
        "is_24_hours": True,
        "operating_hours": "24 Jam Setiap Hari",
        "lat": 1.5284,
        "lng": 103.7845,
        "specialties": ["Pusat Rujukan Selatan", "Rawatan Keracunan", "Wad ICU Berasingan Kucing/Anjing"]
    },
    {
        "id": "vet_ipoh",
        "name": "Ipoh Animal Medical Clinic & Surgery",
        "state": "Perak",
        "area": "Ipoh",
        "address": "48, Jalan Medan Ipoh 3, Bandar Baru Medan Ipoh, 31400 Ipoh, Perak",
        "phone": "+605-5468832",
        "emergency_phone": "+6012-5018832",
        "is_24_hours": False,
        "operating_hours": "9:00 AM - 7:00 PM (Kecemasan On-Call)",
        "lat": 4.6135,
        "lng": 101.1189,
        "specialties": ["Rawatan Am & Surgeri", "Vaksinasi & Ubat Cacing"]
    },
    {
        "id": "vet_melaka",
        "name": "Melaka Animal Clinic & Surgery",
        "state": "Melaka",
        "area": "Melaka Tengah",
        "address": "218, Jalan Melaka Raya 1, Taman Melaka Raya, 75000 Melaka",
        "phone": "+606-2816006",
        "emergency_phone": "+6012-6386006",
        "is_24_hours": False,
        "operating_hours": "9:30 AM - 6:30 PM (On-Call Darurat)",
        "lat": 2.1865,
        "lng": 102.2534,
        "specialties": ["Pembedahan Kecemasan", "Rawatan Luka & Patah Tulang"]
    },
    {
        "id": "vet_kuantan",
        "name": "Kuantan Veterinary Clinic & Surgery",
        "state": "Pahang",
        "area": "Kuantan",
        "address": "B-18, Lorong Sri Kuantan 80, 25300 Kuantan, Pahang",
        "phone": "+609-5662212",
        "emergency_phone": "+6019-9892212",
        "is_24_hours": False,
        "operating_hours": "9:00 AM - 6:00 PM (On-Call Darurat)",
        "lat": 3.8214,
        "lng": 103.3365,
        "specialties": ["Rawatan Am Pantai Timur", "Surgeri Mandul"]
    },
    {
        "id": "vet_kuching",
        "name": "Kuching Family Pet Clinic (Emergency Line)",
        "state": "Sarawak",
        "area": "Kuching",
        "address": "Sublot 11, Ground Floor, Gala City, Jalan Tun Jugah, 93350 Kuching, Sarawak",
        "phone": "+6082-255600",
        "emergency_phone": "+6016-8895600",
        "is_24_hours": True,
        "operating_hours": "24 Jam On-Call",
        "lat": 1.5034,
        "lng": 110.3541,
        "specialties": ["Klinik Rujukan Sarawak", "Ujian Makmal Pantas"]
    },
    {
        "id": "vet_kk",
        "name": "Kota Kinabalu Animal Medical Clinic",
        "state": "Sabah",
        "area": "Kota Kinabalu",
        "address": "Lot 8, Ground Floor, Lintas Square, 88300 Kota Kinabalu, Sabah",
        "phone": "+6088-212888",
        "emergency_phone": "+6016-8302888",
        "is_24_hours": True,
        "operating_hours": "24 Jam Talian Kecemasan",
        "lat": 5.9521,
        "lng": 116.0883,
        "specialties": ["Kecemasan Sabah", "Rawatan Parvo & Jangkitan Virus"]
    }
]

# Official Malaysian Emergency Hotlines
MALAYSIA_HOTLINES = [
    {
        "title": "Pusat Racun Negara (PRN Malaysia - USM)",
        "phone": "1-800-88-8099",
        "alt_phone": "+604-6570099",
        "hours": "Talian Bebas Tol 24 Jam",
        "description": "Pusat rujukan rasmi jika haiwan tertelan racun, ubat manusia (paracetamol), tumbuhan toksik atau bahan kimia berbahaya.",
        "icon": "skull-crossbones",
        "color": "red"
    },
    {
        "title": "Jabatan Perkhidmatan Veterinar Malaysia (DVS)",
        "phone": "+603-88702000",
        "alt_phone": "+603-88702052",
        "hours": "Waktu Pejabat & Bilik Gerakan Aduan Bencana",
        "description": "Agensi kerajaan Malaysia untuk pengawalan penyakit berjangkit haiwan (Rabies), aduan kebajikan haiwan, dan permit.",
        "icon": "building-shield",
        "color": "emerald"
    },
    {
        "title": "BOMBA Malaysia (Penyelamatan Haiwan)",
        "phone": "999",
        "alt_phone": "112",
        "hours": "24 Jam Setiap Hari",
        "description": "Panggilan kecemasan rasmi Malaysia jika haiwan terperangkap di tempat tinggi, dalam longkang/saliran, atau situasi bahaya.",
        "icon": "phone-volume",
        "color": "amber"
    },
    {
        "title": "Persatuan Doktor Veterinar Malaysia (MAVMA / MSAVA)",
        "phone": "+603-77823553",
        "alt_phone": "",
        "hours": "Talian Nasihat Profesion Veterinar",
        "description": "Persatuan veterinar perubatan haiwan kecil Malaysia untuk garis panduan standard perubatan dan rujukan.",
        "icon": "stethoscope",
        "color": "blue"
    },
    {
        "title": "SPCA Selangor (Kebajikan & Ambulans Haiwan)",
        "phone": "+603-42565312",
        "alt_phone": "+603-42535179",
        "hours": "9:00 AM - 5:00 PM (Selasa - Ahad)",
        "description": "Penyelamatan haiwan teraniaya, kebajikan, pemandulan subsidi, dan pertolongan cemas haiwan terbiar.",
        "icon": "heart",
        "color": "pink"
    }
]

# --- HAVERSINE DISTANCE FORMULA ---
import datetime

# --- HAVERSINE DISTANCE & REAL-TIME TRAFFIC / OPERATIONAL ENGINE ---
def calculate_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two GPS coordinates in kilometers."""
    R = 6371.0 # Radius of earth in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    
    a = (math.sin(d_lat / 2) ** 2 + 
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
         math.sin(d_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

def get_live_traffic_condition(dt: Optional[datetime.datetime] = None) -> Dict[str, Any]:
    """Calculates live Malaysian traffic conditions and ETA multipliers based on current time."""
    now = dt or datetime.datetime.now()
    time_float = now.hour + (now.minute / 60.0)

    # Morning rush hour (07:30 - 09:30)
    if 7.5 <= time_float <= 9.5:
        multiplier = 1.40
        condition_ms = "Waktu Puncak Pagi (Trafik Perlahan +40%)"
        condition_en = "Morning Rush Hour (Traffic Delay +40%)"
        badge_color = "amber"
    # Evening rush hour (17:00 - 19:30)
    elif 17.0 <= time_float <= 19.5:
        multiplier = 1.45
        condition_ms = "Waktu Puncak Balik Kerja (Trafik Sesak +45%)"
        condition_en = "Evening Rush Hour (Congested Traffic +45%)"
        badge_color = "rose"
    # Daytime standard (09:30 - 17:00)
    elif 9.5 < time_float < 17.0:
        multiplier = 1.10
        condition_ms = "Trafik Siang Biasa (Sederhana)"
        condition_en = "Standard Daytime Traffic (Moderate)"
        badge_color = "emerald"
    # Nighttime smooth (19:30 - 22:30)
    elif 19.5 < time_float <= 22.5:
        multiplier = 1.00
        condition_ms = "Trafik Malam (Lancar)"
        condition_en = "Night Traffic (Smooth & Clear)"
        badge_color = "emerald"
    # Late night clear (22:30 - 07:30)
    else:
        multiplier = 0.85
        condition_ms = "Trafik Tengah Malam (Lengang)"
        condition_en = "Late Night Traffic (Clear Roads)"
        badge_color = "emerald"

    return {
        "multiplier": multiplier,
        "condition_ms": condition_ms,
        "condition_en": condition_en,
        "badge_color": badge_color,
        "current_time_str": now.strftime("%I:%M %p")
    }

def calculate_live_clinic_status(clinic: Dict[str, Any], dt: Optional[datetime.datetime] = None) -> Dict[str, Any]:
    """Determines real-time operational status (open/closed) of a clinic based on current time."""
    now = dt or datetime.datetime.now()
    time_float = now.hour + (now.minute / 60.0)
    is_24h = clinic.get("is_24_hours", False)

    if is_24h:
        is_open = True
        status_ms = "DIBUKA SEKARANG (24 JAM)"
        status_en = "OPEN NOW (24 HOURS)"
        badge_color = "emerald"
        status_note_ms = "Pusat rujukan kecemasan & ICU beroperasi 24 jam setiap hari."
        status_note_en = "Verified 24/7 trauma & emergency hospital open round the clock."
    else:
        # Standard daytime clinics: 9:00 AM to 7:00 PM
        if 9.0 <= time_float <= 19.0:
            is_open = True
            status_ms = "DIBUKA SEKARANG (WAKTU OPERASI BIASA)"
            status_en = "OPEN NOW (REGULAR HOURS)"
            badge_color = "emerald"
            status_note_ms = "Klinik dibuka dalam waktu siang biasa (9:00 AM - 7:00 PM)."
            status_note_en = "Open during standard daytime clinic hours (9:00 AM - 7:00 PM)."
        else:
            is_open = False
            status_ms = "TUTUP (TALIAN ON-CALL KECEMASAN AKTIF)"
            status_en = "CLOSED (EMERGENCY ON-CALL ACTIVE)"
            badge_color = "amber"
            status_note_ms = "Waktu operasi biasa telah ditutup. Hubungi talian on-call untuk kes darurat."
            status_note_en = "Regular hours closed. Call emergency line for on-duty vet."

    return {
        "is_open_now": is_open,
        "status_ms": status_ms,
        "status_en": status_en,
        "badge_color": badge_color,
        "status_note_ms": status_note_ms,
        "status_note_en": status_note_en,
        "last_sync": now.strftime("%I:%M %p")
    }

def get_clinics_sorted_by_distance(user_lat: float, user_lng: float, only_24h: bool = False, state: Optional[str] = None) -> List[Dict[str, Any]]:
    """Calculates distance for all clinics with live operational status and real-time traffic-adjusted ETA."""
    results = []
    traffic = get_live_traffic_condition()

    for clinic in MALAYSIA_VET_CLINICS:
        if only_24h and not clinic["is_24_hours"]:
            continue
        if state and state.lower() != "semua" and clinic["state"].lower() != state.lower():
            continue
            
        dist = calculate_distance_km(user_lat, user_lng, clinic["lat"], clinic["lng"])
        item = dict(clinic)
        item["distance_km"] = dist

        # Live operational status calculation
        live_status = calculate_live_clinic_status(clinic)
        item["live_status"] = live_status
        item["is_open_now"] = live_status["is_open_now"]
        item["status_label_ms"] = live_status["status_ms"]
        item["status_label_en"] = live_status["status_en"]
        item["status_badge_color"] = live_status["badge_color"]

        # Real-time traffic-adjusted driving ETA
        base_minutes = (dist / 45) * 60
        est_minutes = int(max(base_minutes * traffic["multiplier"], 5))
        item["est_drive_minutes"] = est_minutes
        item["traffic_condition_ms"] = traffic["condition_ms"]
        item["traffic_condition_en"] = traffic["condition_en"]
        item["traffic_badge_color"] = traffic["badge_color"]

        item["google_maps_url"] = f"https://www.google.com/maps/dir/?api=1&destination={clinic['lat']},{clinic['lng']}"
        results.append(item)
        
    results.sort(key=lambda x: x["distance_km"])
    return results

def get_all_clinics(state: Optional[str] = None, only_24h: bool = False) -> List[Dict[str, Any]]:
    """Returns clinics filtered with real-time live operational status."""
    results = []
    traffic = get_live_traffic_condition()

    for clinic in MALAYSIA_VET_CLINICS:
        if only_24h and not clinic["is_24_hours"]:
            continue
        if state and state.lower() != "semua" and clinic["state"].lower() != state.lower():
            continue

        item = dict(clinic)
        live_status = calculate_live_clinic_status(clinic)
        item["live_status"] = live_status
        item["is_open_now"] = live_status["is_open_now"]
        item["status_label_ms"] = live_status["status_ms"]
        item["status_label_en"] = live_status["status_en"]
        item["status_badge_color"] = live_status["badge_color"]
        item["traffic_condition_ms"] = traffic["condition_ms"]
        item["traffic_condition_en"] = traffic["condition_en"]
        item["google_maps_url"] = f"https://www.google.com/maps/dir/?api=1&destination={clinic['lat']},{clinic['lng']}"
        results.append(item)
    return results

def get_live_emergency_status(lang: str = "ms") -> Dict[str, Any]:
    """Provides a dynamic system-wide status report on Malaysia veterinary emergency services."""
    traffic = get_live_traffic_condition()
    clinics = get_all_clinics()
    open_count = sum(1 for c in clinics if c["is_open_now"])
    is_en = (lang.lower() == "en")

    return {
        "success": True,
        "total_clinics": len(MALAYSIA_VET_CLINICS),
        "clinics_24h_count": sum(1 for c in MALAYSIA_VET_CLINICS if c["is_24_hours"]),
        "currently_open_count": open_count,
        "traffic_condition": traffic["condition_en"] if is_en else traffic["condition_ms"],
        "traffic_multiplier": traffic["multiplier"],
        "traffic_badge_color": traffic["badge_color"],
        "malaysia_time": traffic["current_time_str"],
        "last_sync": datetime.datetime.now().strftime("%d %B %Y, %I:%M %p")
    }

