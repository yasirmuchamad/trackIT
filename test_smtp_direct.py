#!/usr/bin/env python
"""
Direct SMTP test without Django
"""
import smtplib
from email.mime.text import MIMEText

def test_smtp_direct():
    print("🔧 DIRECT SMTP TEST")
    print("=" * 30)
    
    # Test configurations
    configs = [
        {
            'name': 'Corporate 163 - SSL 465',
            'host': 'smtphz.qiye.163.com',
            'port': 465,
            'use_ssl': True,
            'use_tls': False
        },
        {
            'name': 'Corporate 163 - TLS 587',
            'host': 'smtphz.qiye.163.com',
            'port': 587,
            'use_ssl': False,
            'use_tls': True
        },
        {
            'name': 'Standard 163 - SSL 465',
            'host': 'applesmtp.163.com',
            'port': 465,
            'use_ssl': True,
            'use_tls': False
        },
        {
            'name': 'Standard 163 - TLS 587',
            'host': 'applesmtp.163.com',
            'port': 587,
            'use_ssl': False,
            'use_tls': True
        }
    ]
    
    username = 'muchamad.yasir@goldenteks.id'
    password = '5jrt7bSpQVb4mJx$'
    
    successful_configs = []
    
    for config in configs:
        print(f"\n🔍 Testing: {config['name']}")
        print(f"   Host: {config['host']}:{config['port']}")
        print(f"   SSL: {config['use_ssl']}, TLS: {config['use_tls']}")
        
        try:
            # Create connection
            if config['use_ssl']:
                server = smtplib.SMTP_SSL(config['host'], config['port'], timeout=10)
            else:
                server = smtplib.SMTP(config['host'], config['port'], timeout=10)
                if config['use_tls']:
                    server.starttls()
            
            # Login
            server.login(username, password)
            
            # Create test message
            msg = MIMEText(f"Test message from {config['name']}")
            msg['Subject'] = f"SMTP Test - {config['name']}"
            msg['From'] = username
            msg['To'] = 'yasir.bpras@gmail.com'
            
            # Send message
            server.send_message(msg)
            server.quit()
            
            print(f"   ✅ SUCCESS!")
            successful_configs.append(config)
            
        except Exception as e:
            print(f"   ❌ FAILED: {e}")
    
    print(f"\n📊 RESULTS:")
    if successful_configs:
        print("✅ SUCCESSFUL CONFIGURATIONS:")
        for config in successful_configs:
            print(f"   • {config['name']}")
            print(f"     Host: {config['host']}, Port: {config['port']}")
            print(f"     SSL: {config['use_ssl']}, TLS: {config['use_tls']}")
        
        # Show recommended .env settings
        best = successful_configs[0]
        print(f"\n💡 RECOMMENDED .ENV SETTINGS:")
        print(f"EMAIL_HOST={best['host']}")
        print(f"EMAIL_PORT={best['port']}")
        print(f"EMAIL_USE_SSL={best['use_ssl']}")
        print(f"EMAIL_USE_TLS={best['use_tls']}")
    else:
        print("❌ NO SUCCESSFUL CONFIGURATIONS")
        print("\n💡 POSSIBLE ISSUES:")
        print("1. Incorrect email credentials")
        print("2. Corporate firewall blocking SMTP")
        print("3. Account requires app-specific password")
        print("4. SMTP servers not accessible from this network")

if __name__ == '__main__':
    test_smtp_direct()