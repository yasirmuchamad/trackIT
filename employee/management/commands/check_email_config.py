from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Check current email configuration'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Checking Email Configuration...")
        
        # Check environment variables directly
        self.stdout.write("\n📋 Environment Variables:")
        env_vars = [
            'EMAIL_BACKEND', 'EMAIL_HOST', 'EMAIL_PORT', 
            'EMAIL_USE_TLS', 'EMAIL_USE_SSL', 'EMAIL_HOST_USER', 
            'EMAIL_HOST_PASSWORD', 'DEFAULT_FROM_EMAIL'
        ]
        
        for var in env_vars:
            value = os.environ.get(var, 'NOT SET')
            if 'PASSWORD' in var and value != 'NOT SET':
                value = value[:4] + '*' * (len(value) - 4)
            self.stdout.write(f"  {var}: {value}")
        
        # Check Django settings
        self.stdout.write("\n⚙️ Django Settings:")
        self.stdout.write(f"  EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        self.stdout.write(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
        self.stdout.write(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
        self.stdout.write(f"  EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', False)}")
        self.stdout.write(f"  EMAIL_USE_SSL: {getattr(settings, 'EMAIL_USE_SSL', False)}")
        self.stdout.write(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        
        password = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
        if password:
            masked = password[:4] + '*' * (len(password) - 4)
            self.stdout.write(f"  EMAIL_HOST_PASSWORD: {masked}")
        else:
            self.stdout.write(f"  EMAIL_HOST_PASSWORD: NOT SET")
            
        self.stdout.write(f"  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        
        # Validation
        self.stdout.write("\n✅ Validation:")
        
        if settings.EMAIL_HOST == 'smtphz.qiye.163.com':
            self.stdout.write(self.style.SUCCESS("  ✅ Correct 163.com SMTP server"))
        else:
            self.stdout.write(self.style.ERROR(f"  ❌ Wrong SMTP server: {settings.EMAIL_HOST}"))
            
        if settings.EMAIL_PORT == 465:
            self.stdout.write(self.style.SUCCESS("  ✅ Correct port for SSL (465)"))
        elif settings.EMAIL_PORT == 587:
            self.stdout.write(self.style.WARNING("  ⚠️ Port 587 (should use TLS, not SSL)"))
        else:
            self.stdout.write(self.style.ERROR(f"  ❌ Unexpected port: {settings.EMAIL_PORT}"))
            
        if getattr(settings, 'EMAIL_USE_SSL', False) and settings.EMAIL_PORT == 465:
            self.stdout.write(self.style.SUCCESS("  ✅ SSL enabled for port 465"))
        elif getattr(settings, 'EMAIL_USE_TLS', False) and settings.EMAIL_PORT == 587:
            self.stdout.write(self.style.SUCCESS("  ✅ TLS enabled for port 587"))
        else:
            self.stdout.write(self.style.ERROR("  ❌ SSL/TLS configuration mismatch"))
            
        if '@goldenteks.id' in settings.EMAIL_HOST_USER:
            self.stdout.write(self.style.SUCCESS("  ✅ Using goldenteks.id email"))
        else:
            self.stdout.write(self.style.ERROR(f"  ❌ Wrong email domain: {settings.EMAIL_HOST_USER}"))
            
        if settings.EMAIL_HOST_PASSWORD:
            self.stdout.write(self.style.SUCCESS("  ✅ Password is set"))
        else:
            self.stdout.write(self.style.ERROR("  ❌ Password not set"))
            
        # Recommendations
        self.stdout.write("\n💡 Recommendations:")
        if settings.EMAIL_HOST != 'smtphz.qiye.163.com':
            self.stdout.write("  - Update EMAIL_HOST in .env file")
        if settings.EMAIL_PORT != 465:
            self.stdout.write("  - Update EMAIL_PORT to 465 in .env file")
        if not getattr(settings, 'EMAIL_USE_SSL', False):
            self.stdout.write("  - Set EMAIL_USE_SSL=True in .env file")
        if not settings.EMAIL_HOST_PASSWORD:
            self.stdout.write("  - Set EMAIL_HOST_PASSWORD in .env file")
            
        self.stdout.write("\n🔄 After making changes:")
        self.stdout.write("  1. Restart Django server")
        self.stdout.write("  2. Run: python manage.py test_email --to your-email@example.com")