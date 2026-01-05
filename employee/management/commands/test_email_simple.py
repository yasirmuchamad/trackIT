from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.mail import send_mail
import os

class Command(BaseCommand):
    help = 'Simple email test'

    def handle(self, *args, **options):
        print("📧 SIMPLE EMAIL TEST")
        print("=" * 30)
        
        # Print current settings
        print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
        print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        
        # Check .env loading
        print(f"\n🔍 ENV VARIABLES:")
        print(f"EMAIL_BACKEND from env: {os.environ.get('EMAIL_BACKEND', 'NOT SET')}")
        print(f"EMAIL_HOST from env: {os.environ.get('EMAIL_HOST', 'NOT SET')}")
        print(f"EMAIL_HOST_USER from env: {os.environ.get('EMAIL_HOST_USER', 'NOT SET')}")
        
        # Test email
        print(f"\n📤 SENDING TEST EMAIL...")
        try:
            result = send_mail(
                subject='Test Email - trackIT System',
                message='This is a test email to verify SMTP configuration is working.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['yasir.bpras@gmail.com'],
                fail_silently=False,
            )
            
            if result == 1:
                print("✅ Email sent successfully!")
            else:
                print(f"⚠️ Email result: {result}")
                
        except Exception as e:
            print(f"❌ Email failed: {e}")
            
        print("\n✨ Test completed")