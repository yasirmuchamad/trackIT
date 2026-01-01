from django.core.management.base import BaseCommand
from django.conf import settings
import requests


class Command(BaseCommand):
    help = 'Simple WhatsApp test'

    def handle(self, *args, **options):
        # Test configuration
        self.stdout.write("📱 Testing WhatsApp Configuration...")
        
        whatsapp_url = getattr(settings, 'WHATSAPP_SERVICE_URL', '')
        whatsapp_token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', '')
        
        self.stdout.write(f"URL: {whatsapp_url}")
        self.stdout.write(f"Token: {whatsapp_token[:10]}..." if whatsapp_token else "Token: NOT SET")
        
        if not whatsapp_url:
            self.stdout.write(self.style.ERROR('❌ WHATSAPP_SERVICE_URL not set'))
            return
            
        if not whatsapp_token:
            self.stdout.write(self.style.ERROR('❌ WHATSAPP_SERVICE_TOKEN not set'))
            return
        
        # Test with hardcoded phone for now
        phone = '6283838786991'  # Your phone number
        message = 'Test dari TrackIT system - onboarding berhasil dikonfigurasi!'
        
        self.stdout.write(f"\n📤 Sending test message to {phone}")
        
        try:
            headers = {
                'Authorization': whatsapp_token,
            }
            
            data = {
                'target': phone,
                'message': message,
                'countryCode': '62',
            }
            
            response = requests.post(whatsapp_url, data=data, headers=headers, timeout=30)
            
            self.stdout.write(f"Status Code: {response.status_code}")
            self.stdout.write(f"Response: {response.text}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get('status'):
                        self.stdout.write(self.style.SUCCESS('✅ WhatsApp sent successfully!'))
                    else:
                        self.stdout.write(self.style.ERROR(f'❌ API Error: {result}'))
                except:
                    self.stdout.write(self.style.WARNING('⚠️ Non-JSON response'))
            else:
                self.stdout.write(self.style.ERROR(f'❌ HTTP Error: {response.status_code}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Exception: {str(e)}'))
        
        self.stdout.write('\n💡 If this works, your WhatsApp is configured correctly!')
        self.stdout.write('Now try: python manage.py test_onboarding --employee-id 99999 --phone 083838786991')