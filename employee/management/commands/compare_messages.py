from django.core.management.base import BaseCommand
from django.conf import settings
from employee.models import Employee, EmployeeOnboarding
from employee.services.onboarding_delivery import build_onboarding_link
import requests


class Command(BaseCommand):
    help = 'Compare simple test vs onboarding message'

    def add_arguments(self, parser):
        parser.add_argument(
            '--phone',
            type=str,
            default='083838786991',
            help='Phone number to test',
        )

    def handle(self, *args, **options):
        phone = options.get('phone')
        
        # Format phone number
        clean_phone = ''.join(filter(str.isdigit, phone))
        if clean_phone.startswith('0'):
            clean_phone = '62' + clean_phone[1:]
        elif not clean_phone.startswith('62'):
            clean_phone = '62' + clean_phone
        
        self.stdout.write("🔍 Comparing Simple Test vs Onboarding Message...")
        self.stdout.write(f"📱 Target phone: {phone} → {clean_phone}")
        
        # Get configuration
        whatsapp_url = getattr(settings, 'WHATSAPP_SERVICE_URL', '')
        whatsapp_token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', '')
        
        if not whatsapp_url or not whatsapp_token:
            self.stdout.write(self.style.ERROR('❌ WhatsApp configuration missing'))
            return
        
        # Test 1: Simple message (like debug_fonnte)
        self.stdout.write("\n🧪 TEST 1: Simple Message (like debug_fonnte)")
        simple_message = f"🧪 Test dari TrackIT System\n\nWaktu: {self.get_current_time()}\nNomor: {clean_phone}\n\nJika Anda menerima pesan ini, konfigurasi WhatsApp berhasil!"
        
        result1 = self.send_message(whatsapp_url, whatsapp_token, clean_phone, simple_message, "Simple Test")
        
        # Test 2: Onboarding-style message
        self.stdout.write("\n🧪 TEST 2: Onboarding-style Message")
        
        # Get a real employee for realistic onboarding message
        employee = Employee.objects.first()
        if not employee:
            self.stdout.write(self.style.WARNING("⚠️ No employee found, creating dummy data"))
            employee_name = "Test Employee"
            onboarding_link = "http://localhost:8000/onboarding/dummy-token/"
        else:
            employee_name = employee.name
            # Create or get onboarding record
            try:
                onboarding = EmployeeOnboarding.objects.get(employee=employee)
            except EmployeeOnboarding.DoesNotExist:
                onboarding = EmployeeOnboarding.create_for_employee(employee)
            
            onboarding_link = build_onboarding_link(onboarding.token)
        
        # This is the EXACT message format used in onboarding
        onboarding_message = f"""
Halo {employee_name}! 👋

Selamat bergabung di perusahaan kami! 

Silakan lengkapi data onboarding Anda melalui link berikut:
{onboarding_link}

Link ini berlaku hingga: 31 Desember 2025, 23:59

Jika ada pertanyaan, silakan hubungi HR.

Terima kasih! 🙏
        """.strip()
        
        result2 = self.send_message(whatsapp_url, whatsapp_token, clean_phone, onboarding_message, "Onboarding Message")
        
        # Test 3: Onboarding message without link
        self.stdout.write("\n🧪 TEST 3: Onboarding Message WITHOUT Link")
        
        onboarding_no_link = f"""
Halo {employee_name}! 👋

Selamat bergabung di perusahaan kami! 

Silakan lengkapi data onboarding Anda.

Jika ada pertanyaan, silakan hubungi HR.

Terima kasih! 🙏
        """.strip()
        
        result3 = self.send_message(whatsapp_url, whatsapp_token, clean_phone, onboarding_no_link, "Onboarding No Link")
        
        # Test 4: Very simple onboarding
        self.stdout.write("\n🧪 TEST 4: Very Simple Onboarding")
        
        simple_onboarding = f"Halo {employee_name}! Selamat bergabung di perusahaan kami. Silakan lengkapi data onboarding."
        
        result4 = self.send_message(whatsapp_url, whatsapp_token, clean_phone, simple_onboarding, "Simple Onboarding")
        
        # Summary
        self.stdout.write("\n📊 SUMMARY:")
        self.stdout.write(f"Test 1 (Simple): {'✅ SUCCESS' if result1 else '❌ FAILED'}")
        self.stdout.write(f"Test 2 (Full Onboarding): {'✅ SUCCESS' if result2 else '❌ FAILED'}")
        self.stdout.write(f"Test 3 (No Link): {'✅ SUCCESS' if result3 else '❌ FAILED'}")
        self.stdout.write(f"Test 4 (Very Simple): {'✅ SUCCESS' if result4 else '❌ FAILED'}")
        
        self.stdout.write("\n🔍 ANALYSIS:")
        if result1 and not result2:
            self.stdout.write("❗ Issue with onboarding message format or content")
            if result3:
                self.stdout.write("   → Problem is likely the LINK in the message")
            else:
                self.stdout.write("   → Problem is the message content/length")
        elif result1 and result2:
            self.stdout.write("✅ Both work - issue might be elsewhere")
        elif not result1 and not result2:
            self.stdout.write("❌ Both fail - issue with Fonnte configuration")
        
        self.stdout.write("\n💡 Wait a few minutes and check if messages arrive")
        self.stdout.write("💡 Sometimes there's a delay in WhatsApp delivery")

    def send_message(self, url, token, phone, message, test_name):
        """Send a message and return success status"""
        try:
            headers = {'Authorization': token}
            data = {
                'target': phone,
                'message': message,
                'countryCode': '62',
            }
            
            self.stdout.write(f"📤 Sending {test_name}...")
            self.stdout.write(f"   Message length: {len(message)} chars")
            self.stdout.write(f"   First 100 chars: {message[:100]}...")
            
            response = requests.post(url, data=data, headers=headers, timeout=30)
            
            self.stdout.write(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    self.stdout.write(f"   Response: {result}")
                    
                    success = result.get('status', False)
                    if success:
                        self.stdout.write(f"   ✅ {test_name}: API SUCCESS")
                        return True
                    else:
                        self.stdout.write(f"   ❌ {test_name}: API FAILED - {result}")
                        return False
                        
                except Exception as e:
                    self.stdout.write(f"   ❌ {test_name}: JSON ERROR - {e}")
                    return False
            else:
                self.stdout.write(f"   ❌ {test_name}: HTTP ERROR - {response.text}")
                return False
                
        except Exception as e:
            self.stdout.write(f"   ❌ {test_name}: EXCEPTION - {str(e)}")
            return False

    def get_current_time(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")