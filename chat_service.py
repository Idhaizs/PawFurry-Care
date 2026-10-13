import os
import re
import datetime
from typing import Dict, Any, Optional, Tuple
from triage_engine import analyze_emergency_triage, TOXIC_SUBSTANCES
from config import Config

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

# --- STRICT DOMAIN GUARDRAILS (CATS & DOGS ONLY) ---
CAT_DOG_KEYWORDS = [
    # Cat terms
    "kucing", "kucingku", "oyen", "si bulu", "si comel", "meow", "meong", "cat", "cats", "kitten", "kittens", "kitty", "feline",
    # Dog terms
    "anjing", "anjingku", "puppy", "puppies", "dog", "dogs", "canine", "pooch", "pup",
    # Common cat/dog breeds in Malaysia
    "persian", "bsh", "british shorthair", "mainecoon", "maine coon", "siamese", "sphynx", "ragdoll", "kampung",
    "retriever", "poodle", "husky", "corgi", "pomeranian", "shih tzu", "rottweiler", "shepherd", "pug", "bulldog"
]

PET_CARE_KEYWORDS = [
    # General pet medical & wellness terms
    "pet", "pets", "haiwan peliharaan", "vet", "veterinar", "veterinary", "klinik", "hospital",
    "vaksin", "vaccin", "vaccine", "vaccination", "cucuk", "booster",
    "cacing", "deworm", "deworming", "drontal", "milbemax",
    "kutu", "flea", "tick", "ear mite", "hama", "spot-on", "revolution", "advocate", "frontline", "nexgard", "bravecto",
    "mandul", "kembiri", "neuter", "spay", "steril",
    "kibble", "wet food", "wetfood", "pasir", "litter", "litterbox", "hairball",
    "sporo", "sporotrichosis", "parvo", "parvovirus", "distemper", "flutd", "bloat", "gdv", "pyometra", "fip", "felv",
    "strok haba", "heatstroke", "kurap", "fungus", "ringworm", "scabies", "rabies"
]

OTHER_ANIMALS_KEYWORDS = [
    "burung", "bird", "birds", "parrot", "unggas",
    "ikan", "fish", "ikan laga", "betta", "aquarium",
    "arnab", "rabbit", "bunny", "hamster", "guinea pig",
    "kura-kura", "turtle", "tortoise", "iguana", "ular", "snake", "cicak",
    "lembu", "cow", "kambing", "goat", "kuda", "horse", "babi hutan", "monyet", "monkey"
]

GREETING_KEYWORDS = [
    "hai", "hello", "hi", "hey", "assalamualaikum", "salam", "selamat pagi", "selamat petang", "selamat malam",
    "good morning", "good afternoon", "good evening", "siapa anda", "who are you", "fungsi anda", "what can you do"
]

def check_cat_dog_domain(user_message: str, lang: str = "ms") -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Strictly verifies that user inquiry is relevant to Cats (kucing) and Dogs (anjing).
    Returns (is_allowed, refusal_message_ms, refusal_message_en).
    """
    msg_lower = user_message.lower().strip()

    # 1. First check if it's an emergency trigger (triage) or emergency toxin keyword
    critical_emergency_words = [
        "panadol", "paracetamol", "lili", "lily", "coklat", "chocolate", "racun", "poison", "toxic",
        "tak boleh kencing", "cannot pee", "kencing berdarah", "bloat", "gdv", "sawan", "seizure",
        "muntah buih", "vomiting foam", "sesak nafas", "tercekik", "choking", "terlanggar", "hit by car",
        "ubat nyamuk", "katak puru", "racun siput", "anggur", "kismis", "raisin"
    ]
    if any(w in msg_lower for w in critical_emergency_words):
        return True, None, None

    # 2. Check if cat or dog keywords are present
    has_cat_or_dog = any(re.search(r'\b' + re.escape(w) + r'\b', msg_lower) for w in CAT_DOG_KEYWORDS)

    # 3. Check if pet care / veterinary keywords are present
    has_pet_care = any(re.search(r'\b' + re.escape(w) + r'\b', msg_lower) for w in PET_CARE_KEYWORDS)

    # 4. Check if greetings
    is_greeting = any(re.search(r'\b' + re.escape(w) + r'\b', msg_lower) for w in GREETING_KEYWORDS) and len(msg_lower.split()) <= 4

    # 5. Check if asking about OTHER animals (and NOT mentioning cat/dog)
    has_other_animals = any(re.search(r'\b' + re.escape(w) + r'\b', msg_lower) for w in OTHER_ANIMALS_KEYWORDS)

    if has_other_animals and not has_cat_or_dog:
        refusal_ms = (
            "🐾 **Maaf ya, sistem PawFurry Care dikhususkan khas untuk penjagaan Kucing dan Anjing sahaja.**\n\n"
            "Buat masa ini, kami tidak menyokong panduan klinikal untuk spesies lain seperti burung, ikan, arnab, atau reptilia.\n\n"
            "Sila ajukan sebarang persoalan berkaitan kesihatan, pemakanan, vaksinasi, atau kecemasan **kucing atau anjing** anda!"
        )
        refusal_en = (
            "🐾 **I apologize, but PawFurry Care is exclusively dedicated to Cats and Dogs.**\n\n"
            "We currently do not cover clinical advice for other species such as birds, fish, rabbits, or reptiles.\n\n"
            "Please feel free to ask any questions regarding your **cat or dog's** health, diet, vaccines, or emergencies!"
        )
        return False, refusal_ms, refusal_en

    # If greeting, allow through to welcome message
    if is_greeting:
        return True, None, None

    # If cat/dog or pet care keyword is present, allowed!
    if has_cat_or_dog or has_pet_care:
        return True, None, None

    # Otherwise, it is completely OUT OF DOMAIN (e.g. "nasi lemak", "resepi masakan", "coding", "politik", etc.)
    refusal_ms = (
        "🐾 **Maaf ya, saya adalah pembantu maya khusus untuk penjagaan Kucing & Anjing sahaja.**\n\n"
        "Saya tidak dapat menjawab pertanyaan mengenai topik luar seperti makanan manusia (*cth: nasi lemak*), resepi masakan, hal ehwal am, cuaca manusia, politik, atau pengaturcaraan.\n\n"
        "Sila ajukan sebarang soalan berkaitan:\n"
        "- 🐱 **Kesihatan & Penjagaan Kucing** (Vaksin Tricat, ubat kutu/cacing, pemandulan, FLUTD)\n"
        "- 🐶 **Kesihatan & Penjagaan Anjing** (Nutrisi, vaksin 6-in-1, pencegahan penyakit, latihan)\n"
        "- 🚨 **Triage Kecemasan & Keracunan** (Tanda-tanda bahaya & hospital vet 24 jam di Malaysia)\n\n"
        "*Ada apa-apa soalan mengenai kucing atau anjing anda yang boleh saya bantu?*"
    )
    refusal_en = (
        "🐾 **I apologize, but I am a digital veterinary assistant dedicated exclusively to Cats & Dogs.**\n\n"
        "I cannot answer queries regarding off-topic subjects such as human food (*e.g., nasi lemak*), cooking recipes, general trivia, politics, or coding.\n\n"
        "Please feel free to ask about:\n"
        "- 🐱 **Cat Health & Care** (Vaccinations, fleas, deworming, spaying, urinary blockage)\n"
        "- 🐶 **Dog Health & Care** (Canine nutrition, DHPPi vaccines, disease prevention)\n"
        "- 🚨 **Emergency Triage & Toxicity** (Warning symptoms & 24-hour veterinary hospitals across Malaysia)\n\n"
        "*How can I assist you with your cat or dog today?*"
    )
    return False, refusal_ms, refusal_en


# --- DYNAMIC SEASONAL ADVISORY ENGINE ---
def get_seasonal_bot_advisory(lang: str = "ms") -> Dict[str, Any]:
    """Generates dynamic seasonal veterinary alerts injected into chatbot conversations."""
    month = datetime.datetime.now().month
    is_en = (lang.lower() == "en")

    if month in [10, 11, 12, 1]:
        season = "Monsoon Season (Okt - Jan)" if not is_en else "Monsoon Season (Oct - Jan)"
        alert_text = (
            "⚠️ **Live Alert Musim Monsun & Hujan Tropika:**\n"
            "- Waspada jangkitan kurap (*Ringworm*) dan Sporotrichosis (*Sporo*) akibat kelembapan tinggi.\n"
            "- Elakkan haiwan minum lopak air hujan untuk cegah kencing tikus (*Leptospirosis*).\n"
            "- Awas katak puru beracun yang kerap keluar di perkarangan rumah waktu malam!"
            if not is_en else
            "⚠️ **Live Monsoon & Rain Season Alert:**\n"
            "- Heightened risk of fungal infections (*Ringworm*) and Sporotrichosis (*Sporo*) due to humidity.\n"
            "- Prevent pets from drinking standing rainwater puddles (*Leptospirosis* risk).\n"
            "- Watch out for nocturnal toxic Asian common toads outdoors!"
        )
    elif month in [2, 3, 4, 5]:
        season = "Hot Weather & Festive (Feb - Mei)" if not is_en else "Hot Weather & Festive (Feb - May)"
        alert_text = (
            "⚠️ **Live Alert Musim Panas & Perayaan:**\n"
            "- Sediakan air bersih mengalir untuk elak strok haba & masalah batu karang.\n"
            "- Jauhkan biskut coklat dan sisa lauk rendang/bawang daripada haiwan peliharaan."
            if not is_en else
            "⚠️ **Live Heatwave & Holiday Alert:**\n"
            "- Provide ample fresh water to prevent heatstroke and urinary blockage.\n"
            "- Keep holiday chocolates and table scraps containing onions away from pets."
        )
    else:
        season = "Tropical Summer & Flea Peak (Jun - Sep)" if not is_en else "Tropical Summer & Flea Peak (Jun - Sep)"
        alert_text = (
            "⚠️ **Live Alert Kawalan Parasit & Cuaca Panas:**\n"
            "- Waktu puncak pembiakan kutu, pinjal & hama telinga. Pastikan ubat titik tengkuk (spot-on) mengikut jadual."
            if not is_en else
            "⚠️ **Live Parasite Control Alert:**\n"
            "- Peak season for fleas, ticks, and ear mites. Keep monthly spot-on treatments up to date."
        )

    return {
        "season": season,
        "alert_text": alert_text,
        "last_sync": datetime.datetime.now().strftime("%d %B %Y, %I:%M %p")
    }


# --- BILINGUAL VETERINARY KNOWLEDGE BASE (MALAYSIAN CONTEXT) ---
VET_KNOWLEDGE_TOPICS_MS = {
    "vaksin": (
        "### 💉 Panduan Jadual Vaksinasi di Malaysia\n\n"
        "**Untuk Kucing:**\n"
        "- **Vaksin Teras (Tricat / FVRCP):** Panleukopenia, Calicivirus, Herpesvirus.\n"
        "  - **Dos 1:** Umur 6 - 8 minggu.\n"
        "  - **Dos 2 (Booster):** Umur 10 - 12 minggu.\n"
        "  - **Dos 3:** Umur 14 - 16 minggu.\n"
        "  - **Booster Tahunan:** 1 dos setiap tahun.\n"
        "- **Vaksin Rabies:** Wajib jika di zon kawalan Rabies (Perlis, Kedah, Pulau Pinang, atau Sarawak).\n\n"
        "**Untuk Anjing:**\n"
        "- **Vaksin Teras (DHPPi/L - 6 in 1 / 7 in 1):** Bermula umur 6-8 minggu (siri 3 dos selang sebulan), diikuti booster tahunan."
    ),
    "cacing": (
        "### 🪱 Jadual Ubat Cacing (Deworming) Haiwan\n\n"
        "- **Anak Haiwan (Bawah 3 Bulan):** Beri ubat cacing setiap 2 minggu sehingga umur 12 minggu.\n"
        "- **Umur 3 hingga 6 Bulan:** Beri sebulan sekali.\n"
        "- **Haiwan Dewasa (6 Bulan ke atas):** Beri secara rutin setiap **3 bulan sekali**.\n"
        "- **Jenama Popular di Vet Malaysia:** Drontal Cat, Drontal Plus Dog, Milbemax (dos mengikut berat kg!)."
    ),
    "kutu": (
        "### 🐜 Kawalan Kutu & Hama Telinga (Fleas, Ticks & Ear Mites)\n\n"
        "- **Ubat Titik Tengkuk (Spot-on):**\n"
        "  - **Kucing:** Revolution Plus, Advocate, Broadline, Frontline Plus.\n"
        "  - **Anjing:** NexGard Spectra (kunyah), Bravecto (tahan 3 bulan), Simparica.\n"
        "- **Peringatan Keselamatan:** JANGAN sesekali menggunakan ubat kutu anjing pada kucing! Bahan *Permethrin* dalam ubat anjing adalah racun maut bagi saraf kucing."
    ),
    "makanan": (
        "### 🥩 Nutrisi & Diet Sihat Mengikut Iklim Malaysia\n\n"
        "- **Kucing:** *Obligate carnivore* (perlukan taurine dan protein haiwan). Elakkan nasi campur ikan bilis masin kerana merosakkan buah pinggang dan menyebabkan batu karang.\n"
        "- **Air Minuman:** Pastikan air bersih sentiasa ada. Penggunaan *water fountain* digalakkan untuk elak batu karang pundi kencing (FLUTD).\n"
        "- **Anjing:** Jangan beri tulang ayam masak kerana rapuh dan boleh mencucuk usus."
    ),
    "mandul": (
        "### ✂️ Pembedahan Pemandulan (Neutering / Spaying)\n\n"
        "- **Umur Sesuai:** Bermula 5 hingga 6 bulan ke atas (berat minima 2kg).\n"
        "- **Kelebihan:** Betina terlindung daripada kanser payudara dan jangkitan nanah rahim (*Pyometra*). Jantan berhenti tabiat menanda kawasan (*spraying*) dan pergaduhan."
    ),
    "strok haba": (
        "### ☀️ Pencegahan Strok Haba (Heatstroke) di Malaysia\n\n"
        "- Cuaca terik Malaysia berisiko tinggi terutamanya baka kemek (Persian, BSH, Pug, French Bulldog).\n"
        "- **Pertolongan Cemas:** Basahkan badan haiwan dengan **air paip suhu bilik biasa** (JANGAN guna air batu) dan hidupkan kipas/aircond sambil segera ke klinik."
    ),
    "nasi lemak": (
        "### ❌ Adakah Kucing / Anjing Boleh Makan Nasi Lemak?\n\n"
        "**Jawapan Pakar Veterinar: SANGAT TIDAK DIGALAKKAN / BERBAHAYA!**\n\n"
        "Walaupun nasi lemak enak untuk manusia, ia membawa risiko kesihatan serius kepada kucing dan anjing:\n\n"
        "1. 🥥 **Santan Kelapa:** Mengandungi asid lemak tepu yang sangat tinggi. Sistem penghadaman karnivor si bulu sukar menghadam santan, menyebabkan cirit-birit berair teruk dan radang pankreas akut (*pancreatitis*).\n"
        "2. 🌶️ **Sambal & Cili:** Mengandungi *capsaicin* yang membakar dinding perut, mengakibatkan muntah dan radang saluran usus.\n"
        "3. 🧅 **Bawang Merah & Bawang Putih:** Bahan wajib dalam sambal nasi lemak adalah **racun toksik** bagi sel darah merah kucing dan anjing (merosakkan hemoglobin / *Heinz body hemolytic anemia*).\n"
        "4. 🐟 **Ikan Bilis Masin & Kacang:** Terlalu tinggi garam dan natrium. Garam berlebihan membebankan buah pinggang dan boleh memicu batu karang pundi kencing (FLUTD).\n\n"
        "💡 **Saranan Vet:** Sekiranya ingin memberi ganjaran kepada si comel, sediakan ayam rebus tanpa garam/bawang atau kibble berkualiti tinggi!"
    ),
    "sporo": (
        "### 🦠 Wabak Sporotrichosis (Sporo) Kucing di Malaysia\n\n"
        "- **Punca:** Jangkitan kulat *Sporothrix schenckii* daripada tanah lembap atau luka cakaran/gigitan kucing liar.\n"
        "- **Simptom:** Luka berdarah berkerak pada hidung, telinga, atau kaki yang tidak sembuh dan makin merebak.\n"
        "- **Zoonotik:** Boleh berjangkit kepada manusia! Pakai sarung tangan ketika merawat haiwan dijangkiti.\n"
        "- **Rawatan:** Memerlukan ubat antikulat khas veterinar (Itraconazole) selama beberapa bulan di bawah seliaan doktor vet."
    )
}

VET_KNOWLEDGE_TOPICS_EN = {
    "vaksin": (
        "### 💉 Vaccination Schedule Guidelines in Malaysia\n\n"
        "**For Cats:**\n"
        "- **Core Vaccine (Tricat / FVRCP):** Feline Panleukopenia, Calicivirus, Herpesvirus.\n"
        "  - **Dose 1:** 6 - 8 weeks old.\n"
        "  - **Dose 2 (Booster):** 10 - 12 weeks old.\n"
        "  - **Dose 3:** 14 - 16 weeks old.\n"
        "  - **Annual Booster:** Once every year.\n"
        "- **Rabies Vaccine:** Mandatory in rabies surveillance zones (Sarawak, Perlis, Kedah, Penang).\n\n"
        "**For Dogs:**\n"
        "- **Core Vaccine (DHPPi/L - 6 in 1 / 7 in 1):** Starts at 6-8 weeks (3-dose series monthly), then annual booster."
    ),
    "cacing": (
        "### 🪱 Pet Deworming Schedule\n\n"
        "- **Puppies / Kittens (Under 3 Months):** Deworm every 2 weeks until 12 weeks old.\n"
        "- **3 to 6 Months Old:** Deworm once monthly.\n"
        "- **Adult Pets (6 Months and Above):** Routinely deworm every **3 months**.\n"
        "- **Common Brands in Malaysian Clinics:** Drontal Cat, Drontal Plus Dog, Milbemax (dose strictly calculated by body weight kg!)."
    ),
    "kutu": (
        "### 🐜 Flea, Tick & Ear Mite Prevention in Tropical Climates\n\n"
        "- **Spot-on & Chewables:**\n"
        "  - **Cats:** Revolution Plus, Advocate, Broadline, Frontline Plus.\n"
        "  - **Dogs:** NexGard Spectra (chewable), Bravecto (lasts 3 months), Simparica.\n"
        "- **Critical Warning:** NEVER use dog flea treatments on cats! *Permethrin* in canine products is neurotoxic and lethal to felines."
    ),
    "makanan": (
        "### 🥩 Healthy Pet Nutrition for Tropical Malaysia\n\n"
        "- **Cats:** Strict *obligate carnivores* requiring high taurine and animal protein. Avoid feeding white rice with salted anchovies (*ikan bilis*), which triggers lethal kidney damage and urinary blockage (FLUTD).\n"
        "- **Hydration:** Always supply clean fresh water. Pet water fountains stimulate drinking and prevent urinary crystal formation.\n"
        "- **Dogs:** Never feed cooked poultry bones as they splinter and pierce digestive tracts."
    ),
    "mandul": (
        "### ✂️ Spaying & Neutering (Sterilization)\n\n"
        "- **Optimal Age:** From 5 to 6 months onwards (minimum weight 2kg).\n"
        "- **Health Benefits:** Females are protected from fatal uterine infections (*Pyometra*) and mammary tumors. Males cease territorial urine spraying and aggressive roaming."
    ),
    "strok haba": (
        "### ☀️ Tropical Heatstroke Prevention in Malaysia\n\n"
        "- High risk in humid tropical temperatures above 34°C, particularly for brachycephalic breeds (Persian, British Shorthair, Pug, French Bulldog).\n"
        "- **Immediate First Aid:** Cool the pet with **room-temperature tap water** (NEVER freezing ice water) and run air conditioning/fan while transporting immediately to an emergency clinic."
    ),
    "nasi lemak": (
        "### ❌ Can Cats or Dogs Eat Nasi Lemak?\n\n"
        "**Veterinary Recommendation: STRICTLY NOT RECOMMENDED / DANGEROUS!**\n\n"
        "Although nasi lemak is a Malaysian staple, it poses serious health hazards to cats and dogs:\n\n"
        "1. 🥥 **Coconut Milk (Santan):** Extremely high saturated fat content triggers severe gastrointestinal upset, watery diarrhea, and life-threatening acute pancreatitis.\n"
        "2. 🌶️ **Sambal & Chili:** Contains *capsaicin*, causing severe stomach burning, nausea, and vomiting.\n"
        "3. 🧅 **Onions & Garlic:** Found abundantly in sambal, these contain *thiosulfate* which destroys canine and feline red blood cells (*Heinz body hemolytic anemia*).\n"
        "4. 🐟 **Salted Anchovies (Ikan Bilis) & Peanuts:** Extremely high sodium damages the kidneys and causes urinary tract crystals (FLUTD).\n\n"
        "💡 **Tip:** If feeding your pet, offer certified feline/canine wet food, premium kibbles, or plain boiled chicken breast without any salt, seasoning, or onion."
    ),
    "sporo": (
        "### 🦠 Sporotrichosis (Sporo) in Malaysian Cats\n\n"
        "- **Cause:** Fungal infection by *Sporothrix schenckii* present in humid soil or transmitted through scratches from outdoor stray cats.\n"
        "- **Symptoms:** Chronic ulcerating crusted wounds on the nose, paws, or ears that fail to heal.\n"
        "- **Zoonotic Warning:** Transmissible to humans! Wear protective gloves when handling infected pets.\n"
        "- **Treatment:** Requires specialized oral veterinary antifungal therapy (Itraconazole) under close veterinarian supervision."
    )
}

def detect_language(text: str) -> str:
    """Detects whether text is predominantly English or Malay."""
    text_lower = text.lower()
    english_keywords = ["cat", "dog", "kitten", "puppy", "vaccine", "vaccination", "flea", "deworm", "eat", "vomit", "pee", "doctor", "vet", "hospital", "poison", "help", "chocolate", "urgent", "what", "how", "when", "why"]
    malay_keywords = ["kucing", "anjing", "anak", "cucuk", "ubat", "cacing", "kutu", "makan", "muntah", "kencing", "doktor", "klinik", "racun", "tolong", "bila", "macam", "kenapa", "panas", "pasir", "buih"]

    en_score = sum(1 for w in english_keywords if re.search(r'\b' + w + r'\b', text_lower))
    ms_score = sum(1 for w in malay_keywords if re.search(r'\b' + w + r'\b', text_lower))

    return "en" if en_score > ms_score else "ms"

def get_chatbot_reply(user_message: str, pet_context: Optional[Dict[str, Any]] = None, requested_lang: Optional[str] = None) -> Dict[str, Any]:
    """
    Main entry point for chatbot interactions.
    Enforces Cat & Dog Domain Guardrail -> Emergency Triage -> Live Seasonal Sync -> Knowledge Engine / AI.
    """
    lang = (requested_lang or detect_language(user_message)).lower()
    is_en = (lang == "en")

    # Step 1: Strict Cat & Dog Domain Guardrail Check
    is_in_domain, refusal_ms, refusal_en = check_cat_dog_domain(user_message, lang=lang)
    if not is_in_domain:
        refusal_reply = refusal_en if is_en else refusal_ms
        return {
            "reply": refusal_reply,
            "is_emergency": False,
            "triage_level": "OUT_OF_DOMAIN",
            "triage_details": {"is_emergency": False, "triage_level": "OUT_OF_DOMAIN"},
            "is_out_of_domain": True,
            "lang": lang
        }

    pet_species = pet_context.get("species", "Kucing" if not is_en else "Cat") if pet_context else ("Cat" if is_en else "Kucing")

    # Step 2: Emergency Triage Detection
    triage = analyze_emergency_triage(user_message, pet_species=pet_species, lang=lang)
    if triage["is_emergency"]:
        dos_formatted = "\n".join([f"✅ **{item}**" for item in triage["dos"]])
        donts_formatted = "\n".join([f"❌ **{item}**" for item in triage["donts"]])
        species_note = f"\n\n> ⚠️ {triage['species_note']}" if triage["species_note"] else ""

        if is_en:
            emergency_reply = (
                f"## {triage['badge']}\n"
                f"### {triage['title']}\n\n"
                f"**{triage['action_prompt']}**\n\n"
                f"{triage['explanation']}{species_note}\n\n"
                f"### 📋 Immediate First Aid (DOs):\n{dos_formatted}\n\n"
                f"### ⛔ Critical Prohibitions (DONTs):\n{donts_formatted}\n\n"
                f"---\n"
                f"🚨 **Malaysia Emergency Contacts:**\n"
                f"- **National Poison Centre (24 Hours):** [1-800-88-8099](tel:1800888099) or [04-657 0099](tel:046570099)\n"
                f"- **Fire & Rescue Emergency (BOMBA):** [999](tel:999)\n\n"
                f"*Click **'Find Nearest 24H Vet (GPS)'** on the tab above to route immediately to the nearest veterinary hospital.*"
            )
        else:
            emergency_reply = (
                f"## {triage['badge']}\n"
                f"### {triage['title']}\n\n"
                f"**{triage['action_prompt']}**\n\n"
                f"{triage['explanation']}{species_note}\n\n"
                f"### 📋 Tindakan Cemas Pantas (DOs):\n{dos_formatted}\n\n"
                f"### ⛔ Perkara yang DILARANG (DONTs):\n{donts_formatted}\n\n"
                f"---\n"
                f"🚨 **Talian Kecemasan Malaysia:**\n"
                f"- **Pusat Racun Negara (24 Jam):** [1-800-88-8099](tel:1800888099) atau [04-657 0099](tel:046570099)\n"
                f"- **Kecemasan Bomba / Penyelamatan:** [999](tel:999)\n\n"
                f"*Tekan butang **'Cari Vet 24 Jam Terdekat'** di atas untuk navigasi segera ke hospital veterinar berdekatan menggunakan GPS.*"
            )

        return {
            "reply": emergency_reply,
            "is_emergency": True,
            "triage_level": triage["triage_level"],
            "triage_details": triage,
            "lang": lang
        }

    seasonal_info = get_seasonal_bot_advisory(lang=lang)
    q_lower = user_message.lower()

    # Step 3: Handle Greetings with Cat & Dog welcome introduction + Live Seasonal Advisory
    is_greeting = any(re.search(r'\b' + re.escape(w) + r'\b', q_lower) for w in GREETING_KEYWORDS) and len(q_lower.split()) <= 4
    if is_greeting:
        if is_en:
            welcome_text = (
                "🐾 **Hello! I am PawFurry AI, your dedicated Veterinary Assistant for Cats and Dogs in Malaysia.**\n\n"
                "I am here 24/7 to answer questions regarding feline and canine health, nutrition, vaccines, behavior, and emergency triage.\n\n"
                f"{seasonal_info['alert_text']}\n\n"
                "**Common questions you can ask me:**\n"
                "- 💉 *'What is the core vaccine schedule for kittens and puppies in Malaysia?'*\n"
                "- 🥩 *'Can cats or dogs eat nasi lemak?'*\n"
                "- 🪱 *'How often should I administer deworming and flea spot-on treatments?'*\n"
                "- ☀️ *'How do I protect my pets from heatstroke in tropical weather?'*\n"
                "- 🚨 *'Emergency signs that require immediate 24-hour clinic visits.'*\n\n"
                "How can I help you with your cat or dog today?"
            )
        else:
            welcome_text = (
                "🐾 **Salam sejahtera! Saya PawFurry AI, pembantu maya veterinar khusus untuk Kucing & Anjing di Malaysia.**\n\n"
                "Saya bersedia membantu anda 24/7 mengenai kesihatan, pemakanan, vaksinasi, kawalan kutu/cacing, dan triage kecemasan si bulu.\n\n"
                f"{seasonal_info['alert_text']}\n\n"
                "**Antara soalan yang anda boleh tanyakan:**\n"
                "- 💉 *'Bila jadual lengkap vaksin Tricat untuk anak kucing di Malaysia?'*\n"
                "- 🥩 *'Boleh ke kucing atau anjing makan nasi lemak?'*\n"
                "- 🪱 *'Berapa kerap jadual ubat cacing dan ubat kutu mengikut berat badan?'*\n"
                "- ☀️ *'Cara cegah strok haba dalam cuaca panas Malaysia?'*\n"
                "- 🚨 *'Tanda-tanda kecemasan yang perlukan rawatan vet 24 jam serta-merta.'*\n\n"
                "Sila kongsikan sebarang persoalan atau simptom mengenai kucing atau anjing anda!"
            )
        return {
            "reply": welcome_text,
            "is_emergency": False,
            "triage_level": "INFO",
            "triage_details": triage,
            "seasonal_advisory": seasonal_info,
            "lang": lang
        }

    # Step 4: Check Google Gemini API with strict Cat & Dog prompt guardrails
    api_key = Config.GEMINI_API_KEY
    if HAS_GENAI and api_key and len(api_key.strip()) > 10:
        try:
            genai.configure(api_key=api_key.strip())
            model = genai.GenerativeModel("gemini-1.5-flash")

            system_lang = "English" if is_en else "Bahasa Melayu"
            system_prompt = (
                f"You are 'PawFurry Care Assistant', an expert veterinary assistant for Malaysia dedicated EXCLUSIVELY to CATS and DOGS. "
                f"Respond in natural, helpful {system_lang}. "
                "CRITICAL DOMAIN GUARDRAIL: You must strictly only answer questions regarding CATS (kucing) and DOGS (anjing), their health, diet, wellness, breed traits, and emergencies. "
                "If the user asks about ANYTHING ELSE (such as human cooking/recipes like nasi lemak recipes, politics, coding, math, general trivia, or other animals like birds/reptiles), politely refuse and clarify that you are exclusively specialized in cat and dog care in Malaysia. "
                "Provide accurate care, nutrition, breed, behavior, and healthcare advice tailored to Malaysia's tropical climate. "
                "Never prescribe prescription-only antibiotics or human medications. Always remind user to see a registered vet for persistent clinical signs."
            )

            prompt = f"{system_prompt}\n\nUser Question: {user_message}"
            response = model.generate_content(prompt)
            if response and response.text:
                return {
                    "reply": response.text,
                    "is_emergency": False,
                    "triage_level": "INFO",
                    "triage_details": triage,
                    "seasonal_advisory": seasonal_info,
                    "lang": lang
                }
        except Exception:
            pass

    # Step 5: Fallback to Bilingual Malaysian Knowledge Engine
    topics = VET_KNOWLEDGE_TOPICS_EN if is_en else VET_KNOWLEDGE_TOPICS_MS
    matched = []

    if "nasi lemak" in q_lower:
        matched.append(topics["nasi lemak"])
    if any(k in q_lower for k in ["sporo", "sporotrichosis"]):
        matched.append(topics["sporo"])
    if any(k in q_lower for k in ["vaksin", "vaccin", "vaccine", "cucuk", "booster", "shot", "tricat"]):
        matched.append(topics["vaksin"])
    if any(k in q_lower for k in ["cacing", "deworm", "worm", "drontal"]):
        matched.append(topics["cacing"])
    if any(k in q_lower for k in ["kutu", "flea", "tick", "hama", "mite", "revolution", "bravecto"]):
        matched.append(topics["kutu"])
    if any(k in q_lower for k in ["makan", "diet", "kibble", "wet food", "fish", "meat", "ikan", "ayam", "food"]):
        matched.append(topics["makanan"])
    if any(k in q_lower for k in ["mandul", "kembiri", "spay", "neuter"]):
        matched.append(topics["mandul"])
    if any(k in q_lower for k in ["panas", "strok", "heatstroke", "hot", "sun"]):
        matched.append(topics["strok haba"])

    if matched:
        reply_body = "\n\n---\n\n".join(matched)
    else:
        if is_en:
            reply_body = (
                "Hello! I am your **PawFurry Care** digital pet health assistant for Malaysia, specialized in **cats and dogs**.\n\n"
                f"{seasonal_info['alert_text']}\n\n"
                "**Common topics you can ask me about:**\n"
                "- 💉 *'What is the core vaccine schedule for kittens and puppies in Malaysia?'*\n"
                "- 🥩 *'Can cats or dogs eat nasi lemak?'*\n"
                "- 🪱 *'How often should I administer deworming and flea spot-on treatments?'*\n"
                "- ✂️ *'What is the recommended age for spaying or neutering?'*\n"
                "- ☀️ *'How do I protect my pet from heatstroke during hot Malaysian weather?'*\n"
                "- 🚨 *'Signs of veterinary emergencies that require 24-hour clinic visits.'*\n\n"
                "Please describe any questions or symptoms your cat or dog is experiencing!"
            )
        else:
            reply_body = (
                "Salam! Saya ialah pembantu pintar **PawFurry Care** khusus untuk **kucing dan anjing** di Malaysia.\n\n"
                f"{seasonal_info['alert_text']}\n\n"
                "**Antara topik yang anda boleh tanyakan:**\n"
                "- 💉 *'Bila masa sesuai untuk ambil dos vaksin pertama & booster?'*\n"
                "- 🥩 *'Boleh ke kucing atau anjing makan nasi lemak?'*\n"
                "- 🪱 *'Bagaimana jadual ubat cacing dan ubat kutu mengikut berat badan?'*\n"
                "- ✂️ *'Berapa umur terbaik untuk mandulkan haiwan peliharaan?'*\n"
                "- ☀️ *'Cara cegah strok haba dalam cuaca panas Malaysia?'*\n"
                "- 🚨 *'Tanda-tanda kecemasan yang perlukan rawatan vet 24 jam serta-merta.'*\n\n"
                "Sila kongsikan sebarang simptom atau persoalan si bulu anda!"
            )

    disclaimer = (
        "\n\n---\n"
        "*(📌 Disclaimer: This advice provides general veterinary care guidelines for cats and dogs. In persistent or emergency symptoms, always consult a licensed Veterinarian.)*"
        if is_en else
        "\n\n---\n"
        "*(📌 Penafian: Nasihat ini bertujuan sebagai panduan maklumat am kesihatan kucing & anjing. Sekiranya terdapat simptom berterusan, sentiasa rujuk kepada Doktor Veterinar bertauliah.)*"
    )

    return {
        "reply": reply_body + disclaimer,
        "is_emergency": False,
        "triage_level": "INFO",
        "triage_details": triage,
        "seasonal_advisory": seasonal_info,
        "lang": lang
    }
