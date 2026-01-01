from django.core.management.base import BaseCommand
from django.conf import settings
import requests


class Command(BaseCommand):
    help = 'Test different phone number formats'

    def add_arguments(self, parser):
        parser.add_argument(
            '--phone',
            type=str,
            default='083838786991',
            help='Base phone number to test',
        )

    def handle(self, *args, **options):
        base_phone = options.get('phone')
        
        self.stdout.write("📱 Testing Different Phone Number Formats...")
        
        # Get configuration
        whatsapp_url = getattr(settings, 'WHATSAPP_SERVICE_URL', '')
        whatsapp_token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', '')
        
        if not whatsapp_url or not whatsapp_token:
            self.stdout.write(self.style.ERROR('❌ WhatsApp configuration missing'))
            return
        
        # Generate different formats
        formats_to_test = []
        
        # Remove all non-digits first
        clean_digits = ''.join(filter(str.isdigit, base_phone))
        
        # Format 1: Original input
        formats_to_test.append(('Original', base_phone))
        
        # Format 2: Clean digits only
        formats_to_test.append(('Clean digits', clean_digits))
        
        # Format 3: With +62 (if starts with 0)
        if clean_digits.startswith('0'):
            format3 = '62' + clean_digits[1:]
            formats_to_test.append(('62xxx format', format3))
        
        # Format 4: With +62 prefix
        if not clean_digits.startswith('62'):
            if clean_digits.startswith('0'):
                format4 = '62' + clean_digits[1:]
            else:
                format4 = '62' + clean_digits
            formats_to_test.append(('+62 prefix', format4))
        
        # Format 5: With country code but no leading +
        if clean_digits.startswith('0'):
            format5 = '62' + clean_digits[1:]
            formats_to_test.append(('Country code', format5))
        
        # Format 6: International format
        if clean_digits.startswith('0'):
            format6 = '+62' + clean_digits[1:]
            formats_to_test.append(('International', format6))
        
        # Remove duplicates while preserving order
        seen = set()
        unique_formats = []
        for name, phone in formats_to_test:
            if phone not in seen:
                seen.add(phone)
                unique_formats.append((name, phone))
        
        self.stdout.write(f"📋 Testing {len(unique_formats)} different formats:")
        
        results = []
        message = f"🧪 Test format nomor - {self.get_current_time()}"
        
        for i, (format_name, phone_format) in enumerate(unique_formats, 1):
            self.stdout.write(f"\n📤 Test {i}: {format_name} → {phone_format}")
            
            success = self.send_test_message(
                whatsapp_url, whatsapp_token, phone_format, 
                f"{message}\nFormat: {format_name}"
            )
            
            results.append((format_name, phone_format, success))
            
            # Small delay between tests
            import time
            time.sleep(1)
        
        # Summary
        self.stdout.write("\n📊 RESULTS SUMMARY:")
        self.stdout.write("=" * 50)
        
        successful_formats = []
        failed_formats = []
        
        for format_name, phone_format, success in results:
            status = "✅ SUCCESS" if success else "❌ FAILED"
            self.stdout.write(f"{format_name:15} | {phone_format:15} | {status}")
            
            if success:
                successful_formats.append((format_name, phone_format))
            else:
                failed_formats.append((format_name, phone_format))
        
        self.stdout.write("\n🎯 RECOMMENDATIONS:")
        
        if successful_formats:
            self.stdout.write("✅ Working formats:")
            for name, phone in successful_formats:
                self.stdout.write(f"   • {name}: {phone}")
            
            # Check what onboarding system uses
            self.stdout.write("\n🔍 Onboarding system formatting:")
            test_input = base_phone
            clean_phone = ''.join(filter(str.isdigit, test_input))
            if clean_phone.startswith('0'):
                onboarding_format = '62' + clean_phone[1:]
            elif not clean_phone.startswith('62'):
                onboarding_format = '62' + clean_phone
            else:
                onboarding_format = clean_phone
            
            self.stdout.write(f"   Onboarding uses: {test_input} → {onboarding_format}")
            
            # Check if onboarding format matches any successful format
            if onboarding_format in [phone for _, phone in successful_formats]:
                self.stdout.write("   ✅ Onboarding format matches working format")
            else:
                self.stdout.write("   ❌ Onboarding format doesn't match any working format!")
                self.stdout.write("   💡 This might be the issue!")
        
        if failed_formats:
            self.stdout.write("\n❌ Failed formats:")
            for name, phone in failed_formats:
                self.stdout.write(f"   • {name}: {phone}")
        
        self.stdout.write("\n💡 Wait a few minutes to see which messages actually arrive")
        self.stdout.write("💡 The format that delivers messages is the correct one to use")

    def send_test_message(self, url, token, phone, message):
        """Send test message and return success status"""
        try:
            headers = {'Authorization': token}
            data = {
                'target': phone,
                'message': message,
                'countryCode': '62',
            }
            
            response = requests.post(url, data=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    success = result.get('status', False)
                    
                    if success:
                        self.stdout.write(f"   ✅ API Success: {result.get('detail', 'OK')}")
                    else:
                        self.stdout.write(f"   ❌ API Failed: {result}")
                    
                    return success
                    
                except Exception as e:
                    self.stdout.write(f"   ❌ JSON Error: {e}")
                    return False
            else:
                self.stdout.write(f"   ❌ HTTP Error: {response.status_code}")
                return False
                
        except Exception as e:
            self.stdout.write(f"   ❌ Exception: {str(e)}")
            return False

    def get_current_time(self):
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")