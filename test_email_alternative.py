#!/usr/bin/env python
"""
Alternative email test script to diagnose SMTP issues
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackIT.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail
from django.core.mail.backends.smtp import EmailBackend
import smtplib
from email.mime.text import MIMEText

def test_direct_smtp():
    """Test SMTP connection directly without Django"""
    print("🔧 TESTING DIRECT SMTP CONNECTION")
    print("=" * 40)
    
    host = 'smtphz.qiye.163.com'
    port = 587
    username = 'muchamad.yasir@goldenteks.id'
    password = '$FdSfa%xMq3ZRj31'
    
    try:
        print(f"Connecting to {host}:{port}...")
        server = smtplib.SMTP(host, port)
        server.set_debuglevel(1)  # Enable debug output
        
        print("Starting TLS...")
        server.starttls()
        
        print("Logging in...")
        server.login(username, password)
        
        print("Creating test message...")
        msg = MIMEText("Test message from direct SMTP")
        msg['Subject'] = 'Direct SMTP Test'
        msg['From'] = username
        msg['To'] = 'yasir.bpras@gmail.com'
        
        print("Sending message...")
        server.send_message(msg)
        
        print("Closing connection...")
        server.quit()
        
        print("✅ Direct SMTP test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Direct SMTP test failed: {e}")
        return False

def test_django_email():
    """Test Django email configuration"""
    print("\n📧 TESTING DJANGO EMAIL")
    print("=" * 40)
    
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    
    try:
        result = send_mail(
            subject='Django Email Test',
            message='This is a test email from Django.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['yasir.bpras@gmail.com'],
            fail_silently=False,
        )
        
        if result == 1:
            print("✅ Django email test successful!")
            return True
        else:
            print(f"⚠️ Django email returned: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Django email test failed: {e}")
        return False

def test_alternative_config():
    """Test with SSL instead of TLS"""
    print("\n🔒 TESTING ALTERNATIVE CONFIG (SSL)")
    print("=" * 40)
    
    try:
        # Create custom email backend with SSL
        backend = EmailBackend(
            host='smtphz.qiye.163.com',
            port=465,
            username='muchamad.yasir@goldenteks.id',
            password='$FdSfa%xMq3ZRj31',
            use_tls=False,
            use_ssl=True,
            timeout=30,
        )
        
        # Test connection
        backend.open()
        print("✅ SSL connection successful!")
        backend.close()
        
        return True
        
    except Exception as e:
        print(f"❌ SSL test failed: {e}")
        return False

if __name__ == '__main__':
    print("🚀 EMAIL DIAGNOSTIC TOOL")
    print("=" * 50)
    
    # Test 1: Direct SMTP
    test1 = test_direct_smtp()
    
    # Test 2: Django Email
    test2 = test_django_email()
    
    # Test 3: Alternative Config
    test3 = test_alternative_config()
    
    print(f"\n📊 RESULTS SUMMARY:")
    print(f"Direct SMTP (TLS): {'✅' if test1 else '❌'}")
    print(f"Django Email: {'✅' if test2 else '❌'}")
    print(f"Alternative (SSL): {'✅' if test3 else '❌'}")
    
    if not any([test1, test2, test3]):
        print(f"\n💡 TROUBLESHOOTING SUGGESTIONS:")
        print("1. Verify email credentials are correct")
        print("2. Check if corporate firewall blocks SMTP")
        print("3. Try different SMTP server (Gmail, Outlook)")
        print("4. Contact email provider for SMTP settings")
        print("5. Check if account has SMTP access enabled")