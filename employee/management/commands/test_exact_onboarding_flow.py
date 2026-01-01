from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from employee.models import Employee, EmployeeOnboarding
from employee.services.onboarding_delivery import send_onboarding_links
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Test the EXACT onboarding flow that web interface uses'

    def add_arguments(self, parser):
        parser.add_argument(
            '--employee-id',
            type=int,
            help='Employee ID to test',
        )
        parser.add_argument(
            '--onboarding-id',
            type=int,
            help='Onboarding ID to test (like web interface)',
        )

    def handle(self, *args, **options):
        employee_id = options.get('employee_id')
        onboarding_id = options.get('onboarding_id')
        
        self.stdout.write("🎯 Testing EXACT onboarding flow...")
        
        # Method 1: Using onboarding_id (exactly like web interface)
        if onboarding_id:
            self.test_with_onboarding_id(onboarding_id)
        
        # Method 2: Using employee_id
        elif employee_id:
            self.test_with_employee_id(employee_id)
        
        # Method 3: Find any available onboarding
        else:
            self.test_with_any_onboarding()

    def test_with_onboarding_id(self, onboarding_id):
        """Test using onboarding ID - EXACTLY like web interface"""
        self.stdout.write(f"\n🔍 Method 1: Using onboarding_id {onboarding_id} (like web interface)")
        
        try:
            # This is EXACTLY what resend_onboarding view does
            onboarding = get_object_or_404(EmployeeOnboarding, id=onboarding_id)
            
            self.stdout.write(f"✅ Found onboarding for: {onboarding.employee.name}")
            self.stdout.write(f"📧 Email: {onboarding.employee.private_mail}")
            self.stdout.write(f"📱 Phone: {onboarding.employee.phone}")
            self.stdout.write(f"🎫 Token: {onboarding.token}")
            self.stdout.write(f"⏰ Expires: {onboarding.expires_at}")
            self.stdout.write(f"✅ Completed: {onboarding.is_completed}")
            
            # EXACT same call as resend_onboarding view
            self.stdout.write("\n📤 Calling send_onboarding_links (EXACT same as web interface)...")
            
            results = send_onboarding_links(
                onboarding,
                email=onboarding.employee.private_mail,
                phone=onboarding.employee.phone,
            )
            
            self.stdout.write(f"📊 Results: {results}")
            
            # Same success/error logic as web interface
            success_messages = []
            error_messages = []
            
            if onboarding.employee.private_mail:
                if results['email']:
                    success_messages.append(f"email sent to {onboarding.employee.private_mail}")
                else:
                    error_messages.append(f"failed to send email to {onboarding.employee.private_mail}")
            
            if onboarding.employee.phone:
                if results['whatsapp']:
                    success_messages.append(f"WhatsApp sent to {onboarding.employee.phone}")
                else:
                    error_messages.append(f"failed to send WhatsApp to {onboarding.employee.phone}")
            
            if success_messages:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ SUCCESS: {', '.join(success_messages)}"
                    )
                )
            
            if error_messages:
                self.stdout.write(
                    self.style.ERROR(
                        f"❌ ERRORS: {', '.join(error_messages)}"
                    )
                )
            
            if not success_messages and not error_messages:
                self.stdout.write(
                    self.style.WARNING(
                        f"⚠️ WARNING: No contact information available"
                    )
                )
            
            # Show recent delivery records
            self.show_delivery_records(onboarding)
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Exception: {str(e)}"))
            logger.error(f"Exception in test_with_onboarding_id: {str(e)}", exc_info=True)

    def test_with_employee_id(self, employee_id):
        """Test using employee ID"""
        self.stdout.write(f"\n🔍 Method 2: Using employee_id {employee_id}")
        
        try:
            employee = Employee.objects.get(employee_id=employee_id)
            
            # Get or create onboarding
            try:
                onboarding = EmployeeOnboarding.objects.get(employee=employee)
                self.stdout.write(f"✅ Found existing onboarding: {onboarding.id}")
            except EmployeeOnboarding.DoesNotExist:
                onboarding = EmployeeOnboarding.create_for_employee(employee)
                self.stdout.write(f"✅ Created new onboarding: {onboarding.id}")
            
            # Now test with onboarding_id
            self.test_with_onboarding_id(onboarding.id)
            
        except Employee.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"❌ Employee {employee_id} not found"))

    def test_with_any_onboarding(self):
        """Test with any available onboarding"""
        self.stdout.write(f"\n🔍 Method 3: Using any available onboarding")
        
        onboarding = EmployeeOnboarding.objects.filter(
            is_completed=False
        ).first()
        
        if onboarding:
            self.stdout.write(f"✅ Found onboarding: {onboarding.id}")
            self.test_with_onboarding_id(onboarding.id)
        else:
            self.stdout.write(self.style.ERROR("❌ No incomplete onboarding records found"))
            
            # Create one for testing
            employee = Employee.objects.first()
            if employee:
                onboarding = EmployeeOnboarding.create_for_employee(employee)
                self.stdout.write(f"✅ Created test onboarding: {onboarding.id}")
                self.test_with_onboarding_id(onboarding.id)
            else:
                self.stdout.write(self.style.ERROR("❌ No employees found to create onboarding"))

    def show_delivery_records(self, onboarding):
        """Show recent delivery records"""
        self.stdout.write("\n📋 Recent Delivery Records:")
        
        deliveries = onboarding.deliveries.all().order_by('-sent_at')[:5]
        
        if deliveries:
            for delivery in deliveries:
                status = '✅' if delivery.is_success else '❌'
                self.stdout.write(
                    f'{status} {delivery.channel.upper()} to {delivery.destination} '
                    f'at {delivery.sent_at.strftime("%Y-%m-%d %H:%M:%S")}'
                )
                if not delivery.is_success and delivery.error_message:
                    self.stdout.write(f'   Error: {delivery.error_message}')
        else:
            self.stdout.write("   No delivery records found")
        
        self.stdout.write("\n💡 IMPORTANT:")
        self.stdout.write("   • This command does EXACTLY what the web interface does")
        self.stdout.write("   • If this works but web interface doesn't, the issue is in:")
        self.stdout.write("     - Browser/JavaScript")
        self.stdout.write("     - CSRF token")
        self.stdout.write("     - Session/authentication")
        self.stdout.write("     - Middleware")
        self.stdout.write("   • If this fails too, the issue is in the onboarding system itself")
        
        self.stdout.write("\n🔍 Next steps if this works but web doesn't:")
        self.stdout.write("   1. Check browser Developer Tools → Network tab")
        self.stdout.write("   2. Check for JavaScript errors in Console")
        self.stdout.write("   3. Verify CSRF token in form")
        self.stdout.write("   4. Check Django logs for web requests")
        self.stdout.write("   5. Test with different browser/incognito mode")