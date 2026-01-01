from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from employee.models import Employee, EmployeeOnboarding
from employee.services.onboarding_delivery import send_onboarding_links


class Command(BaseCommand):
    help = 'Test web interface functionality directly'

    def handle(self, *args, **options):
        self.stdout.write("🌐 Testing Web Interface Functionality")
        
        # Find an employee with onboarding
        onboarding = EmployeeOnboarding.objects.filter(is_completed=False).first()
        
        if not onboarding:
            self.stdout.write("❌ No incomplete onboarding found")
            return
        
        employee = onboarding.employee
        
        self.stdout.write(f"\n👤 Testing with employee: {employee.name}")
        self.stdout.write(f"📧 Email: {employee.private_mail}")
        self.stdout.write(f"📱 Phone: {employee.phone}")
        self.stdout.write(f"🎫 Onboarding ID: {onboarding.id}")
        
        # This is EXACTLY what the web interface does
        self.stdout.write("\n🔄 Simulating Web Interface Resend...")
        self.stdout.write("This is exactly what happens when you click resend button:")
        
        try:
            # Exact same call as resend_onboarding view
            results = send_onboarding_links(
                onboarding,
                email=employee.private_mail,
                phone=employee.phone,
            )
            
            self.stdout.write(f"📊 Results: {results}")
            
            # Same logic as web interface
            success_messages = []
            error_messages = []
            
            if employee.private_mail:
                if results['email']:
                    success_messages.append(f"email sent to {employee.private_mail}")
                else:
                    error_messages.append(f"failed to send email to {employee.private_mail}")
            
            if employee.phone:
                if results['whatsapp']:
                    success_messages.append(f"WhatsApp sent to {employee.phone}")
                else:
                    error_messages.append(f"failed to send WhatsApp to {employee.phone}")
            
            if success_messages:
                self.stdout.write(f"✅ SUCCESS: {', '.join(success_messages)}")
            
            if error_messages:
                self.stdout.write(f"❌ ERRORS: {', '.join(error_messages)}")
            
            if not success_messages and not error_messages:
                self.stdout.write("⚠️ WARNING: No contact information available")
            
        except Exception as e:
            self.stdout.write(f"❌ EXCEPTION: {str(e)}")
        
        # Check delivery records
        self.stdout.write("\n📋 Recent Delivery Records:")
        deliveries = onboarding.deliveries.all().order_by('-sent_at')[:3]
        
        for delivery in deliveries:
            status = '✅' if delivery.is_success else '❌'
            self.stdout.write(f"{status} {delivery.channel.upper()} to {delivery.destination} at {delivery.sent_at.strftime('%H:%M:%S')}")
            if not delivery.is_success and delivery.error_message:
                self.stdout.write(f"   Error: {delivery.error_message}")
        
        # Instructions for web testing
        self.stdout.write("\n🌐 WEB INTERFACE TEST:")
        self.stdout.write("Now test the actual web interface:")
        self.stdout.write(f"1. Go to: http://localhost:8000/employees/onboarding/")
        self.stdout.write(f"2. Find employee: {employee.name}")
        self.stdout.write(f"3. Click 'Resend' button for onboarding ID: {onboarding.id}")
        self.stdout.write("4. Check browser Developer Tools → Network tab")
        self.stdout.write("5. Look for any JavaScript errors in Console")
        self.stdout.write("6. Check if HTTP request is sent successfully")
        
        self.stdout.write("\n🔍 DEBUGGING WEB INTERFACE:")
        self.stdout.write("If web interface doesn't work but this command does:")
        self.stdout.write("• Check browser JavaScript console for errors")
        self.stdout.write("• Check browser Network tab for failed requests")
        self.stdout.write("• Check CSRF token in form")
        self.stdout.write("• Try different browser or incognito mode")
        self.stdout.write("• Check Django logs for web requests")
        
        self.stdout.write(f"\n💡 DIRECT URL TEST:")
        self.stdout.write(f"Try this URL directly in browser:")
        self.stdout.write(f"http://localhost:8000/employees/onboarding/{onboarding.id}/resend/")
        self.stdout.write("(This should show a POST form or redirect)")
        
        self.stdout.write("\n🎯 CONCLUSION:")
        if results.get('whatsapp'):
            self.stdout.write("✅ Backend system works perfectly!")
            self.stdout.write("✅ WhatsApp functionality is operational!")
            self.stdout.write("🔍 If web interface doesn't work, it's a frontend issue")
        else:
            self.stdout.write("❌ Backend system has issues")
            self.stdout.write("🔍 Need to debug backend first")