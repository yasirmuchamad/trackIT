from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail.backends.smtp import EmailBackend
import smtplib

class Command(BaseCommand):
    help = 'Test email with SSL configuration'

    def handle(self, *args, **options):
        print("📧 TEST EMAIL WITH SSL")
        print("=" * 30)
        
        # Print current settings
        print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
        print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        print(f"EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
        print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        
        # Test 1: Direct SMTP with SSL
        print(f"\n🔒 TEST 1: DIRECT SMTP WITH SSL")
        try:
            server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.set_debuglevel(1)
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            
            # Send test message
            from email.mime.text import MIMEText
            msg = MIMEText("Test message with SSL")
            msg['Subject'] = 'SSL Test'
            msg['From'] = settings.EMAIL_HOST_USER
            msg['To'] = 'yasir.bpras@gmail.com'
            
            server.send_message(msg)
            server.quit()
            
            print("✅ Direct SMTP SSL test successful!")
            
        except Exception as e:
            print(f"❌ Direct SMTP SSL test failed: {e}")
        
        # Test 2: Django email with SSL
        print(f"\n📤 TEST 2: DJANGO EMAIL WITH SSL")
        try:
            result = send_mail(
                subject='Django SSL Test',
                message='This is a test email using SSL configuration.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['yasir.bpras@gmail.com'],
                fail_silently=False,
            )
            
            if result == 1:
                print("✅ Django SSL email test successful!")
            else:
                print(f"⚠️ Django SSL email result: {result}")
                
        except Exception as e:
            print(f"❌ Django SSL email test failed: {e}")
            
        print("\n✨ SSL test completed")