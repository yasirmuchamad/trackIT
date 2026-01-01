from django.core.management.base import BaseCommand
from employee.models import Employee, EmployeeOnboarding
from employee.services.onboarding_delivery import send_onboarding_links, send_via_fonnte
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Compare debug_fonnte vs resend function behavior'

    def add_arguments(self, parser):
        parser.add_argument(
            '--employee-id',
            type=int,
            help='Employee ID to test',
        )
        parser.add_argument(
            '--phone',
            type=str,
            help='Phone number to test',
        )

    def handle(self, *args, **options):
        employee_id = options.get('employee_id')
        test_phone = options.get('phone', '083838786991')
        
        self.stdout.write("🔍 Comparing debug_fonnte vs resend function...")
        
        # Format phone like debug_fonnte does
        clean_phone = ''.join(filter(str.isdigit, test_phone))
        if clean_phone.startswith('0'):
            clean_phone = '62' + clean_phone[1:]
        elif not clean_phone.startswith('62'):
            clean_phone = '62' + clean_phone
        
        self.stdout.write(f"📱 Phone: {test_phone} → {clean_phone}")
        
        # Test 1: Direct debug_fonnte style call
        self.stdout.write("\n🧪 TEST 1: Direct debug_fonnte style call")
        message = f"🧪 Test 1 - Direct call dari compare script"
        
        try:
            result1 = send_via_fonnte(clean_phone, message)
            if result1:
                self.stdout.write(self.style.SUCCESS("✅ Test 1 SUCCESS"))
            else:
                self.stdout.write(self.style.ERROR("❌ Test 1 FAILED"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Test 1 ERROR: {str(e)}"))
            result1 = False
        
        # Test 2: Using resend function path (if employee exists)
        if employee_id:
            try:
                employee = Employee.objects.get(employee_id=employee_id)
                
                # Get or create onboarding
                try:
                    onboarding = EmployeeOnboarding.objects.get(employee=employee)
                except EmployeeOnboarding.DoesNotExist:
                    onboarding = EmployeeOnboarding.create_for_employee(employee)
                
                self.stdout.write(f"\n🧪 TEST 2: Resend function path for {employee.name}")
                self.stdout.write(f"Employee phone: {employee.phone}")
                self.stdout.write(f"Employee email: {employee.private_mail}")
                
                # Override phone for testing
                original_phone = employee.phone
                employee.phone = test_phone
                
                try:
                    results = send_onboarding_links(
                        onboarding,
                        email=None,  # Skip email for this test
                        phone=employee.phone,
                    )
                    
                    if results['whatsapp']:
                        self.stdout.write(self.style.SUCCESS("✅ Test 2 SUCCESS"))
                    else:
                        self.stdout.write(self.style.ERROR("❌ Test 2 FAILED"))
                        
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"❌ Test 2 ERROR: {str(e)}"))
                finally:
                    # Restore original phone
                    employee.phone = original_phone
                    
            except Employee.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"⚠️ Employee {employee_id} not found, skipping Test 2"))
        else:
            self.stdout.write(self.style.WARNING("⚠️ No employee-id provided, skipping Test 2"))
        
        # Test 3: Check configuration differences
        self.stdout.write("\n🔧 TEST 3: Configuration check")
        
        whatsapp_url = getattr(settings, 'WHATSAPP_SERVICE_URL', '')
        whatsapp_token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', '')
        
        self.stdout.write(f"WHATSAPP_SERVICE_URL: {whatsapp_url}")
        self.stdout.write(f"WHATSAPP_SERVICE_TOKEN: {whatsapp_token[:10]}..." if whatsapp_token else "WHATSAPP_SERVICE_TOKEN: NOT SET")
        
        # Test 4: Check logging configuration
        self.stdout.write("\n📝 TEST 4: Logging check")
        
        # Test logging
        logger.info("Test log message from compare script")
        self.stdout.write("Check logs/onboarding.log for this test message")
        
        # Summary
        self.stdout.write("\n📊 SUMMARY:")
        self.stdout.write("If Test 1 works but Test 2 fails, the issue is in send_onboarding_links function")
        self.stdout.write("If both fail, the issue is in send_via_fonnte function")
        self.stdout.write("If both work, the issue might be in the web interface or employee data")
        
        self.stdout.write("\n💡 NEXT STEPS:")
        self.stdout.write("1. Check the actual employee phone number in database")
        self.stdout.write("2. Check if there are any middleware or authentication issues")
        self.stdout.write("3. Check browser network tab when clicking resend button")
        self.stdout.write("4. Verify the onboarding_id being passed to resend function")