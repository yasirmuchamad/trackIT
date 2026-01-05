#!/usr/bin/env python
"""
Complete onboarding test - both email and WhatsApp
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackIT.settings')
django.setup()

from employee.models import EmployeeOnboarding
from employee.services.onboarding_delivery import send_onboarding_links

def test_complete_onboarding():
    """Test complete onboarding flow"""
    print("🚀 COMPLETE ONBOARDING TEST")
    print("=" * 50)
    
    # Find a test onboarding
    onboarding = EmployeeOnboarding.objects.filter(is_completed=False).first()
    
    if not onboarding:
        print("❌ No test onboarding found")
        return
    
    employee = onboarding.employee
    print(f"Testing with employee: {employee.name}")
    print(f"Email: {employee.private_mail}")
    print(f"Phone: {employee.phone}")
    print(f"Onboarding token: {onboarding.token}")
    print(f"Expires at: {onboarding.expires_at}")
    
    # Test the complete flow
    print(f"\n📤 SENDING ONBOARDING LINKS...")
    
    results = send_onboarding_links(
        onboarding=onboarding,
        email=employee.private_mail,
        phone=employee.phone
    )
    
    print(f"\n📊 RESULTS:")
    print(f"Email: {'✅ Success' if results['email'] else '❌ Failed'}")
    print(f"WhatsApp: {'✅ Success' if results['whatsapp'] else '❌ Failed'}")
    
    # Show onboarding link
    from employee.services.onboarding_delivery import build_onboarding_link
    link = build_onboarding_link(onboarding.token)
    print(f"\n🔗 ONBOARDING LINK:")
    print(f"{link}")
    
    return results

if __name__ == '__main__':
    test_complete_onboarding()