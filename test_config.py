#!/usr/bin/env python
"""
Quick test script to verify email configuration
Run: python test_config.py
"""

import os
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackIT.settings')

# Add project to path
import sys
sys.path.append(str(BASE_DIR))

django.setup()

from django.conf import settings

print("🔍 Current Email Configuration:")
print(f"Backend: {settings.EMAIL_BACKEND}")
print(f"Host: {settings.EMAIL_HOST}")
print(f"Port: {settings.EMAIL_PORT}")
print(f"TLS: {getattr(settings, 'EMAIL_USE_TLS', False)}")
print(f"SSL: {getattr(settings, 'EMAIL_USE_SSL', False)}")
print(f"User: {settings.EMAIL_HOST_USER}")
print(f"From: {settings.DEFAULT_FROM_EMAIL}")

# Check if using correct 163.com config
if settings.EMAIL_HOST == 'smtphz.qiye.163.com':
    print("✅ Using correct 163.com SMTP server")
else:
    print(f"❌ Wrong SMTP server: {settings.EMAIL_HOST}")

if settings.EMAIL_PORT == 465:
    print("✅ Using correct port for SSL")
else:
    print(f"❌ Wrong port: {settings.EMAIL_PORT}")

if getattr(settings, 'EMAIL_USE_SSL', False):
    print("✅ SSL enabled")
else:
    print("❌ SSL not enabled")

if '@goldenteks.id' in settings.EMAIL_HOST_USER:
    print("✅ Using goldenteks.id email")
else:
    print(f"❌ Wrong email domain: {settings.EMAIL_HOST_USER}")