from django.core.management.base import BaseCommand
from django.conf import settings
from employee.services.onboarding_delivery import send_via_fonnte
import requests


class Command(BaseCommand):
    help = 'Compare simple test vs resend system requests'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Comparing Simple Test vs Resend System")
        
        phone = '6283838786991'
        token = 'urWuiF1pMJyGM25uJEjA'
        
        # Test 1: Simple test method (WORKING)
        self.stdout.write("\n🧪 TEST 1: Simple Test Method (WORKING)")
        self.stdout.write("This is exactly what simple_fonnte_test does:")
        
        try:
            headers_simple = {'Authorization': token}
            data_simple = {
                'target': phone,
                'message': '🧪 Test 1 - Simple method',
                'countryCode': '62'
            }
            
            self.stdout.write(f"URL: https://api.fonnte.com/send")
            self.stdout.write(f"Headers: {headers_simple}")
            self.stdout.write(f"Data: {data_simple}")
            
            response1 = requests.post('https://api.fonnte.com/send',
                                    headers=headers_simple,
                                    data=data_simple,
                                    timeout=30)
            
            self.stdout.write(f"Status: {response1.status_code}")
            self.stdout.write(f"Response: {response1.text}")
            
            if response1.status_code == 200:
                try:
                    result1 = response1.json()
                    if result1.get('status') and 'id' in result1:
                        msg_id = result1['id'][0] if isinstance(result1['id'], list) else result1['id']
                        self.stdout.write(f"✅ Simple method SUCCESS - Message ID: {msg_id}")
                    else:
                        self.stdout.write(f"❌ Simple method FAILED: {result1}")
                except:
                    self.stdout.write("⚠️ Non-JSON response")
            
        except Exception as e:
            self.stdout.write(f"❌ Simple method ERROR: {str(e)}")
        
        # Test 2: Resend system method (NOT WORKING)
        self.stdout.write("\n🚀 TEST 2: Resend System Method (NOT WORKING)")
        self.stdout.write("This is what send_via_fonnte does:")
        
        try:
            # Get settings like resend system does
            django_url = getattr(settings, 'WHATSAPP_SERVICE_URL', 'https://api.fonnte.com/send')
            django_token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', '')
            
            self.stdout.write(f"Django URL: {django_url}")
            self.stdout.write(f"Django Token: {django_token}")
            
            if not django_token:
                self.stdout.write("❌ Django token is empty!")
                return
            
            # Call send_via_fonnte function
            self.stdout.write("Calling send_via_fonnte function...")
            result2 = send_via_fonnte(phone, '🧪 Test 2 - Resend system method')
            
            self.stdout.write(f"send_via_fonnte result: {result2}")
            
        except Exception as e:
            self.stdout.write(f"❌ Resend system ERROR: {str(e)}")
        
        # Test 3: Manual replication of send_via_fonnte
        self.stdout.write("\n🔧 TEST 3: Manual Replication of send_via_fonnte")
        
        try:
            # Replicate exactly what send_via_fonnte does
            url = getattr(settings, 'WHATSAPP_SERVICE_URL', 'https://api.fonnte.com/send')
            token_from_settings = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', '')
            
            self.stdout.write(f"URL from settings: {url}")
            self.stdout.write(f"Token from settings: {token_from_settings}")
            
            if not token_from_settings:
                self.stdout.write("❌ Token from settings is empty!")
                return
            
            headers_system = {'Authorization': token_from_settings}
            data_system = {
                'target': phone,
                'message': '🧪 Test 3 - Manual replication',
                'countryCode': '62',
            }
            
            self.stdout.write(f"Headers: {headers_system}")
            self.stdout.write(f"Data: {data_system}")
            
            response3 = requests.post(url, data=data_system, headers=headers_system, timeout=30)
            
            self.stdout.write(f"Status: {response3.status_code}")
            self.stdout.write(f"Response: {response3.text}")
            
            if response3.status_code == 200:
                try:
                    result3 = response3.json()
                    if result3.get('status') and 'id' in result3:
                        msg_id = result3['id'][0] if isinstance(result3['id'], list) else result3['id']
                        self.stdout.write(f"✅ Manual replication SUCCESS - Message ID: {msg_id}")
                    else:
                        self.stdout.write(f"❌ Manual replication FAILED: {result3}")
                except:
                    self.stdout.write("⚠️ Non-JSON response")
            
        except Exception as e:
            self.stdout.write(f"❌ Manual replication ERROR: {str(e)}")
        
        # Analysis
        self.stdout.write("\n🎯 ANALYSIS:")
        self.stdout.write("Compare the three methods above:")
        self.stdout.write("1. If Test 1 works but Test 2/3 fail:")
        self.stdout.write("   → Problem in Django settings or send_via_fonnte function")
        self.stdout.write("2. If Test 1 and Test 3 work but Test 2 fails:")
        self.stdout.write("   → Problem specifically in send_via_fonnte function")
        self.stdout.write("3. If all tests work:")
        self.stdout.write("   → Problem might be in web interface or timing")
        
        self.stdout.write("\n💡 NEXT STEPS:")
        self.stdout.write("1. Check which tests produce message IDs")
        self.stdout.write("2. Check Fonnte dashboard for each message ID")
        self.stdout.write("3. Compare request parameters between working and non-working methods")
        self.stdout.write("4. Check logs/onboarding.log for detailed error messages")