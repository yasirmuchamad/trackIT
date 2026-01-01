from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from employee.models import Employee, EmployeeOnboarding
from employee.services.onboarding_delivery import send_onboarding_links
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Simulate exactly what the resend button does'

    def add_arguments(self, parser):
        parser.add_argument(
            '--onboarding-id',
            type=int,
            help='Onboarding ID to resend (same as what button uses)',
        )

    def handle(self, *args, **options):
        onboarding_id = options.get('onboarding_id')
        
        if not onboarding_id:
            # Find any onboarding record
            onboarding = EmployeeOnboarding.objects.filter(
                is_completed=False
            ).first()
            
            if not onboarding:
                self.stdout.write(self.style.ERROR('No incomplete onboarding records found'))
                return
                
            onboarding_id = onboarding.id
        else:
            onboarding = get_object_or_404(EmployeeOnboarding, id=onboarding_id)
        
        self.stdout.write(f"🎯 Simulating resend button for onboarding ID: {onboarding_id}")
        self.stdout.write(f"👤 Employee: {onboarding.employee.name}")
        self.stdout.write(f"📧 Email: {onboarding.employee.private_mail}")
        self.stdout.write(f"📱 Phone: {onboarding.employee.phone}")
        
        # This is EXACTLY what the resend button does
        self.stdout.write("\n📤 Calling send_onboarding_links (same as resend button)...")
        
        try:
            # Exact same call as in resend_onboarding view
            results = send_onboarding_links(
                onboarding,
                email=onboarding.employee.private_mail,
                phone=onboarding.employee.phone,
            )
            
            self.stdout.write(f"📊 Results: {results}")
            
            # Same logic as in resend_onboarding view
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
                        f"✅ SUCCESS: Onboarding notifications resent to {onboarding.employee.name}: " + 
                        ", ".join(success_messages) + "."
                    )
                )
            
            if error_messages:
                self.stdout.write(
                    self.style.ERROR(
                        f"❌ ERROR: Failed to resend some notifications to {onboarding.employee.name}: " + 
                        ", ".join(error_messages) + "."
                    )
                )
            
            if not success_messages and not error_messages:
                self.stdout.write(
                    self.style.WARNING(
                        f"⚠️ WARNING: No contact information available for {onboarding.employee.name}."
                    )
                )
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ EXCEPTION: Failed to resend onboarding notifications: {str(e)}"))
        
        self.stdout.write("\n💡 This command does EXACTLY what the resend button does")
        self.stdout.write("💡 If this works but the button doesn't, the issue is in the web interface")
        self.stdout.write("💡 Check logs/onboarding.log for detailed logs")
        
        # Show recent delivery records
        self.stdout.write("\n📋 Recent Delivery Records:")
        deliveries = onboarding.deliveries.all().order_by('-sent_at')[:3]
        
        for delivery in deliveries:
            status = '✅' if delivery.is_success else '❌'
            self.stdout.write(
                f'{status} {delivery.channel.upper()} to {delivery.destination} '
                f'at {delivery.sent_at.strftime("%Y-%m-%d %H:%M:%S")}'
            )
            if not delivery.is_success and delivery.error_message:
                self.stdout.write(f'   Error: {delivery.error_message}')