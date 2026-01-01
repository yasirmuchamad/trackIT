from django.core.management.base import BaseCommand
import requests


class Command(BaseCommand):
    help = 'Test with custom Fonnte token'

    def add_arguments(self, parser):
        parser.add_argument(
            '--token',
            type=str,
            help='Your real Fonnte token to test',
        )
        parser.add_argument(
            '--phone',
            type=str,
            default='6283838786991',
            help='Phone number to test',
        )

    def handle(self, *args, **options):
        token = options.get('token')
        phone = options.get('phone')
        
        if not token:
            self.stdout.write("❌ Please provide --token argument")
            self.stdout.write("Example: python manage.py test_custom_token --token YOUR_REAL_TOKEN")
            self.stdout.write("Get token from: https://console.fonnte.com")
            return
        
        self.stdout.write("🧪 Testing Custom Fonnte Token")
        self.stdout.write(f"Token: {token}")
        self.stdout.write(f"Phone: {phone}")
        
        # Test API call
        try:
            url = 'https://api.fonnte.com/send'
            headers = {'Authorization': token}
            data = {
                'target': phone,
                'message': f'🧪 Test custom token - {self.get_current_time()}',
                'countryCode': '62',
            }
            
            self.stdout.write("\n📤 Sending test message...")
            response = requests.post(url, data=data, headers=headers, timeout=10)
            
            self.stdout.write(f"Status: {response.status_code}")
            self.stdout.write(f"Response: {response.text}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get('status'):
                        self.stdout.write("✅ SUCCESS! Your token is VALID!")
                        self.stdout.write("💡 Now update .env file with this token:")
                        self.stdout.write(f"   WHATSAPP_SERVICE_TOKEN={token}")
                        
                        if 'id' in result:
                            self.stdout.write(f"📝 Message ID: {result['id']}")
                            
                        self.stdout.write("\n📋 Next steps:")
                        self.stdout.write("1. Update .env file with this token")
                        self.stdout.write("2. Restart Django server")
                        self.stdout.write("3. Test onboarding system")
                        self.stdout.write("4. Check Fonnte dashboard")
                        
                    else:
                        self.stdout.write(f"❌ Token INVALID: {result}")
                        self.stdout.write("💡 Check your Fonnte account:")
                        self.stdout.write("   • Token might be wrong")
                        self.stdout.write("   • Account might be suspended")
                        self.stdout.write("   • Device might be disconnected")
                        
                except Exception as e:
                    self.stdout.write(f"⚠️ Non-JSON response: {response.text}")
            else:
                self.stdout.write(f"❌ HTTP Error: {response.status_code}")
                self.stdout.write("💡 Check token and try again")
                
        except Exception as e:
            self.stdout.write(f"❌ Exception: {str(e)}")
        
        self.stdout.write("\n💡 How to get real token:")
        self.stdout.write("   1. Go to https://console.fonnte.com")
        self.stdout.write("   2. Login or register")
        self.stdout.write("   3. Connect your WhatsApp device")
        self.stdout.write("   4. Copy your API token")
        self.stdout.write("   5. Test with this command")

    def get_current_time(self):
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")