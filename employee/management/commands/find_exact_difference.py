from django.core.management.base import BaseCommand
from django.conf import settings
import requests

class Command(BaseCommand):
    help = 'Find exact difference between working simple test vs onboarding system'

    def handle(self, *args, **options):
        print("🔍 MENCARI PERBEDAAN EKSAK")
        print("=" * 50)
        
        print("📋 PERBANDINGAN IMPLEMENTASI:")
        print("-" * 30)
        
        print("🟢 SIMPLE_FONNTE_TEST (YANG BEKERJA):")
        print("   - Token: HARDCODED 'urWuiF1pMJyGM25uJEjA'")
        print("   - URL: HARDCODED 'https://api.fonnte.com/send'")
        print("   - Headers: {'Authorization': token}")
        print("   - Data: {'target': '6283838786991', 'message': 'Test simple', 'countryCode': '62'}")
        print("   - Method: requests.post(url, headers=headers, data=data)")
        
        print("\n🔴 ONBOARDING SYSTEM (YANG BERMASALAH):")
        print("   - Token: getattr(settings, 'WHATSAPP_SERVICE_TOKEN', '')")
        print("   - URL: getattr(settings, 'WHATSAPP_SERVICE_URL', 'https://api.fonnte.com/send')")
        print("   - Headers: {'Authorization': token}")
        print("   - Data: {'target': phone, 'message': message, 'countryCode': '62'}")
        print("   - Method: requests.post(url, data=data, headers=headers, timeout=30)")
        
        print("\n🎯 PERBEDAAN YANG DITEMUKAN:")
        print("1. ⏰ TIMEOUT: Simple test TIDAK ada timeout, Onboarding ada timeout=30")
        print("2. 🔑 TOKEN SOURCE: Simple test hardcoded, Onboarding dari settings")
        print("3. 📝 LOGGING: Simple test minimal, Onboarding extensive logging")
        print("4. 📱 MESSAGE: Simple test pendek, Onboarding panjang dengan link")
        
        # Test actual values
        print("\n🧪 TEST NILAI AKTUAL:")
        print("-" * 30)
        
        # Get values from settings
        settings_token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', 'NOT_FOUND')
        settings_url = getattr(settings, 'WHATSAPP_SERVICE_URL', 'NOT_FOUND')
        
        print(f"Settings Token: {settings_token}")
        print(f"Settings URL: {settings_url}")
        print(f"Hardcoded Token: urWuiF1pMJyGM25uJEjA")
        
        # Check if they match
        if settings_token == 'urWuiF1pMJyGM25uJEjA':
            print("✅ Token SAMA antara simple test dan onboarding")
        else:
            print("❌ Token BERBEDA!")
            print("   Ini bisa jadi penyebab masalah")
        
        # Test both methods side by side
        print("\n🔬 TEST KEDUA METHOD BERSAMAAN:")
        print("-" * 30)
        
        # Method 1: Simple test way (hardcoded)
        print("1️⃣ Method Simple Test:")
        try:
            response1 = requests.post(
                'https://api.fonnte.com/send',
                headers={'Authorization': 'urWuiF1pMJyGM25uJEjA'},
                data={
                    'target': '6283838786991',
                    'message': '🧪 Test method 1 - hardcoded',
                    'countryCode': '62'
                }
            )
            print(f"   Status: {response1.status_code}")
            print(f"   Response: {response1.text}")
            
            if response1.status_code == 200:
                result1 = response1.json()
                if result1.get('status'):
                    print("   ✅ Method 1: SUCCESS")
                else:
                    print("   ❌ Method 1: FAILED")
        except Exception as e:
            print(f"   ❌ Method 1 Error: {e}")
        
        # Method 2: Onboarding way (from settings)
        print("\n2️⃣ Method Onboarding System:")
        try:
            response2 = requests.post(
                settings_url,
                headers={'Authorization': settings_token},
                data={
                    'target': '6283838786991',
                    'message': '🧪 Test method 2 - from settings',
                    'countryCode': '62'
                },
                timeout=30
            )
            print(f"   Status: {response2.status_code}")
            print(f"   Response: {response2.text}")
            
            if response2.status_code == 200:
                result2 = response2.json()
                if result2.get('status'):
                    print("   ✅ Method 2: SUCCESS")
                else:
                    print("   ❌ Method 2: FAILED")
        except Exception as e:
            print(f"   ❌ Method 2 Error: {e}")
        
        # Test with long message (like onboarding)
        print("\n3️⃣ Test dengan Pesan Panjang (seperti onboarding):")
        long_message = """Halo Test User! 👋

Selamat bergabung di perusahaan kami! 

Silakan lengkapi data onboarding Anda melalui link berikut:
http://localhost:8000/onboarding/test-token/

Link ini berlaku hingga: 2026-01-02

Jika ada pertanyaan, silakan hubungi HR.

Terima kasih! 🙏"""
        
        try:
            response3 = requests.post(
                'https://api.fonnte.com/send',
                headers={'Authorization': 'urWuiF1pMJyGM25uJEjA'},
                data={
                    'target': '6283838786991',
                    'message': long_message,
                    'countryCode': '62'
                }
            )
            print(f"   Status: {response3.status_code}")
            print(f"   Response: {response3.text}")
            
            if response3.status_code == 200:
                result3 = response3.json()
                if result3.get('status'):
                    print("   ✅ Long message: SUCCESS")
                else:
                    print("   ❌ Long message: FAILED")
        except Exception as e:
            print(f"   ❌ Long message Error: {e}")
        
        print("\n🎯 KESIMPULAN:")
        print("-" * 30)
        print("Jika semua 3 test di atas SUCCESS:")
        print("   → Masalah BUKAN di kode atau konfigurasi")
        print("   → Masalah di device Fonnte atau WhatsApp policy")
        print("Jika ada yang FAILED:")
        print("   → Kita temukan perbedaan yang menyebabkan masalah")
        
        print("\n💡 LANGKAH SELANJUTNYA:")
        print("1. Cek hasil 3 test di atas")
        print("2. Jika semua SUCCESS, cek dashboard Fonnte")
        print("3. Jika ada yang FAILED, analisis error message")
        print("4. Bandingkan response detail antara yang SUCCESS vs FAILED")