from django.core.management.base import BaseCommand
from django.conf import settings
import requests
import json


class Command(BaseCommand):
    help = 'Check Fonnte account status and test message delivery'

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
        
        self.stdout.write("🔍 Checking Fonnte Account Status...")
        
        # Get configuration
        whatsapp_url = getattr(settings, 'WHATSAPP_SERVICE_URL', '')
        whatsapp_token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', '')
        
        if not whatsapp_url or not whatsapp_token:
            self.stdout.write(self.style.ERROR('❌ WhatsApp configuration missing'))
            return
        
        # Step 1: Check account profile
        self.check_account_profile(whatsapp_token)
        
        # Step 2: Check device status
        self.check_device_status(whatsapp_token)
        
        # Step 3: Send test message with detailed analysis
        self.send_test_message_detailed(whatsapp_url, whatsapp_token, clean_phone)
        
        # Step 4: Check message history/status
        self.check_message_history(whatsapp_token)

    def check_account_profile(self, token):
        """Check Fonnte account profile"""
        self.stdout.write("\n📊 Checking Account Profile...")
        
        try:
            url = "https://api.fonnte.com/profile"
            headers = {'Authorization': token}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                profile = response.json()
                self.stdout.write("✅ Account Profile:")
                
                for key, value in profile.items():
                    self.stdout.write(f"  {key}: {value}")
                
                # Check critical fields
                if profile.get('status') != 'connect':
                    self.stdout.write(self.style.WARNING(f"⚠️ Device status: {profile.get('status')}"))
                    self.stdout.write("   Device might not be connected to WhatsApp")
                
                if 'quota' in profile:
                    quota = profile['quota']
                    if isinstance(quota, (int, float)) and quota <= 0:
                        self.stdout.write(self.style.ERROR("❌ Quota habis!"))
                    else:
                        self.stdout.write(f"✅ Quota: {quota}")
                        
            else:
                self.stdout.write(self.style.ERROR(f"❌ Profile check failed: {response.status_code} - {response.text}"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Profile check error: {str(e)}"))

    def check_device_status(self, token):
        """Check WhatsApp device connection status"""
        self.stdout.write("\n📱 Checking Device Status...")
        
        try:
            url = "https://api.fonnte.com/device"
            headers = {'Authorization': token}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                device_info = response.json()
                self.stdout.write("📱 Device Info:")
                
                for key, value in device_info.items():
                    self.stdout.write(f"  {key}: {value}")
                
                # Analyze device status
                if isinstance(device_info, dict):
                    status = device_info.get('status', 'unknown')
                    if status != 'connect':
                        self.stdout.write(self.style.WARNING(f"⚠️ Device not connected: {status}"))
                        self.stdout.write("   This could be why messages aren't being delivered")
                    else:
                        self.stdout.write("✅ Device connected")
                        
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Device check failed: {response.status_code} - {response.text}"))
                
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"⚠️ Device check error: {str(e)}"))

    def send_test_message_detailed(self, url, token, phone):
        """Send test message with detailed response analysis"""
        self.stdout.write(f"\n📤 Sending Test Message to {phone}...")
        
        message = f"🧪 Test dari TrackIT - {self.get_current_time()}\n\nJika Anda menerima pesan ini, sistem WhatsApp berfungsi dengan baik."
        
        try:
            headers = {'Authorization': token}
            data = {
                'target': phone,
                'message': message,
                'countryCode': '62',
            }
            
            self.stdout.write("📋 Request Details:")
            self.stdout.write(f"  URL: {url}")
            self.stdout.write(f"  Token: {token[:10]}...")
            self.stdout.write(f"  Target: {phone}")
            self.stdout.write(f"  Message length: {len(message)} chars")
            
            response = requests.post(url, data=data, headers=headers, timeout=30)
            
            self.stdout.write(f"\n📨 Response Details:")
            self.stdout.write(f"  Status Code: {response.status_code}")
            self.stdout.write(f"  Response Time: {response.elapsed.total_seconds():.2f}s")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    self.stdout.write(f"  JSON Response: {json.dumps(result, indent=2)}")
                    
                    # Detailed analysis
                    if result.get('status'):
                        self.stdout.write(self.style.SUCCESS("✅ API Response: SUCCESS"))
                        
                        # Check for message ID
                        if 'id' in result:
                            msg_id = result['id']
                            self.stdout.write(f"📝 Message ID: {msg_id}")
                            self.stdout.write("💡 Save this ID to check delivery status later")
                        
                        # Check for detail message
                        if 'detail' in result:
                            detail = result['detail']
                            self.stdout.write(f"📄 Detail: {detail}")
                            
                            # Analyze detail message
                            if 'sent' in detail.lower():
                                self.stdout.write("✅ Message sent to WhatsApp servers")
                            if 'queue' in detail.lower():
                                self.stdout.write("⏳ Message queued for delivery")
                        
                        # Important note about delivery
                        self.stdout.write("\n⚠️ IMPORTANT NOTES:")
                        self.stdout.write("   • 'Success' means message was SENT to WhatsApp servers")
                        self.stdout.write("   • It does NOT guarantee DELIVERY to recipient")
                        self.stdout.write("   • Delivery depends on:")
                        self.stdout.write("     - Recipient's phone is online")
                        self.stdout.write("     - Number is registered in WhatsApp")
                        self.stdout.write("     - Number hasn't blocked your WhatsApp Business")
                        self.stdout.write("     - Message doesn't violate WhatsApp policies")
                        
                    else:
                        self.stdout.write(self.style.ERROR("❌ API Response: FAILED"))
                        self.stdout.write(f"Error details: {result}")
                        
                        # Common error analysis
                        self.analyze_error_response(result)
                        
                except json.JSONDecodeError:
                    self.stdout.write(self.style.ERROR("❌ Response is not valid JSON"))
                    self.stdout.write(f"Raw response: {response.text}")
            else:
                self.stdout.write(self.style.ERROR(f"❌ HTTP Error: {response.status_code}"))
                self.stdout.write(f"Response: {response.text}")
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Request failed: {str(e)}"))

    def check_message_history(self, token):
        """Check recent message history"""
        self.stdout.write("\n📜 Checking Message History...")
        
        try:
            url = "https://api.fonnte.com/history"
            headers = {'Authorization': token}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                history = response.json()
                
                if isinstance(history, list) and history:
                    self.stdout.write("📜 Recent Messages:")
                    
                    for i, msg in enumerate(history[:5]):  # Show last 5 messages
                        self.stdout.write(f"\n  Message {i+1}:")
                        for key, value in msg.items():
                            self.stdout.write(f"    {key}: {value}")
                else:
                    self.stdout.write("📜 No message history found")
                    
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ History check failed: {response.status_code}"))
                
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"⚠️ History check error: {str(e)}"))

    def analyze_error_response(self, result):
        """Analyze error response for common issues"""
        error_str = str(result).lower()
        
        if 'invalid' in error_str:
            self.stdout.write("🔍 Possible causes:")
            self.stdout.write("   • Invalid phone number format")
            self.stdout.write("   • Invalid authorization token")
            
        elif 'quota' in error_str or 'balance' in error_str:
            self.stdout.write("🔍 Possible causes:")
            self.stdout.write("   • Account quota exceeded")
            self.stdout.write("   • Insufficient balance")
            self.stdout.write("   • Check your Fonnte dashboard")
            
        elif 'blocked' in error_str:
            self.stdout.write("🔍 Possible causes:")
            self.stdout.write("   • Phone number blocked your WhatsApp Business")
            self.stdout.write("   • Try with a different number")
            
        elif 'not registered' in error_str:
            self.stdout.write("🔍 Possible causes:")
            self.stdout.write("   • Phone number not registered in WhatsApp")
            self.stdout.write("   • Number format incorrect")

    def get_current_time(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")