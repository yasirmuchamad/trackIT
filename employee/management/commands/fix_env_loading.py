from django.core.management.base import BaseCommand
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Fix .env loading issues'

    def handle(self, *args, **options):
        self.stdout.write("🛠️ Fixing .env Loading Issues...")
        
        # Step 1: Locate .env file
        self.stdout.write("\n📁 Step 1: Locating .env file")
        
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        env_path = BASE_DIR / '.env'
        
        self.stdout.write(f"   Looking for .env at: {env_path}")
        
        if not env_path.exists():
            self.stdout.write("   ❌ .env file not found!")
            self.stdout.write("   💡 Creating .env file from template...")
            
            # Create .env from template
            env_template = """# Development Environment Variables
# This file should NOT be committed to Git

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtphz.qiye.163.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=muchamad.yasir@goldenteks.id
EMAIL_HOST_PASSWORD=$FdSfa%xMq3ZRj31
DEFAULT_FROM_EMAIL=muchamad.yasir@goldenteks.id

# Frontend URL
FRONT_END_BASE_URL=http://localhost:8000

# WhatsApp Configuration - Fonnte.com
WHATSAPP_SERVICE_URL=https://api.fonnte.com/send
WHATSAPP_SERVICE_TOKEN=urWuiF1pMJyGM25uJEjA
"""
            
            with open(env_path, 'w') as f:
                f.write(env_template)
            
            self.stdout.write("   ✅ Created .env file")
        else:
            self.stdout.write("   ✅ .env file found")
        
        # Step 2: Check file permissions
        self.stdout.write("\n🔐 Step 2: Checking file permissions")
        
        if os.access(env_path, os.R_OK):
            self.stdout.write("   ✅ .env file is readable")
        else:
            self.stdout.write("   ❌ .env file is not readable")
            self.stdout.write("   💡 Fixing permissions...")
            os.chmod(env_path, 0o644)
            self.stdout.write("   ✅ Fixed permissions")
        
        # Step 3: Test direct loading
        self.stdout.write("\n📖 Step 3: Testing direct loading")
        
        env_vars = {}
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        try:
                            key, value = line.split('=', 1)
                            env_vars[key] = value
                            # Set in OS environment for immediate use
                            os.environ[key] = value
                        except ValueError:
                            self.stdout.write(f"   ⚠️ Skipping malformed line {line_num}: {line}")
            
            self.stdout.write(f"   ✅ Loaded {len(env_vars)} variables into environment")
            
            # Show WhatsApp config
            if 'WHATSAPP_SERVICE_URL' in env_vars:
                self.stdout.write(f"   📱 WHATSAPP_SERVICE_URL: {env_vars['WHATSAPP_SERVICE_URL']}")
            if 'WHATSAPP_SERVICE_TOKEN' in env_vars:
                self.stdout.write(f"   📱 WHATSAPP_SERVICE_TOKEN: {env_vars['WHATSAPP_SERVICE_TOKEN'][:10]}...")
                
        except Exception as e:
            self.stdout.write(f"   ❌ Error loading .env: {str(e)}")
        
        # Step 4: Update settings.py for manual loading
        self.stdout.write("\n⚙️ Step 4: Creating manual .env loader")
        
        manual_loader = '''
# Manual .env loader (add to settings.py if decouple fails)
import os
from pathlib import Path

def load_env_manual():
    """Manually load .env file if decouple fails"""
    BASE_DIR = Path(__file__).resolve().parent.parent
    env_path = BASE_DIR / '.env'
    
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key, value)

# Call the manual loader
load_env_manual()

# Now use os.environ.get() instead of config()
WHATSAPP_SERVICE_URL = os.environ.get('WHATSAPP_SERVICE_URL', 'https://api.fonnte.com/send')
WHATSAPP_SERVICE_TOKEN = os.environ.get('WHATSAPP_SERVICE_TOKEN', 'urWuiF1pMJyGM25uJEjA')
'''
        
        self.stdout.write("   💡 Manual loader code created (see below)")
        
        # Step 5: Test current state
        self.stdout.write("\n🧪 Step 5: Testing current state")
        
        # Test if variables are now in environment
        url_test = os.environ.get('WHATSAPP_SERVICE_URL', 'NOT_FOUND')
        token_test = os.environ.get('WHATSAPP_SERVICE_TOKEN', 'NOT_FOUND')
        
        if url_test != 'NOT_FOUND':
            self.stdout.write(f"   ✅ WHATSAPP_SERVICE_URL now in environment: {url_test}")
        else:
            self.stdout.write("   ❌ WHATSAPP_SERVICE_URL still not in environment")
            
        if token_test != 'NOT_FOUND':
            self.stdout.write(f"   ✅ WHATSAPP_SERVICE_TOKEN now in environment: {token_test[:10]}...")
        else:
            self.stdout.write("   ❌ WHATSAPP_SERVICE_TOKEN still not in environment")
        
        # Final instructions
        self.stdout.write("\n📋 FINAL INSTRUCTIONS:")
        
        if url_test != 'NOT_FOUND' and token_test != 'NOT_FOUND':
            self.stdout.write("   ✅ Environment variables are now loaded!")
            self.stdout.write("   🔄 Restart Django server to apply changes")
            self.stdout.write("   🧪 Test with: python manage.py test_exact_onboarding_flow")
        else:
            self.stdout.write("   ❌ Manual loading didn't work")
            self.stdout.write("   💡 Try the manual loader code in settings.py:")
            self.stdout.write("\n" + manual_loader)
        
        self.stdout.write("\n🎯 REMEMBER:")
        self.stdout.write("   • Replace 'urWuiF1pMJyGM25uJEjA' with real Fonnte token")
        self.stdout.write("   • Restart Django server after any changes")
        self.stdout.write("   • Check Fonnte dashboard for message history")