from django.core.management.base import BaseCommand
from django.conf import settings
import requests
import os

class Command(BaseCommand):
    help = 'Final diagnosis - check everything step by step'

    def handle(self, *args, **options):
        print("🔍 DIAGNOSIS FINAL - LANGKAH DEMI LANGKAH")
        print("=" * 60)
        
        # Step 1: Check .env file directly
        print("1️⃣ CEK FILE .ENV LANGSUNG")
        print("-" * 30)
        try:
            with open('.env', 'r') as f:
                content = f.read()
                if 'WHATSAPP_SERVICE_TOKEN=' in content:
                    for line in content.split('\n'):
                        if line.startswith('WHATSAPP_SERVICE_TOKEN='):
                            token_in_file = line.split('=', 1)[1].strip()
                            print(f"✅ Token di .env: {token_in_file}")
                            break
                else:
                    print("❌ WHATSAPP_SERVICE_TOKEN tidak ada di .env")
        except Exception as e:
            print(f"❌ Error reading .env: {e}")
        
        # Step 2: Check OS environment
        print("\n2️⃣ CEK OS ENVIRONMENT")
        print("-" * 30)
        os_token = os.environ.get('WHATSAPP_SERVICE_TOKEN', 'NOT_FOUND')
        print(f"OS Environment: {os_token}")
        
        # Step 3: Check Django settings
        print("\n3️⃣ CEK DJANGO SETTINGS")
        print("-" * 30)
        django_token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', 'NOT_IN_SETTINGS')
        django_url = getattr(settings, 'WHATSAPP_SERVICE_URL', 'NOT_IN_SETTINGS')
        print(f"Django URL: {django_url}")
        print(f"Django Token: {django_token}")
        
        if not django_token or django_token == 'NOT_IN_SETTINGS':
            print("❌ MASALAH: Token tidak terbaca di Django settings")
            return
        
        # Step 4: Test API call
        print("\n4️⃣ TEST API CALL")
        print("-" * 30)
        try:
            # Test profile first
            profile_response = requests.get(
                'https://api.fonnte.com/profile',
                headers={'Authorization': django_token},
                timeout=10
            )
            print(f"Profile API Status: {profile_response.status_code}")
            
            if profile_response.status_code == 200:
                profile = profile_response.json()
                print(f"✅ Akun: {profile.get('name', 'N/A')}")
                print(f"✅ Device: {profile.get('device', 'N/A')}")
                print(f"✅ Status: {profile.get('status', 'N/A')}")
                
                device_status = profile.get('status', '').lower()
                if 'disconnect' in device_status or 'offline' in device_status:
                    print("🚨 MASALAH UTAMA: DEVICE WHATSAPP OFFLINE!")
                    print("   Ini sebabnya pesan tidak masuk ke history Fonnte")
                    print("   Solusi: Hubungkan kembali device WhatsApp di dashboard Fonnte")
                elif 'connect' in device_status or 'online' in device_status:
                    print("✅ Device WhatsApp online")
                    
                    # If device is online, test sending message
                    print("\n📤 Test kirim pesan...")
                    test_response = requests.post(
                        'https://api.fonnte.com/send',
                        headers={'Authorization': django_token},
                        data={
                            'target': '6283838786991',
                            'message': '🧪 Test final diagnosis',
                            'countryCode': '62',
                        },
                        timeout=10
                    )
                    print(f"Send API Status: {test_response.status_code}")
                    print(f"Send Response: {test_response.text}")
                    
                    if test_response.status_code == 200:
                        result = test_response.json()
                        if result.get('status'):
                            print("✅ Pesan berhasil dikirim!")
                            print("📱 Cek WhatsApp untuk memastikan pesan masuk")
                        else:
                            print("❌ API return failed")
                    
            elif profile_response.status_code == 401:
                print("❌ MASALAH: Token tidak valid (401 Unauthorized)")
                print("   Cek token di dashboard Fonnte")
            else:
                print(f"❌ Error: {profile_response.text}")
                
        except Exception as e:
            print(f"❌ Error API call: {e}")
        
        # Step 5: Summary
        print("\n5️⃣ KESIMPULAN")
        print("-" * 30)
        print("Berdasarkan diagnosis:")
        print("1. Jika token valid tapi device offline → Reconnect device di Fonnte")
        print("2. Jika token invalid → Update token di .env")
        print("3. Jika semua OK tapi pesan tidak masuk → Cek nomor tujuan")
        print("4. Jika API error → Cek koneksi internet")
        
        print(f"\n🌐 Dashboard Fonnte: https://console.fonnte.com")
        print("📞 Support Fonnte: https://fonnte.com/contact")