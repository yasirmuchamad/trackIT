#!/usr/bin/env python
"""
Test actual resend functionality with real employee data
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

from employee.models import Employee, EmployeeOnboarding
from employee.services.onboarding_delivery import send_onboarding_links

def test_resend_with_real_data():
    """Test resend with actual employee data"""
    print("🔍 Testing resend with real employee data...")
    
    # Find an employee with onboarding record
    employees_with_onboarding = Employee.objects.filter(
        onboarding_records__isnull=False
    ).distinct()
    
    if not employees_with_onboarding.exists():
        print("❌ No employees with onboarding records found")
        return
    
    employee = employees_with_onboarding.first()
    onboarding = employee.onboarding_records.first()
    
    print(f"👤 Testing with employee: {employee.name}")
    print(f"📧 Email: {employee.private_mail}")
    print(f"📱 Phone: {employee.phone}")
    print(f"🎫 Onboarding token: {onboarding.token}")
    
    # Test with original phone number
    if employee.phone:
        print(f"\n📤 Testing WhatsApp to original phone: {employee.phone}")
        
        results = send_onboarding_links(
            onboarding,
            email=None,  # Skip email
            phone=employee.phone,
        )
        
        if results['whatsapp']:
            print("✅ WhatsApp with original phone: SUCCESS")
        else:
            print("❌ WhatsApp with original phone: FAILED")
    
    # Test with test phone number
    test_phone = "083838786991"
    print(f"\n📤 Testing WhatsApp to test phone: {test_phone}")
    
    results = send_onboarding_links(
        onboarding,
        email=None,  # Skip email
        phone=test_phone,
    )
    
    if results['whatsapp']:
        print("✅ WhatsApp with test phone: SUCCESS")
    else:
        print("❌ WhatsApp with test phone: FAILED")
    
    print("\n💡 Check logs/onboarding.log for detailed logs")
    print("💡 This simulates exactly what the resend button does")

if __name__ == "__main__":
    test_resend_with_real_data()