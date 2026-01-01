from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Debug Django settings and environment variables'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Debugging Django Settings and Environment...")
        
        # Check environment variables directly
        self.stdout.write("\n📋 Environment Variables (.env):")
        env_vars = [
            'WHATSAPP_SERVICE_URL',
            'WHATSAPP_SERVICE_TOKEN',
            'EMAIL_HOST',
            'EMAIL_PORT',
            'EMAIL_HOST_USER',
            'EMAIL_HOST_PASSWORD',
        ]
        
        for var in env_vars:
            value = os.environ.get(var, 'NOT SET')
            if 'PASSWORD' in var or 'TOKEN' in var:
                display_value = value[:10] + '...' if value != 'NOT SET' else 'NOT SET'
            else:
                display_value = value
            self.stdout.write(f"   {var}: {display_value}")
        
        # Check Django settings
        self.stdout.write("\n⚙️ Django Settings:")
        django_settings = [
            ('WHATSAPP_SERVICE_URL', ''),
            ('WHATSAPP_SERVICE_TOKEN', ''),
            ('EMAIL_HOST', 'localhost'),
            ('EMAIL_PORT', 25),
            ('EMAIL_HOST_USER', ''),
            ('EMAIL_HOST_PASSWORD', ''),
        ]
        
        for setting_name, default in django_settings:
            value = getattr(settings, setting_name, default)
            if 'PASSWORD' in setting_name or 'TOKEN' in setting_name:
                display_value = str(value)[:10] + '...' if value else 'NOT SET'
            else:
                display_value = value
            self.stdout.write(f"   {setting_name}: {display_value}")
        
        # Check if .env file exists
        self.stdout.write("\n📁 File System Check:")
        env_file_path = '.env'
        if os.path.exists(env_file_path):
            self.stdout.write(f"   ✅ .env file exists: {os.path.abspath(env_file_path)}")
            
            # Read .env file content
            try:
                with open(env_file_path, 'r') as f:
                    content = f.read()
                    lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
                    self.stdout.write(f"   📄 .env file has {len(lines)} configuration lines")
                    
                    # Show WhatsApp related lines
                    whatsapp_lines = [line for line in lines if 'WHATSAPP' in line]
                    if whatsapp_lines:
                        self.stdout.write("   📱 WhatsApp configurations in .env:")
                        for line in whatsapp_lines:
                            if 'TOKEN' in line:
                                key, value = line.split('=', 1)
                                self.stdout.write(f"      {key}={value[:10]}...")
                            else:
                                self.stdout.write(f"      {line}")
                    else:
                        self.stdout.write("   ⚠️ No WhatsApp configurations found in .env")
                        
            except Exception as e:
                self.stdout.write(f"   ❌ Error reading .env file: {str(e)}")
        else:
            self.stdout.write(f"   ❌ .env file not found: {os.path.abspath(env_file_path)}")
        
        # Check django-environ or python-decouple
        self.stdout.write("\n🔧 Configuration Library Check:")
        try:
            import environ
            self.stdout.write("   ✅ django-environ is installed")
        except ImportError:
            self.stdout.write("   ❌ django-environ not found")
        
        try:
            import decouple
            self.stdout.write("   ✅ python-decouple is installed")
        except ImportError:
            self.stdout.write("   ❌ python-decouple not found")
        
        # Test direct comparison
        self.stdout.write("\n🧪 Direct Comparison Test:")
        
        # Method 1: Direct os.environ
        env_url = os.environ.get('WHATSAPP_SERVICE_URL', 'NOT_FOUND')
        env_token = os.environ.get('WHATSAPP_SERVICE_TOKEN', 'NOT_FOUND')
        
        # Method 2: Django settings
        django_url = getattr(settings, 'WHATSAPP_SERVICE_URL', 'NOT_FOUND')
        django_token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', 'NOT_FOUND')
        
        self.stdout.write(f"   Environment URL: {env_url}")
        self.stdout.write(f"   Django URL: {django_url}")
        self.stdout.write(f"   Match: {'✅' if env_url == django_url else '❌'}")
        
        self.stdout.write(f"   Environment Token: {env_token[:10]}..." if env_token != 'NOT_FOUND' else "   Environment Token: NOT_FOUND")
        self.stdout.write(f"   Django Token: {django_token[:10]}..." if django_token != 'NOT_FOUND' else "   Django Token: NOT_FOUND")
        self.stdout.write(f"   Match: {'✅' if env_token == django_token else '❌'}")
        
        # Diagnosis
        self.stdout.write("\n🎯 DIAGNOSIS:")
        
        if env_url == 'NOT_FOUND' and django_url == 'NOT_FOUND':
            self.stdout.write("   ❌ WhatsApp URL not found in environment OR Django settings")
            self.stdout.write("   → Check .env file and settings.py configuration")
        elif env_url != 'NOT_FOUND' and django_url == 'NOT_FOUND':
            self.stdout.write("   ❌ WhatsApp URL found in environment but NOT in Django settings")
            self.stdout.write("   → Check settings.py - missing WHATSAPP_SERVICE_URL = config('WHATSAPP_SERVICE_URL')")
        elif env_url == 'NOT_FOUND' and django_url != 'NOT_FOUND':
            self.stdout.write("   ❌ WhatsApp URL found in Django settings but NOT in environment")
            self.stdout.write("   → Check .env file - missing WHATSAPP_SERVICE_URL=...")
        else:
            self.stdout.write("   ✅ WhatsApp URL found in both environment and Django settings")
        
        self.stdout.write("\n💡 RECOMMENDATIONS:")
        self.stdout.write("   1. Ensure .env file is in the correct location")
        self.stdout.write("   2. Check settings.py has proper config() calls")
        self.stdout.write("   3. Restart Django server after .env changes")
        self.stdout.write("   4. Verify no typos in variable names")
        self.stdout.write("   5. Check file permissions on .env file")