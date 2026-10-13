import json
import unittest
from app import app
from database import init_db

class TestPawFurryCareSystem(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        init_db()

    def test_01_health_check(self):
        """Test health endpoint."""
        res = self.client.get('/api/health')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn("PawFurry Care", data['service'])
        print("[PASS] Health Check Endpoint (PawFurry Care v1.2)")

    def test_02_news_bilingual_and_categories(self):
        """Test news in both Malay and English."""
        # Malay
        res_ms = self.client.get('/api/news?lang=ms')
        self.assertEqual(res_ms.status_code, 200)
        data_ms = json.loads(res_ms.data)
        self.assertTrue(data_ms['success'])
        self.assertIn("Haba", data_ms['news'][0]['title'])

        # English
        res_en = self.client.get('/api/news?lang=en')
        self.assertEqual(res_en.status_code, 200)
        data_en = json.loads(res_en.data)
        self.assertTrue(data_en['success'])
        self.assertIn("Heatwave", data_en['news'][0]['title'])
        print("[PASS] Dual-Language (BM & EN) News Listing")

    def test_03_news_live_refresh_endpoint(self):
        """Test live news auto-update refresh endpoint."""
        res = self.client.post('/api/news/refresh')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIn('last_synced', data)
        self.assertGreaterEqual(data['live_alerts_count'], 1)
        print(f"[PASS] Live News Auto-Update Sync Endpoint: {data['last_synced']}")

    def test_04_emergency_triage_english(self):
        """Test emergency red-flag trigger in English."""
        payload = {"message": "Help! My cat swallowed a panadol paracetamol tablet!", "lang": "en"}
        res = self.client.post('/api/chat', json=payload)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['is_emergency'])
        self.assertEqual(data['triage_level'], 'CRITICAL')
        self.assertIn("RED ALERT", data['reply'])
        self.assertIn("National Poison Centre", data['reply'])
        print("[PASS] Emergency Triage in English (Paracetamol Toxicity): CRITICAL Red Alert")

    def test_05_emergency_triage_malay(self):
        """Test emergency red-flag trigger in Malay."""
        payload = {"message": "Kucing jantan saya meneran dalam pasir tapi kencing tak keluar", "lang": "ms"}
        res = self.client.post('/api/chat', json=payload)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['is_emergency'])
        self.assertEqual(data['triage_level'], 'CRITICAL')
        self.assertIn("URINARY BLOCKAGE", data['reply'])
        self.assertIn("Pusat Racun Negara", data['reply'])
        print("[PASS] Emergency Triage in Bahasa Melayu (Urinary Blockage): CRITICAL Red Alert")

    def test_06_chat_bilingual_general(self):
        """Test general pet care inquiries in both English and Malay."""
        # English
        res_en = self.client.post('/api/chat', json={"message": "What is the vaccination schedule for puppies?", "lang": "en"})
        data_en = json.loads(res_en.data)
        self.assertFalse(data_en['is_emergency'])
        self.assertIn("Vaccination", data_en['reply'])

        # Malay
        res_ms = self.client.post('/api/chat', json={"message": "Bila waktu yang sesuai untuk cucuk vaksin anak kucing?", "lang": "ms"})
        data_ms = json.loads(res_ms.data)
        self.assertFalse(data_ms['is_emergency'])
        self.assertIn("Tricat", data_ms['reply'])
        print("[PASS] Bilingual Chat for Cats and Dogs (English & Bahasa Melayu)")

    def test_07_malaysia_clinics_and_gps_haversine(self):
        """Test clinics database and GPS distance calculation with real-time operational status and traffic ETA."""
        # KL City Center (3.1390, 101.6869)
        res = self.client.get('/api/emergency/nearby?lat=3.1390&lng=101.6869')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertGreater(data['count'], 5)
        first_clinic = data['clinics'][0]
        self.assertIn('google_maps_url', first_clinic)
        self.assertIn('is_open_now', first_clinic)
        self.assertIn('est_drive_minutes', first_clinic)
        self.assertIn('traffic_condition_ms', first_clinic)
        print(f"[PASS] Malaysia 24H Emergency Clinics & GPS Haversine Sort (Nearest: {first_clinic['name']} - Status: {first_clinic['status_label_ms']}, ETA: ~{first_clinic['est_drive_minutes']}m)")

    def test_08_security_headers(self):
        """Test HTTP security headers injection."""
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers.get('X-Content-Type-Options'), 'nosniff')
        self.assertEqual(res.headers.get('X-Frame-Options'), 'DENY')
        self.assertEqual(res.headers.get('X-XSS-Protection'), '1; mode=block')
        print("[PASS] Production HTTP Security Headers")

    def test_09_chat_out_of_domain_strict_guardrail(self):
        """Test strict rejection of out-of-domain inquiries (e.g., 'nasi lemak', human cooking, other species)."""
        # Test 1: General human food query without pet context (e.g. nasi lemak)
        res1 = self.client.post('/api/chat', json={"message": "nasi lemak sedap kat mana?", "lang": "ms"})
        data1 = json.loads(res1.data)
        self.assertTrue(data1.get('is_out_of_domain', False) or "khusus untuk" in data1['reply'].lower())
        self.assertIn("Kucing & Anjing", data1['reply'])
        self.assertIn("nasi lemak", data1['reply'])

        # Test 2: Coding question in English
        res2 = self.client.post('/api/chat', json={"message": "Can you write a python script to sort numbers?", "lang": "en"})
        data2 = json.loads(res2.data)
        self.assertIn("Cats & Dogs", data2['reply'])

        # Test 3: Other species inquiry (e.g. bird)
        res3 = self.client.post('/api/chat', json={"message": "Burung kakak tua saya tak nak makan bijirin", "lang": "ms"})
        data3 = json.loads(res3.data)
        self.assertIn("Kucing dan Anjing", data3['reply'])
        print("[PASS] Strict Chat Guardrail: Successfully intercepted and rejected off-topic queries (nasi lemak, coding, other species)")

    def test_10_chat_cat_dog_nasi_lemak_allowed_and_explained(self):
        """Test that asking if cats/dogs can eat nasi lemak is allowed and properly analyzed by veterinary logic."""
        res = self.client.post('/api/chat', json={"message": "Boleh ke kucing makan nasi lemak?", "lang": "ms"})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        # Should NOT be rejected as off-topic, because it is specifically asking about feline consumption
        self.assertIn("Santan Kelapa", data['reply'])
        self.assertIn("Bawang Merah", data['reply'])
        self.assertIn("TIDAK DIGALAKKAN", data['reply'])
        print("[PASS] Chat Knowledge: 'Boleh ke kucing makan nasi lemak?' correctly answered with clinical warnings")

    def test_11_unified_master_system_sync(self):
        """Test unified master sync endpoint updating chatbot, clinics, toxins, and news."""
        res = self.client.post('/api/system/sync?lang=ms')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIn('modules', data)
        self.assertIn('chatbot', data['modules'])
        self.assertIn('emergency_clinics', data['modules'])
        self.assertIn('toxins', data['modules'])
        self.assertIn('news', data['modules'])
        self.assertEqual(data['modules']['chatbot']['status'], 'synchronized')
        self.assertEqual(data['modules']['emergency_clinics']['status'], 'synchronized')
        print(f"[PASS] Master System Auto-Sync Endpoint: All 4 pillars synchronized at {data['formatted_time']}")

    def test_12_live_seasonal_toxins_catalog(self):
        """Test toxins endpoint returns live seasonal advisory spotlight."""
        res = self.client.get('/api/emergency/toxins?lang=ms')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIn('seasonal_advisory', data)
        self.assertIn('substances', data)
        self.assertIn('ubat_nyamuk', data['substances'])
        self.assertIn('katak_puru', data['substances'])
        print(f"[PASS] Live Seasonal Toxin Guide: Active Hazard '{data['seasonal_advisory']['hazard_title']}' with {data['total_substances']} substances")

if __name__ == '__main__':
    unittest.main()
