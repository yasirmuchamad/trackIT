from django.core.management.base import BaseCommand
from django.conf import settings
import requests


class Command(BaseCommand):
    help = 'Test WhatsApp configuration and send test message'

    def add_arguments(self, parser):
        parser.add_argument(
            '--phone',
            type=str,
            help='Phone number to send test message (e.g., 08123456789)',
        )
        parser.add_argument(
            '--message',
            type=str,
            default='Test message from TrackIT system',
            help='Test message to send',
        )

    def handle(self, *args, **options):
        phone = options.get('phone')
        message = options['message']
        
        if not phone:
            self.stdout.write(
                self.style.ERROR('❌ Please provide --phone argument')
            )
            self.stdout.write('Example: python manage.py test_whatsapp --phone 08123456789')
            return
        
        # Format phone number
        clean_phone = ''.join(filter(str.isdigit, phone))
        if clean_phone.startswith('0'):
            clean_phone = '62' + clean_phone[1:]
        elif not clean_phone.startswith('62'):
            clean_phone = '62' + clean_phone
        
        self.stdout.write("📱 Testing WhatsApp Configuration...")
        
        # Check configuration - NO fallback to dummy token
        whatsapp_url = getattr(settings, 'WHATSAPP_SERVICE_URL', 'https://api.fonnte.com/send')
        whatsapp_token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', '')  # Empty default
        
        self.stdout.write(f"URL: {whatsapp_url}")
        self.stdout.write(f"Token: {whatsapp_token[:10]}..." if whatsapp_token else "Token: NOT SET")
        self.stdout.write(f"Phone: {phone} → {clean_phone}")
        
        if not whatsapp_url or not whatsapp_token:
            self.stdout.write(
                self.style.ERROR('❌ WhatsApp service not configured')
            )
            self.stdout.write('Please set WHATSAPP_SERVICE_URL and WHATSAPP_SERVICE_TOKEN in .env file')
            return
        
        # Test Fonnte API
        if 'fonnte' in whatsapp_url.lower():
            self.test_fonnte(clean_phone, message, whatsapp_url, whatsapp_token)
        else:
            self.stdout.write(
                self.style.WARNING('⚠️ Unknown WhatsApp service. Only Fonnte is supported in this test.')
            )

    def test_fonnte(self, phone, message, url, token):
        """Test Fonnte.com API"""
        self.stdout.write("\n🔌 Testing Fonnte API...")
        
        try:
            headers = {
                'Authorization': token,
            }
            
            data = {
                'target': phone,
                'message': message,
                'countryCode': '62',
            }
            
            self.stdout.write(f"Sending to: {phone}")
            self.stdout.write(f"Message: {message}")
            
            response = requests.post(url, data=data, headers=headers, timeout=30)
            
            self.stdout.write(f"Response Status: {response.status_code}")
            self.stdout.write(f"Response Body: {response.text}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get('status'):
                        self.stdout.write(
                            self.style.SUCCESS('✅ WhatsApp message sent successfully!')
                        )
                        if 'id' in result:
                            self.stdout.write(f"Message ID: {result['id']}")
                    else:
                        self.stdout.write(
                            self.style.ERROR(f'❌ Fonnte API returned error: {result}')
                        )
                except ValueError:
                    self.stdout.write(
                        self.style.WARNING('⚠️ Response is not valid JSON')
                    )
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ HTTP Error: {response.status_code}')
                )
                
        except requests.exceptions.Timeout:
            self.stdout.write(
                self.style.ERROR('❌ Request timeout - check internet connection')
            )
        except requests.exceptions.ConnectionError:
            self.stdout.write(
                self.style.ERROR('❌ Connection error - check internet connection')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {str(e)}')
            )
        
        # Troubleshooting tips
        self.stdout.write('\n💡 Troubleshooting Tips:')
        self.stdout.write('1. Check if Fonnte token is valid')
        self.stdout.write('2. Verify phone number format (should start with 62)')
        self.stdout.write('3. Check Fonnte account balance/quota')
        self.stdout.write('4. Ensure WhatsApp number is registered')
        self.stdout.write('5. Check internet connection')