#!/usr/bin/env python
"""
Test .env file loading
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackIT.settings')
django.setup()

from django.conf import settings

def main():
    print("🔍 TESTING .ENV FILE LOADING")
    print("=" * 40)
    
    # Check environment variables directly
    print("📁 ENVIRONMENT VARIABLES:")
    print(f"EMAIL_HOST (env): {os.environ.get('EMAIL_HOST', 'NOT SET')}")
    print(f"EMAIL_PORT (env): {os.environ.get('EMAIL_PORT', 'NOT SET')}")
    print(f"EMAIL_USE_SSL (env): {os.environ.get('EMAIL_USE_SSL', 'NOT SET')}")
    print(f"EMAIL_USE_TLS (env): {os.environ.get('EMAIL_USE_TLS', 'NOT SET')}")
    print(f"PROOF_ENV_LOADED (env): {os.environ.get('PROOF_ENV_LOADED', 'NOT SET')}")
    
    # Check Django settings
    print(f"\n⚙️ DJANGO SETTINGS:")
    print(f"EMAIL_HOST (django): {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT (django): {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_SSL (django): {settings.EMAIL_USE_SSL}")
    print(f"EMAIL_USE_TLS (django): {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_HOST_USER (django): {settings.EMAIL_HOST_USER}")
    print(f"EMAIL_BACKEND (django): {settings.EMAIL_BACKEND}")
    
    # Check if .env file exists and read it directly
    print(f"\n📄 .ENV FILE CONTENT:")
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines, 1):
                if line.strip() and not line.strip().startswith('#'):
                    print(f"Line {i:2d}: {line.strip()}")
    except Exception as e:
        print(f"Error reading .env file: {e}")
    
    # Test if settings match .env
    print(f"\n✅ VERIFICATION:")
    env_host = os.environ.get('EMAIL_HOST', '')
    django_host = settings.EMAIL_HOST
    
    if env_host == django_host:
        print(f"✅ EMAIL_HOST matches: {django_host}")
    else:
        print(f"❌ EMAIL_HOST mismatch:")
        print(f"   ENV: '{env_host}'")
        print(f"   Django: '{django_host}'")
    
    env_port = os.environ.get('EMAIL_PORT', '')
    django_port = str(settings.EMAIL_PORT)
    
    if env_port == django_port:
        print(f"✅ EMAIL_PORT matches: {django_port}")
    else:
        print(f"❌ EMAIL_PORT mismatch:")
        print(f"   ENV: '{env_port}'")
        print(f"   Django: '{django_port}'")

if __name__ == '__main__':
    main()