from django.core.management.base import BaseCommand
from django.conf import settings
from decouple import config
import os


class Command(BaseCommand):
    help = 'Test if .env loading fix works'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Testing .env Loading Fix...")
        
        # Test 1: Check if .env file exists and location
        self.stdout.write("\n📁 Step 1: File Location Check")
        
        from pathlib import Path
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        env_path = BASE_DIR / '.env'
        
        self.stdout.write(f"   Project root: {BASE_DIR}")
        self.stdout.write(f"   .env path: {env_path}")
        self.stdout.write(f"   .env exists: {'✅' if env_path.exists() else '❌'}")
        
        if env_path.exists():
            # Show file size and permissions
            stat = env_path.stat()
            self.stdout.write(f"   .env size: {stat.st_size} bytes")
            self.stdout.write(f"   .env readable: {'✅' if os.access(env_path, os.R_OK) else '❌'}")
        
        # Test 2: Try to read .env directly
        self.stdout.write("\n📖 Step 2: Direct File Reading")
        
        try:
            with open(env_path, 'r') as f:
                content = f.read()
                lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
                self.stdout.write(f"   ✅ Successfully read .env file")
                self.stdout.write(f"   📄 Found {len(lines)} configuration lines")
                
                # Show WhatsApp config from file
                for line in lines:
                    if 'WHATSAPP_SERVICE' in line:
                        key, value = line.split('=', 1)
                        if 'TOKEN' in key:
                            self.stdout.write(f"   📱 {key}={value[:10]}...")
                        else:
                            self.stdout.write(f"   📱 {key}={value}")
                            
        except Exception as e:
            self.stdout.write(f"   ❌ Error reading .env file: {str(e)}")
        
        # Test 3: Test decouple config after fix
        self.stdout.write("\n🔧 Step 3: Decouple Config Test")
        
        # Test with unique variable first
        test_value = config('WHATSAPP_SERVICE_URL', default='DECOUPLE_NOT_WORKING')
        self.stdout.write(f"   WHATSAPP_SERVICE_URL: {test_value}")
        
        if test_value == 'DECOUPLE_NOT_WORKING':
            self.stdout.write("   ❌ Decouple still not reading .env file")
        elif test_value == 'https://api.fonnte.com/send':
            self.stdout.write("   ✅ Decouple is reading .env file!")
        else:
            self.stdout.write(f"   ⚠️ Unexpected value: {test_value}")
        
        # Test token
        token_value = config('WHATSAPP_SERVICE_TOKEN', default='TOKEN_NOT_FOUND')
        if token_value == 'TOKEN_NOT_FOUND':
            self.stdout.write("   ❌ Token not found in .env")
        else:
            self.stdout.write(f"   ✅ Token found: {token_value[:10]}...")
        
        # Test 4: Check Django settings
        self.stdout.write("\n⚙️ Step 4: Django Settings Check")
        
        django_url = getattr(settings, 'WHATSAPP_SERVICE_URL', 'NOT_IN_SETTINGS')
        django_token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', 'NOT_IN_SETTINGS')
        
        self.stdout.write(f"   Django URL: {django_url}")
        self.stdout.write(f"   Django Token: {django_token[:10]}..." if django_token != 'NOT_IN_SETTINGS' else "   Django Token: NOT_IN_SETTINGS")
        
        # Test 5: Final verification
        self.stdout.write("\n🎯 Step 5: Final Verification")
        
        if test_value != 'DECOUPLE_NOT_WORKING' and django_url == test_value:
            self.stdout.write("   ✅ SUCCESS: .env file is now being loaded correctly!")
            self.stdout.write("   ✅ Decouple and Django settings match")
            
            if token_value == 'urWuiF1pMJyGM25uJEjA':
                self.stdout.write("   ⚠️ NOTE: Token is still the example/dummy token")
                self.stdout.write("   💡 Replace with real Fonnte token for actual functionality")
            else:
                self.stdout.write("   ✅ Token appears to be customized")
                
        else:
            self.stdout.write("   ❌ PROBLEM: .env file still not loading correctly")
            self.stdout.write("   💡 Try restarting Django server")
        
        # Instructions
        self.stdout.write("\n📋 NEXT STEPS:")
        self.stdout.write("   1. If .env is now loading: Replace dummy token with real Fonnte token")
        self.stdout.write("   2. If still not loading: Restart Django server and try again")
        self.stdout.write("   3. Test WhatsApp functionality: python manage.py test_exact_onboarding_flow")
        self.stdout.write("   4. Check Fonnte dashboard for message history")