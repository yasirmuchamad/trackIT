from django.core.management.base import BaseCommand
from decouple import config
import os


class Command(BaseCommand):
    help = 'Simple proof that .env is loaded or not'

    def handle(self, *args, **options):
        self.stdout.write("🔍 PROOF: Is .env file loaded?")
        
        # Step 1: Add unique variable to .env
        self.stdout.write("\n📝 Step 1: Adding unique test variable to .env...")
        
        env_content = ""
        try:
            with open('.env', 'r') as f:
                env_content = f.read()
        except:
            self.stdout.write("❌ Cannot read .env file")
            return
        
        # Check if test variable already exists
        if 'PROOF_ENV_LOADED=' not in env_content:
            # Add test variable
            with open('.env', 'a') as f:
                f.write('\n# Test variable to prove .env loading\n')
                f.write('PROOF_ENV_LOADED=YES_ENV_IS_LOADED\n')
            self.stdout.write("✅ Added PROOF_ENV_LOADED to .env file")
        else:
            self.stdout.write("✅ PROOF_ENV_LOADED already exists in .env file")
        
        # Step 2: Try to read the variable
        self.stdout.write("\n📖 Step 2: Reading test variable...")
        
        # Method 1: Direct decouple
        decouple_value = config('PROOF_ENV_LOADED', default='NOT_FOUND_DECOUPLE')
        self.stdout.write(f"   Decouple config(): {decouple_value}")
        
        # Method 2: OS environment
        os_value = os.environ.get('PROOF_ENV_LOADED', 'NOT_FOUND_OS')
        self.stdout.write(f"   OS environment: {os_value}")
        
        # Method 3: Django settings (if configured)
        try:
            from django.conf import settings
            django_value = getattr(settings, 'PROOF_ENV_LOADED', 'NOT_IN_DJANGO_SETTINGS')
            self.stdout.write(f"   Django settings: {django_value}")
        except:
            self.stdout.write("   Django settings: NOT_CONFIGURED")
        
        # Step 3: Diagnosis
        self.stdout.write("\n🎯 DIAGNOSIS:")
        
        if decouple_value == 'YES_ENV_IS_LOADED':
            self.stdout.write("   ✅ PROOF: .env file IS being loaded by decouple!")
            
            if os_value == 'YES_ENV_IS_LOADED':
                self.stdout.write("   ✅ BONUS: .env variables are also in OS environment")
            else:
                self.stdout.write("   ⚠️ NOTE: .env loaded by decouple but not in OS environment")
                
        else:
            self.stdout.write("   ❌ PROBLEM: .env file is NOT being loaded!")
            self.stdout.write("   💡 Possible causes:")
            self.stdout.write("      - .env file in wrong location")
            self.stdout.write("      - python-decouple not working")
            self.stdout.write("      - File permissions issue")
        
        # Step 4: Test with WhatsApp token
        self.stdout.write("\n🔍 Step 4: Testing actual WhatsApp configuration...")
        
        whatsapp_token = config('WHATSAPP_SERVICE_TOKEN', default='DEFAULT_TOKEN')
        
        if whatsapp_token == 'DEFAULT_TOKEN':
            self.stdout.write("   ❌ WHATSAPP_SERVICE_TOKEN not found in .env")
        elif whatsapp_token == 'urWuiF1pMJyGM25uJEjA':
            self.stdout.write("   ⚠️ WHATSAPP_SERVICE_TOKEN is using example/dummy value")
            self.stdout.write("   💡 This explains why Fonnte dashboard is empty!")
        else:
            self.stdout.write(f"   ✅ WHATSAPP_SERVICE_TOKEN found: {whatsapp_token[:10]}...")
            self.stdout.write("   💡 This should be a real Fonnte token")
        
        # Step 5: Clean up
        self.stdout.write("\n🧹 Step 5: Cleanup...")
        self.stdout.write("   💡 You can remove PROOF_ENV_LOADED from .env file if you want")
        
        # Final conclusion
        self.stdout.write("\n📋 FINAL CONCLUSION:")
        
        if decouple_value == 'YES_ENV_IS_LOADED':
            if whatsapp_token == 'urWuiF1pMJyGM25uJEjA':
                self.stdout.write("   🎯 .env IS loaded, but WhatsApp token is DUMMY/EXAMPLE")
                self.stdout.write("   🛠️ SOLUTION: Replace token with real Fonnte token")
            else:
                self.stdout.write("   ✅ .env IS loaded and WhatsApp token looks real")
                self.stdout.write("   🔍 If still not working, check token validity in Fonnte dashboard")
        else:
            self.stdout.write("   ❌ .env is NOT loaded - need to fix Django configuration")
            self.stdout.write("   🛠️ SOLUTION: Check decouple setup in settings.py")