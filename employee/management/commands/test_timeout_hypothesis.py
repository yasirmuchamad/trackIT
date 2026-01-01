from django.core.management.base import BaseCommand
import requests
import time

class Command(BaseCommand):
    help = 'Test if timeout parameter causes the issue'

    def handle(self, *args, **options):
        print("🎯 TEST HIPOTESIS: PARAMETER TIMEOUT MENYEBABKAN MASALAH")
        print("=" * 60)
        
        token = 'urWuiF1pMJyGM25uJEjA'
        url = 'https://api.fonnte.com/send'
        target = '6283838786991'
        
        # Test dengan parameter identik, hanya beda timeout
        base_data = {
            'target': target,
            'message': 'Test timeout hypothesis',
            'countryCode': '62'
        }
        base_headers = {'Authorization': token}
        
        print(f"🧪 PARAMETER IDENTIK:")
        print(f"URL: {url}")
        print(f"Headers: {base_headers}")
        print(f"Data: {base_data}")
        
        # Test 1: TANPA timeout (seperti simple_fonnte_test)
        print(f"\n1️⃣ TEST TANPA TIMEOUT (simple_fonnte_test style):")
        try:
            response1 = requests.post(url, headers=base_headers, data=base_data)
            
            print(f"   Status: {response1.status_code}")
            print(f"   Response: {response1.text}")
            
            if response1.status_code == 200:
                result1 = response1.json()
                success1 = result1.get('status', False)
                message_id1 = result1.get('id', [])
                print(f"   Success: {success1}")
                print(f"   Message ID: {message_id1}")
            else:
                success1 = False
                message_id1 = None
                
        except Exception as e:
            print(f"   Error: {e}")
            success1 = False
            message_id1 = None
        
        # Wait between requests
        print(f"   ⏳ Menunggu 3 detik...")
        time.sleep(3)
        
        # Test 2: DENGAN timeout=30 (seperti onboarding system)
        print(f"\n2️⃣ TEST DENGAN TIMEOUT=30 (onboarding style):")
        try:
            response2 = requests.post(url, headers=base_headers, data=base_data, timeout=30)
            
            print(f"   Status: {response2.status_code}")
            print(f"   Response: {response2.text}")
            
            if response2.status_code == 200:
                result2 = response2.json()
                success2 = result2.get('status', False)
                message_id2 = result2.get('id', [])
                print(f"   Success: {success2}")
                print(f"   Message ID: {message_id2}")
            else:
                success2 = False
                message_id2 = None
                
        except Exception as e:
            print(f"   Error: {e}")
            success2 = False
            message_id2 = None
        
        # Test 3: Dengan timeout berbeda
        print(f"\n3️⃣ TEST DENGAN TIMEOUT=10:")
        try:
            response3 = requests.post(url, headers=base_headers, data=base_data, timeout=10)
            
            print(f"   Status: {response3.status_code}")
            print(f"   Response: {response3.text}")
            
            if response3.status_code == 200:
                result3 = response3.json()
                success3 = result3.get('status', False)
                message_id3 = result3.get('id', [])
                print(f"   Success: {success3}")
                print(f"   Message ID: {message_id3}")
            else:
                success3 = False
                message_id3 = None
                
        except Exception as e:
            print(f"   Error: {e}")
            success3 = False
            message_id3 = None
        
        # Test 4: Dengan timeout sangat kecil
        print(f"\n4️⃣ TEST DENGAN TIMEOUT=1:")
        try:
            response4 = requests.post(url, headers=base_headers, data=base_data, timeout=1)
            
            print(f"   Status: {response4.status_code}")
            print(f"   Response: {response4.text}")
            
            if response4.status_code == 200:
                result4 = response4.json()
                success4 = result4.get('status', False)
                message_id4 = result4.get('id', [])
                print(f"   Success: {success4}")
                print(f"   Message ID: {message_id4}")
            else:
                success4 = False
                message_id4 = None
                
        except Exception as e:
            print(f"   Error: {e}")
            success4 = False
            message_id4 = None
        
        # Analysis
        print(f"\n📊 HASIL ANALISIS:")
        print(f"=" * 40)
        print(f"{'Test':<20} {'Success':<8} {'Message ID'}")
        print(f"-" * 40)
        print(f"{'No timeout':<20} {'✅' if success1 else '❌':<8} {message_id1}")
        print(f"{'Timeout=30':<20} {'✅' if success2 else '❌':<8} {message_id2}")
        print(f"{'Timeout=10':<20} {'✅' if success3 else '❌':<8} {message_id3}")
        print(f"{'Timeout=1':<20} {'✅' if success4 else '❌':<8} {message_id4}")
        
        # Conclusion
        print(f"\n🎯 KESIMPULAN:")
        
        if success1 and not success2:
            print("🚨 MASALAH DITEMUKAN: TIMEOUT=30 MENYEBABKAN KEGAGALAN!")
            print("   → Hapus parameter timeout dari sistem onboarding")
            print("   → Ini menjelaskan mengapa simple test berhasil tapi onboarding gagal")
        elif success1 and success2:
            print("✅ Timeout BUKAN masalah - kedua test berhasil")
            print("   → Masalah di tempat lain dalam sistem onboarding")
        elif not success1 and success2:
            print("🤔 Aneh: Timeout malah membantu - tanpa timeout gagal")
            print("   → Mungkin ada race condition atau timing issue")
        else:
            print("❌ Kedua test gagal - masalah di akun atau koneksi")
        
        # Check response differences
        if 'response1' in locals() and 'response2' in locals():
            if response1.text != response2.text:
                print(f"\n🔍 RESPONSE BERBEDA:")
                print(f"No timeout: {response1.text}")
                print(f"With timeout: {response2.text}")
            else:
                print(f"\n✅ Response identik meskipun parameter berbeda")
        
        print(f"\n💡 LANGKAH SELANJUTNYA:")
        if success1 and not success2:
            print("1. Hapus timeout=30 dari send_via_fonnte function")
            print("2. Test ulang sistem onboarding")
            print("3. Jika berhasil, masalah solved!")
        elif success1 and success2:
            print("1. Masalah bukan di timeout")
            print("2. Cek perbedaan lain (headers, data encoding, dll)")
            print("3. Cek apakah ada middleware yang interfere")
        else:
            print("1. Cek koneksi internet")
            print("2. Cek status akun Fonnte")
            print("3. Cek apakah token masih valid")