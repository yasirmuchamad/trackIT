from django.core.management.base import BaseCommand
from django.conf import settings
from decouple import config
import os


class Command(BaseCommand):
    help = 'Verify system is using real token from .env'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Verifying Real Token Usage...")
        
        # Step 1: Check what's in .env file
        self.stdout.write("\n📁 Step 1: Reading .env file")
        
        env_token = None
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('WHATSAPP_SERVICE_TOKEN='):
                        env_token = line.split('=', 1)[1].strip()
                        break
            
            if env_token:
                self.stdout.write(f"   📱 Token in .env: {env_token}")
                if env_token == 'urWuiF1pMJyGM25uJEjA':
                    self.stdout.write("   ❌ .env still contains DUMMY token!")
                    self.stdout.write("   🛠️ Please replace with real Fonnte token")
                    return
                else:
                    self.stdout.write("   ✅ .env contains custom token (not dummy)")
            else:
                self.stdout.write("   ❌ WHATSAPP_SERVICE_TOKEN not found in .env")
                return
                
        except Exception as e:
            self.stdout.write(f"   ❌ Error reading .env: {str(e)}")
            return
        
        # Step 2: Check what Django sees
        self.stdout.write("\n🐍 Step 2: Checking Django configuration")
        
        try:
            django_token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', 'NOT_FOUND')
            self.stdout.write(f"   Django token: {django_token}")
            
            if django_token == 'NOT_FOUND':
                self.stdout.write("   ❌ Django can't find WHATSAPP_SERVICE_TOKEN")
            elif django_token == 'urWuiF1pMJyGM25uJEjA':
                self.stdout.write("   ❌ Django is still using DUMMY token!")
            elif django_token == env_token:
                self.stdout.write("   ✅ Django token matches .env token")
            else:
                self.stdout.write(f"   ⚠️ Django token differs from .env token")
                
        except Exception as e:
            self.stdout.write(f"   ❌ Error checking Django settings: {str(e)}")
        
        # Step 3: Test actual API call
        self.stdout.write("\n🧪 Step 3: Testing API call with real token")
        
        try:
            import requests
            
            # Use the token Django sees
            test_token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', '')
            test_url = getattr(settings, 'WHATSAPP_SERVICE_URL', 'https://api.fonnte.com/send')
            
            if not test_token:
                self.stdout.write("   ❌ No token available for testing")
                return
            
            self.stdout.write(f"   📤 Testing with token: {test_token}")
            self.stdout.write(f"   📤 Testing with URL: {test_url}")
            
            # Make test API call
            headers = {'Authorization': test_token}
            data = {
                'target': '6283838786991',
                'message': f'🧪 Test token verification - Real token test',
                'countryCode': '62',
            }
            
            response = requests.post(test_url, data=data, headers=headers, timeout=10)
            
            self.stdout.write(f"   📊 Response status: {response.status_code}")
            self.stdout.write(f"   📊 Response body: {response.text}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get('status'):
                        self.stdout.write("   ✅ API call SUCCESS with real token!")
                        self.stdout.write("   💡 Check Fonnte dashboard - this should appear in history")
                        
                        if 'id' in result:
                            self.stdout.write(f"   📝 Message ID: {result['id']}")
                            
                    else:
                        self.stdout.write(f"   ❌ API call failed: {result}")
                        self.stdout.write("   💡 Token might be invalid or account has issues")
                        
                except Exception as e:
                    self.stdout.write(f"   ⚠️ Non-JSON response: {response.text}")
            else:
                self.stdout.write(f"   ❌ HTTP error: {response.status_code}")
                
        except Exception as e:
            self.stdout.write(f"   ❌ Error testing API: {str(e)}")
        
        # Step 4: Test onboarding system
        self.stdout.write("\n🚀 Step 4: Testing onboarding system")
        
        try:
            from employee.services.onboarding_delivery import send_via_fonnte
            
            self.stdout.write("   📤 Testing send_via_fonnte function...")
            result = send_via_fonnte('6283838786991', '🧪 Test onboarding system with real token')
            
            if result:
                self.stdout.write("   ✅ Onboarding system SUCCESS!")
                self.stdout.write("   💡 Check Fonnte dashboard and WhatsApp")
            else:
                self.stdout.write("   ❌ Onboarding system FAILED")
                self.stdout.write("   💡 Check logs/onboarding.log for details")
                
        except Exception as e:
            self.stdout.write(f"   ❌ Error testing onboarding system: {str(e)}")
        
        # Final instructions
        self.stdout.write("\n📋 FINAL VERIFICATION:")
        self.stdout.write("   1. Check Fonnte dashboard (https://console.fonnte.com)")
        self.stdout.write("   2. Look for test messages in message history")
        self.stdout.write("   3. Check WhatsApp on phone 083838786991")
        self.stdout.write("   4. If messages appear in dashboard but not WhatsApp:")
        self.stdout.write("      • Phone number not registered in WhatsApp")
        self.stdout.write("      • Phone has no internet connection")
        self.stdout.write("      • Messages in WhatsApp spam folder")
        self.stdout.write("   5. If messages don't appear in dashboard:")
        self.stdout.write("      • Token is still invalid")
        self.stdout.write("      • Account has no balance/quota")
        self.stdout.write("      • Account is suspended")