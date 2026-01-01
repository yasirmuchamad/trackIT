from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Check WhatsApp configuration'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Checking WhatsApp Configuration...")
        
        # Check settings
        whatsapp_url = getattr(settings, 'WHATSAPP_SERVICE_URL', '')
        whatsapp_token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', '')
        
        self.stdout.write(f"WHATSAPP_SERVICE_URL: '{whatsapp_url}'")
        self.stdout.write(f"WHATSAPP_SERVICE_TOKEN: '{whatsapp_token[:10]}...'" if whatsapp_token else "WHATSAPP_SERVICE_TOKEN: NOT SET")
        
        # Validation
        if not whatsapp_url:
            self.stdout.write(self.style.ERROR('❌ WHATSAPP_SERVICE_URL is empty'))
        elif whatsapp_url == 'https://api.fonnte.com/send':
            self.stdout.write(self.style.SUCCESS('✅ WHATSAPP_SERVICE_URL is correct for Fonnte'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠️ Unknown WhatsApp service: {whatsapp_url}'))
        
        if not whatsapp_token:
            self.stdout.write(self.style.ERROR('❌ WHATSAPP_SERVICE_TOKEN is empty'))
        elif len(whatsapp_token) > 10:
            self.stdout.write(self.style.SUCCESS('✅ WHATSAPP_SERVICE_TOKEN is set'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ WHATSAPP_SERVICE_TOKEN seems too short'))
        
        # Check .env file
        import os
        env_path = os.path.join(settings.BASE_DIR, '.env')
        if os.path.exists(env_path):
            self.stdout.write(f"\n📄 Checking .env file: {env_path}")
            with open(env_path, 'r') as f:
                lines = f.readlines()
                
            whatsapp_lines = [line.strip() for line in lines if 'WHATSAPP' in line and not line.strip().startswith('#')]
            
            if whatsapp_lines:
                self.stdout.write("WhatsApp lines in .env:")
                for line in whatsapp_lines:
                    self.stdout.write(f"  {line}")
            else:
                self.stdout.write("❌ No WhatsApp configuration found in .env")
        else:
            self.stdout.write("❌ .env file not found")
        
        self.stdout.write("\n🔧 Next steps:")
        if not whatsapp_url or not whatsapp_token:
            self.stdout.write("1. Update .env file with correct WhatsApp configuration")
            self.stdout.write("2. Restart Django server")
            self.stdout.write("3. Run: python manage.py simple_whatsapp_test")
        else:
            self.stdout.write("1. Run: python manage.py simple_whatsapp_test")
            self.stdout.write("2. If successful, test onboarding: python manage.py test_onboarding --employee-id 99999")