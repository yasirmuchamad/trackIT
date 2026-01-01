#!/usr/bin/env python
"""
Simple WhatsApp test script to verify Fonnte configuration
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackIT.settings')
django.setup()

from django.conf import settings
from employee.services.onboarding_delivery import send_via_fonnte

def test_whatsapp_config():
    """Test WhatsApp configuration"""
    print("🔍 Testing WhatsApp Configuration...")
    
    # Check settings
    whatsapp_url = getattr(settings, 'WHATSAPP_SERVICE_URL', '')
    whatsapp_token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', '')
    
    print(f"URL: {whatsapp_url}")
    print(f"Token: {whatsapp_token[:10]}..." if whatsapp_token else "Token: NOT SET")
    
    if not whatsapp_url or not whatsapp_token:
        print("❌ WhatsApp configuration missing!")
        return False
    
    # Test with a simple message
    test_phone = "6283838786991"  # From logs
    test_message = "🧪 Test dari TrackIT - Konfigurasi WhatsApp berhasil!"
    
    print(f"\n📤 Sending test message to {test_phone}...")
    
    try:
        result = send_via_fonnte(test_phone, test_message)
        
        if result:
            print("✅ WhatsApp test successful!")
            print("💡 If you don't receive the message, check:")
            print("   - Phone is registered in WhatsApp")
            print("   - Phone has internet connection")
            print("   - Check spam/blocked messages")
            print("   - Fonnte account balance")
        else:
            print("❌ WhatsApp test failed!")
            
        return result
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_whatsapp_config()