import datetime
from typing import List, Dict, Any, Optional

# --- BILINGUAL PET CARE NEWS & ADVISORIES DATABASE (MALAYSIA) ---

MALAYSIA_PET_NEWS = [
    {
        "id": "news_live_alert_heatwave",
        "title": "AMARAN CUACA: Gelombang Haba Panas Terik di Malaysia — Langkah Lindungi Haiwan Peliharaan",
        "title_en": "WEATHER ADVISORY: Extreme Heatwave in Malaysia — Steps to Protect Your Pets",
        "category": "Musim & Iklim Malaysia",
        "category_en": "Malaysian Climate & Seasons",
        "author": "Dr. Sarah (Veterinar Bertauliah, DVS Malaysia)",
        "author_en": "Dr. Sarah (Certified Veterinarian, DVS Malaysia)",
        "published_date": "13 Oktober 2026 (Terkini)",
        "published_date_en": "13 October 2026 (Live Alert)",
        "read_time": "4 min bacaan",
        "read_time_en": "4 min read",
        "badge_color": "rose",
        "is_live_alert": True,
        "summary": "Jabatan Meteorologi (MetMalaysia) mengeluarkan amaran gelombang haba tahap berjaga-jaga. Suhu melebihi 35°C membahayakan baka muka kemek (BSH, Persian, Pug) dan boleh mencetuskan strok haba dalam masa 30 minit.",
        "summary_en": "MetMalaysia issued an advisory heatwave alert. Temperatures exceeding 35°C put brachycephalic breeds (BSH, Persian, Pug) at severe risk of fatal heatstroke within 30 minutes.",
        "content": """
### Mengapa Haiwan Peliharaan Mudah Terkena Strok Haba di Malaysia?
Haiwan seperti kucing dan anjing **tidak mempunyai kelenjar peluh di seluruh badan** seperti manusia. Mereka hanya mengeluarkan haba melalui tapak kaki (*pads*) dan pernafasan tercungap-cungap (*panting*).

Di Malaysia, gabungan **suhu panas dan kelembapan udara yang tinggi (*high humidity*)** menyukarkan haba badan haiwan disejukkan secara semula jadi.

---

### Tanda-Tanda Amaran Strok Haba:
1. **Pernafasan Tercungap Laju:** Lidah terjelir panjang dan air liur meleleh pekat.
2. **Warna Gusi Tidak Normal:** Gusi bertukar merah darah terang atau merah keunguan (kekurangan oksigen).
3. **Muntah atau Cirit:** Disertai hilang keseimbangan badan semasa berjalan.
4. **Rebah & Sawan:** Suhu badan melebihi 39.5°C ke 41°C.

---

### Langkah Perlindungan Harian:
* **Sediakan Air Bersih Sejuk:** Letakkan beberapa mangkuk air di sudut rumah berbeza. Penggunaan *fountain* air sangat digalakkan.
* **Elakkan Sangkar di Luar Rumah:** Jangan kurung haiwan di kawasan beratap zink tanpa pengudaraan atau di balkoni kondo semasa matahari terik (11:00 AM – 4:00 PM).
* **Alas Tidur Penyejuk (*Cooling Mat*):** Letakkan alas penyejuk atau tuala lembap di lantai jubin sejuk.
* **JANGAN Mandikan dengan Air Ais Sejuk:** Jika haiwan kepanasan, basahkan badan dengan **air paip suhu bilik biasa**. Air berais mengecutkan salur darah dan memerangkap haba di organ dalaman.
        """,
        "content_en": """
### Why Are Pets Prone to Heatstroke in Malaysia?
Unlike humans, dogs and cats **do not have sweat glands across their bodies**. They only dissipate heat through their paw pads and rapid panting.

In Malaysia, the combination of **high tropical temperatures and elevated humidity** makes it difficult for pets to cool down naturally.

---

### Critical Warning Signs of Heatstroke:
1. **Excessive Heavy Panting:** Extended tongue and thick, sticky drool.
2. **Abnormal Gum Color:** Bright brick-red or bluish-purple gums (oxygen deprivation).
3. **Vomiting or Diarrhea:** Accompanied by staggering gait and weakness.
4. **Collapse & Seizures:** Body core temperature exceeding 39.5°C up to 41°C.

---

### Daily Protective Measures:
* **Provide Multiple Fresh Water Bowls:** Place cold fresh water in multiple rooms. Pet water fountains stimulate drinking.
* **Keep Pets Indoors:** Never keep pets in outdoor zinc-roofed cages or condo balconies during peak sun hours (11:00 AM – 4:00 PM).
* **Use Pet Cooling Mats:** Provide ceramic tile access or damp towels.
* **NEVER Use Freezing Ice Water:** If a pet is overheating, wet their body with **room-temperature tap water**. Ice water constricts superficial blood vessels and traps deadly heat inside vital organs.
        """,
        "tags": ["Strok Haba", "Cuaca Panas", "Kucing BSH", "Pertolongan Cemas"],
        "tags_en": ["Heatstroke", "Hot Weather", "BSH Cat", "First Aid"]
    },
    {
        "id": "news_live_sporo_monsoon",
        "title": "AMARAN KESIHATAN: Musim Hujan & Banjir — Waspada Wabak Sporo (Kulat Zoonotik) & Leptospirosis",
        "title_en": "HEALTH ADVISORY: Monsoon Season & Floods — Beware of Sporotrichosis (Sporo) & Leptospirosis",
        "category": "Kesihatan & Penyakit",
        "category_en": "Health & Diseases",
        "author": "Persatuan Kesihatan Veterinar Malaysia (MSAVA)",
        "author_en": "Malaysian Small Animal Veterinary Association (MSAVA)",
        "published_date": "11 Oktober 2026",
        "published_date_en": "11 October 2026",
        "read_time": "5 min bacaan",
        "read_time_en": "5 min read",
        "badge_color": "amber",
        "is_live_alert": True,
        "summary": "Musim tengkujuh meningkatkan risiko kulat Sporothrix schenckii (Sporo) yang boleh berjangkit kepada manusia (zoonotik) serta bakteria Leptospirosis daripada air bertakung dan banjir.",
        "summary_en": "Monsoon rains elevate risks of Sporothrix fungus (transmissible to humans) and Leptospirosis bacteria from stagnant puddles and flood water.",
        "content": """
### Ancaman Sporo di Malaysia: Penyakit Kulat yang Boleh Menjangkiti Manusia
*Sporotrichosis* (Sporo) adalah jangkitan kulat kronik yang kerap menyerang kucing di kawasan tropika berkelembapan tinggi seperti Malaysia. Kulat ini hidup dalam tanah lembap dan tumbuhan reput.

**Bahaya Utama:** Sporo adalah penyakit **Zoonotik**, bermakna ia boleh berjangkit kepada pemilik haiwan melalui calaran atau gigitan kucing yang dijangkiti!

---

### Tanda-Tanda Sporo pada Kucing:
* Luka berdarah atau berkudis di hidung, telinga, atau kaki yang **tidak pernah sembuh** walaupun disapu ubat biasa.
* Hidung bengkak seperti badut (*clown nose*) dan kerap bersin berdarah.
* Bengkak nodus limfa.

---

### Cara Pencegahan Semasa Musim Hujan:
1. **Kurung Kucing di Dalam Rumah (*Indoor Only*):** Kucing yang berkeliaran di luar mudah bergaduh dan terdedah kepada tanah berlumpur yang tercemar spora kulat.
2. **Jauhkan Anjing dari Air Bertakung/Banjir:** Jangan biarkan anjing minum air longkang atau lopak air untuk mengelakkan bakteria *Leptospirosis* (kencing tikus).
3. **Gunakan Sarung Tangan:** Jika merawat sebarang luka terbuka pada kucing, sentiasa pakai sarung tangan getah dan cuci tangan dengan sabun antiseptik.
4. **Dapatkan Rawatan Ubat Antikulat Segera:** Ubat khusus seperti *Itraconazole* daripada doktor vet perlu diberikan secara berdisiplin selama beberapa bulan sehingga luka sembuh sepenuhnya.
        """,
        "content_en": """
### Sporotrichosis in Malaysia: A Serious Zoonotic Threat
*Sporotrichosis* (Sporo) is a chronic fungal infection prevalent among cats in humid tropical climates like Malaysia. The fungus thrives in damp soil and decomposing vegetation.

**Key Risk:** Sporo is **zoonotic**, meaning it can easily transmit to humans through minor scratches, bites, or contact with open cat lesions!

---

### Common Symptoms in Cats:
* Ulcerative skin lesions on the nose, ears, or paws that **refuse to heal** with standard antiseptic treatments.
* Swollen 'clown nose' deformity with frequent bloody sneezing.
* Swollen regional lymph nodes.

---

### Monsoon Prevention Protocols:
1. **Strictly Keep Cats Indoors:** Outdoor roaming cats frequently fight and contract fungal spores from wet soil.
2. **Keep Dogs Away from Puddles & Flood Water:** Prevent dogs from drinking flood runoff to stop deadly *Leptospirosis* bacterial infection.
3. **Wear Protective Gloves:** Always handle cats with suspect lesions using disposable gloves, followed by antiseptic washing.
4. **Prompt Antifungal Therapy:** Prescription medications like *Itraconazole* must be administered consistently under veterinary care until full remission.
        """,
        "tags": ["Sporo", "Musim Hujan", "Kulat Kucing", "Zoonotik", "Banjir"],
        "tags_en": ["Sporo", "Monsoon", "Cat Fungus", "Zoonotic", "Floods"]
    },
    {
        "id": "news_rabies_malaysia_zone",
        "title": "Zon Kawalan Rabies di Malaysia: Kewajipan Vaksin & Keselamatan Pemilik Haiwan",
        "title_en": "Rabies Control Zones in Malaysia: Mandatory Vaccinations & Pet Owner Compliance",
        "category": "Undang-Undang & Kebajikan",
        "category_en": "Law & Pet Welfare",
        "author": "Biro Kesihatan Awam Veterinar DVS Putrajaya",
        "author_en": "Veterinary Public Health Division, DVS Putrajaya",
        "published_date": "08 Oktober 2026",
        "published_date_en": "08 October 2026",
        "read_time": "4 min bacaan",
        "read_time_en": "4 min read",
        "badge_color": "emerald",
        "is_live_alert": False,
        "summary": "Status terkini wabak rabies di Sarawak dan kawasan zon penampan utara Semenanjung. Ketahui tanggungjawab perundangan pemilik anjing dan kucing.",
        "summary_en": "Current rabies outbreak containment in Sarawak and Northern Peninsular buffer zones. Mandatory microchipping, licensing, and vaccination laws.",
        "content": """
### Status Semasa Penyakit Rabies (Anjing Gila) di Malaysia
Di Malaysia, negeri **Sarawak** masih diklasifikasikan sebagai kawasan wabak aktif Rabies, manakala kawasan utara Semenanjung (Perlis, Kedah, Pulau Pinang) diletakkan di bawah pengawasan zon imunisasi penampan.

Rabies adalah virus maut yang menyerang sistem saraf pusat. Sebaik sahaja simptom muncul, kadar kematian bagi haiwan dan manusia adalah **hampir 100%**.

---

### Tanggungjawab Pemilik di Kawasan Berisiko:
* **Vaksinasi Rabies Tahunan Wajib:** Semua anjing dan kucing di Sarawak dan kawasan zon kawalan diwajibkan mengambil suntikan vaksin Rabies setiap tahun.
* **Pemasangan Mikrocip & Lesen PBT:** Daftarkan anjing anda dengan Majlis Perbandaran tempatan dan pasangkan mikrocip pengenalan.
* **Kawal Haiwan Peliharaan:** Jangan biarkan haiwan berkeliaran tanpa tali pengikat (*leash*) di tempat awam.

---

### Tindakan Jika Digigit atau Dicalar Haiwan:
1. Basuh luka gigitan dengan **air mengalir dan sabun selama sekurang-kurangnya 15 minit** serta-merta.
2. Dapatkan suntikan vaksin profilaksis pasca-pendedahan (PEP) di hospital kerajaan terdekat pada hari yang sama.
3. Laporkan kepada Pejabat Perkhidmatan Veterinar Daerah (DVS) untuk tujuan kuarantin haiwan berkenaan.
        """,
        "content_en": """
### Current Rabies Status in Malaysia
The state of **Sarawak** remains designated as an active Rabies surveillance zone, while Northern Peninsular states (Perlis, Kedah, Penang) maintain immune buffer surveillance.

Rabies is a fatal viral zoonosis targeting the central nervous system. Once clinical symptoms develop, mortality in both humans and animals is **virtually 100%**.

---

### Legal Requirements for Pet Owners:
* **Mandatory Annual Rabies Vaccination:** Dogs and outdoor pets in designated zones must receive regular certified rabies vaccines.
* **Microchipping & Local Council Licensing:** Ensure dogs possess local city council tags and identification microchips.
* **Leash Laws:** Dogs must be kept on a leash and not allowed to roam unsupervised in public spaces.

---

### Immediate Bite Wound Protocol:
1. Wash bite wounds vigorously under **running tap water with soap for at least 15 minutes** immediately.
2. Seek urgent post-exposure prophylaxis (PEP) rabies vaccine at the nearest government hospital.
3. Notify the District Veterinary Services (DVS) office for animal quarantine tracking.
        """,
        "tags": ["Rabies", "Sarawak", "DVS Malaysia", "Vaksin Wajib", "Undang-Undang"],
        "tags_en": ["Rabies", "Sarawak", "DVS Malaysia", "Mandatory Vaccine", "Regulations"]
    },
    {
        "id": "news_batu_karang_flutd",
        "title": "Bahaya Ikan Bilis Masin & Makanan Bergaram: Ancaman Batu Karang Kucing Tempatan",
        "title_en": "The Danger of Salted Anchovies & Table Food: Blocked Bladder (FLUTD) in Local Cats",
        "category": "Diet & Nutrisi",
        "category_en": "Diet & Nutrition",
        "author": "Dr. Halim (Pakar Pemakanan Haiwan Kecil)",
        "author_en": "Dr. Halim (Small Animal Nutrition Specialist)",
        "published_date": "01 Oktober 2026",
        "published_date_en": "01 October 2026",
        "read_time": "3 min bacaan",
        "read_time_en": "3 min read",
        "badge_color": "teal",
        "is_live_alert": False,
        "summary": "Amalan tradisi memberi nasi gaul ikan bilis atau lauk manusia berkuah mengundang risiko batu karang maut (FLUTD / Feline Lower Urinary Tract Disease) kepada kucing jantan.",
        "summary_en": "Feeding cats salted anchovies and seasoned table food causes deadly struvite bladder stones and urinary blockage (FLUTD) in male cats.",
        "content": """
### Mitos 'Nasi Gaul Ikan Bilis' untuk Kucing Kampung
Ramai pemilik kucing di Malaysia menganggap hidangan tradisional nasi campur ikan bilis atau isi ikan kembung goreng bergaram adalah makanan terbaik untuk kucing kampung.

**Hakikat Perubatan Veterinar:**
* Ikan bilis kering mengandungi **kandungan garam (sodium) dan mineral magnesium/fosforus yang terlampau tinggi** untuk organ kucing.
* Kucing adalah *obligate carnivore* yang memerlukan protein daging haiwan dan taurine, bukan karbohidrat kanji seperti nasi putih.

---

### Bahaya Batu Karang Saluran Kencing (FLUTD / Struvite):
Bila buah pinggang kucing memproses mineral berlebihan daripada makanan masin, kristal halus (*struvite*) akan terbentuk di dalam pundi kencing.

Bagi **kucing jantan**, saluran kencingnya (*urethra*) adalah sempit. Kristal ini boleh menyumbat saluran kencing sepenuhnya dalam sekelip mata!
* Kucing tidak dapat membuang air kencing langsung.
* Toksin kencing (urea & potassium) berkumpul dalam darah.
* Dalam tempoh **24 hingga 48 jam**, jantung kucing boleh terhenti akibat *hyperkalemia*.

---

### Pilihan Diet Selamat:
1. Elakkan sama sekali memberi makanan bergaram, berperisa, atau sisa lauk pauk manusia.
2. Pilih makanan kering (*kibble*) yang mempunyai label seimbang kawalan pH kencing (*Urinary Care / Magnesium controlled*).
3. Selang-selikan dengan makanan basah (*wet food*) atau ayam rebus tanpa garam untuk meningkatkan pengambilan air harian.
        """,
        "content_en": """
### The 'Rice with Salted Anchovies' Myth
Many Malaysian pet owners traditionally feed their cats white rice mixed with dried salted anchovies (*ikan bilis*) or fried fish.

**Veterinary Medical Reality:**
* Dried anchovies carry **excessive levels of sodium, magnesium, and phosphorus** that overload feline kidneys.
* Cats are strict *obligate carnivores* needing animal proteins and taurine, not high-starch carbohydrates like white rice.

---

### The Threat of Blocked Bladders (FLUTD / Struvite Stones):
Excess dietary minerals precipitate into sharp microscopic crystals inside the bladder.

In **male cats**, the urethra is extremely narrow. These crystals form a solid plug, completely blocking urine output!
* The cat strains agonizingly in the litter box without passing urine.
* Lethal metabolic wastes (urea and potassium) flood the bloodstream.
* Within **24 to 48 hours**, cardiac arrest occurs due to severe *hyperkalemia*.

---

### Safe Feeding Guidelines:
1. Never give table scraps, salty gravy, or cured dried fish.
2. Select quality commercial kibble formulated with urinary pH and mineral controls.
3. Incorporate wet food and unseasoned boiled chicken breasts to boost essential daily hydration.
        """,
        "tags": ["Nutrisi Kucing", "Batu Karang", "FLUTD", "Ikan Bilis", "Diet Sihat"],
        "tags_en": ["Cat Nutrition", "Bladder Stones", "FLUTD", "Anchovies", "Healthy Diet"]
    },
    {
        "id": "news_akta_kebajikan_haiwan",
        "title": "Akta Kebajikan Haiwan 2015: Penalti Hingga RM100,000 Jika Mengabaikan Haiwan Kesayangan",
        "title_en": "Animal Welfare Act 2015: Fines up to RM100,000 for Pet Neglect and Cruelty",
        "category": "Undang-Undang & Kebajikan",
        "category_en": "Law & Pet Welfare",
        "author": "Jabatan Perkhidmatan Veterinar Malaysia (DVS)",
        "author_en": "Department of Veterinary Services Malaysia (DVS)",
        "published_date": "25 September 2026",
        "published_date_en": "25 September 2026",
        "read_time": "4 min bacaan",
        "read_time_en": "4 min read",
        "badge_color": "purple",
        "is_live_alert": False,
        "summary": "Ketahui hak haiwan dan kewajipan undang-undang pemilik di Malaysia di bawah Seksyen 29 & 30 Akta Kebajikan Haiwan 2015 (Akta 772).",
        "summary_en": "Understanding pet owners' legal duties under Sections 29 & 30 of Malaysia's Animal Welfare Act 2015 (Act 772).",
        "content": """
### Pemilik Haiwan Terikat dengan Undang-Undang Malaysia
Ramai yang tidak menyedari bahawa mengabaikan atau tidak menyediakan keperluan asas kepada haiwan peliharaan adalah satu **kesalahan jenayah serius** di bawah **Akta Kebajikan Haiwan 2015 (Akta 772)**.

Jika disabitkan kesalahan, pesalah boleh dikenakan denda antara **RM20,000 hingga RM100,000** atau hukuman penjara sehingga **3 tahun**, atau kedua-duanya sekali!

---

### 5 Kewajipan Asas Pemilik di Bawah Akta 772:
1. **Keperluan Makanan & Air Bersih:** Menyediakan diet berkhasiat dan air minuman yang mencukupi setiap hari.
2. **Tempat Perlindungan yang Sesuai:** Haiwan tidak boleh dibiarkan berhujan atau berpanas tanpa bumbung berteduh.
3. **Pencegahan daripada Kesakitan & Penyakit:** Wajib membawa haiwan yang sakit mendapatkan rawatan veterinar yang wajar.
4. **Peluang Mengekspresikan Tingkah Laku Semula Jadi:** Ruang pergerakan yang selesa dan tidak dirantai sepanjang hari tanpa henti.
5. **Perlindungan daripada Ketakutan & Tekanan:** Tidak didera secara fizikal atau mental.

---

### Saluran Aduan Rasmi Penganiayaan Haiwan:
Jika anda menyaksikan sebarang kes penderaan atau pengabaian haiwan di kawasan kejiranan anda:
* Layari Portal Aduan Rasmi DVS: **awa.dvs.gov.my**
* Hubungi Bilik Gerakan Kebajikan Haiwan DVS: **03-8870 2000**
        """,
        "content_en": """
### Pet Owners Are Bound by Malaysian Law
Failing to provide basic welfare standards for your pets is a **serious criminal offense** under the **Animal Welfare Act 2015 (Act 772)**.

Convicted offenders face mandatory fines ranging from **RM20,000 up to RM100,000**, imprisonment for up to **3 years**, or both!

---

### The 5 Essential Freedoms Under Act 772:
1. **Nutritious Food & Clean Water:** Suitable sustenance supplied daily.
2. **Proper Shelter:** Adequate protection from tropical heat, heavy rain, and harsh weather.
3. **Veterinary Medical Care:** Sick or injured pets must receive timely certified veterinary treatment.
4. **Natural Behavioral Freedom:** Adequate space to move freely; continuous inhumane chaining is strictly prohibited.
5. **Protection from Mental & Physical Distress:** Free from abuse, abandonment, and cruelty.

---

### Official Animal Cruelty Reporting Portals:
To report cruelty or neglect cases across Malaysia:
* Official DVS Cruelty Portal: **awa.dvs.gov.my**
* DVS Animal Welfare Operations Hotline: **03-8870 2000**
        """,
        "tags": ["Akta 772", "DVS", "Kebajikan Haiwan", "Undang-Undang", "Denda"],
        "tags_en": ["Act 772", "DVS", "Animal Welfare", "Law", "Penalties"]
    },
    {
        "id": "news_subsidi_mandul_spca",
        "title": "Program Subsidi Pemandulan Kucing & Anjing: Cara Jimat Kos Mandul di Malaysia",
        "title_en": "Subsidized Spaying & Neutering Programs: How to Save Costs on Pet Sterilization in Malaysia",
        "category": "Kesihatan & Penyakit",
        "category_en": "Health & Diseases",
        "author": "Klinik Kembiri SPCA & Klinik Haiwan Kerajaan",
        "author_en": "SPCA Spay Clinic & Community Animal Welfare",
        "published_date": "18 September 2026",
        "published_date_en": "18 September 2026",
        "read_time": "3 min bacaan",
        "read_time_en": "3 min read",
        "badge_color": "emerald",
        "is_live_alert": False,
        "summary": "Panduan mendapatkan subsidi kos pemandulan (spay/neuter) serendah RM60-RM120 melalui Klinik Kembiri SPCA dan program veterinar komuniti.",
        "summary_en": "A practical guide to securing affordable spay/neuter subsidies from RM60-RM120 via SPCA Klinik Kembiri and community veterinary initiatives.",
        "content": """
### Mengapa Pemandulan Sangat Penting?
Di klinik swasta biasa, kos pemandulan boleh mencecah antara RM120 hingga RM350 untuk kucing dan RM250 hingga RM600 untuk anjing.

Walau bagaimanapun, pemandulan (*spaying / neutering*) adalah kunci utama untuk:
* Mencegah pembiakan luar kawalan haiwan terbiar di jalanan.
* Mengelakkan jangkitan nanah rahim maut (*Pyometra*) pada kucing betina.
* Menghapuskan tabiat kencing menanda kawasan (*spraying*) dan pergaduhan haiwan jantan.

---

### Tempat Mendapatkan Rawatan Mandul Bersubsidi:
1. **Klinik Kembiri SPCA Selangor:**
   * Terletak di Ampang, Selangor. Menyediakan pemandulan dengan caj mampu milik untuk kucing dan anjing baka tempatan.
   * Hubungi: **03-4256 5312**.
2. **Hospital Veterinar Universiti (UVH - UPM):**
   * Menyediakan kadar rawatan pelajar/komuniti bagi kes pemandulan rutin.
   * Hubungi: **03-9769 3900**.
3. **Klinik Veterinar Kerajaan (DVS Negeri):**
   * Sesetengah cawangan DVS daerah menawarkan khidmat pemandulan haiwan pada kadar subsidi kerajaan mengikut jadual temujanji bulanan.
4. **Program TNRM (*Trap-Neuter-Release-Manage*):**
   * Organisasi NGO seperti PAWS Animal Welfare Society dan Malaysian Dogs Deserve Better (MDDB) sering menganjurkan klinik kembiri bergerak.
        """,
        "content_en": """
### Why Sterilization Is Vital for Pets:
Private clinic spaying fees range from RM120 to RM350 for cats and RM250 to RM600 for dogs.

However, spaying and neutering are crucial for:
* Preventing stray pet overpopulation.
* Eliminating deadly uterine infections (*Pyometra*) in unspayed female cats and dogs.
* Reducing territorial urine spraying and aggressive fighting in males.

---

### Where to Find Subsidized Sterilization:
1. **SPCA Selangor Klinik Kembiri:**
   * Located in Ampang, Selangor. Offers heavily subsidized neutering services for local rescue animals.
   * Contact: **03-4256 5312**.
2. **Universiti Putra Malaysia Veterinary Hospital (UVH - UPM):**
   * Provides community/teaching hospital rates for routine neutering surgeries.
   * Contact: **03-9769 3900**.
3. **Government Veterinary Clinics (State DVS):**
   * Select regional DVS branches offer seasonal sterilization slots at government-subsidized rates.
4. **TNRM (Trap-Neuter-Release-Manage) Community Programs:**
   * NGOs like PAWS Animal Welfare Society and MDDB frequently organize mobile low-cost spay clinics.
        """,
        "tags": ["Kembiri", "Mandul", "SPCA", "Subsidi Kos", "Jimat Belanja"],
        "tags_en": ["Neutering", "Spaying", "SPCA", "Subsidized Care", "Budget Pet Care"]
    }
]

# Track live sync timestamp
LAST_SYNCED = datetime.datetime.now()

def refresh_live_advisories() -> Dict[str, Any]:
    """
    Simulates / triggers live sync of Malaysian pet advisories,
    updating timestamps and fetching latest weather-health correlations.
    """
    global LAST_SYNCED
    LAST_SYNCED = datetime.datetime.now()
    now_str = LAST_SYNCED.strftime("%d %B %Y, %I:%M %p")
    
    # Update live alert publication dates to current moment
    for item in MALAYSIA_PET_NEWS:
        if item.get("is_live_alert"):
            item["published_date"] = f"{now_str} (Live Updated)"
            item["published_date_en"] = f"{now_str} (Live Updated)"
            
    return {
        "success": True,
        "last_synced": now_str,
        "total_articles": len(MALAYSIA_PET_NEWS),
        "live_alerts_count": sum(1 for x in MALAYSIA_PET_NEWS if x.get("is_live_alert"))
    }

def get_all_news(category: Optional[str] = None, search_query: Optional[str] = None, lang: str = "ms") -> List[Dict[str, Any]]:
    """Returns list of news localized to requested language ('ms' or 'en')."""
    results = []
    cat_clean = (category or "").strip().lower()
    query = (search_query or "").strip().lower()

    for item in MALAYSIA_PET_NEWS:
        # Check category match (in either language)
        item_cat_ms = item.get("category", "").lower()
        item_cat_en = item.get("category_en", "").lower()
        
        if cat_clean and cat_clean not in ["semua", "all"]:
            if (cat_clean not in item_cat_ms and item_cat_ms not in cat_clean and
                cat_clean not in item_cat_en and item_cat_en not in cat_clean):
                continue

        # Check search query (in either language)
        if query:
            match_ms = (query in item.get("title", "").lower() or 
                        query in item.get("summary", "").lower() or
                        any(query in t.lower() for t in item.get("tags", [])))
            match_en = (query in item.get("title_en", "").lower() or 
                        query in item.get("summary_en", "").lower() or
                        any(query in t.lower() for t in item.get("tags_en", [])))
            if not (match_ms or match_en):
                continue

        # Prepare localized output dict
        is_en = (lang.lower() == "en")
        loc_item = {
            "id": item["id"],
            "title": item.get("title_en") if is_en else item.get("title"),
            "category": item.get("category_en") if is_en else item.get("category"),
            "author": item.get("author_en") if is_en else item.get("author"),
            "published_date": item.get("published_date_en") if is_en else item.get("published_date"),
            "read_time": item.get("read_time_en") if is_en else item.get("read_time"),
            "badge_color": item.get("badge_color", "emerald"),
            "is_live_alert": item.get("is_live_alert", False),
            "summary": item.get("summary_en") if is_en else item.get("summary"),
            "tags": item.get("tags_en") if is_en else item.get("tags")
        }
        results.append(loc_item)

    return results

def get_news_by_id(news_id: str, lang: str = "ms") -> Optional[Dict[str, Any]]:
    """Fetches single news article localized to requested language."""
    for item in MALAYSIA_PET_NEWS:
        if item["id"] == news_id:
            is_en = (lang.lower() == "en")
            return {
                "id": item["id"],
                "title": item.get("title_en") if is_en else item.get("title"),
                "category": item.get("category_en") if is_en else item.get("category"),
                "author": item.get("author_en") if is_en else item.get("author"),
                "published_date": item.get("published_date_en") if is_en else item.get("published_date"),
                "read_time": item.get("read_time_en") if is_en else item.get("read_time"),
                "badge_color": item.get("badge_color", "emerald"),
                "is_live_alert": item.get("is_live_alert", False),
                "summary": item.get("summary_en") if is_en else item.get("summary"),
                "content": item.get("content_en") if is_en else item.get("content"),
                "tags": item.get("tags_en") if is_en else item.get("tags")
            }
    return None
