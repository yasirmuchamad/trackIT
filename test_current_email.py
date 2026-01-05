#!/usr/bin/env python
"""
Test current email configuration
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackIT.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail

def main():
    print("📧 TESTING CURRENT EMAIL CONFIGURATION")
    print("=" * 50)
    
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    print(f"\n📤 SENDING TEST EMAIL...")
    
    try:
        result = send_mail(
            subject='Test Email - Current Configuration',
            message='This is a test email to verify the current SMTP configuration is working.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['yasir.bpras@gmail.com'],
            fail_silently=False,
        )
        
        if result == 1:
            print("✅ EMAIL SENT SUCCESSFULLY!")
            print("The current configuration is working.")
        else:
            print(f"⚠️ Email result: {result}")
            
    except Exception as e:
        print(f"❌ EMAIL FAILED: {e}")
        print(f"Exception type: {type(e).__name__}")
        
        # Provide specific troubleshooting
        if "Connection unexpectedly closed" in str(e):
            print("\n💡 TROUBLESHOOTING:")
            print("1. Try different SMTP server (applesmtp.163.com vs smtphz.qiye.163.com)")
            print("2. Verify email credentials are correct")
            print("3. Check if corporate firewall blocks SMTP")
            print("4. Try port 587 with TLS instead of 465 with SSL")
        elif "Authentication failed" in str(e):
            print("\n💡 TROUBLESHOOTING:")
            print("1. Verify username and password are correct")
            print("2. Check if account requires app-specific password")
        elif "timeout" in str(e).lower():
            print("\n💡 TROUBLESHOOTING:")
            print("1. Check network connectivity")
            print("2. Try different SMTP server")
            print("3. Check firewall settings")

if __name__ == '__main__':
    main()