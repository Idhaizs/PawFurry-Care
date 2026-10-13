import os
import datetime
from flask import Flask, request, jsonify, render_template, g
from flask_cors import CORS

from config import Config
from database import (
    init_db, create_user, get_user_by_username_or_email, get_user_by_id,
    create_pet, get_user_pets, get_pet_by_id, update_pet, delete_pet,
    save_chat_message, get_chat_history
)
from security import (
    hash_password, verify_password, generate_jwt_token,
    token_required, optional_token, rate_limit,
    sanitize_text, validate_email, validate_password_strength,
    apply_security_headers
)
from emergency_data import (
    MALAYSIA_VET_CLINICS, MALAYSIA_HOTLINES,
    get_clinics_sorted_by_distance, get_all_clinics,
    get_live_emergency_status
)
from triage_engine import (
    TOXIC_SUBSTANCES, get_live_toxin_catalog, get_seasonal_toxin_advisory
)
from chat_service import get_chatbot_reply, get_seasonal_bot_advisory
from news_data import get_all_news, get_news_by_id, refresh_live_advisories

# Initialize Flask App
app = Flask(__name__, static_folder="static", template_folder="templates")
app.config.from_object(Config)

# Enable CORS for secure cross-origin API integration if needed
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Apply Security Headers Middleware
@app.after_request
def security_middleware(response):
    return apply_security_headers(response)

# --- FRONTEND ROUTE ---
@app.route("/")
def index():
    return render_template("index.html")

# --- AUTHENTICATION APIS ---
@app.route("/api/auth/register", methods=["POST"])
@rate_limit(Config.RATE_LIMIT_REGISTER)
def register():
    data = request.get_json(silent=True) or {}
    username = sanitize_text(data.get("username", ""), max_length=50)
    email = sanitize_text(data.get("email", ""), max_length=100)
    password = data.get("password", "")
    full_name = sanitize_text(data.get("full_name", ""), max_length=100)
    phone = sanitize_text(data.get("phone_number", ""), max_length=20)

    if not username or len(username) < 3:
        return jsonify({"success": False, "error": "Nama pengguna mestilah sekurang-kurangnya 3 aksara."}), 400

    if not validate_email(email):
        return jsonify({"success": False, "error": "Format emel tidak sah."}), 400

    is_valid, msg = validate_password_strength(password)
    if not is_valid:
        return jsonify({"success": False, "error": msg}), 400

    existing = get_user_by_username_or_email(username)
    if existing:
        return jsonify({"success": False, "error": "Nama pengguna atau emel ini telah didaftarkan."}), 400

    hashed_pw = hash_password(password)
    user_id = create_user(username, email, hashed_pw, full_name, phone)
    if not user_id:
        return jsonify({"success": False, "error": "Gagal mendaftar pengguna. Sila cuba lagi."}), 500

    token = generate_jwt_token(user_id, username, email)
    return jsonify({
        "success": True,
        "message": "Pendaftaran berjaya!",
        "token": token,
        "user": {
            "id": user_id,
            "username": username,
            "email": email,
            "full_name": full_name
        }
    }), 201

@app.route("/api/auth/login", methods=["POST"])
@rate_limit(Config.RATE_LIMIT_LOGIN)
def login():
    data = request.get_json(silent=True) or {}
    identifier = sanitize_text(data.get("identifier", ""), max_length=100)
    password = data.get("password", "")

    if not identifier or not password:
        return jsonify({"success": False, "error": "Sila masukkan nama pengguna/emel dan kata laluan."}), 400

    user = get_user_by_username_or_email(identifier)
    if not user or not verify_password(password, user["password_hash"]):
        return jsonify({"success": False, "error": "Nama pengguna atau kata laluan tidak tepat."}), 401

    token = generate_jwt_token(user["id"], user["username"], user["email"])
    return jsonify({
        "success": True,
        "message": "Log masuk berjaya!",
        "token": token,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "full_name": user["full_name"],
            "phone_number": user["phone_number"]
        }
    }), 200

@app.route("/api/auth/me", methods=["GET"])
@token_required
def get_current_user_profile():
    user = get_user_by_id(g.current_user["id"])
    if not user:
        return jsonify({"success": False, "error": "Pengguna tidak ditemui."}), 404
    return jsonify({"success": True, "user": user})

# --- PET CRUD APIS ---
@app.route("/api/pets", methods=["GET"])
@token_required
def list_pets():
    pets = get_user_pets(g.current_user["id"])
    return jsonify({"success": True, "pets": pets})

@app.route("/api/pets", methods=["POST"])
@token_required
def add_pet():
    data = request.get_json(silent=True) or {}
    name = sanitize_text(data.get("name", ""), max_length=50)
    if not name:
        return jsonify({"success": False, "error": "Nama haiwan peliharaan wajib diisi."}), 400

    clean_data = {
        "name": name,
        "species": sanitize_text(data.get("species", "Kucing"), max_length=30),
        "breed": sanitize_text(data.get("breed", ""), max_length=50),
        "age_years": int(data.get("age_years", 0) or 0),
        "age_months": int(data.get("age_months", 0) or 0),
        "weight_kg": float(data.get("weight_kg", 0.0) or 0.0),
        "gender": sanitize_text(data.get("gender", "Jantan"), max_length=30),
        "is_neutered": bool(data.get("is_neutered", False)),
        "allergies": sanitize_text(data.get("allergies", ""), max_length=255),
        "medical_history": sanitize_text(data.get("medical_history", ""), max_length=500),
        "emergency_notes": sanitize_text(data.get("emergency_notes", ""), max_length=500)
    }

    pet_id = create_pet(g.current_user["id"], clean_data)
    created_pet = get_pet_by_id(pet_id, g.current_user["id"])
    return jsonify({"success": True, "message": "Profil haiwan berjaya dicipta!", "pet": created_pet}), 201

@app.route("/api/pets/<int:pet_id>", methods=["GET"])
@token_required
def get_single_pet(pet_id: int):
    pet = get_pet_by_id(pet_id, g.current_user["id"])
    if not pet:
        return jsonify({"success": False, "error": "Profil haiwan tidak dijumpai."}), 404
    return jsonify({"success": True, "pet": pet})

@app.route("/api/pets/<int:pet_id>", methods=["PUT"])
@token_required
def edit_pet(pet_id: int):
    data = request.get_json(silent=True) or {}
    name = sanitize_text(data.get("name", ""), max_length=50)
    if not name:
        return jsonify({"success": False, "error": "Nama haiwan wajib diisi."}), 400

    clean_data = {
        "name": name,
        "species": sanitize_text(data.get("species", "Kucing"), max_length=30),
        "breed": sanitize_text(data.get("breed", ""), max_length=50),
        "age_years": int(data.get("age_years", 0) or 0),
        "age_months": int(data.get("age_months", 0) or 0),
        "weight_kg": float(data.get("weight_kg", 0.0) or 0.0),
        "gender": sanitize_text(data.get("gender", "Jantan"), max_length=30),
        "is_neutered": bool(data.get("is_neutered", False)),
        "allergies": sanitize_text(data.get("allergies", ""), max_length=255),
        "medical_history": sanitize_text(data.get("medical_history", ""), max_length=500),
        "emergency_notes": sanitize_text(data.get("emergency_notes", ""), max_length=500)
    }

    updated = update_pet(pet_id, g.current_user["id"], clean_data)
    if not updated:
        return jsonify({"success": False, "error": "Gagal mengemaskini profil atau haiwan tidak wujud."}), 404

    return jsonify({"success": True, "message": "Profil haiwan berjaya dikemaskini!", "pet": get_pet_by_id(pet_id, g.current_user["id"])})

@app.route("/api/pets/<int:pet_id>", methods=["DELETE"])
@token_required
def remove_pet(pet_id: int):
    deleted = delete_pet(pet_id, g.current_user["id"])
    if not deleted:
        return jsonify({"success": False, "error": "Haiwan tidak ditemui atau anda tiada kebenaran."}), 404
    return jsonify({"success": True, "message": "Profil haiwan berjaya dipadam."})

# --- CHATBOT APIS ---
@app.route("/api/chat", methods=["POST"])
@rate_limit(Config.RATE_LIMIT_CHAT)
@optional_token
def chat():
    data = request.get_json(silent=True) or {}
    raw_message = data.get("message", "")
    message = sanitize_text(raw_message, max_length=1000)
    pet_id = data.get("pet_id", None)

    if not message:
        return jsonify({"success": False, "error": "Sila masukkan mesej anda."}), 400

    # Retrieve pet context if pet_id provided and user is authenticated
    pet_context = None
    if pet_id and g.current_user:
        pet_context = get_pet_by_id(int(pet_id), g.current_user["id"])

    # If no authenticated pet found, fallback to guest sample pet or custom payload
    if not pet_context and data.get("guest_pet"):
        pet_context = data.get("guest_pet")

    # Extract optional language preference
    lang = data.get("lang", None)

    # Generate chatbot response
    bot_result = get_chatbot_reply(message, pet_context=pet_context, requested_lang=lang)

    # Save to history if user is authenticated
    if g.current_user:
        save_chat_message(
            user_id=g.current_user["id"],
            pet_id=pet_context["id"] if pet_context else None,
            sender="user",
            message=message
        )
        save_chat_message(
            user_id=g.current_user["id"],
            pet_id=pet_context["id"] if pet_context else None,
            sender="bot",
            message=bot_result["reply"],
            is_emergency=bot_result["is_emergency"],
            triage_level=bot_result["triage_level"]
        )

    return jsonify({
        "success": True,
        "reply": bot_result["reply"],
        "is_emergency": bot_result["is_emergency"],
        "triage_level": bot_result["triage_level"],
        "triage_details": bot_result.get("triage_details", {})
    })

@app.route("/api/chat/history", methods=["GET"])
@token_required
def chat_history():
    pet_id = request.args.get("pet_id", type=int)
    history = get_chat_history(g.current_user["id"], pet_id=pet_id)
    return jsonify({"success": True, "history": history})

# --- EMERGENCY & MALAYSIA CLINIC DIRECTORY APIS ---
@app.route("/api/emergency/clinics", methods=["GET"])
def list_clinics():
    state = request.args.get("state", default=None)
    only_24h = request.args.get("only_24h", default="false").lower() == "true"
    clinics = get_all_clinics(state=state, only_24h=only_24h)
    return jsonify({"success": True, "count": len(clinics), "clinics": clinics})

@app.route("/api/emergency/nearby", methods=["GET"])
def nearby_clinics():
    try:
        lat = float(request.args.get("lat"))
        lng = float(request.args.get("lng"))
    except (TypeError, ValueError):
        return jsonify({"success": False, "error": "Koordinat latitud & longitud (lat, lng) diperlukan."}), 400

    only_24h = request.args.get("only_24h", default="false").lower() == "true"
    state = request.args.get("state", default=None)

    sorted_clinics = get_clinics_sorted_by_distance(lat, lng, only_24h=only_24h, state=state)
    return jsonify({
        "success": True,
        "user_coords": {"lat": lat, "lng": lng},
        "count": len(sorted_clinics),
        "clinics": sorted_clinics
    })

@app.route("/api/emergency/hotlines", methods=["GET"])
def list_hotlines():
    return jsonify({"success": True, "hotlines": MALAYSIA_HOTLINES})

@app.route("/api/emergency/toxins", methods=["GET"])
def list_toxins():
    lang = request.args.get("lang", default="ms")
    return jsonify(get_live_toxin_catalog(lang=lang))

@app.route("/api/emergency/status", methods=["GET"])
def emergency_status():
    lang = request.args.get("lang", default="ms")
    return jsonify(get_live_emergency_status(lang=lang))

# --- MALAYSIA PET CARE NEWS & ADVISORIES APIS ---
@app.route("/api/news", methods=["GET"])
def list_news():
    category = request.args.get("category", default=None)
    search_query = request.args.get("search", default=None)
    lang = request.args.get("lang", default="ms")
    news_items = get_all_news(category=category, search_query=search_query, lang=lang)
    return jsonify({"success": True, "count": len(news_items), "news": news_items, "lang": lang})

@app.route("/api/news/<string:news_id>", methods=["GET"])
def single_news(news_id: str):
    lang = request.args.get("lang", default="ms")
    article = get_news_by_id(news_id, lang=lang)
    if not article:
        return jsonify({"success": False, "error": "Artikel tidak dijumpai."}), 404
    return jsonify({"success": True, "article": article, "lang": lang})

@app.route("/api/news/refresh", methods=["POST"])
def refresh_news():
    result = refresh_live_advisories()
    return jsonify(result)

# --- UNIFIED SYSTEM-WIDE LIVE AUTO-SYNC APIS ---
@app.route("/api/system/sync", methods=["POST", "GET"])
def system_sync():
    """
    Unified master synchronization endpoint for PawFurry Care.
    Auto-updates & syncs all 4 system pillars simultaneously:
    1. Chatbot Seasonal Knowledge & Triage Guard
    2. Malaysia 24H Emergency Clinics & Real-Time Traffic ETA
    3. Live Seasonal Poison & Toxin Advisory
    4. Official Pet Care News & Bulletins
    """
    lang = request.args.get("lang", default="ms")

    # 1. Refresh Live News Bulletins
    news_sync = refresh_live_advisories()

    # 2. Live Clinic & Traffic Operational Status
    clinic_sync = get_live_emergency_status(lang=lang)

    # 3. Live Seasonal Poison & Toxin Catalog
    toxin_sync = get_live_toxin_catalog(lang=lang)

    # 4. Live Seasonal Chatbot Context
    bot_sync = get_seasonal_bot_advisory(lang=lang)

    now_iso = datetime.datetime.now().isoformat()
    now_formatted = datetime.datetime.now().strftime("%d %B %Y, %I:%M:%S %p")

    return jsonify({
        "success": True,
        "message": "Semua sistem PawFurry Care telah diselaraskan secara langsung!" if lang == "ms" else "All PawFurry Care systems successfully synchronized in real time!",
        "timestamp": now_iso,
        "formatted_time": now_formatted,
        "modules": {
            "chatbot": {
                "status": "synchronized",
                "scope": "Strict Cats & Dogs (Kucing & Anjing Sahaja)",
                "season": bot_sync["season"],
                "last_sync": bot_sync["last_sync"]
            },
            "emergency_clinics": {
                "status": "synchronized",
                "total_clinics": clinic_sync["total_clinics"],
                "clinics_24h": clinic_sync["clinics_24h_count"],
                "open_now_count": clinic_sync["currently_open_count"],
                "traffic_condition": clinic_sync["traffic_condition"],
                "traffic_multiplier": clinic_sync["traffic_multiplier"],
                "traffic_badge_color": clinic_sync["traffic_badge_color"],
                "last_sync": clinic_sync["last_sync"]
            },
            "toxins": {
                "status": "synchronized",
                "total_substances": toxin_sync["total_substances"],
                "active_season": toxin_sync["seasonal_advisory"]["season_name"],
                "hazard_title": toxin_sync["seasonal_advisory"]["hazard_title"],
                "last_sync": toxin_sync["last_synced"]
            },
            "news": {
                "status": "synchronized",
                "live_alerts_count": news_sync.get("live_alerts_count", 0),
                "last_sync": news_sync.get("last_synced")
            }
        }
    })

# --- HEALTH CHECK ---
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "PawFurry Care Malaysia API", "version": "1.2.0"})

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    print(f"[RUNNING] PawFurry Care Malaysia Server Running at http://127.0.0.1:{port}")
    app.run(host="127.0.0.1", port=port, debug=True)
