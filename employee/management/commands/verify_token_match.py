from django.core.management.base import BaseCommand
from django.conf import settings
import requests

class Command(BaseCommand):
    help = 'Verify if settings token matches hardcoded token'

    def handle(self, *args, **options):
        print("🔍 VERIFIKASI TOKEN MATCH")
        print("=" * 40)
        
        # Get token from settings
        settings_token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', 'NOT_FOUND')
        hardcoded_token = 'urWuiF1pMJyGM25uJEjA'
        
        print(f"Settings token: {settings_token}")
        print(f"Hardcoded token: {hardcoded_token}")
        
        if settings_token == hardcoded_token:
            print("✅ TOKEN SAMA - masalah bukan di token")
        else:
            print("❌ TOKEN BERBEDA - ini penyebab masalah!")
            return
        
        # Test both with same exact message
        test_message = "🧪 Test exact same message"
        target = "6283838786991"
        
        print(f"\n📤 Test dengan pesan: {test_message}")
        print(f"📱 Target: {target}")
        
        # Test 1: Hardcoded way (simple_fonnte_test style)
        print("\n1️⃣ Method Hardcoded (simple_fonnte_test):")
        try:
            response1 = requests.post(
                'https://api.fonnte.com/send',
                headers={'Authorization': hardcoded_token},
                data={
                    'target': target,
                    'message': test_message,
                    'countryCode': '62'
                }
            )
            print(f"   Status: {response1.status_code}")
            print(f"   Response: {response1.text}")
            
            success1 = False
            if response1.status_code == 200:
                result1 = response1.json()
                success1 = result1.get('status', False)
                print(f"   Success: {success1}")
        except Exception as e:
            print(f"   Error: {e}")
            success1 = False
        
        # Test 2: Settings way (onboarding style)
        print("\n2️⃣ Method Settings (onboarding):")
        try:
            response2 = requests.post(
                getattr(settings, 'WHATSAPP_SERVICE_URL', 'https://api.fonnte.com/send'),
                headers={'Authorization': settings_token},
                data={
                    'target': target,
                    'message': test_message,
                    'countryCode': '62'
                },
                timeout=30
            )
            print(f"   Status: {response2.status_code}")
            print(f"   Response: {response2.text}")
            
            success2 = False
            if response2.status_code == 200:
                result2 = response2.json()
                success2 = result2.get('status', False)
                print(f"   Success: {success2}")
        except Exception as e:
            print(f"   Error: {e}")
            success2 = False
        
        # Compare results
        print(f"\n🎯 HASIL PERBANDINGAN:")
        print(f"Method 1 (hardcoded): {'✅ SUCCESS' if success1 else '❌ FAILED'}")
        print(f"Method 2 (settings): {'✅ SUCCESS' if success2 else '❌ FAILED'}")
        
        if success1 and success2:
            print("\n✅ KEDUA METHOD BERHASIL")
            print("   → Masalah BUKAN di token atau method")
            print("   → Kemungkinan masalah di:")
            print("     - Panjang pesan onboarding")
            print("     - Content pesan (link, emoji)")
            print("     - WhatsApp anti-spam filter")
            print("     - Device Fonnte offline")
        elif success1 and not success2:
            print("\n⚠️ HARDCODED BERHASIL, SETTINGS GAGAL")
            print("   → Masalah di konfigurasi settings")
            print("   → Cek WHATSAPP_SERVICE_URL dan WHATSAPP_SERVICE_TOKEN")
        elif not success1 and success2:
            print("\n⚠️ SETTINGS BERHASIL, HARDCODED GAGAL")
            print("   → Masalah di hardcoded token")
            print("   → Token mungkin sudah expired atau berubah")
        else:
            print("\n❌ KEDUA METHOD GAGAL")
            print("   → Masalah di akun Fonnte atau koneksi")
            print("   → Cek status device di dashboard Fonnte")
        
        # Test with onboarding-like message
        print(f"\n3️⃣ Test dengan pesan seperti onboarding:")
        onboarding_message = f"""Halo Test User! 👋

Selamat bergabung di perusahaan kami! 

Silakan lengkapi data onboarding Anda melalui link berikut:
http://localhost:8000/onboarding/test-token/

Link ini berlaku hingga: 02 January 2026, 07:11

Jika ada pertanyaan, silakan hubungi HR.

Terima kasih! 🙏"""
        
        try:
            response3 = requests.post(
                'https://api.fonnte.com/send',
                headers={'Authorization': hardcoded_token},
                data={
                    'target': target,
                    'message': onboarding_message,
                    'countryCode': '62'
                }
            )
            print(f"   Status: {response3.status_code}")
            print(f"   Response: {response3.text}")
            
            if response3.status_code == 200:
                result3 = response3.json()
                success3 = result3.get('status', False)
                print(f"   Success: {success3}")
                
                if success3:
                    print("   ✅ Pesan panjang dengan link juga berhasil")
                    print("   → Masalah kemungkinan di device atau delivery")
                else:
                    print("   ❌ Pesan panjang dengan link GAGAL")
                    print("   → Ini penyebab masalah onboarding!")
        except Exception as e:
            print(f"   Error: {e}")
        
        print(f"\n💡 REKOMENDASI:")
        print("1. Jika semua test SUCCESS → Cek dashboard Fonnte")
        print("2. Jika ada yang FAILED → Analisis error message")
        print("3. Cek device WhatsApp Business status")
        print("4. Test dengan pesan lebih pendek tanpa link")