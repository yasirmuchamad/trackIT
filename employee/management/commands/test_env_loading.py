from django.core.management.base import BaseCommand
from django.conf import settings
from decouple import config
import os


class Command(BaseCommand):
    help = 'Test if .env file is properly loaded and used'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Testing .env File Loading...")
        
        # Test 1: Direct file reading vs environment variables
        self.test_direct_vs_env()
        
        # Test 2: Decouple config() vs Django settings
        self.test_decouple_vs_django()
        
        # Test 3: Create unique test variable
        self.test_unique_variable()
        
        # Test 4: Test with modified .env
        self.test_env_modification()

    def test_direct_vs_env(self):
        """Test 1: Compare direct file reading with environment variables"""
        self.stdout.write("\n🧪 Test 1: Direct File Reading vs Environment Variables")
        
        # Read .env file directly
        env_from_file = {}
        try:
            with open('.env', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_from_file[key] = value
            
            self.stdout.write(f"   📁 Variables in .env file: {len(env_from_file)}")
            
            # Check if these are in environment
            for key, file_value in env_from_file.items():
                env_value = os.environ.get(key, 'NOT_FOUND')
                
                if env_value == file_value:
                    self.stdout.write(f"   ✅ {key}: File and Environment MATCH")
                elif env_value == 'NOT_FOUND':
                    self.stdout.write(f"   ❌ {key}: In file but NOT in environment")
                else:
                    self.stdout.write(f"   ⚠️ {key}: File='{file_value}' vs Env='{env_value}'")
                    
        except Exception as e:
            self.stdout.write(f"   ❌ Error reading .env file: {str(e)}")

    def test_decouple_vs_django(self):
        """Test 2: Compare decouple config() with Django settings"""
        self.stdout.write("\n🧪 Test 2: Decouple config() vs Django settings")
        
        test_vars = [
            'WHATSAPP_SERVICE_URL',
            'WHATSAPP_SERVICE_TOKEN',
            'EMAIL_HOST',
            'EMAIL_HOST_USER',
            'EMAIL_HOST_PASSWORD',
        ]
        
        for var in test_vars:
            # Get from decouple directly
            decouple_value = config(var, default='DECOUPLE_NOT_FOUND')
            
            # Get from Django settings
            django_value = getattr(settings, var, 'DJANGO_NOT_FOUND')
            
            # Compare
            if decouple_value == django_value:
                self.stdout.write(f"   ✅ {var}: Decouple and Django MATCH")
            else:
                self.stdout.write(f"   ❌ {var}: Decouple='{decouple_value}' vs Django='{django_value}'")

    def test_unique_variable(self):
        """Test 3: Add unique test variable to verify .env loading"""
        self.stdout.write("\n🧪 Test 3: Unique Test Variable")
        
        # Check if our test variable exists
        test_value = config('TEST_ENV_LOADING', default='NOT_FOUND')
        
        if test_value == 'NOT_FOUND':
            self.stdout.write("   ⚠️ TEST_ENV_LOADING not found in .env")
            self.stdout.write("   💡 Add this line to .env file to test:")
            self.stdout.write("   TEST_ENV_LOADING=this_proves_env_is_loaded")
        else:
            self.stdout.write(f"   ✅ TEST_ENV_LOADING found: '{test_value}'")
            
            # Also check if it's in Django settings
            try:
                django_test = getattr(settings, 'TEST_ENV_LOADING', 'NOT_IN_DJANGO')
                if django_test == test_value:
                    self.stdout.write("   ✅ Test variable also available in Django settings")
                else:
                    self.stdout.write("   ⚠️ Test variable not in Django settings (need to add to settings.py)")
            except:
                self.stdout.write("   ⚠️ Test variable not configured in Django settings")

    def test_env_modification(self):
        """Test 4: Test if .env changes are reflected"""
        self.stdout.write("\n🧪 Test 4: Environment Modification Test")
        
        # Get current value
        current_token = config('WHATSAPP_SERVICE_TOKEN', default='NOT_FOUND')
        self.stdout.write(f"   Current WHATSAPP_SERVICE_TOKEN: {current_token}")
        
        # Instructions for manual test
        self.stdout.write("\n   📝 Manual Test Instructions:")
        self.stdout.write("   1. Note the current token above")
        self.stdout.write("   2. Edit .env file and change WHATSAPP_SERVICE_TOKEN to 'MODIFIED_TOKEN'")
        self.stdout.write("   3. Run this command again WITHOUT restarting Django")
        self.stdout.write("   4. If value changes to 'MODIFIED_TOKEN', .env is loaded dynamically")
        self.stdout.write("   5. If value stays the same, Django caches .env on startup")
        
        # Check if this is a known test value
        if current_token == 'MODIFIED_TOKEN':
            self.stdout.write("   ✅ Token shows as MODIFIED_TOKEN - .env changes are reflected!")
            self.stdout.write("   💡 Change it back to the real token when done testing")

    def comprehensive_diagnosis(self):
        """Provide comprehensive diagnosis"""
        self.stdout.write("\n🎯 COMPREHENSIVE DIAGNOSIS:")
        
        # Check all indicators
        indicators = {
            'env_file_exists': os.path.exists('.env'),
            'decouple_installed': True,  # We know it's installed from previous test
            'django_reads_env': False,
            'values_match': False,
        }
        
        try:
            # Test if Django reads .env
            test_val = config('WHATSAPP_SERVICE_URL', default='TEST_DEFAULT')
            django_val = getattr(settings, 'WHATSAPP_SERVICE_URL', 'DJANGO_DEFAULT')
            
            if test_val != 'TEST_DEFAULT':
                indicators['django_reads_env'] = True
                
            if test_val == django_val:
                indicators['values_match'] = True
                
        except Exception as e:
            self.stdout.write(f"   ❌ Error in diagnosis: {str(e)}")
        
        # Provide diagnosis
        if all(indicators.values()):
            self.stdout.write("   ✅ PERFECT: .env file is properly loaded and used")
        elif indicators['env_file_exists'] and indicators['decouple_installed']:
            if not indicators['django_reads_env']:
                self.stdout.write("   ❌ PROBLEM: .env file exists but Django doesn't read it")
                self.stdout.write("   💡 Check if decouple is properly configured in settings.py")
            elif not indicators['values_match']:
                self.stdout.write("   ❌ PROBLEM: Django reads .env but values don't match")
                self.stdout.write("   💡 Check if settings.py uses config() correctly")
        else:
            self.stdout.write("   ❌ PROBLEM: Basic requirements not met")
            
        # Final recommendations
        self.stdout.write("\n💡 RECOMMENDATIONS:")
        self.stdout.write("   1. Ensure .env file is in project root (same level as manage.py)")
        self.stdout.write("   2. Verify settings.py imports: from decouple import config")
        self.stdout.write("   3. Check settings.py uses: VARIABLE = config('VARIABLE')")
        self.stdout.write("   4. Restart Django server after .env changes")
        self.stdout.write("   5. Check file permissions on .env file")

    def handle(self, *args, **options):
        self.stdout.write("🔍 Testing .env File Loading...")
        
        self.test_direct_vs_env()
        self.test_decouple_vs_django()
        self.test_unique_variable()
        self.test_env_modification()
        self.comprehensive_diagnosis()