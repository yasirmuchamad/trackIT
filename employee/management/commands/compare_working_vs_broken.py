from django.core.management.base import BaseCommand
from django.conf import settings
import requests

class Command(BaseCommand):
    help = 'Compare working simple test vs broken onboarding system'

    def handle(self, *args, **options):
        print("🔍 PERBANDINGAN: SIMPLE TEST vs ONBOARDING SYSTEM")
        print("=" * 60)
        
        token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', '')
        if not token:
            print("❌ Token tidak ditemukan")
            return
            
        print(f"🔑 Token: {token}")
        
        # Test 1: Simple working method (like simple_fonnte_test.py)
        print("\n1️⃣ SIMPLE TEST (YANG BEKERJA)")
        print("-" * 30)
        try:
            response = requests.post(
                'https://api.fonnte.com/send',
                headers={'Authorization': token},
                data={
                    'target': '6283838786991',
                    'message': '🧪 Simple test - working method',
                    'countryCode': '62',
                }
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status'):
                    print("✅ Simple test: SUCCESS")
                    print(f"📨 Message ID: {result.get('id', 'N/A')}")
                else:
                    print("❌ Simple test: FAILED")
        except Exception as e:
            print(f"❌ Simple test error: {e}")
        
        # Test 2: Onboarding method (current implementation)
        print("\n2️⃣ ONBOARDING METHOD (YANG BERMASALAH)")
        print("-" * 30)
        
        # Simulate onboarding message
        onboarding_message = """Halo Test User! 👋

Selamat bergabung di perusahaan kami! 

Silakan lengkapi data onboarding Anda melalui link berikut:
http://localhost:8000/onboarding/test-token/

Link ini berlaku hingga: 2026-01-02

Jika ada pertanyaan, silakan hubungi HR.

Terima kasih! 🙏"""
        
        try:
            response = requests.post(
                'https://api.fonnte.com/send',
                headers={'Authorization': token},
                data={
                    'target': '6283838786991',
                    'message': onboarding_message,
                    'countryCode': '62',
                }
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status'):
                    print("✅ Onboarding test: SUCCESS")
                    print(f"📨 Message ID: {result.get('id', 'N/A')}")
                else:
                    print("❌ Onboarding test: FAILED")
        except Exception as e:
            print(f"❌ Onboarding test error: {e}")
        
        # Test 3: Check message history
        print("\n3️⃣ CEK MESSAGE HISTORY")
        print("-" * 30)
        try:
            response = requests.get(
                'https://api.fonnte.com/history',
                headers={'Authorization': token}
            )
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                history = response.json()
                if isinstance(history, list):
                    print(f"📋 Total messages in history: {len(history)}")
                    if len(history) > 0:
                        print("📱 Recent messages:")
                        for i, msg in enumerate(history[:3]):
                            target = msg.get('target', 'N/A')
                            message = msg.get('message', 'N/A')[:50] + '...'
                            status = msg.get('status', 'N/A')
                            print(f"   {i+1}. {target} - {message} [{status}]")
                    else:
                        print("❌ MASALAH: History kosong!")
                        print("   Ini konfirmasi bahwa pesan tidak sampai ke Fonnte server")
                else:
                    print(f"⚠️ Unexpected history format: {history}")
            else:
                print(f"❌ History error: {response.text}")
        except Exception as e:
            print(f"❌ History check error: {e}")
        
        # Test 4: Check account profile
        print("\n4️⃣ CEK PROFILE AKUN")
        print("-" * 30)
        try:
            response = requests.get(
                'https://api.fonnte.com/profile',
                headers={'Authorization': token}
            )
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                profile = response.json()
                print(f"👤 Nama: {profile.get('name', 'N/A')}")
                print(f"📱 Device: {profile.get('device', 'N/A')}")
                print(f"🔌 Status: {profile.get('status', 'N/A')}")
                print(f"💰 Quota: {profile.get('quota', 'N/A')}")
                
                # Check device status
                device_status = profile.get('status', '').lower()
                if 'disconnect' in device_status or 'offline' in device_status:
                    print("\n🚨 MASALAH DITEMUKAN!")
                    print("   Device WhatsApp OFFLINE/DISCONNECT")
                    print("   Ini menjelaskan mengapa pesan tidak masuk ke history")
                    print("   Solusi: Reconnect device di dashboard Fonnte")
                elif 'connect' in device_status or 'online' in device_status:
                    print("\n✅ Device WhatsApp ONLINE")
                    print("   Masalah mungkin di tempat lain")
            else:
                print(f"❌ Profile error: {response.text}")
        except Exception as e:
            print(f"❌ Profile check error: {e}")
        
        print("\n🎯 KESIMPULAN")
        print("-" * 30)
        print("Jika kedua test (simple & onboarding) return SUCCESS tapi history kosong:")
        print("1. 🔌 Device WhatsApp offline - reconnect di dashboard")
        print("2. 💰 Quota habis - top up balance")
        print("3. 📱 Nomor tujuan bermasalah - test dengan nomor lain")
        print("4. 🚫 Pesan terlalu panjang - WhatsApp block spam")
        
        print(f"\n🌐 Dashboard: https://console.fonnte.com")
        print("📞 Support: https://fonnte.com/contact")