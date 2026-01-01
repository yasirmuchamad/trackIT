from django.core.management.base import BaseCommand
from django.conf import settings
import requests
import json


class Command(BaseCommand):
    help = 'Debug Fonnte WhatsApp service with detailed response'

    def add_arguments(self, parser):
        parser.add_argument(
            '--phone',
            type=str,
            help='Phone number to test (e.g., 083838786991)',
        )

    def handle(self, *args, **options):
        phone = options.get('phone', '083838786991')  # Default phone
        
        # Format phone number
        clean_phone = ''.join(filter(str.isdigit, phone))
        if clean_phone.startswith('0'):
            clean_phone = '62' + clean_phone[1:]
        elif not clean_phone.startswith('62'):
            clean_phone = '62' + clean_phone
        
        self.stdout.write("🔍 Debugging Fonnte WhatsApp Service...")
        
        # Get configuration
        whatsapp_url = getattr(settings, 'WHATSAPP_SERVICE_URL', '')
        whatsapp_token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', '')
        
        self.stdout.write(f"URL: {whatsapp_url}")
        self.stdout.write(f"Token: {whatsapp_token}")
        self.stdout.write(f"Phone: {phone} → {clean_phone}")
        
        if not whatsapp_url or not whatsapp_token:
            self.stdout.write(self.style.ERROR('❌ WhatsApp configuration missing'))
            return
        
        # Test message
        message = f"🧪 Test dari TrackIT System\n\nWaktu: {self.get_current_time()}\nNomor: {clean_phone}\n\nJika Anda menerima pesan ini, konfigurasi WhatsApp berhasil!"
        
        # Step 1: Check Fonnte account info
        self.check_fonnte_account(whatsapp_token)
        
        # Step 2: Send test message with detailed logging
        self.send_test_message(whatsapp_url, whatsapp_token, clean_phone, message)
        
        # Step 3: Check message status (if supported)
        # self.check_message_status(whatsapp_token)

    def check_fonnte_account(self, token):
        """Check Fonnte account information"""
        self.stdout.write("\n📊 Checking Fonnte Account...")
        
        try:
            # Fonnte profile endpoint
            profile_url = "https://api.fonnte.com/profile"
            headers = {'Authorization': token}
            
            response = requests.get(profile_url, headers=headers, timeout=10)
            
            self.stdout.write(f"Profile Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    profile = response.json()
                    self.stdout.write("Account Info:")
                    self.stdout.write(f"  Name: {profile.get('name', 'N/A')}")
                    self.stdout.write(f"  Phone: {profile.get('phone', 'N/A')}")
                    self.stdout.write(f"  Status: {profile.get('status', 'N/A')}")
                    self.stdout.write(f"  Package: {profile.get('package', 'N/A')}")
                    
                    # Check quota/balance if available
                    if 'quota' in profile:
                        self.stdout.write(f"  Quota: {profile['quota']}")
                    if 'balance' in profile:
                        self.stdout.write(f"  Balance: {profile['balance']}")
                        
                except json.JSONDecodeError:
                    self.stdout.write(f"Profile Response: {response.text}")
            else:
                self.stdout.write(self.style.ERROR(f"❌ Profile check failed: {response.text}"))
                
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"⚠️ Could not check profile: {str(e)}"))

    def send_test_message(self, url, token, phone, message):
        """Send test message with detailed response logging"""
        self.stdout.write(f"\n📤 Sending test message to {phone}...")
        
        try:
            headers = {
                'Authorization': token,
            }
            
            data = {
                'target': phone,
                'message': message,
                'countryCode': '62',
            }
            
            self.stdout.write("Request Details:")
            self.stdout.write(f"  URL: {url}")
            self.stdout.write(f"  Headers: Authorization: {token[:10]}...")
            self.stdout.write(f"  Data: {data}")
            
            response = requests.post(url, data=data, headers=headers, timeout=30)
            
            self.stdout.write(f"\nResponse Details:")
            self.stdout.write(f"  Status Code: {response.status_code}")
            self.stdout.write(f"  Headers: {dict(response.headers)}")
            self.stdout.write(f"  Raw Response: {response.text}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    self.stdout.write(f"  Parsed JSON: {json.dumps(result, indent=2)}")
                    
                    # Analyze response
                    if result.get('status'):
                        self.stdout.write(self.style.SUCCESS('✅ API returned success'))
                        
                        if 'id' in result:
                            self.stdout.write(f"  Message ID: {result['id']}")
                        if 'detail' in result:
                            self.stdout.write(f"  Detail: {result['detail']}")
                            
                        # Common reasons why message might not be delivered
                        self.stdout.write("\n🔍 If you don't receive the message, check:")
                        self.stdout.write("  1. Is the WhatsApp number registered and active?")
                        self.stdout.write("  2. Is the phone connected to internet?")
                        self.stdout.write("  3. Check WhatsApp spam/blocked messages")
                        self.stdout.write("  4. Try sending to a different number")
                        self.stdout.write("  5. Check Fonnte dashboard for delivery status")
                        
                    else:
                        self.stdout.write(self.style.ERROR('❌ API returned failure'))
                        self.stdout.write(f"  Error: {result}")
                        
                        # Common error analysis
                        error_msg = str(result).lower()
                        if 'invalid' in error_msg:
                            self.stdout.write("  → Possible invalid phone number or token")
                        elif 'quota' in error_msg or 'balance' in error_msg:
                            self.stdout.write("  → Possible quota/balance issue")
                        elif 'blocked' in error_msg:
                            self.stdout.write("  → Number might be blocked")
                            
                except json.JSONDecodeError:
                    self.stdout.write(self.style.WARNING('⚠️ Response is not valid JSON'))
                    
            else:
                self.stdout.write(self.style.ERROR(f'❌ HTTP Error: {response.status_code}'))
                
        except requests.exceptions.Timeout:
            self.stdout.write(self.style.ERROR('❌ Request timeout'))
        except requests.exceptions.ConnectionError:
            self.stdout.write(self.style.ERROR('❌ Connection error'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Exception: {str(e)}'))

    def get_current_time(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")