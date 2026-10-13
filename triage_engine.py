import re
from typing import Dict, Any, List, Optional

# --- BILINGUAL TOXICITY KNOWLEDGE BASE ---
TOXIC_SUBSTANCES: Dict[str, Dict[str, Any]] = {
    "paracetamol": {
        "name": "Paracetamol / Panadol",
        "risk_level": "CRITICAL",
        "species_affected": "Kucing (Sangat Maut!) & Anjing / Cats (Highly Fatal!) & Dogs",
        "danger_explanation": "Kucing TIADA enzim 'glucuronyl transferase' untuk memproses paracetamol. Separuh biji Panadol boleh membawa maut dalam tempoh beberapa jam sahaja kerana memusnahkan sel darah merah (methemoglobinemia) dan merosakkan hati.",
        "danger_explanation_en": "Cats LACK the 'glucuronyl transferase' enzyme to metabolize paracetamol. Even half a tablet of Panadol/Tylenol can be fatal within hours, destroying red blood cells (methemoglobinemia) and inducing acute liver necrosis.",
        "symptoms": ["Gusi/lidah bertukar warna coklat/kebiruan", "Sesak nafas", "Bengkak di muka dan kaki", "Muntah dan rebah"],
        "symptoms_en": ["Brownish/cyanotic gums and tongue", "Severe respiratory distress", "Facial/paw swelling", "Hypothermia and collapse"],
        "first_aid_dos": [
            "SEGERA bawa ke hospital veterinar 24 jam dalam masa terdekat!",
            "Bawa baki pek ubat atau ketahui dos berapa mg yang telah dimakan untuk makluman doktor vet.",
            "Doktor vet perlu suntik penawar khusus (N-acetylcysteine) serta-merta."
        ],
        "first_aid_dos_en": [
            "RUSH to a 24-hour veterinary hospital immediately!",
            "Bring the packaging or exact dosage (mg) for the attending veterinarian.",
            "Veterinarians must administer the specific antidote (N-acetylcysteine) as quickly as possible."
        ],
        "first_aid_donts": [
            "JANGAN cuba beri susu, minyak kelapa, atau air garam untuk paksa muntah sendiri di rumah!",
            "JANGAN tunggu tengok simptom keluar dahulu baru nak pergi vet."
        ],
        "first_aid_donts_en": [
            "DO NOT induce vomiting at home with salt water, milk, or oil!",
            "DO NOT wait for visible symptoms to emerge before heading to the clinic."
        ]
    },
    "panadol": {
        "name": "Panadol (Paracetamol / Tylenol)",
        "risk_level": "CRITICAL",
        "species_affected": "Kucing & Anjing / Cats & Dogs",
        "danger_explanation": "Panadol adalah sangat bertoksik terutamanya untuk kucing. Menghancurkan sel darah merah dan membawa kegagalan fungsi hati akut.",
        "danger_explanation_en": "Panadol/Paracetamol is extremely lethal to cats. It destroys red blood cells and precipitates sudden liver failure.",
        "symptoms": ["Sesak nafas", "Muka bengkak", "Gusi kebiruan/coklat", "Rebah"],
        "symptoms_en": ["Breathing difficulty", "Swollen face", "Bluish/brown gums", "Collapse"],
        "first_aid_dos": [
            "Terus bawa ke klinik veterinar kecemasan 24 jam sekarang juga!",
            "Simpan bungkusan ubat untuk ditunjukkan kepada veterinar."
        ],
        "first_aid_dos_en": [
            "Go straight to a 24-hour veterinary emergency hospital right now!",
            "Keep the medication packaging to show the vet."
        ],
        "first_aid_donts": [
            "JANGAN beri sebarang ubat manusia lain seperti ubat selsema atau ponstan!",
            "JANGAN tunda masa perjalanan ke klinik."
        ],
        "first_aid_donts_en": [
            "DO NOT administer any other human NSAIDs or cold medications!",
            "DO NOT delay your travel time to the veterinary clinic."
        ]
    },
    "lili": {
        "name": "Bunga Lili (Lilies - Lilium & Hemerocallis)",
        "risk_level": "CRITICAL",
        "species_affected": "Kucing (Maut Ekstrem) / Cats (Extremely Fatal)",
        "danger_explanation": "Semua bahagian pokok lili (daun, kelopak, debunga, malah air di dalam pasu lili) adalah racun maut bagi kucing. Menyebabkan kegagalan buah pinggang akut (acute kidney failure) dalam tempoh 24-72 jam.",
        "danger_explanation_en": "Every part of the lily plant (leaves, petals, pollen, and vase water) is highly toxic to cats. Causes acute kidney failure within 24-72 hours.",
        "symptoms": ["Muntah", "Hilang selera makan serta-merta", "Kerap kencing kemudian terus tak kencing", "Lemah lesu"],
        "symptoms_en": ["Vomiting", "Sudden anorexia", "Frequent urination progressing to complete anuria", "Extreme lethargy"],
        "first_aid_dos": [
            "Bawa kucing ke hospital vet segera untuk infusi cecair IV (IV drip) berterusan sebelum kerosakan buah pinggang kekal berlaku.",
            "Jika ada debunga pada bulu, lap segera dengan kain basah suam supaya kucing tidak menjilatnya."
        ],
        "first_aid_dos_en": [
            "Take your cat to a vet immediately for continuous IV fluid therapy before permanent kidney damage sets in.",
            "Wipe away any pollen from coat with a damp warm towel so the cat doesn't ingest it while grooming."
        ],
        "first_aid_donts": [
            "JANGAN tunggu 24 jam untuk tengok keadaan.",
            "JANGAN simpan sebarang bunga lili di dalam rumah yang ada kucing."
        ],
        "first_aid_donts_en": [
            "DO NOT wait 24 hours to monitor.",
            "DO NOT keep any lilies in households with cats."
        ]
    },
    "coklat": {
        "name": "Coklat / Chocolate (Theobromine)",
        "risk_level": "HIGH",
        "species_affected": "Anjing & Kucing / Dogs & Cats",
        "danger_explanation": "Coklat mengandungi Theobromine. Dark chocolate dan serbuk koko paling bahaya berbanding milk chocolate. Merangsang sistem saraf dan jantung secara berlebihan.",
        "danger_explanation_en": "Chocolate contains Theobromine. Dark chocolate and baking cocoa are far more dangerous than milk chocolate, overstimulating the cardiac and nervous systems.",
        "symptoms": ["Jantung berdegup sangat kencang", "Muntah & cirit-birit", "Gelisah mundar-mandir", "Sawan (kes berat)"],
        "symptoms_en": ["Rapid heart rate (tachycardia)", "Vomiting and diarrhea", "Restlessness and pacing", "Seizures in severe cases"],
        "first_aid_dos": [
            "Kira anggaran berat coklat yang dimakan dan jenis coklat.",
            "Bawa ke klinik haiwan dalam tempoh 1-2 jam pertama untuk prosedur dekontaminasi perut."
        ],
        "first_aid_dos_en": [
            "Estimate the weight and type of chocolate consumed.",
            "Bring pet to a veterinary clinic within 1-2 hours for safe gastric decontamination."
        ],
        "first_aid_donts": [
            "JANGAN paksa muntah sendiri jika anjing sudah menunjukkan tanda sawan atau tidak sedarkan diri."
        ],
        "first_aid_donts_en": [
            "DO NOT induce vomiting if the pet is already convulsing or unconscious."
        ]
    },
    "ubat_nyamuk": {
        "name": "Ubat Nyamuk Lingkaran & Semburan Aerosol (Pyrethroids / Permethrin)",
        "risk_level": "CRITICAL",
        "species_affected": "Kucing (Sangat Bahaya!) & Anjing / Cats (Highly Fatal!) & Dogs",
        "danger_explanation": "Ubat nyamuk lingkaran, aerosol dan ubat kutu anjing kerap mengandungi bahan Pyrethroid/Permethrin. Hati kucing tidak berupaya memecahkan bahan kimia ini, merosakkan sistem saraf pusat dan menyebabkan sawan maut.",
        "danger_explanation_en": "Mosquito coils, household aerosols, and canine spot-on medications contain pyrethroids/permethrin. Felines cannot metabolize these compounds, leading to lethal neurotoxicity and violent tremors.",
        "symptoms": ["Menggeletar seluruh badan (tremors)", "Mulut berbuih lebat dan air liur meleleh", "Jalan terhuyung-hayang (ataxia)", "Sawan dan suhu badan melonjak"],
        "symptoms_en": ["Severe body tremors and muscle twitching", "Profuse hypersalivation/foaming at mouth", "Staggering wobbly gait (ataxia)", "Seizures and hyperthermia"],
        "first_aid_dos": [
            "Jika terkena pada bulu/kulit, mandikan segera dengan sabun pencuci pinggan lembut (cth: Sunlight) dan air suam.",
            "Bawa segera ke klinik kecemasan 24 jam untuk suntikan ubat penenang/sawan (methocarbamol/diazepam)."
        ],
        "first_aid_dos_en": [
            "If exposed topically on fur, bathe immediately with mild dishwashing liquid and lukewarm water.",
            "Rush to an emergency 24-hour vet for intravenous muscle relaxants and anti-seizure therapy."
        ],
        "first_aid_donts": [
            "JANGAN gunakan ubat kutu anjing pada kucing!",
            "JANGAN biarkan kucing terdedah kepada asap lingkaran ubat nyamuk dalam bilik bertutup."
        ],
        "first_aid_donts_en": [
            "NEVER apply dog tick/flea treatments onto cats!",
            "DO NOT burn mosquito coils in enclosed rooms with felines."
        ]
    },
    "katak_puru": {
        "name": "Katak Puru Beracun Selepas Hujan (Asian Common Toad - Duttaphrynus / Bufo)",
        "risk_level": "CRITICAL",
        "species_affected": "Anjing & Kucing / Dogs & Cats",
        "danger_explanation": "Katak puru yang keluar selepas hujan lebat merembeskan racun Bufotoxin pada kelenjar parotoid apabila digigit oleh anjing atau kucing. Toksin ini diserap pantas melalui gusi dan boleh menyebabkan degupan jantung terhenti.",
        "danger_explanation_en": "Asian common toads emerging after heavy tropical rains secrete potent bufotoxin when mouthed or bitten by pets. Rapidly absorbed via oral mucosa, causing severe cardiac arrhythmias.",
        "symptoms": ["Mulut berbuih pekat serta-merta", "Gusi bertukar warna merah bata terang", "Menggesel mulut dengan kaki", "Degupan jantung tidak sekata dan sawan"],
        "symptoms_en": ["Instant profuse foaming at mouth", "Brick-red congested gums", "Frantic pawing at the mouth", "Cardiac arrhythmia and convulsions"],
        "first_aid_dos": [
            "SEGERA siram dan bilas rongga mulut haiwan ke arah tepi dengan air paip mengalir selama 10-15 minit (condongkan kepala ke bawah agar air tidak masuk ke paru-paru).",
            "Bawa ke hospital veterinar kecemasan 24 jam dengan kadar segera."
        ],
        "first_aid_dos_en": [
            "IMMEDIATELY flush and rinse the mouth sideways with running tap water for 10-15 minutes (head pointed downward to avoid aspiration).",
            "Transport to an emergency 24-hour hospital immediately."
        ],
        "first_aid_donts": [
            "JANGAN sembur air terus ke dalam kerongkong (risiko lemas air masuk paru-paru).",
            "JANGAN tunggu simptom reda sendiri."
        ],
        "first_aid_donts_en": [
            "DO NOT spray water directly down the throat (prevents drowning/aspiration).",
            "DO NOT wait to see if symptoms resolve on their own."
        ]
    },
    "racun_siput": {
        "name": "Racun Siput Babi / Siput Gondang (Metaldehyde)",
        "risk_level": "CRITICAL",
        "species_affected": "Anjing & Kucing / Dogs & Cats",
        "danger_explanation": "Pelet racun siput di laman rumah mengandungi Metaldehyde yang sangat berbau harum bagi anjing. Menyebabkan sindrom neurotoksik teruk 'shake and bake' dengan sawan berterusan dan kegagalan pelbagai organ.",
        "danger_explanation_en": "Garden slug/snail bait pellets contain Metaldehyde, which smells palatable to dogs. Causes acute 'shake-and-bake' neurotoxicity with hyperthermia and fatal convulsions.",
        "symptoms": ["Menggigil kuat tanpa henti", "Suhu badan melebihi 41°C", "Sawan ganas", "Hilang kesedaran"],
        "symptoms_en": ["Incessant tremors", "Extreme hyperthermia (>41°C)", "Violent tonic-clonic seizures", "Stupor and coma"],
        "first_aid_dos": [
            "Bawa segera ke klinik kecemasan untuk bilasan perut dan ubat penenang.",
            "Bawa bungkusan pelet racun siput yang digunakan di laman."
        ],
        "first_aid_dos_en": [
            "Immediately rush to emergency clinic for gastric lavage and seizure stabilization.",
            "Bring the snail bait packaging to identify active ingredients."
        ],
        "first_aid_donts": [
            "JANGAN tabur pelet racun siput di laman jika ada memelihara anjing atau kucing."
        ],
        "first_aid_donts_en": [
            "DO NOT use open snail bait in yards accessible to dogs or cats."
        ]
    },
    "bawang": {
        "name": "Bawang Merah, Bawang Putih & Daun Bawang (Allium species)",
        "risk_level": "HIGH",
        "species_affected": "Kucing & Anjing / Cats & Dogs",
        "danger_explanation": "Semua jenis bawang (mentah, masak, serbuk bawang dalam makanan manusia/kuah kari/sambal) mengandungi sebatian n-propyl disulfide yang memecahkan sel darah merah haiwan dan menyebabkan anemia maut.",
        "danger_explanation_en": "All allium species (raw, cooked, garlic powders in human gravies/sambal) contain n-propyl disulfide which causes oxidative breakdown of red blood cells (Heinz body hemolytic anemia).",
        "symptoms": ["Kencing berwarna coklat gelap/merah", "Gusi pucat keputihan", "Lemas lesu dan cepat penat", "Muntah dan hilang selera"],
        "symptoms_en": ["Reddish-brown dark urine", "Pale white gums", "Extreme lethargy and weakness", "Vomiting and anorexia"],
        "first_aid_dos": [
            "Bawa ke klinik untuk ujian darah (CBC / PCV) dan terapi sokongan antioksidan."
        ],
        "first_aid_dos_en": [
            "Take to clinic for immediate complete blood count (CBC) and antioxidant supportive care."
        ],
        "first_aid_donts": [
            "JANGAN sesekali memberi lauk masakan manusia (sup, kuah kari, sambal) kepada kucing atau anjing."
        ],
        "first_aid_donts_en": [
            "NEVER feed table scraps, onion-rich gravies, or human curries to pets."
        ]
    },
    "anggur": {
        "name": "Anggur & Kismis (Grapes & Raisins - Tartaric Acid)",
        "risk_level": "CRITICAL",
        "species_affected": "Anjing & Kucing / Dogs & Cats",
        "danger_explanation": "Kandungan asid tartarik dalam anggur dan kismis menyebabkan kegagalan buah pinggang akut secara mendadak pada anjing walaupun dalam kuantiti beberapa biji sahaja.",
        "danger_explanation_en": "Tartaric acid in grapes and raisins induces sudden, irreversible acute kidney failure in dogs, even in tiny doses of just a few berries.",
        "symptoms": ["Muntah dalam 6-12 jam", "Cirit-birit", "Hilang selera makan", "Berhenti kencing (anuria) menandakan kerosakan buah pinggang"],
        "symptoms_en": ["Vomiting within 6-12 hours", "Diarrhea", "Complete loss of appetite", "Cessation of urine output (anuria)"],
        "first_aid_dos": [
            "Bawa ke klinik dengan pantas untuk rawatan dehidrasi dan titisan IV bagi melindungi buah pinggang."
        ],
        "first_aid_dos_en": [
            "Rush to clinic for urgent gastric decontamination and aggressive IV fluid diuresis."
        ],
        "first_aid_donts": [
            "JANGAN beri biskut, kek atau roti yang mengandungi kismis kepada anjing."
        ],
        "first_aid_donts_en": [
            "DO NOT feed fruitcakes, buns, or snacks with raisins to dogs."
        ]
    }
}

# --- BILINGUAL RED FLAG EMERGENCY TRIGGERS ---
CRITICAL_TRIGGERS = [
    # Urinary obstruction in male cats (FLUTD / Blockage)
    (r"\b(tak boleh kencing|kencing tak keluar|kencing berdarah|meneran tak keluar|batu karang tersumbat|menangis kencing|litter box menangis|penis merah|kemaluan tersumbat|cannot pee|can't pee|can't urinate|cannot urinate|straining to urinate|urinary blockage|blocked bladder|blocked cat|crying in litter box)\b",
     "KECEMASAN SALURAN KENCING TERSUMBAT (URINARY BLOCKAGE)",
     "CRITICAL EMERGENCY: BLOCKED BLADDER / URINARY OBSTRUCTION",
     "Kucing jantan yang meneran tetapi air kencing tidak keluar adalah situasi MAUT dalam tempoh 24-48 jam akibat pengumpulan toksin potassium (hyperkalemia) yang boleh menghentikan degupan jantung.",
     "Male cats straining without passing urine face a FATAL emergency within 24-48 hours. Potassium build-up (hyperkalemia) will trigger sudden cardiac arrest."),

    # Paracetamol / Panadol toxicity
    (r"\b(panadol|paracetamol|tylenol|ubat demam manusia|ubat selsema|ponstan|ibuprofen|aspirin|ate panadol|ate paracetamol|swallowed panadol|swallowed paracetamol)\b",
     "KERACUNAN UBAT MANUSIA (PARACETAMOL/NSAIDS)",
     "CRITICAL EMERGENCY: HUMAN MEDICATION TOXICITY (PARACETAMOL)",
     "Ubat paracetamol/panadol adalah RACUN MAUT untuk kucing kerana ketiadaan enzim hati yang sesuai. Memerlukan penawar vet dalam kadar segera!",
     "Paracetamol/Panadol is DEADLY to cats due to absence of glucuronyl transferase. Requires immediate veterinary antidotal treatment!"),

    # Lily toxicity
    (r"\b(bunga lili|bunga lily|daun lili|pokok lili|debunga lili|chewed lily|ate lily|lily flower|lily pollen)\b",
     "KERACUNAN POKOK LILI (LILY TOXICITY)",
     "CRITICAL EMERGENCY: LILY TOXICITY IN CATS",
     "Semua bahagian bunga lili adalah maut bagi kucing dan menyebabkan kegagalan buah pinggang kekal dalam tempoh singkat.",
     "All parts of lilies are lethal to cats, causing irreversible acute renal failure within 24-72 hours."),

    # Bloat / GDV in dogs
    (r"\b(perut kembung keras|perut membesar tiba-tiba|bloat|gdv|cuba muntah tak keluar apa|perut bunyi keras tegang|stomach swollen hard|distended belly|unproductive retching)\b",
     "KECEMASAN PERUT BERPUSING (BLOAT / GDV - GASTRIC DILATATION-VOLVULUS)",
     "CRITICAL EMERGENCY: GASTRIC DILATATION-VOLVULUS (BLOAT / GDV)",
     "Perut anjing yang kembung keras dan berpusing adalah kecemasan surgeri serta-merta. Boleh membawa maut dalam masa 1-2 jam jika aliran darah terputus.",
     "A swollen, distended and twisted stomach in dogs is an immediate surgical emergency. Fatal within 1-2 hours as blood supply gets cut off."),

    # Respiratory distress
    (r"\b(sesak nafas|susah bernafas|tercungap-cungap|nafas laju|lidah biru|gusi biru|bernafas guna mulut|difficulty breathing|trouble breathing|gasping for air|blue tongue|blue gums|breathing through mouth|cyanosis)\b",
     "KECEMASAN SALURAN PERNAFASAN (RESPIRATORY DISTRESS)",
     "CRITICAL EMERGENCY: ACUTE RESPIRATORY DISTRESS",
     "Haiwan yang bernafas menggunakan mulut (terutamanya kucing), bernafas laju berbunyi, atau gusi bertukar biru/pucat sedang kekurangan oksigen kritikal.",
     "Pets breathing through an open mouth (especially cats), gasping rapidly, or displaying blue/pale gums suffer from critical oxygen depletion."),

    # Severe bleeding / Trauma
    (r"\b(pendarahan banyak|darah tak henti|kena langgar|terlanggar kereta|jatuh tingkat|patah tulang terkeluar|luka robek besar|heavy bleeding|bleeding heavily|hit by car|open fracture|deep wound)\b",
     "TRAUMA & PENDARAHAN KRITIKAL",
     "CRITICAL EMERGENCY: TRAUMA & SEVERE HEMORRHAGE",
     "Haiwan mengalami pendarahan aktif atau trauma hentaman. Perlu rawatan hemostasis dan pemantauan kejutan (shock) di hospital haiwan.",
     "Pet is experiencing active bleeding or impact trauma. Requires immediate wound stabilization and shock management at an animal hospital."),

    # Prolonged seizure
    (r"\b(sawan|kejang berterusan|menggeletar tak sedar diri|epilepsi teruk|mulut berbuih kejang|seizure|convulsing|continuous seizure|fit)\b",
     "SAWAN BERTERUSAN (STATUS EPILEPTICUS)",
     "CRITICAL EMERGENCY: PROLONGED SEIZURE (STATUS EPILEPTICUS)",
     "Sawan yang berterusan melebihi 2 minit atau berulang-ulang boleh merosakkan otak dan meningkatkan suhu badan ke tahap maut.",
     "Seizures lasting beyond 2 minutes or recurring rapidly cause brain damage and dangerous hyperthermia."),

    # Choking
    (r"\b(tercekik tulang|tercekik|tersumbat tekak|tersedak tak boleh nafas|choking on bone|choking|foreign object stuck in throat)\b",
     "SALURAN UDARA TERHALANG (CHOKING)",
     "CRITICAL EMERGENCY: AIRWAY OBSTRUCTION / CHOKING",
     "Objek asing atau tulang menghalang saluran pernafasan. Oksigen tidak sampai ke paru-paru.",
     "Foreign body or bone is obstructing the airway, blocking vital oxygen to the lungs.")
]

HIGH_TRIGGERS = [
    # General toxins
    (r"\b(coklat|koko|bawang|garlic|anggur|kismis|raisin|racun tikus|ubat nyamuk|minyak kayu putih|tea tree oil|pokok keladi|dieffenbachia|xylitol|chocolate|cocoa|onion|garlic|grapes|raisins|rat poison|essential oil)\b",
     "POTENSI KERACUNAN MAKANAN / TUMBUHAN",
     "HIGH ALERT: POTENTIAL TOXIC INGESTION",
     "Bahan yang dimakan disyaki mengandungi sebatian toksik kepada sistem organ haiwan peliharaan.",
     "The ingested substance contains chemical compounds that are toxic to animal organ systems."),

    # Severe vomiting / diarrhea
    (r"\b(muntah berak berdarah|muntah warna kuning hijau kerap|parvo|panleukopenia|cirit darah busuk hanyir|tak makan 2 hari lembik|vomiting blood|bloody stool|parvovirus|severe diarrhea)\b",
     "JANGKITAN VIRUS / GASTROENTERITIS TERUK",
     "HIGH ALERT: SEVERE GASTROENTERITIS / VIRAL INFECTION",
     "Risiko dehidrasi melampau dan jangkitan virus berbahaya seperti Parvovirus atau Feline Panleukopenia.",
     "Severe risk of acute dehydration and deadly viral infections such as Parvovirus or Feline Panleukopenia."),

    # Eye trauma
    (r"\b(mata bengkak terkeluar|mata berdarah|ulser mata|mata putih kelabu kabur|mata bernanah teruk|eye swollen|eye bleeding|corneal ulcer|cloudy eye)\b",
     "KECEMASAN MATA (OPHTHALMIC EMERGENCY)",
     "HIGH ALERT: OPHTHALMIC EMERGENCY",
     "Trauma mata berisiko menyebabkan kebutaan kekal jika kornea terkoyak atau dijangkiti kuman.",
     "Eye trauma risks permanent vision loss if corneal lacerations or severe ulcers are left untreated.")
]

def analyze_emergency_triage(user_message: str, pet_species: str = "Kucing", lang: str = "ms") -> Dict[str, Any]:
    """Analyzes message for emergency red flags with full bilingual support ('ms' or 'en')."""
    msg_lower = user_message.lower()
    is_en = (lang.lower() == "en")

    # 1. Check CRITICAL triggers
    for pattern, title_ms, title_en, exp_ms, exp_en in CRITICAL_TRIGGERS:
        if re.search(pattern, msg_lower):
            species_note = ""
            species_note_en = ""
            if any(k in pattern for k in ["kencing", "pee", "urinate"]) and any(s in pet_species.lower() for s in ["kucing", "cat"]):
                species_note = "PERINGATAN KHAS: Untuk kucing jantan, masalah kencing tidak keluar adalah status 'RED ALERT' tertinggi!"
                species_note_en = "SPECIAL WARNING: For male cats, complete inability to urinate is a top-tier RED ALERT emergency!"

            return {
                "is_emergency": True,
                "triage_level": "CRITICAL",
                "badge": "🔴 CRITICAL EMERGENCY (RED ALERT)" if is_en else "🔴 KECEMASAN KRITIKAL (RED ALERT)",
                "title": title_en if is_en else title_ms,
                "explanation": exp_en if is_en else exp_ms,
                "species_note": species_note_en if is_en else species_note,
                "action_prompt": "GO TO A 24-HOUR VETERINARY HOSPITAL IMMEDIATELY!" if is_en else "BAWA KE HOSPITAL VETERINAR 24 JAM SERTA-MERTA!",
                "dos": [
                    "Keep pet calm, in a dark, quiet, ventilated carrier box.",
                    "If active bleeding, apply gentle direct pressure with a clean sterile cloth.",
                    "Call the nearest 24-hour emergency veterinary hospital while en route."
                ] if is_en else [
                    "Kekalkan haiwan dalam keadaan tenang, gelap, dan selesa di dalam sangkar pembawa (carrier).",
                    "Jika berlaku pendarahan aktif, gunakan kain bersih yang ditekan lembut pada bahagian luka.",
                    "Hubungi klinik kecemasan 24 jam dalam senarai di bawah SEKARANG sebelum bertolak."
                ],
                "donts": [
                    "DO NOT attempt home remedies (no salt water, coconut oil, or human medications).",
                    "DO NOT force pet to eat or drink while gasping or semi-conscious.",
                    "DO NOT wait until morning."
                ] if is_en else [
                    "JANGAN cuba merawat sendiri dengan petua kampung (minyak kelapa, air garam, susu).",
                    "JANGAN paksa haiwan makan atau minum ketika sesak nafas atau separuh sedar.",
                    "JANGAN tangguh masa sehingga keesokan pagi."
                ]
            }

    # 2. Check Specific Toxic Substances
    for toxin_key, data in TOXIC_SUBSTANCES.items():
        if toxin_key in msg_lower or (toxin_key == "coklat" and "chocolate" in msg_lower):
            is_crit = data["risk_level"] == "CRITICAL"
            badge = ("🔴 CRITICAL TOXIC EMERGENCY" if is_crit else "🟡 URGENT ATTENTION (AMBER ALERT)") if is_en else ("🔴 KECEMASAN TOKSIK" if is_crit else "🟡 PERHATIAN SEGERA (AMBER ALERT)")
            return {
                "is_emergency": True,
                "triage_level": data["risk_level"],
                "badge": badge,
                "title": f"TOXIC DANGER: {data['name']}" if is_en else f"BAHAYA TOKSIK: {data['name']}",
                "explanation": data.get("danger_explanation_en", data["danger_explanation"]) if is_en else data["danger_explanation"],
                "species_note": f"Target: {data['species_affected']}",
                "action_prompt": "CALL NATIONAL POISON CENTRE (1-800-88-8099) OR 24H VET" if is_en else "HUBUNGI PUSAT RACUN NEGARA (1-800-88-8099) ATAU VET 24 JAM",
                "dos": data.get("first_aid_dos_en", data["first_aid_dos"]) if is_en else data["first_aid_dos"],
                "donts": data.get("first_aid_donts_en", data["first_aid_donts"]) if is_en else data["first_aid_donts"]
            }

    # 3. Check HIGH triggers
    for pattern, title_ms, title_en, exp_ms, exp_en in HIGH_TRIGGERS:
        if re.search(pattern, msg_lower):
            return {
                "is_emergency": True,
                "triage_level": "HIGH",
                "badge": "🟡 HIGH PRIORITY (AMBER ALERT)" if is_en else "🟡 PERHATIAN TINGGI (HIGH PRIORITY)",
                "title": title_en if is_en else title_ms,
                "explanation": exp_en if is_en else exp_ms,
                "species_note": "",
                "action_prompt": "Please seek veterinary examination within 4-8 hours." if is_en else "Sila bawa untuk pemeriksaan veterinar dalam tempoh 4-8 jam.",
                "dos": [
                    "Monitor pet's gum color, body temperature, and breathing rate.",
                    "Ensure fresh drinking water is accessible if pet is able to swallow safely.",
                    "Take photos or videos of the vomit/stool/symptom for the veterinarian."
                ] if is_en else [
                    "Pantau suhu badan, warna gusi, dan kadar pernafasan haiwan.",
                    "Sediakan air minuman bersih sekiranya haiwan masih mampu menelan.",
                    "Ambil gambar atau rekod video simptom untuk ditunjukkan kepada doktor vet."
                ],
                "donts": [
                    "DO NOT administer human medicine without prescription.",
                    "DO NOT leave pet unattended."
                ] if is_en else [
                    "JANGAN beri ubat manusia tanpa preskripsi doktor vet.",
                    "JANGAN biarkan haiwan tanpa pemantauan."
                ]
            }

    # 4. Default: INFO
    return {
        "is_emergency": False,
        "triage_level": "INFO",
        "badge": "🟢 GENERAL PET CARE" if is_en else "🟢 INFO PENJAGAAN AM",
        "title": "General Care & Advice" if is_en else "Nasihat & Penjagaan Am",
        "explanation": "",
        "species_note": "",
        "action_prompt": "",
        "dos": [],
        "donts": []
    }

def get_seasonal_toxin_advisory(lang: str = "ms") -> Dict[str, Any]:
    """Generates real-time seasonal poison & toxin advisories based on Malaysian weather calendar."""
    import datetime
    month = datetime.datetime.now().month
    is_en = (lang.lower() == "en")
    
    # Months 10, 11, 12, 1 (Monsoon Season / Musim Tengkujuh & Hujan Tropika)
    if month in [10, 11, 12, 1]:
        season_name = "Monsoon & Heavy Rain Season (Northeast Monsoon)" if is_en else "Musim Monsun Timur Laut & Hujan Tropika Lebat"
        hazard_title = "Asian Common Toad (Bufo) & Mosquito Coils Alert" if is_en else "Amaran Katak Puru Beracun & Asap Ubat Nyamuk"
        alert_badge = "CRITICAL SEASONAL HAZARD" if is_en else "BAHAYA MUSIMAN KRITIKAL"
        description = (
            "Heavy rains drive toxic Asian common toads (*Duttaphrynus melanostictus*) into house porches at night. Additionally, high mosquito activity leads owners to burn mosquito coils (*Pyrethroids*), which cause fatal tremors in cats. Keep pets indoors after twilight!"
            if is_en else
            "Hujan lebat menyebabkan katak puru beracun (*Duttaphrynus*) kerap melompat masuk ke kawasan garaj/laman rumah pada waktu malam. Selain itu, asap lingkaran ubat nyamuk (*Pyrethroids*) untuk halau nyamuk adalah racun maut kepada saraf kucing. Pastikan haiwan di dalam rumah selepas maghrib!"
        )
        substances_spotlight = ["katak_puru", "ubat_nyamuk", "racun_siput"]
    # Months 2, 3, 4, 5 (Festive & Heatwave Season / Hari Raya & Cuaca Panas)
    elif month in [2, 3, 4, 5]:
        season_name = "Hot Dry Season & Festive Holidays" if is_en else "Musim Panas Kering & Perayaan"
        hazard_title = "Festive Chocolate, Grapes & Onion Gravies Alert" if is_en else "Amaran Coklat, Biskut Raya, Kismis & Kuah Berbawang"
        alert_badge = "HIGH FESTIVE HAZARD" if is_en else "BAHAYA MUSIM PERAYAAN TINGGI"
        description = (
            "During festive gatherings, guests frequently drop holiday chocolates, raisin cookies, or feed human table scraps rich in onions/garlic, triggering severe toxic emergencies."
            if is_en else
            "Semasa musim perayaan dan rumah terbuka, sisa biskut coklat, kismis, serta lauk berkuah bawang/sambal kerap termakan oleh haiwan. Awasi meja hidangan daripada si comel!"
        )
        substances_spotlight = ["coklat", "bawang", "anggur"]
    # Months 6, 7, 8, 9 (Mid-Year Garden & Flea Peak)
    else:
        season_name = "Mid-Year Tropical Garden & Pest Control" if is_en else "Musim Penjagaan Laman & Kawalan Serangga"
        hazard_title = "Garden Snail Baits & Dog Flea Spot-On Danger on Cats" if is_en else "Amaran Racun Siput Gondang & Ubat Kutu Anjing Pada Kucing"
        alert_badge = "ACTIVE SEASONAL HAZARD" if is_en else "BAHAYA TOKSIK AKTIF"
        description = (
            "Garden fertilizer, weed killer, and snail pellets (metaldehyde) are common summer hazards. Never apply canine flea/tick spot-on treatments onto cats."
            if is_en else
            "Penggunaan racun siput (metaldehyde) di laman serta kesilapan menitiskan ubat kutu anjing ke atas badan kucing adalah punca utama kes kecemasan klinik vet."
        )
        substances_spotlight = ["racun_siput", "ubat_nyamuk", "paracetamol"]

    return {
        "season_name": season_name,
        "hazard_title": hazard_title,
        "alert_badge": alert_badge,
        "description": description,
        "spotlight_substances": substances_spotlight,
        "last_sync": datetime.datetime.now().strftime("%d %B %Y, %I:%M %p")
    }

def get_live_toxin_catalog(lang: str = "ms") -> Dict[str, Any]:
    """Returns all toxic substances along with real-time dynamic seasonal advisories."""
    advisory = get_seasonal_toxin_advisory(lang=lang)
    return {
        "success": True,
        "seasonal_advisory": advisory,
        "total_substances": len(TOXIC_SUBSTANCES),
        "substances": TOXIC_SUBSTANCES,
        "last_synced": advisory["last_sync"]
    }

