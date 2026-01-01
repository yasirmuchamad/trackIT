from django.core.management.base import BaseCommand
from django.conf import settings
import requests
import json

class Command(BaseCommand):
    help = 'Comprehensive Fonnte issue diagnosis'

    def handle(self, *args, **options):
        print("🔍 DIAGNOSA LENGKAP MASALAH FONNTE")
        print("=" * 60)
        
        # Get token from settings
        token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', '')
        
        if not token:
            print("❌ Token tidak ditemukan di settings")
            return
            
        print(f"🔑 Token: {token[:10]}...")
        
        # 1. Check account profile
        print("\n1️⃣ CEK PROFIL AKUN FONNTE")
        print("-" * 30)
        try:
            response = requests.get(
                'https://api.fonnte.com/profile',
                headers={'Authorization': token}
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                profile = response.json()
                print(f"✅ Nama: {profile.get('name', 'N/A')}")
                print(f"✅ Device: {profile.get('device', 'N/A')}")
                print(f"✅ Status: {profile.get('status', 'N/A')}")
                print(f"✅ Quota: {profile.get('quota', 'N/A')}")
                
                # Check device status
                device_status = profile.get('status', '').lower()
                if 'disconnect' in device_status or 'offline' in device_status:
                    print("🚨 MASALAH DITEMUKAN: Device WhatsApp OFFLINE!")
                    print("   Ini menjelaskan mengapa pesan tidak masuk ke history")
                elif 'connect' in device_status or 'online' in device_status:
                    print("✅ Device WhatsApp online")
                else:
                    print(f"⚠️ Status device tidak jelas: {device_status}")
            else:
                print(f"❌ Error: {response.text}")
        except Exception as e:
            print(f"❌ Error checking profile: {e}")
        
        # 2. Check message history
        print("\n2️⃣ CEK HISTORY PESAN")
        print("-" * 30)
        try:
            response = requests.get(
                'https://api.fonnte.com/history',
                headers={'Authorization': token}
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                history = response.json()
                if isinstance(history, list) and len(history) > 0:
                    print(f"✅ Ditemukan {len(history)} pesan dalam history")
                    # Show last 3 messages
                    for i, msg in enumerate(history[:3]):
                        print(f"   {i+1}. {msg.get('target', 'N/A')} - {msg.get('message', 'N/A')[:50]}...")
                else:
                    print("❌ MASALAH: History kosong atau tidak ada pesan")
                    print("   Ini konfirmasi bahwa pesan tidak sampai ke Fonnte server")
            else:
                print(f"❌ Error: {response.text}")
        except Exception as e:
            print(f"❌ Error checking history: {e}")
        
        # 3. Send test message and track it
        print("\n3️⃣ TEST KIRIM PESAN & TRACKING")
        print("-" * 30)
        test_phone = "6283838786991"  # From logs
        test_message = "🧪 Test diagnosis - " + str(int(__import__('time').time()))
        
        try:
            response = requests.post(
                'https://api.fonnte.com/send',
                headers={'Authorization': token},
                data={
                    'target': test_phone,
                    'message': test_message,
                    'countryCode': '62',
                }
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status'):
                    print("✅ API mengembalikan 'success'")
                    message_id = result.get('id', [])
                    if message_id:
                        print(f"📨 Message ID: {message_id}")
                    
                    # Wait and check if message appears in history
                    print("\n⏳ Menunggu 10 detik untuk cek history...")
                    __import__('time').sleep(10)
                    
                    # Check history again
                    history_response = requests.get(
                        'https://api.fonnte.com/history',
                        headers={'Authorization': token}
                    )
                    
                    if history_response.status_code == 200:
                        new_history = history_response.json()
                        found_message = False
                        if isinstance(new_history, list):
                            for msg in new_history:
                                if test_message in msg.get('message', ''):
                                    found_message = True
                                    print("✅ Pesan DITEMUKAN di history!")
                                    print(f"   Status: {msg.get('status', 'N/A')}")
                                    break
                        
                        if not found_message:
                            print("❌ MASALAH KONFIRMASI: Pesan TIDAK DITEMUKAN di history")
                            print("   Meskipun API return 'success', pesan tidak masuk ke sistem")
                            print("   Kemungkinan penyebab:")
                            print("   - Device WhatsApp offline/disconnect")
                            print("   - Quota habis")
                            print("   - Nomor tidak valid")
                            print("   - Pesan di-block oleh WhatsApp")
                else:
                    print("❌ API mengembalikan 'failed'")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error sending test: {e}")
        
        # 4. Recommendations
        print("\n4️⃣ REKOMENDASI SOLUSI")
        print("-" * 30)
        print("Berdasarkan diagnosis:")
        print("1. 🔍 Cek status device di dashboard Fonnte")
        print("2. 📱 Pastikan WhatsApp Business device online")
        print("3. 💰 Cek quota/balance akun Fonnte")
        print("4. 📞 Verifikasi nomor tujuan valid")
        print("5. 🔄 Restart/reconnect device jika perlu")
        
        print(f"\n🌐 Dashboard: https://console.fonnte.com")
        print("📧 Jika masalah berlanjut, hubungi support Fonnte")