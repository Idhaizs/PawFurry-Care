// PawFurry Care Malaysia - Enterprise Platform Controller (Dual Language & Telehealth Services)

// State
let currentLang = localStorage.getItem('pawfurry_lang') || 'ms';
let allNews = [];
let allClinics = [];
let userCoords = null;
let currentNewsCategory = 'Semua';
let autoRefreshTimer = null;

// --- DUAL LANGUAGE DICTIONARY (i18n) ---
const TRANSLATIONS = {
    ms: {
        navSubtitle: "Platform Telekesihatan Veterinar & Triage Kecemasan 24/7",
        masterSyncStatusLabel: "🟢 <strong>Auto-Sync Bersepadu Aktif:</strong> Chatbot Kucing & Anjing, Vet 24 Jam GPS, Panduan Toksin & Berita Live",
        masterSyncBtnLabel: "Sync Semula",
        chatBadgeTriageText: "Kucing & Anjing Sahaja",
        telemetryStatus: "Sistem Triage Aktif & Beroperasi 24/7",
        telemetryGov: "Pusat Rujukan: DVS Malaysia & Pusat Racun Negara (PRN USM)",
        sosBtnText: "SOS KECEMASAN",
        tabLabelChat: "Pembantu AI Veterinar",
        tabLabelNews: "Berita & Panduan Malaysia",
        tabLabelEmergency: "Vet 24 Jam & Hotline (GPS)",
        tabLabelToxins: "Panduan Racun & Toksin",
        stat1Label: "Hospital Vet 24 Jam Disahkan",
        stat2Label: "Masa Respons Triage Cemas",
        stat3Label: "Talian Pusat Racun Negara",
        stat4Label: "Liputan GPS Seluruh Malaysia",
        rapidEvaluatorTitle: "Penilai Simptom Pantas (Pilih Simptom untuk Nasihat Segera):",
        chatAssistantTitle: "Dr. PawFurry AI • Pakar Maya Veterinar",
        chatAssistantSubtitle: "Khusus Kucing & Anjing • Triage Kecemasan & Penjagaan Tropika Malaysia",
        chatInputPlaceholder: "Tanya soalan penjagaan atau simptom (cth: 'Kucing muntah buih' atau 'Boleh kucing makan nasi lemak?')...",
        sendBtnText: "Hantar",
        chatDisclaimerText: "⚠️ Nasihat ini bertujuan sebagai panduan maklumat am kesihatan haiwan. Dalam situasi kecemasan klinikal, sentiasa bawa ke klinik veterinar bertauliah.",
        newsBannerTag: "Buletin Rasmi & Panduan Penjagaan Malaysia",
        newsBannerTitle: "Informasi Terkini Kesihatan Haiwan Tempatan",
        newsBannerSubtitle: "Rujukan sahih berkaitan cuaca tropika, amaran musim banjir/hujan, wabak serantau (Sporo, Rabies), undang-undang kebajikan haiwan (Akta 772), serta panduan diet selamat.",
        newsSearchPlaceholder: "Cari artikel (cth: sporo, rabies, haba)...",
        liveSyncStatusText: "🟢 <strong>Live Sync Aktif:</strong> Berita dan amaran cuaca dikemaskini secara automatik",
        refreshBtnLabel: "Kemaskini Sekarang",
        newsShowingCountText: "Menunjukkan",
        newsArticlesText: "panduan artikel",
        newsVerifiedBadge: '<i class="fa-solid fa-check-circle text-xs"></i> Ditentusahkan Doktor Veterinar Bertauliah',
        gpsBannerTag: "Direktori Kecemasan Veterinar Malaysia",
        gpsBannerTitle: "Cari Hospital Vet 24 Jam Paling Dekat",
        gpsBannerSubtitle: "Kesan koordinat GPS semasa anda untuk mengira jarak tepat (KM) dan anggaran masa pemanduan ke hospital veterinar beroperasi 24 jam di Malaysia.",
        gpsLocateBtnText: "Kesan Lokasi Saya (GPS)",
        hotlineHeaderTitle: '<i class="fa-solid fa-phone-volume text-rose-600"></i> Talian Hotline Kecemasan Kebangsaan',
        filterStateLabel: "Tapis Negeri:",
        filter24hLabel: "Hanya Tunjukkan Klinik 24 Jam",
        clinicHeaderTitle: "Senarai Hospital & Klinik",
        toxinBannerTag: "Ensiklopedia Keselamatan Haiwan",
        toxinBannerTitle: "Bahan & Makanan Toksik di Rumah",
        toxinBannerSubtitle: "Senarai bahan lazim yang kerap menyebabkan keracunan maut pada kucing dan anjing di Malaysia.",
        toxinHotlineLabel: "Talian Keracunan:",
        footerText1: "Sistem Keselamatan & Sokongan Veterinar Bersepadu.",
        footerText2: "Direka khas untuk pemilik haiwan di Malaysia • Dilengkapi Perlindungan Triage Pintar",
        sosModalTitle: "Panggilan Kecemasan Veterinar (PawFurry SOS)",
        sosModalSubtitle: "Pilih talian bantuan kecemasan serta-merta mengikut situasi haiwan anda:",
        sosBombaSub: "Penyelamatan haiwan terperangkap / darurat",
        sosGpsTitle: "Navigasi ke Vet 24 Jam Terdekat",
        sosGpsSub: "Kira jarak GPS & pandu arah segera",
        artTagsLabel: "Topik Berkaitan:",
        artCloseBtn: "Tutup",
        artAskAiBtn: "Tanya AI Pasal Topik Ini",
        bannerCallText: "Hubungi Sekarang",
        bannerGpsText: "Cari Vet Terdekat",
        categories: ["Semua Topik", "Kesihatan & Penyakit", "Musim & Iklim Tropika", "Undang-Undang & Kebajikan", "Diet & Nutrisi"]
    },
    en: {
        navSubtitle: "24/7 Veterinary Telehealth & Emergency Triage Platform",
        masterSyncStatusLabel: "🟢 <strong>Unified Live Auto-Sync Active:</strong> Cat & Dog Chatbot, 24H Vet GPS, Toxin Guide & Live Bulletins",
        masterSyncBtnLabel: "Sync Now",
        chatBadgeTriageText: "Cats & Dogs Only",
        telemetryStatus: "Emergency Triage Engine Active & 24/7 Operational",
        telemetryGov: "Reference Hub: DVS Malaysia & National Poison Centre (PRN USM)",
        sosBtnText: "SOS EMERGENCY",
        tabLabelChat: "AI Veterinary Assistant",
        tabLabelNews: "Live Bulletins & Pet Care Guides",
        tabLabelEmergency: "24H Vet Directory (GPS)",
        tabLabelToxins: "Poison & Toxin Encyclopedia",
        stat1Label: "Verified 24H Emergency Hospitals",
        stat2Label: "Avg Triage Response Latency",
        stat3Label: "National Poison Control Hotline",
        stat4Label: "Nationwide Malaysia GPS Coverage",
        rapidEvaluatorTitle: "Rapid Symptom Evaluator (Click any symptom for immediate triage):",
        chatAssistantTitle: "Dr. PawFurry AI • Virtual Veterinary Specialist",
        chatAssistantSubtitle: "Exclusively for Cats & Dogs • Emergency Triage & Malaysian Tropical Care",
        chatInputPlaceholder: "Ask pet care or health questions (e.g. 'Cat vomiting foam' or 'Can cats eat nasi lemak?')...",
        sendBtnText: "Send",
        chatDisclaimerText: "⚠️ This advice serves as general informational pet care guidance. In persistent or emergency clinical cases, always visit a certified veterinary hospital.",
        newsBannerTag: "Official Malaysia Pet Care Advisories",
        newsBannerTitle: "Latest Local Pet Health & Weather Updates",
        newsBannerSubtitle: "Verified guides on tropical climate heatwaves, monsoon fungal warnings (Sporo, Rabies), animal welfare laws (Act 772), and safe feeding guidelines.",
        newsSearchPlaceholder: "Search articles (e.g., sporo, rabies, heatwave)...",
        liveSyncStatusText: "🟢 <strong>Live Sync Active:</strong> News and weather advisories update automatically",
        refreshBtnLabel: "Refresh Now",
        newsShowingCountText: "Displaying",
        newsArticlesText: "guides & advisories",
        newsVerifiedBadge: '<i class="fa-solid fa-check-circle text-xs"></i> Certified by Registered Malaysian Veterinarians',
        gpsBannerTag: "Malaysian Veterinary Emergency Directory",
        gpsBannerTitle: "Find Nearest 24-Hour Emergency Vet",
        gpsBannerSubtitle: "Detect your real-time GPS location to calculate exact distance (KM) and driving ETA to verified 24-hour veterinary hospitals across Malaysia.",
        gpsLocateBtnText: "Locate My Position (GPS)",
        hotlineHeaderTitle: '<i class="fa-solid fa-phone-volume text-rose-600"></i> National Emergency Veterinary Hotlines',
        filterStateLabel: "Filter State:",
        filter24hLabel: "Show 24-Hour Clinics Only",
        clinicHeaderTitle: "List of Hospitals & Clinics",
        toxinBannerTag: "Pet Safety Encyclopedia",
        toxinBannerTitle: "Household Toxins & Poison Hazards",
        toxinBannerSubtitle: "Common household foods and chemicals that cause fatal poisoning in dogs and cats in Malaysia.",
        toxinHotlineLabel: "Poison Hotline:",
        footerText1: "Integrated Veterinary Safety & Advisory System.",
        footerText2: "Built specifically for Malaysian pet parents • Powered by Intelligent Triage Guard",
        sosModalTitle: "Veterinary Emergency SOS Call",
        sosModalSubtitle: "Select immediate emergency assistance according to your pet's current distress:",
        sosBombaSub: "Fire & Rescue trapped animal emergency",
        sosGpsTitle: "Navigate to Nearest 24-Hour Vet",
        sosGpsSub: "Calculate GPS distance & turn-by-turn directions",
        artTagsLabel: "Related Topics:",
        artCloseBtn: "Close",
        artAskAiBtn: "Ask AI About This Topic",
        bannerCallText: "Call Now",
        bannerGpsText: "Find Nearest Vet",
        categories: ["All Topics", "Health & Diseases", "Malaysian Climate & Seasons", "Law & Pet Welfare", "Diet & Nutrition"]
    }
};

const QUICK_PILLS = {
    ms: [
        { label: "🚨 Kucing makan Panadol!", prompt: "Kucing saya termakan panadol! Apa nak buat?", style: "rose" },
        { label: "🚨 Kucing tak boleh kencing (FLUTD)", prompt: "Kucing jantan saya meneran dalam litter box tapi kencing tak keluar langsung", style: "rose" },
        { label: "🍛 Boleh kucing makan Nasi Lemak?", prompt: "Boleh ke kucing atau anjing makan nasi lemak? Bahaya tak untuk si bulu?", style: "amber" },
        { label: "💉 Jadual Vaksin Kucing (Tricat)", prompt: "Apakah jadual vaksin lengkap untuk anak kucing di Malaysia?", style: "emerald" },
        { label: "☀️ Cuaca Panas & Strok Haba", prompt: "Bila cuaca panas terik di Malaysia, macam mana nak elak kucing kena strok haba?", style: "teal" },
        { label: "🪱 Jadual Ubat Cacing & Kutu", prompt: "Berapa kerap kena beri ubat cacing dan ubat kutu?", style: "slate" }
    ],
    en: [
        { label: "🚨 Cat ate Panadol / Tylenol!", prompt: "My cat swallowed half a panadol paracetamol tablet! What should I do?", style: "rose" },
        { label: "🚨 Cat straining / blocked bladder", prompt: "My male cat is straining painfully in the litter box and cannot pee at all", style: "rose" },
        { label: "🍛 Can pets eat Nasi Lemak?", prompt: "Can cats or dogs eat nasi lemak? Is it safe or dangerous for them?", style: "amber" },
        { label: "💉 Kitten Vaccine Schedule (Tricat)", prompt: "What is the complete vaccination schedule for kittens in Malaysia?", style: "emerald" },
        { label: "☀️ Tropical Heatstroke Prevention", prompt: "During hot weather in Malaysia, how do I prevent heatstroke in my pets?", style: "teal" },
        { label: "🪱 Deworming & Flea Spot-on Schedule", prompt: "How often should I administer deworming and flea spot-on treatments in Malaysia?", style: "slate" }
    ]
};

// Initialize on Load
document.addEventListener('DOMContentLoaded', async () => {
    applyLanguage(currentLang);
    await triggerMasterSystemSync(false);

    // Master Auto-sync timer: Syncs all 4 pillars every 60 seconds (1 minute)
    autoRefreshTimer = setInterval(async () => {
        await triggerMasterSystemSync(false);
    }, 60000);
});

// --- RAPID SYMPTOM EVALUATOR ---
function evaluateSymptomQuick(symptomKey) {
    const isEn = currentLang === 'en';
    const prompts = {
        'cat_urinary': isEn 
            ? "My male cat is straining in the litter box, crying in pain, and cannot urinate at all. Is this an emergency?"
            : "Kucing jantan saya meneran dalam litter box tapi kencing tak keluar langsung. Adakah ini kecemasan?",
        'panadol_poison': isEn
            ? "Help! My cat swallowed half a panadol paracetamol tablet. What immediate steps should I take?"
            : "Tolong! Kucing saya termakan panadol separuh biji. Apakah langkah kecemasan segera?",
        'heatstroke': isEn
            ? "My pet is panting heavily with thick drool after being in the hot sun. Is this heatstroke and what first aid should I do?"
            : "Haiwan saya tercungap-cungap laju dan air liur meleleh selepas berada di bawah matahari panas terik. Adakah ini strok haba?",
        'dog_bloat': isEn
            ? "My dog's stomach suddenly became bloated and hard like a drum, trying to vomit with nothing coming out."
            : "Perut anjing saya membesar kembung keras tiba-tiba macam dram, cuba muntah tapi tak keluar apa-apa."
    };

    const promptText = prompts[symptomKey] || "";
    if (promptText) {
        switchTab('chat');
        sendQuickPrompt(promptText);
    }
}

// --- LANGUAGE SWITCHER CONTROLLER ---
function changeLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('pawfurry_lang', lang);
    applyLanguage(lang);
    loadNews();
}

function applyLanguage(lang) {
    const t = TRANSLATIONS[lang] || TRANSLATIONS.ms;

    // Toggle button styling
    const btnMs = document.getElementById('langBtnMs');
    const btnEn = document.getElementById('langBtnEn');
    if (btnMs) btnMs.innerText = "BM";
    if (btnEn) btnEn.innerText = "EN";

    if (lang === 'en') {
        btnEn.className = "px-2.5 py-1 text-xs font-bold rounded-lg transition bg-white text-emerald-700 shadow-2xs";
        btnMs.className = "px-2.5 py-1 text-xs font-semibold text-slate-500 rounded-lg transition hover:text-slate-800";
    } else {
        btnMs.className = "px-2.5 py-1 text-xs font-bold rounded-lg transition bg-white text-emerald-700 shadow-2xs";
        btnEn.className = "px-2.5 py-1 text-xs font-semibold text-slate-500 rounded-lg transition hover:text-slate-800";
    }

    // Update text content across DOM
    for (const [key, val] of Object.entries(t)) {
        const el = document.getElementById(key);
        if (el) {
            if (val.includes('<')) {
                el.innerHTML = val;
            } else {
                el.innerText = val;
            }
        }
    }

    // Placeholders
    const chatInput = document.getElementById('chatInput');
    if (chatInput) chatInput.placeholder = t.chatInputPlaceholder;
    const newsSearch = document.getElementById('newsSearchInput');
    if (newsSearch) newsSearch.placeholder = t.newsSearchPlaceholder;

    // Render Quick Prompts Pills
    renderQuickPills(lang);

    // Render Category Pills
    renderCategoryPills(lang);

    // Render Welcome Chat
    renderWelcomeChatMessage(lang);
}

function renderQuickPills(lang) {
    const container = document.getElementById('quickPillsContainer');
    const pills = QUICK_PILLS[lang] || QUICK_PILLS.ms;
    const label = lang === 'en' ? 'Quick Topics:' : 'Topik Pantas:';

    container.innerHTML = `
        <span class="text-slate-400 font-bold whitespace-nowrap text-[11px]">${label}</span>
        ${pills.map(p => `
            <button onclick="sendQuickPrompt('${p.prompt.replace(/'/g, "\\'")}')" class="px-3 py-1 bg-white hover:bg-${p.style}-50 text-${p.style}-700 border border-${p.style}-200 rounded-full font-medium whitespace-nowrap transition shadow-2xs">
                ${p.label}
            </button>
        `).join('')}
    `;
}

function renderCategoryPills(lang) {
    const container = document.getElementById('newsCategoriesContainer');
    const t = TRANSLATIONS[lang] || TRANSLATIONS.ms;
    const cats = t.categories;

    container.innerHTML = cats.map((cat, idx) => `
        <button onclick="filterNewsCategory('${idx === 0 ? 'Semua' : cat}')" class="news-cat-btn ${idx === 0 ? 'active bg-emerald-600 text-white' : 'bg-white hover:bg-slate-100 text-slate-600'} px-3.5 py-1.5 font-bold rounded-full transition shadow-xs whitespace-nowrap border border-slate-200">
            ${cat}
        </button>
    `).join('');
}

function renderWelcomeChatMessage(lang) {
    const chat = document.getElementById('chatMessages');
    const isEn = lang === 'en';

    chat.innerHTML = `
        <div class="flex items-start gap-3">
            <div class="w-10 h-10 rounded-2xl bg-emerald-600 text-white flex items-center justify-center text-lg shadow-sm shrink-0">
                <i class="fa-solid fa-user-doctor"></i>
            </div>
            <div class="bg-slate-100 rounded-2xl rounded-tl-sm p-4 text-xs sm:text-sm text-slate-800 max-w-[85%] leading-relaxed border border-slate-200 shadow-2xs">
                <p class="font-extrabold text-emerald-800 mb-1 flex items-center gap-1.5">
                    <span>Dr. PawFurry AI • Virtual Specialist</span>
                    <span class="text-[9px] bg-emerald-200/60 text-emerald-900 font-bold px-2 py-0.5 rounded-full">${isEn ? 'Dual Language Active' : 'Konteks Malaysia'}</span>
                </p>
                <p>${isEn ? 'Hello and welcome to <strong>PawFurry Care Telehealth System</strong>.' : 'Salam sejahtera dan selamat datang ke <strong>PawFurry Care Telehealth System</strong>.'}</p>
                <p class="mt-2">${isEn ? 'I can help answer your questions regarding pet health, vaccination protocols (Tricat / 6-in-1), tropical parasitic deworming, or assess clinical symptoms.' : 'Saya bersedia membantu menjawab sebarang persoalan mengenai kesihatan haiwan, protokol vaksinasi (Tricat / 6-in-1), kawalan kutu dan cacing tropika, mahupun menilai simptom klinikal.'}</p>
                <div class="mt-3 p-3 bg-rose-50 rounded-xl border border-rose-200 text-xs text-rose-900 flex items-start gap-2.5">
                    <span class="text-lg">🚨</span>
                    <div>
                        <strong class="font-bold">${isEn ? 'Zero-Delay Emergency Triage Active:' : 'Sistem Triage Deterministik Tanpa Lengah:'}</strong> 
                        ${isEn ? 'If your pet experiences life-threatening emergencies (such as blocked urinary tract, Panadol/Lily poisoning, bloat, or choking), the platform automatically activates immediate first-aid protocols and verified 24-hour hospital hotlines!' : 'Sekiranya haiwan anda menunjukkan tanda kecemasan maut (seperti kencing tersumbat, keracunan Panadol/Lili, perut kembung, atau sesak nafas), sistem terus mengaktifkan panduan cemas pantas serta talian hospital vet 24 jam!'}
                    </div>
                </div>
            </div>
        </div>
    `;
}

// --- TAB SWITCHING ---
function switchTab(tabId) {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active', 'text-emerald-700', 'border-emerald-600');
        btn.classList.add('text-slate-500', 'border-transparent');
    });
    document.querySelectorAll('.tab-section').forEach(sec => sec.classList.add('hidden'));

    const activeBtn = document.getElementById(`tab-btn-${tabId}`);
    if (activeBtn) {
        activeBtn.classList.add('active', 'text-emerald-700', 'border-emerald-600');
        activeBtn.classList.remove('text-slate-500', 'border-transparent');
    }
    const activeSec = document.getElementById(`section-${tabId}`);
    if (activeSec) {
        activeSec.classList.remove('hidden');
    }
}

// --- NEWS & CARE ARTICLES ---
async function loadNews() {
    try {
        const res = await fetch(`/api/news?lang=${currentLang}`);
        const data = await res.json();
        if (data.success) {
            allNews = data.news || [];
            renderNews(allNews);
        }
    } catch (err) {
        console.error("Failed to load pet care news:", err);
    }
}

async function triggerLiveNewsRefresh(showFeedback = true) {
    const btn = document.getElementById('refreshNewsBtn');
    const syncText = document.getElementById('lastSyncTimeText');

    if (btn && showFeedback) {
        btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin text-xs"></i> <span>${currentLang === 'en' ? 'Updating...' : 'Mengemaskini...'}</span>`;
        btn.disabled = true;
    }

    try {
        const res = await fetch('/api/news/refresh', { method: 'POST' });
        const data = await res.json();
        if (data.success) {
            await loadNews();
            if (syncText) {
                const label = currentLang === 'en' ? 'Last synced:' : 'Terakhir dikemaskini:';
                syncText.innerText = `${label} ${data.last_synced}`;
            }
        }
    } catch (err) {
        console.error("Live sync failed:", err);
    } finally {
        if (btn && showFeedback) {
            btn.innerHTML = `<i class="fa-solid fa-arrows-rotate text-xs"></i> <span>${TRANSLATIONS[currentLang].refreshBtnLabel}</span>`;
            btn.disabled = false;
        }
    }
}

function renderNews(articles) {
    const grid = document.getElementById('newsGrid');
    const countEl = document.getElementById('newsCount');
    if (countEl) countEl.innerText = articles.length;

    if (articles.length === 0) {
        grid.innerHTML = `
            <div class="col-span-full p-8 text-center bg-white rounded-3xl border border-slate-200">
                <i class="fa-solid fa-file-circle-question text-3xl text-slate-300 mb-2"></i>
                <h4 class="font-bold text-slate-700">${currentLang === 'en' ? 'No Articles Found' : 'Tiada Panduan Ditemui'}</h4>
                <p class="text-xs text-slate-500 mt-1">${currentLang === 'en' ? 'Try another keyword or select "All Topics".' : 'Cuba kata kunci lain atau pilih kategori Semua Topik.'}</p>
            </div>
        `;
        return;
    }

    grid.innerHTML = articles.map(art => `
        <div class="bg-white rounded-3xl p-5 sm:p-6 border ${art.is_live_alert ? 'border-amber-300 ring-2 ring-amber-100 shadow-sm' : 'border-slate-200/80 shadow-2xs'} hover:shadow-md transition flex flex-col justify-between group">
            <div>
                <!-- Category Badge & Live Alert Tag -->
                <div class="flex items-center justify-between mb-3">
                    <span class="text-[10px] font-black px-2.5 py-1 rounded-full ${art.is_live_alert ? 'bg-amber-100 text-amber-900 animate-pulse' : 'bg-emerald-100 text-emerald-800'}">
                        ${art.is_live_alert ? '⚡ LIVE ALERT: ' : ''}${art.category}
                    </span>
                    <span class="text-xs text-slate-400 flex items-center gap-1">
                        <i class="fa-regular fa-clock text-[10px]"></i> ${art.read_time}
                    </span>
                </div>

                <!-- Title -->
                <h3 class="font-bold text-sm sm:text-base text-slate-900 leading-snug group-hover:text-emerald-700 transition mb-2">
                    ${art.title}
                </h3>

                <!-- Summary -->
                <p class="text-xs text-slate-500 line-clamp-3 leading-relaxed mb-4">
                    ${art.summary}
                </p>

                <!-- Tags -->
                <div class="flex flex-wrap gap-1 mb-4">
                    ${(art.tags || []).slice(0, 3).map(tag => `
                        <span class="text-[10px] bg-slate-100 text-slate-600 font-semibold px-2 py-0.5 rounded-md">#${tag}</span>
                    `).join('')}
                </div>
            </div>

            <!-- Card Bottom -->
            <div class="pt-3 border-t border-slate-100 flex items-center justify-between">
                <span class="text-[11px] text-slate-400 font-medium">${art.published_date}</span>
                <button onclick="openArticleModal('${art.id}')" class="px-3.5 py-1.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 font-bold text-xs rounded-xl transition flex items-center gap-1 active:scale-95">
                    <span>${currentLang === 'en' ? 'Read Guide' : 'Baca Penuh'}</span>
                    <i class="fa-solid fa-arrow-right text-[10px]"></i>
                </button>
            </div>
        </div>
    `).join('');
}

function filterNewsCategory(cat) {
    currentNewsCategory = cat;
    document.querySelectorAll('.news-cat-btn').forEach(btn => {
        if (btn.innerText.includes(cat) || (cat === 'Semua' && (btn.innerText.includes('Semua') || btn.innerText.includes('All')))) {
            btn.className = "news-cat-btn active px-3.5 py-1.5 bg-emerald-600 text-white font-bold rounded-full transition shadow-xs whitespace-nowrap border border-emerald-600";
        } else {
            btn.className = "news-cat-btn px-3.5 py-1.5 bg-white hover:bg-slate-100 text-slate-600 font-semibold rounded-full border border-slate-200 transition whitespace-nowrap";
        }
    });

    let filtered = [...allNews];
    if (cat !== 'Semua' && cat !== 'All Topics') {
        const cleanCat = cat.replace(/[🩺🌦️⚖️🥩]/g, '').trim().toLowerCase();
        filtered = filtered.filter(n => n.category.toLowerCase().includes(cleanCat));
    }
    renderNews(filtered);
}

function onSearchNews(val) {
    const query = val.toLowerCase().trim();
    let filtered = allNews.filter(n => {
        return !query || 
            n.title.toLowerCase().includes(query) || 
            n.summary.toLowerCase().includes(query) || 
            (n.tags || []).some(t => t.toLowerCase().includes(query));
    });
    renderNews(filtered);
}

async function openArticleModal(newsId) {
    try {
        const res = await fetch(`/api/news/${newsId}?lang=${currentLang}`);
        const data = await res.json();
        if (data.success && data.article) {
            const article = data.article;
            document.getElementById('artCategoryBadge').innerText = article.category;
            document.getElementById('artTitle').innerText = article.title;
            document.getElementById('artAuthor').innerHTML = `<i class="fa-solid fa-user-doctor text-emerald-600 mr-1"></i> ${article.author}`;
            document.getElementById('artDate').innerHTML = `<i class="fa-regular fa-calendar mr-1"></i> ${article.published_date}`;
            document.getElementById('artReadTime').innerHTML = `<i class="fa-regular fa-clock mr-1"></i> ${article.read_time}`;
            document.getElementById('artContent').innerHTML = marked.parse(article.content);

            const tagsContainer = document.getElementById('artTags');
            tagsContainer.innerHTML = (article.tags || []).map(t => `
                <span class="text-xs bg-emerald-50 text-emerald-800 font-semibold px-2.5 py-1 rounded-lg border border-emerald-200">#${t}</span>
            `).join('');

            document.getElementById('articleModal').classList.remove('hidden');
        }
    } catch (err) {
        console.error("Failed to load article:", err);
    }
}

function closeArticleModal() {
    document.getElementById('articleModal').classList.add('hidden');
}

// --- CHATBOT CONTROLLER WITH COPY ACTIONS ---
async function handleChatSubmit(e) {
    e.preventDefault();
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    if (!message) return;

    input.value = "";
    appendUserMessage(message);
    const typingId = appendBotTypingIndicator();

    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                lang: currentLang
            })
        });

        const data = await res.json();
        removeBotTypingIndicator(typingId);

        if (data.success) {
            appendBotMessage(data.reply, data.is_emergency, data.triage_level, data.triage_details);

            if (data.is_emergency) {
                showEmergencyBanner(data.triage_details);
            }
        } else {
            appendBotMessage(data.error || "An error occurred.", false, 'INFO');
        }
    } catch (err) {
        removeBotTypingIndicator(typingId);
        appendBotMessage("Network connection error. Please try again.", false, 'INFO');
    }
}

function sendQuickPrompt(promptText) {
    document.getElementById('chatInput').value = promptText;
    document.getElementById('chatForm').dispatchEvent(new Event('submit', { cancelable: true }));
}

function appendUserMessage(text) {
    const chat = document.getElementById('chatMessages');
    const msgDiv = document.createElement('div');
    msgDiv.className = "flex items-start justify-end gap-3";
    msgDiv.innerHTML = `
        <div class="bg-emerald-600 text-white rounded-2xl rounded-tr-sm p-3.5 text-xs sm:text-sm max-w-[85%] shadow-sm leading-relaxed">
            <p>${escapeHtml(text)}</p>
        </div>
        <div class="w-8 h-8 rounded-full bg-slate-700 text-white flex items-center justify-center text-xs shadow-xs shrink-0">
            <i class="fa-solid fa-user"></i>
        </div>
    `;
    chat.appendChild(msgDiv);
    chat.scrollTop = chat.scrollHeight;
}

function appendBotTypingIndicator() {
    const chat = document.getElementById('chatMessages');
    const id = "typing-" + Date.now();
    const div = document.createElement('div');
    div.id = id;
    div.className = "flex items-start gap-3";
    div.innerHTML = `
        <div class="w-9 h-9 rounded-2xl bg-emerald-600 text-white flex items-center justify-center text-base shadow-xs shrink-0">
            <i class="fa-solid fa-user-doctor"></i>
        </div>
        <div class="bg-slate-100 rounded-2xl p-3 text-xs text-slate-500 flex items-center gap-2">
            <span class="inline-block w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span>${currentLang === 'en' ? 'Dr. PawFurry AI is analyzing clinical data...' : 'Dr. PawFurry AI sedang menganalisis maklumat klinikal...'}</span>
        </div>
    `;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
    return id;
}

function removeBotTypingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function appendBotMessage(replyMarkdown, isEmergency, triageLevel, triageDetails) {
    const chat = document.getElementById('chatMessages');
    const msgDiv = document.createElement('div');
    msgDiv.className = "flex items-start gap-3";

    const isCritical = triageLevel === 'CRITICAL';
    const bgClass = isCritical 
        ? 'bg-rose-50 border-2 border-rose-500' 
        : (isEmergency ? 'bg-amber-50 border border-amber-300' : 'bg-slate-50 border border-slate-200');

    const parsedHtml = marked.parse(replyMarkdown);
    const msgId = "bot-msg-" + Date.now();

    msgDiv.innerHTML = `
        <div class="w-9 h-9 rounded-2xl ${isEmergency ? 'bg-rose-600' : 'bg-emerald-600'} text-white flex items-center justify-center text-base shadow-sm shrink-0">
            <i class="fa-solid ${isEmergency ? 'fa-triangle-exclamation' : 'fa-user-doctor'}"></i>
        </div>
        <div class="${bgClass} rounded-2xl rounded-tl-sm p-4 text-xs sm:text-sm text-slate-800 max-w-[85%] leading-relaxed shadow-2xs markdown-body relative group">
            <div id="${msgId}">${parsedHtml}</div>
            
            <div class="mt-3 pt-2.5 border-t border-slate-200/60 flex items-center justify-between text-[11px] text-slate-400">
                <span class="font-mono text-[10px]">PawFurry Telehealth Verified</span>
                <button onclick="copyAdviceText('${msgId}')" class="text-slate-400 hover:text-slate-700 flex items-center gap-1 transition">
                    <i class="fa-regular fa-copy"></i> <span>${currentLang === 'en' ? 'Copy Advice' : 'Salin Nasihat'}</span>
                </button>
            </div>

            ${isEmergency ? `
                <div class="mt-3 pt-3 border-t border-rose-200 flex flex-wrap items-center gap-2">
                    <button onclick="switchTab('emergency'); findNearbyClinicsGps();" class="px-3.5 py-1.5 bg-rose-600 hover:bg-rose-700 text-white font-bold text-xs rounded-xl shadow-xs flex items-center gap-1.5 transition active:scale-95">
                        <i class="fa-solid fa-location-crosshairs"></i> ${currentLang === 'en' ? 'Route to Nearest Vet (GPS)' : 'Buka Navigasi Vet Terdekat'}
                    </button>
                    <a href="tel:1800888099" class="px-3.5 py-1.5 bg-white border border-rose-300 hover:bg-rose-50 text-rose-700 font-bold text-xs rounded-xl shadow-xs flex items-center gap-1.5 transition active:scale-95">
                        <i class="fa-solid fa-phone"></i> ${currentLang === 'en' ? 'Call Poison Centre (24H)' : 'Hubungi Pusat Racun (24 Jam)'}
                    </a>
                </div>
            ` : ''}
        </div>
    `;
    chat.appendChild(msgDiv);
    chat.scrollTop = chat.scrollHeight;
}

function copyAdviceText(elementId) {
    const el = document.getElementById(elementId);
    if (!el) return;
    const text = el.innerText;
    navigator.clipboard.writeText(text).then(() => {
        alert(currentLang === 'en' ? "Veterinary advice copied to clipboard!" : "Nasihat veterinar telah disalin ke papan keratan (clipboard)!");
    });
}

function clearChatScreen() {
    const chat = document.getElementById('chatMessages');
    chat.innerHTML = `
        <div class="text-center py-8 text-xs text-slate-400 font-medium">
            <i class="fa-solid fa-circle-check text-emerald-500 text-base mb-1 block"></i>
            ${currentLang === 'en' ? 'Conversation history cleared. Ready for your questions.' : 'Perbualan telah dipadamkan. Sedia untuk soalan baru anda.'}
        </div>
    `;
}

// --- EMERGENCY BANNER & SOS CONTROLS ---
function showEmergencyBanner(details) {
    const banner = document.getElementById('emergencyTopBanner');
    const title = document.getElementById('bannerEmergencyTitle');
    const sub = document.getElementById('bannerEmergencySubtitle');

    if (details && details.title) {
        title.innerText = details.title;
        sub.innerText = details.action_prompt || (currentLang === 'en' ? "Please rush to a 24-hour vet hospital or contact emergency hotlines." : "Sila bawa ke hospital veterinar atau hubungi talian kecemasan.");
    }

    banner.classList.remove('hidden');
}

function dismissEmergencyBanner() {
    document.getElementById('emergencyTopBanner').classList.add('hidden');
}

function openSosModal() {
    document.getElementById('sosModal').classList.remove('hidden');
}
function closeSosModal() {
    document.getElementById('sosModal').classList.add('hidden');
}

// --- UNIFIED MASTER SYSTEM AUTO-SYNC CONTROLLER ---
async function triggerMasterSystemSync(showFeedback = true) {
    const btn = document.getElementById('masterSyncBtn');
    const syncTimeText = document.getElementById('masterSyncTimeText');
    const lastSyncNews = document.getElementById('lastSyncTimeText');

    if (btn && showFeedback) {
        btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin text-xs"></i> <span>${currentLang === 'en' ? 'Syncing...' : 'Menyelaras...'}</span>`;
        btn.disabled = true;
    }

    try {
        const res = await fetch(`/api/system/sync?lang=${currentLang}`, { method: 'POST' });
        const data = await res.json();
        if (data.success) {
            if (syncTimeText) {
                syncTimeText.innerText = `Auto-Synced: ${data.formatted_time}`;
            }
            if (lastSyncNews) {
                lastSyncNews.innerText = `Auto-Synced: ${data.formatted_time}`;
            }

            await Promise.all([
                loadNews(),
                loadClinics(),
                loadHotlines(),
                loadToxins()
            ]);
        }
    } catch (err) {
        console.error("Master system sync error:", err);
    } finally {
        if (btn && showFeedback) {
            btn.innerHTML = `<i class="fa-solid fa-arrows-rotate text-xs"></i> <span>${TRANSLATIONS[currentLang].masterSyncBtnLabel}</span>`;
            btn.disabled = false;
        }
    }
}

// --- CLINICS & GPS GEOLOCATION DIRECTORY WITH WAZE & MAPS ---
async function loadClinics() {
    try {
        const res = await fetch(`/api/emergency/clinics?lang=${currentLang}`);
        const data = await res.json();
        if (data.success) {
            allClinics = data.clinics || [];
            renderClinics(allClinics);
        }

        const statusRes = await fetch(`/api/emergency/status?lang=${currentLang}`);
        const statusData = await statusRes.json();
        if (statusData.success) {
            updateLiveTrafficBar(statusData);
        }
    } catch (err) {
        console.error("Failed to load clinics:", err);
    }
}

function updateLiveTrafficBar(status) {
    const textEl = document.getElementById('liveTrafficStatusText');
    const badgeEl = document.getElementById('liveClinicsOpenBadge');
    const trafficEl = document.getElementById('liveTrafficBadge');

    if (textEl) {
        textEl.innerHTML = currentLang === 'en' 
            ? `<strong>Live Malaysia Time (${status.malaysia_time}):</strong> Emergency response standby active`
            : `<strong>Waktu Malaysia (${status.malaysia_time}):</strong> Pasukan kecemasan vet sedia bertugas`;
    }
    if (badgeEl) {
        badgeEl.innerText = currentLang === 'en'
            ? `${status.currently_open_count}/${status.total_clinics} Clinics Open`
            : `${status.currently_open_count}/${status.total_clinics} Klinik Dibuka`;
    }
    if (trafficEl) {
        trafficEl.innerText = status.traffic_condition;
        trafficEl.className = `bg-${status.traffic_badge_color}-100 text-${status.traffic_badge_color}-800 font-bold px-2 py-0.5 rounded text-[10px]`;
    }
}

async function loadHotlines() {
    try {
        const res = await fetch('/api/emergency/hotlines');
        const data = await res.json();
        if (data.success) {
            renderHotlines(data.hotlines || []);
        }
    } catch (err) {
        console.error("Failed to load hotlines:", err);
    }
}

async function loadToxins() {
    try {
        const res = await fetch(`/api/emergency/toxins?lang=${currentLang}`);
        const data = await res.json();
        if (data.success) {
            renderToxins(data.substances || data.toxins || {});
            if (data.seasonal_advisory) {
                renderSeasonalToxinAlert(data.seasonal_advisory);
            }
        }
    } catch (err) {
        console.error("Failed to load toxins:", err);
    }
}

function renderSeasonalToxinAlert(advisory) {
    const titleEl = document.getElementById('seasonalToxinTitle');
    const badgeEl = document.getElementById('seasonalToxinBadge');
    const descEl = document.getElementById('seasonalToxinDesc');
    const syncTimeEl = document.getElementById('seasonalToxinSyncTime');

    if (titleEl) titleEl.innerText = advisory.hazard_title;
    if (badgeEl) badgeEl.innerText = advisory.alert_badge;
    if (descEl) descEl.innerText = advisory.description;
    if (syncTimeEl) {
        syncTimeEl.innerText = `Auto-Synced: ${advisory.last_sync} (${advisory.season_name})`;
    }
}

function renderHotlines(hotlines) {
    const container = document.getElementById('hotlinesList');
    container.innerHTML = hotlines.map(h => `
        <div class="bg-white p-5 rounded-3xl border border-slate-200/80 shadow-2xs hover:shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-bold text-slate-800">${h.title}</span>
                    <span class="text-[10px] bg-slate-100 text-slate-700 font-bold px-2.5 py-0.5 rounded-full">${h.hours}</span>
                </div>
                <p class="text-[11px] text-slate-500 leading-relaxed mb-3">${h.description}</p>
            </div>
            <div class="flex items-center gap-2 pt-2 border-t border-slate-100">
                <a href="tel:${h.phone.replace(/[^0-9]/g, '')}" class="flex-1 py-2.5 bg-rose-600 hover:bg-rose-700 text-white font-extrabold text-xs rounded-xl shadow-xs text-center transition flex items-center justify-center gap-1.5 active:scale-95">
                    <i class="fa-solid fa-phone text-[10px]"></i> ${h.phone}
                </a>
            </div>
        </div>
    `).join('');
}

function renderClinics(clinics) {
    const container = document.getElementById('clinicsGrid');
    document.getElementById('clinicCount').innerText = clinics.length;

    if (clinics.length === 0) {
        container.innerHTML = `
            <div class="col-span-full p-8 text-center bg-white rounded-3xl border border-slate-200">
                <p class="text-xs text-slate-500">${currentLang === 'en' ? 'No clinics found for the selected filter.' : 'Tiada klinik ditemui mengikut tapisan yang dipilih.'}</p>
            </div>
        `;
        return;
    }

    container.innerHTML = clinics.map(c => {
        const wazeUrl = `https://waze.com/ul?ll=${c.lat},${c.lng}&navigate=yes`;
        const isOpen = c.is_open_now;
        const statusBadge = isOpen
            ? `<span class="text-[10px] font-black px-2.5 py-1 rounded-full shrink-0 bg-emerald-100 text-emerald-800 flex items-center gap-1">
                 <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                 ${currentLang === 'en' ? (c.status_label_en || 'OPEN NOW') : (c.status_label_ms || 'DIBUKA SEKARANG')}
               </span>`
            : `<span class="text-[10px] font-black px-2.5 py-1 rounded-full shrink-0 bg-amber-100 text-amber-800">
                 ${currentLang === 'en' ? (c.status_label_en || 'CLOSED (ON-CALL)') : (c.status_label_ms || 'TUTUP (ON-CALL)')}
               </span>`;

        return `
            <div class="bg-white p-5 sm:p-6 rounded-3xl border border-slate-200/80 shadow-2xs hover:shadow-md transition flex flex-col justify-between">
                <div>
                    <div class="flex items-start justify-between gap-2">
                        <div>
                            <h4 class="font-extrabold text-sm sm:text-base text-slate-900">${c.name}</h4>
                            <p class="text-xs text-emerald-700 font-bold mt-0.5">${c.area}, ${c.state}</p>
                        </div>
                        ${statusBadge}
                    </div>

                    <p class="text-xs text-slate-500 mt-2.5 flex items-start gap-1.5 leading-relaxed">
                        <i class="fa-solid fa-location-dot text-slate-400 mt-0.5 shrink-0"></i>
                        <span>${c.address}</span>
                    </p>

                    ${c.distance_km !== undefined ? `
                        <div class="mt-3 p-2.5 bg-emerald-50 border border-emerald-200 rounded-2xl flex items-center justify-between text-xs text-emerald-900">
                            <span class="font-bold">📍 ${currentLang === 'en' ? 'Distance:' : 'Jarak:'} ${c.distance_km} KM</span>
                            <span class="font-medium flex items-center gap-1">
                                🚗 ~${c.est_drive_minutes} mins
                                <span class="text-[10px] text-slate-500 font-normal">(${currentLang === 'en' ? (c.traffic_condition_en || 'Live Traffic') : (c.traffic_condition_ms || 'Trafik Semasa')})</span>
                            </span>
                        </div>
                    ` : ''}

                    <div class="mt-3 flex flex-wrap gap-1">
                        ${(c.specialties || []).map(s => `<span class="text-[10px] bg-slate-100 text-slate-600 font-medium px-2 py-0.5 rounded-md">${s}</span>`).join('')}
                    </div>
                </div>

                <div class="mt-4 pt-3.5 border-t border-slate-100 flex items-center gap-2">
                    <a href="tel:${(c.emergency_phone || c.phone).replace(/[^0-9+]/g, '')}" class="flex-1 py-2.5 bg-rose-600 hover:bg-rose-700 text-white font-black text-xs rounded-xl shadow-xs text-center transition flex items-center justify-center gap-1.5 active:scale-95">
                        <i class="fa-solid fa-phone"></i> ${currentLang === 'en' ? 'Call Vet' : 'Hubungi Vet'}
                    </a>
                    <a href="${c.google_maps_url}" target="_blank" rel="noopener noreferrer" class="px-3.5 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs rounded-xl transition flex items-center justify-center gap-1">
                        <i class="fa-solid fa-map-location-dot text-emerald-600"></i> Google Maps
                    </a>
                    <a href="${wazeUrl}" target="_blank" rel="noopener noreferrer" class="px-3 py-2.5 bg-sky-50 hover:bg-sky-100 text-sky-700 font-bold text-xs rounded-xl transition flex items-center justify-center gap-1">
                        <i class="fa-brands fa-waze text-sky-600"></i> Waze
                    </a>
                </div>
            </div>
        `;
    }).join('');
}

function filterClinics() {
    const state = document.getElementById('stateFilterSelect').value;
    const only24h = document.getElementById('only24hCheckbox').checked;

    let filtered = [...allClinics];
    if (state !== 'Semua') {
        filtered = filtered.filter(c => c.state.toLowerCase() === state.toLowerCase());
    }
    if (only24h) {
        filtered = filtered.filter(c => c.is_24_hours);
    }
    renderClinics(filtered);
}

// GPS Location Lookup
function findNearbyClinicsGps() {
    const btn = document.getElementById('gpsLocateBtn');
    if (!navigator.geolocation) {
        alert(currentLang === 'en' ? "Your browser does not support GPS Geolocation." : "Penyemak imbas anda tidak menyokong Geolocation GPS.");
        return;
    }

    btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> ${currentLang === 'en' ? 'Locating GPS Coordinates...' : 'Mengesan Lokasi GPS...'}`;
    btn.disabled = true;

    navigator.geolocation.getCurrentPosition(
        async (position) => {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;
            userCoords = { lat, lng };

            try {
                const res = await fetch(`/api/emergency/nearby?lat=${lat}&lng=${lng}`);
                const data = await res.json();
                if (data.success) {
                    allClinics = data.clinics;
                    renderClinics(allClinics);
                    const badge = document.getElementById('gpsStatusBadge');
                    if (badge) {
                        badge.innerText = currentLang === 'en' ? '📍 Sorted by Nearest GPS Distance' : '📍 Disusun mengikut jarak terdekat';
                        badge.classList.remove('hidden');
                    }
                }
            } catch (err) {
                alert(currentLang === 'en' ? "Failed to retrieve nearest clinics." : "Gagal memuat senarai klinik terdekat.");
            } finally {
                btn.innerHTML = `<i class="fa-solid fa-location-crosshairs text-base"></i><span>${TRANSLATIONS[currentLang].gpsLocateBtnText}</span>`;
                btn.disabled = false;
            }
        },
        (error) => {
            btn.innerHTML = `<i class="fa-solid fa-location-crosshairs text-base"></i><span>${TRANSLATIONS[currentLang].gpsLocateBtnText}</span>`;
            btn.disabled = false;
            alert(currentLang === 'en' ? "Unable to access GPS. Please grant browser location permission." : "Tidak dapat mengakses GPS. Sila benarkan kebenaran lokasi.");
        },
        { enableHighAccuracy: true, timeout: 10000 }
    );
}

function triggerEmergencyGps() {
    switchTab('emergency');
    findNearbyClinicsGps();
}

// --- TOXINS ENCYCLOPEDIA ---
function renderToxins(toxins) {
    const container = document.getElementById('toxinsGrid');
    const items = Object.values(toxins);

    container.innerHTML = items.map(t => `
        <div class="bg-white p-5 sm:p-6 rounded-3xl border ${t.risk_level === 'CRITICAL' ? 'border-rose-300 ring-2 ring-rose-50' : 'border-amber-300 ring-2 ring-amber-50'} shadow-2xs flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between mb-2">
                    <h4 class="font-extrabold text-sm sm:text-base text-slate-900">${t.name}</h4>
                    <span class="text-[10px] font-black px-2.5 py-0.5 rounded-full ${t.risk_level === 'CRITICAL' ? 'bg-rose-100 text-rose-800' : 'bg-amber-100 text-amber-800'}">
                        ${t.risk_level}
                    </span>
                </div>
                <p class="text-xs text-rose-700 font-bold mb-2">${currentLang === 'en' ? 'Target:' : 'Sasaran:'} ${t.species_affected}</p>
                <p class="text-xs text-slate-600 leading-relaxed mb-3">${currentLang === 'en' ? (t.danger_explanation_en || t.danger_explanation) : t.danger_explanation}</p>

                <div class="bg-slate-50 p-3.5 rounded-2xl border border-slate-100 mb-3 text-xs">
                    <strong class="text-slate-800 block mb-1.5 font-bold">${currentLang === 'en' ? 'Toxicity Symptoms:' : 'Simptom Keracunan:'}</strong>
                    <ul class="list-disc list-inside text-slate-600 space-y-1">
                        ${((currentLang === 'en' ? t.symptoms_en : t.symptoms) || t.symptoms || []).map(s => `<li>${s}</li>`).join('')}
                    </ul>
                </div>
            </div>

            <div class="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                <span class="text-slate-400 text-[11px] font-medium">${currentLang === 'en' ? 'Emergency Protocol: Seek Vet' : 'Protokol: Bawa ke vet segera'}</span>
                <a href="tel:1800888099" class="px-3.5 py-1.5 bg-rose-600 hover:bg-rose-700 text-white font-black rounded-xl text-xs shadow-xs transition active:scale-95">
                    ${currentLang === 'en' ? 'Call Poison Hotline' : 'Call Hotline PRN'}
                </a>
            </div>
        </div>
    `).join('');
}

// --- UTILS ---
function escapeHtml(str) {
    return str.replace(/[&<>'"]/g, 
        tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag] || tag)
    );
}
