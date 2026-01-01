from django.core.management.base import BaseCommand
from django.conf import settings
import requests


class Command(BaseCommand):
    help = 'Final test - check if real token is working'

    def handle(self, *args, **options):
        self.stdout.write("🎯 FINAL TEST: Real Token Check")
        
        # Get token from Django settings
        token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', '')
        url = getattr(settings, 'WHATSAPP_SERVICE_URL', 'https://api.fonnte.com/send')
        
        self.stdout.write(f"Token: {token}")
        self.stdout.write(f"URL: {url}")
        
        if not token:
            self.stdout.write("❌ No token found - check .env file")
            return
            
        if token == 'urWuiF1pMJyGM25uJEjA':
            self.stdout.write("❌ Still using dummy token!")
            return
        
        # Test API call
        self.stdout.write("\n📤 Testing API call...")
        
        try:
            headers = {'Authorization': token}
            data = {
                'target': '6283838786991',
                'message': '🎯 FINAL TEST - Real token verification',
                'countryCode': '62',
            }
            
            response = requests.post(url, data=data, headers=headers, timeout=10)
            
            self.stdout.write(f"Status: {response.status_code}")
            self.stdout.write(f"Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status'):
                    self.stdout.write("✅ SUCCESS! Real token is working!")
                    self.stdout.write("💡 Check Fonnte dashboard and WhatsApp")
                else:
                    self.stdout.write(f"❌ API Error: {result}")
            else:
                self.stdout.write("❌ HTTP Error")
                
        except Exception as e:
            self.stdout.write(f"❌ Exception: {str(e)}")
        
        self.stdout.write("\n📋 Next Steps:")
        self.stdout.write("1. Check Fonnte dashboard for message history")
        self.stdout.write("2. Check WhatsApp on target phone")
        self.stdout.write("3. If dashboard shows message but WhatsApp doesn't receive:")
        self.stdout.write("   - Phone not registered in WhatsApp")
        self.stdout.write("   - Phone offline")
        self.stdout.write("   - Message in spam folder")
        self.stdout.write("4. Test web interface: click resend button")