from django.core.management.base import BaseCommand
from django.conf import settings
from employee.services.onboarding_delivery import send_via_fonnte
from employee.models import EmployeeOnboarding
import requests

class Command(BaseCommand):
    help = 'Test if removing timeout fixes the onboarding issue'

    def handle(self, *args, **options):
        print("🔧 TEST: APAKAH MENGHAPUS TIMEOUT MENYELESAIKAN MASALAH?")
        print("=" * 60)
        
        # Test 1: Direct API call comparison
        print("1️⃣ DIRECT API CALL COMPARISON:")
        print("-" * 30)
        
        token = 'urWuiF1pMJyGM25uJEjA'
        url = 'https://api.fonnte.com/send'
        target = '6283838786991'
        message = 'Test timeout fix'
        
        # Test A: Simple style (no timeout)
        print("A. Simple style (no timeout):")
        try:
            response_a = requests.post(url,
                                     headers={'Authorization': token},
                                     data={
                                         'target': target,
                                         'message': message,
                                         'countryCode': '62'
                                     })
            print(f"   Status: {response_a.status_code}")
            print(f"   Response: {response_a.text}")
            success_a = response_a.json().get('status', False) if response_a.status_code == 200 else False
            print(f"   Success: {success_a}")
        except Exception as e:
            print(f"   Error: {e}")
            success_a = False
        
        # Test B: Onboarding style (no timeout - after fix)
        print("\nB. Onboarding style (no timeout - after fix):")
        try:
            response_b = requests.post(url,
                                     headers={'Authorization': token},
                                     data={
                                         'target': target,
                                         'message': message,
                                         'countryCode': '62'
                                     })
            print(f"   Status: {response_b.status_code}")
            print(f"   Response: {response_b.text}")
            success_b = response_b.json().get('status', False) if response_b.status_code == 200 else False
            print(f"   Success: {success_b}")
        except Exception as e:
            print(f"   Error: {e}")
            success_b = False
        
        # Test 2: Using actual onboarding function
        print(f"\n2️⃣ TEST FUNGSI ONBOARDING SEBENARNYA:")
        print("-" * 30)
        
        try:
            # Test send_via_fonnte function directly
            result = send_via_fonnte('6283838786991', 'Test onboarding function after timeout fix')
            print(f"send_via_fonnte result: {result}")
            
            if result:
                print("✅ Fungsi onboarding berhasil!")
            else:
                print("❌ Fungsi onboarding masih gagal")
                
        except Exception as e:
            print(f"❌ Error in onboarding function: {e}")
            result = False
        
        # Test 3: Full onboarding flow test
        print(f"\n3️⃣ TEST FULL ONBOARDING FLOW:")
        print("-" * 30)
        
        # Find a test onboarding
        onboarding = EmployeeOnboarding.objects.filter(is_completed=False).first()
        
        if onboarding:
            print(f"Testing with onboarding: {onboarding.employee.name}")
            print(f"Phone: {onboarding.employee.phone}")
            
            try:
                from employee.services.onboarding_delivery import send_onboarding_whatsapp
                
                whatsapp_result = send_onboarding_whatsapp(
                    onboarding, 
                    onboarding.employee.phone
                )
                
                print(f"send_onboarding_whatsapp result: {whatsapp_result}")
                
                if whatsapp_result:
                    print("✅ Full onboarding WhatsApp berhasil!")
                else:
                    print("❌ Full onboarding WhatsApp masih gagal")
                    
            except Exception as e:
                print(f"❌ Error in full onboarding: {e}")
                whatsapp_result = False
        else:
            print("❌ No test onboarding found")
            whatsapp_result = None
        
        # Summary
        print(f"\n📊 RINGKASAN HASIL:")
        print("=" * 40)
        print(f"Direct API simple style: {'✅ SUCCESS' if success_a else '❌ FAILED'}")
        print(f"Direct API onboarding style: {'✅ SUCCESS' if success_b else '❌ FAILED'}")
        print(f"send_via_fonnte function: {'✅ SUCCESS' if result else '❌ FAILED'}")
        print(f"Full onboarding flow: {'✅ SUCCESS' if whatsapp_result else '❌ FAILED' if whatsapp_result is not None else '⚠️ NOT TESTED'}")
        
        # Conclusion
        print(f"\n🎯 KESIMPULAN:")
        
        if all([success_a, success_b, result]):
            print("🎉 MASALAH SOLVED! Menghapus timeout berhasil!")
            print("   → Semua test berhasil setelah timeout dihapus")
            print("   → Sistem onboarding sekarang berfungsi normal")
            print("   → Coba test resend button di web interface")
        elif success_a and success_b and not result:
            print("⚠️ API calls berhasil tapi fungsi onboarding masih bermasalah")
            print("   → Ada masalah lain di fungsi send_via_fonnte")
            print("   → Perlu debug lebih lanjut")
        elif not success_a or not success_b:
            print("❌ Masih ada masalah di level API")
            print("   → Timeout bukan satu-satunya masalah")
            print("   → Perlu investigasi lebih lanjut")
        else:
            print("🤔 Hasil tidak konsisten - perlu analisis lebih lanjut")
        
        print(f"\n💡 LANGKAH SELANJUTNYA:")
        if all([success_a, success_b, result]):
            print("1. ✅ Test resend button di web interface")
            print("2. ✅ Cek apakah pesan masuk ke Fonnte history")
            print("3. ✅ Cek apakah pesan sampai ke WhatsApp")
            print("4. ✅ Jika semua OK, masalah completely solved!")
        else:
            print("1. ❌ Debug fungsi yang masih gagal")
            print("2. ❌ Cek log error untuk detail masalah")
            print("3. ❌ Mungkin ada masalah lain selain timeout")
        
        print(f"\n🔍 UNTUK VERIFIKASI FINAL:")
        print("1. Buka web interface: http://127.0.0.1:8000/employees/onboarding/")
        print("2. Klik tombol 'Resend (Fixed)'")
        print("3. Cek dashboard Fonnte: https://console.fonnte.com")
        print("4. Lihat apakah pesan muncul di message history")
        print("5. Cek WhatsApp untuk memastikan pesan diterima")