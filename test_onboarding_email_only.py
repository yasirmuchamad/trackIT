#!/usr/bin/env python
"""
Test onboarding email function specifically
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackIT.settings')
django.setup()

from employee.models import EmployeeOnboarding
from employee.services.onboarding_delivery import send_onboarding_email

def main():
    print("📋 TESTING ONBOARDING EMAIL FUNCTION")
    print("=" * 50)
    
    # Find a test onboarding
    onboarding = EmployeeOnboarding.objects.filter(is_completed=False).first()
    
    if not onboarding:
        print("❌ No test onboarding found")
        print("Create an employee with onboarding first")
        return
    
    employee = onboarding.employee
    print(f"Testing with employee: {employee.name}")
    print(f"Email: {employee.private_mail}")
    print(f"Onboarding token: {onboarding.token}")
    print(f"Expires at: {onboarding.expires_at}")
    
    # Test the onboarding email function
    print(f"\n📤 SENDING ONBOARDING EMAIL...")
    
    try:
        result = send_onboarding_email(onboarding, employee.private_mail)
        
        if result:
            print("✅ ONBOARDING EMAIL SENT SUCCESSFULLY!")
            
            # Show the onboarding link
            from employee.services.onboarding_delivery import build_onboarding_link
            link = build_onboarding_link(onboarding.token)
            print(f"\n🔗 ONBOARDING LINK:")
            print(f"{link}")
            
        else:
            print("❌ ONBOARDING EMAIL FAILED")
            
    except Exception as e:
        print(f"❌ ONBOARDING EMAIL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()