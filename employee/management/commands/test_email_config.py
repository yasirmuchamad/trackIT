from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import get_connection

class Command(BaseCommand):
    help = 'Test email configuration'

    def handle(self, *args, **options):
        print("📧 TEST EMAIL CONFIGURATION")
        print("=" * 40)
        
        # Check email settings
        print("🔧 EMAIL SETTINGS:")
        print(f"   EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
        print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
        print(f"   EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        print(f"   EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
        print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        print(f"   EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
        print(f"   DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        
        # Test connection
        print(f"\n🔗 TEST EMAIL CONNECTION:")
        try:
            connection = get_connection()
            connection.open()
            print("   ✅ Email connection successful")
            connection.close()
        except Exception as e:
            print(f"   ❌ Email connection failed: {e}")
            return
        
        # Test sending email
        print(f"\n📤 TEST SENDING EMAIL:")
        try:
            result = send_mail(
                subject='Test Email from trackIT',
                message='This is a test email to verify email configuration.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['yasir.bpras@gmail.com'],  # Test email
                fail_silently=False,
            )
            
            if result:
                print("   ✅ Email sent successfully")
            else:
                print("   ❌ Email sending failed (no exception but result is 0)")
                
        except Exception as e:
            print(f"   ❌ Email sending failed: {e}")
            import traceback
            traceback.print_exc()
        
        # Test onboarding email function
        print(f"\n📋 TEST ONBOARDING EMAIL FUNCTION:")
        try:
            from employee.services.onboarding_delivery import send_onboarding_email
            from employee.models import EmployeeOnboarding
            
            # Find a test onboarding
            onboarding = EmployeeOnboarding.objects.filter(is_completed=False).first()
            
            if onboarding:
                print(f"   Testing with: {onboarding.employee.name}")
                print(f"   Email: {onboarding.employee.private_mail}")
                
                result = send_onboarding_email(onboarding, onboarding.employee.private_mail)
                
                if result:
                    print("   ✅ Onboarding email function successful")
                else:
                    print("   ❌ Onboarding email function failed")
            else:
                print("   ⚠️ No test onboarding found")
                
        except Exception as e:
            print(f"   ❌ Onboarding email function error: {e}")
            import traceback
            traceback.print_exc()
        
        print(f"\n💡 TROUBLESHOOTING:")
        print("1. Check if EMAIL_BACKEND is set to SMTP backend")
        print("2. Verify email credentials are correct")
        print("3. Check if SMTP server allows connections")
        print("4. Test with different email provider if needed")
        print("5. Check firewall/antivirus blocking SMTP connections")