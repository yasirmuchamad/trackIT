from django.core.management.base import BaseCommand
from django.conf import settings
from decouple import config
import os
import glob


class Command(BaseCommand):
    help = 'Find all dummy tokens in the system'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Searching for Dummy Tokens...")
        
        dummy_token = 'urWuiF1pMJyGM25uJEjA'
        
        # Search locations
        locations_to_check = [
            ('.env', 'Environment file'),
            ('trackIT/settings.py', 'Django settings'),
            ('employee/services/onboarding_delivery.py', 'Onboarding service'),
            ('employee/management/commands/*.py', 'Management commands'),
            ('employee/settings_example.py', 'Settings example'),
        ]
        
        found_dummy = False
        
        # Check 1: .env file
        self.stdout.write("\n📁 Checking .env file...")
        try:
            with open('.env', 'r') as f:
                content = f.read()
                if dummy_token in content:
                    self.stdout.write(f"   ❌ FOUND dummy token in .env file!")
                    found_dummy = True
                    
                    # Show the line
                    for line_num, line in enumerate(content.split('\n'), 1):
                        if dummy_token in line:
                            self.stdout.write(f"   Line {line_num}: {line}")
                else:
                    self.stdout.write("   ✅ No dummy token in .env file")
                    
                # Show what token is actually in .env
                for line in content.split('\n'):
                    if line.startswith('WHATSAPP_SERVICE_TOKEN='):
                        actual_token = line.split('=', 1)[1]
                        self.stdout.write(f"   📱 Current token in .env: {actual_token}")
                        break
                        
        except FileNotFoundError:
            self.stdout.write("   ⚠️ .env file not found")
        except Exception as e:
            self.stdout.write(f"   ❌ Error reading .env: {str(e)}")
        
        # Check 2: settings.py
        self.stdout.write("\n⚙️ Checking settings.py...")
        try:
            with open('trackIT/settings.py', 'r') as f:
                content = f.read()
                if dummy_token in content:
                    self.stdout.write(f"   ❌ FOUND dummy token in settings.py!")
                    found_dummy = True
                    
                    # Show the lines
                    for line_num, line in enumerate(content.split('\n'), 1):
                        if dummy_token in line:
                            self.stdout.write(f"   Line {line_num}: {line.strip()}")
                else:
                    self.stdout.write("   ✅ No dummy token in settings.py")
                    
        except Exception as e:
            self.stdout.write(f"   ❌ Error reading settings.py: {str(e)}")
        
        # Check 3: onboarding_delivery.py
        self.stdout.write("\n🚀 Checking onboarding_delivery.py...")
        try:
            with open('employee/services/onboarding_delivery.py', 'r') as f:
                content = f.read()
                if dummy_token in content:
                    self.stdout.write(f"   ❌ FOUND dummy token in onboarding_delivery.py!")
                    found_dummy = True
                    
                    # Show the lines
                    for line_num, line in enumerate(content.split('\n'), 1):
                        if dummy_token in line:
                            self.stdout.write(f"   Line {line_num}: {line.strip()}")
                else:
                    self.stdout.write("   ✅ No dummy token in onboarding_delivery.py")
                    
        except Exception as e:
            self.stdout.write(f"   ❌ Error reading onboarding_delivery.py: {str(e)}")
        
        # Check 4: All Python files for hardcoded tokens
        self.stdout.write("\n🔍 Checking all Python files...")
        
        python_files = glob.glob('**/*.py', recursive=True)
        files_with_dummy = []
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if dummy_token in content:
                        files_with_dummy.append(file_path)
            except:
                continue  # Skip files that can't be read
        
        if files_with_dummy:
            self.stdout.write(f"   ❌ Found dummy token in {len(files_with_dummy)} files:")
            for file_path in files_with_dummy:
                self.stdout.write(f"      • {file_path}")
        else:
            self.stdout.write("   ✅ No dummy tokens found in Python files")
        
        # Check 5: What Django actually sees
        self.stdout.write("\n🐍 Checking what Django actually uses...")
        
        try:
            # Direct decouple test
            decouple_token = config('WHATSAPP_SERVICE_TOKEN', default='DECOUPLE_FAILED')
            self.stdout.write(f"   Decouple config(): {decouple_token}")
            
            # Django settings
            django_token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', 'DJANGO_FAILED')
            self.stdout.write(f"   Django settings: {django_token}")
            
            # OS environment
            os_token = os.environ.get('WHATSAPP_SERVICE_TOKEN', 'OS_FAILED')
            self.stdout.write(f"   OS environment: {os_token}")
            
            # Check if any of these is dummy
            if decouple_token == dummy_token:
                self.stdout.write("   ❌ Decouple is returning dummy token!")
                found_dummy = True
            if django_token == dummy_token:
                self.stdout.write("   ❌ Django settings has dummy token!")
                found_dummy = True
            if os_token == dummy_token:
                self.stdout.write("   ❌ OS environment has dummy token!")
                found_dummy = True
                
        except Exception as e:
            self.stdout.write(f"   ❌ Error checking Django config: {str(e)}")
        
        # Check 6: Test actual API call
        self.stdout.write("\n🧪 Testing actual API call...")
        
        try:
            from employee.services.onboarding_delivery import send_via_fonnte
            
            # This will show us exactly what token is being used
            self.stdout.write("   📤 Making test API call to see what token is used...")
            
            # We'll check the logs to see what token was actually sent
            import logging
            
            # Temporarily increase log level to capture the request details
            logger = logging.getLogger('employee.services.onboarding_delivery')
            original_level = logger.level
            logger.setLevel(logging.DEBUG)
            
            # Make a test call (will fail but we'll see the token in logs)
            result = send_via_fonnte('6283838786991', 'Test token verification')
            
            # Restore log level
            logger.setLevel(original_level)
            
            self.stdout.write(f"   API call result: {result}")
            self.stdout.write("   💡 Check logs/onboarding.log for the actual token used")
            
        except Exception as e:
            self.stdout.write(f"   ❌ Error testing API call: {str(e)}")
        
        # Summary
        self.stdout.write("\n🎯 SUMMARY:")
        
        if found_dummy:
            self.stdout.write("   ❌ DUMMY TOKENS FOUND! System is using fake tokens.")
            self.stdout.write("   🛠️ ACTION REQUIRED:")
            self.stdout.write("      1. Replace ALL dummy tokens with real Fonnte token")
            self.stdout.write("      2. Restart Django server")
            self.stdout.write("      3. Test again")
        else:
            self.stdout.write("   ✅ No dummy tokens found in code")
            self.stdout.write("   🤔 If WhatsApp still not working, possible causes:")
            self.stdout.write("      • Token is invalid/expired")
            self.stdout.write("      • Fonnte account has no balance/quota")
            self.stdout.write("      • Phone number not registered in WhatsApp")
            self.stdout.write("      • Message content violates WhatsApp policy")
        
        self.stdout.write("\n💡 NEXT STEPS:")
        self.stdout.write("   1. Check logs/onboarding.log for actual token used")
        self.stdout.write("   2. Login to Fonnte dashboard to verify token validity")
        self.stdout.write("   3. Check Fonnte account balance/quota")
        self.stdout.write("   4. Test with a different phone number")
        self.stdout.write("   5. Verify phone number is registered in WhatsApp")