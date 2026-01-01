from django.core.management.base import BaseCommand
import requests


class Command(BaseCommand):
    help = 'Test with different phone numbers'

    def add_arguments(self, parser):
        parser.add_argument('--phone', type=str, help='Phone number to test')

    def handle(self, *args, **options):
        phone = options.get('phone')
        
        if not phone:
            self.stdout.write("Usage: python manage.py test_different_numbers --phone 08123456789")
            return
        
        # Format phone
        clean_phone = ''.join(filter(str.isdigit, phone))
        if clean_phone.startswith('0'):
            clean_phone = '62' + clean_phone[1:]
        elif not clean_phone.startswith('62'):
            clean_phone = '62' + clean_phone
        
        self.stdout.write(f"🧪 Testing phone: {phone} → {clean_phone}")
        
        token = 'urWuiF1pMJyGM25uJEjA'
        
        try:
            response = requests.post('https://api.fonnte.com/send',
                                   headers={'Authorization': token},
                                   data={
                                       'target': clean_phone,
                                       'message': f'🧪 Test ke nomor {phone} - Apakah sampai?',
                                       'countryCode': '62'
                                   })
            
            self.stdout.write(f"Status: {response.status_code}")
            self.stdout.write(f"Response: {response.text}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get('status') and 'id' in result:
                        msg_id = result['id'][0] if isinstance(result['id'], list) else result['id']
                        self.stdout.write(f"✅ Message sent! ID: {msg_id}")
                        self.stdout.write("💡 Check this number's WhatsApp in 1-2 minutes")
                        self.stdout.write(f"💡 Also check Fonnte dashboard for message ID: {msg_id}")
                    else:
                        self.stdout.write(f"❌ Failed: {result}")
                except:
                    self.stdout.write("⚠️ Non-JSON response")
            
        except Exception as e:
            self.stdout.write(f"❌ Error: {str(e)}")
        
        self.stdout.write("\n📋 Next steps:")
        self.stdout.write("1. Check WhatsApp on the target phone")
        self.stdout.write("2. Check Fonnte dashboard for delivery status")
        self.stdout.write("3. If this number receives but 083838786991 doesn't:")
        self.stdout.write("   → 083838786991 has issues (not registered, blocked, etc.)")
        self.stdout.write("4. If no numbers receive messages:")
        self.stdout.write("   → Device connection issue in Fonnte dashboard")