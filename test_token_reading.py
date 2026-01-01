#!/usr/bin/env python
"""
Test script to verify token reading from .env file
Run this from the trackIT directory: python test_token_reading.py
"""

import os
import sys

# Add Django project to path
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackIT.settings')

import django
django.setup()

from django.conf import settings

print("🔍 TEST PEMBACAAN TOKEN DARI .ENV")
print("=" * 50)

# 1. Check .env file directly
print("1️⃣ Baca file .env langsung:")
try:
    with open('.env', 'r') as f:
        for line_num, line in enumerate(f, 1):
            if 'WHATSAPP_SERVICE_TOKEN' in line:
                print(f"   Line {line_num}: {line.strip()}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 2. Check OS environment
print("\n2️⃣ OS Environment:")
os_token = os.environ.get('WHATSAPP_SERVICE_TOKEN', 'NOT_FOUND')
print(f"   {os_token}")

# 3. Check Django settings
print("\n3️⃣ Django Settings:")
django_token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', 'NOT_IN_SETTINGS')
django_url = getattr(settings, 'WHATSAPP_SERVICE_URL', 'NOT_IN_SETTINGS')
print(f"   URL: {django_url}")
print(f"   Token: {django_token}")

# 4. Test decouple directly
print("\n4️⃣ Test decouple langsung:")
try:
    from decouple import config
    decouple_token = config('WHATSAPP_SERVICE_TOKEN', default='DECOUPLE_FAILED')
    print(f"   Decouple: {decouple_token}")
except Exception as e:
    print(f"   ❌ Decouple error: {e}")

# 5. Manual .env parsing
print("\n5️⃣ Manual parsing .env:")
try:
    with open('.env', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                if key == 'WHATSAPP_SERVICE_TOKEN':
                    print(f"   Manual parse: {value}")
                    break
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n🎯 DIAGNOSIS:")
if django_token and django_token != 'NOT_IN_SETTINGS':
    print("✅ Token berhasil dibaca oleh Django")
    if django_token == 'urWuiF1pMJyGM25uJEjA':
        print("✅ Token sesuai dengan yang ada di .env")
        print("💡 Masalah bukan di pembacaan token")
        print("💡 Kemungkinan masalah di device Fonnte atau API")
    else:
        print("⚠️ Token berbeda dari yang diharapkan")
else:
    print("❌ Token tidak terbaca oleh Django")
    print("💡 Masalah di konfigurasi .env atau settings.py")