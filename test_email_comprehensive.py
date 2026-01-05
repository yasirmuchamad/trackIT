#!/usr/bin/env python
"""
Comprehensive email test with multiple configurations
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackIT.settings')
django.setup()

import smtplib
from email.mime.text import MIMEText
from django.core.mail import send_mail
from django.core.mail.backends.smtp import EmailBackend

def test_smtp_config(host, port, use_ssl, use_tls, username, password, description):
    """Test a specific SMTP configuration"""
    print(f"\n🔧 TESTING: {description}")
    print(f"   Host: {host}:{port}")
    print(f"   SSL: {use_ssl}, TLS: {use_tls}")
    print(f"   User: {username}")
    
    try:
        if use_ssl:
            # Use SMTP_SSL for port 465
            server = smtplib.SMTP_SSL(host, port, timeout=30)
        else:
            # Use regular SMTP for port 587
            server = smtplib.SMTP(host, port, timeout=30)
            if use_tls:
                server.starttls()
        
        server.set_debuglevel(0)  # Disable debug for cleaner output
        server.login(username, password)
        
        # Create test message
        msg = MIMEText(f"Test from {description}")
        msg['Subject'] = f'SMTP Test - {description}'
        msg['From'] = username
        msg['To'] = 'yasir.bpras@gmail.com'
        
        # Send message
        server.send_message(msg)
        server.quit()
        
        print(f"   ✅ SUCCESS: {description}")
        return True
        
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        return False

def test_django_email_config(host, port, use_ssl, use_tls, username, password, description):
    """Test Django email with specific configuration"""
    print(f"\n📧 DJANGO TEST: {description}")
    
    try:
        # Create custom backend
        backend = EmailBackend(
            host=host,
            port=port,
            username=username,
            password=password,
            use_tls=use_tls,
            use_ssl=use_ssl,
            timeout=30,
        )
        
        # Test connection
        backend.open()
        backend.close()
        
        print(f"   ✅ Django connection successful: {description}")
        return True
        
    except Exception as e:
        print(f"   ❌ Django failed: {e}")
        return False

def main():
    print("🚀 COMPREHENSIVE EMAIL TEST")
    print("=" * 60)
    
    username = 'muchamad.yasir@goldenteks.id'
    password = '5jrt7bSpQVb4mJx$'
    
    # Test configurations
    configs = [
        # Corporate 163.com server configurations
        ('smtphz.qiye.163.com', 465, True, False, 'Corporate 163 - SSL 465'),
        ('smtphz.qiye.163.com', 587, False, True, 'Corporate 163 - TLS 587'),
        ('smtphz.qiye.163.com', 25, False, False, 'Corporate 163 - Plain 25'),
        
        # Standard 163.com server configurations
        ('applesmtp.163.com', 465, True, False, 'Standard 163 - SSL 465'),
        ('applesmtp.163.com', 587, False, True, 'Standard 163 - TLS 587'),
        
        # Alternative 163.com servers
        ('smtp.163.com', 465, True, False, 'Alt 163 - SSL 465'),
        ('smtp.163.com', 587, False, True, 'Alt 163 - TLS 587'),
    ]
    
    successful_configs = []
    
    for host, port, use_ssl, use_tls, description in configs:
        # Test direct SMTP
        if test_smtp_config(host, port, use_ssl, use_tls, username, password, description):
            successful_configs.append((host, port, use_ssl, use_tls, description))
            
            # Also test Django backend for successful configs
            test_django_email_config(host, port, use_ssl, use_tls, username, password, description)
    
    print(f"\n📊 RESULTS SUMMARY")
    print("=" * 60)
    
    if successful_configs:
        print("✅ SUCCESSFUL CONFIGURATIONS:")
        for host, port, use_ssl, use_tls, description in successful_configs:
            print(f"   • {description}")
            print(f"     Host: {host}, Port: {port}, SSL: {use_ssl}, TLS: {use_tls}")
        
        # Recommend the best configuration
        best_config = successful_configs[0]
        print(f"\n💡 RECOMMENDED CONFIGURATION:")
        print(f"   EMAIL_HOST={best_config[0]}")
        print(f"   EMAIL_PORT={best_config[1]}")
        print(f"   EMAIL_USE_SSL={best_config[2]}")
        print(f"   EMAIL_USE_TLS={best_config[3]}")
        
    else:
        print("❌ NO SUCCESSFUL CONFIGURATIONS FOUND")
        print("\n💡 TROUBLESHOOTING SUGGESTIONS:")
        print("1. Verify email credentials are correct")
        print("2. Check if corporate firewall blocks SMTP")
        print("3. Contact IT admin for correct SMTP settings")
        print("4. Try enabling 'Less secure app access' if using Gmail")
        print("5. Check if account requires app-specific password")

if __name__ == '__main__':
    main()