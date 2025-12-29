from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from employee.models import Employee, EmployeeOnboarding
from employee.services.onboarding_delivery import send_onboarding_links


class Command(BaseCommand):
    help = 'Test onboarding email and WhatsApp delivery'

    def add_arguments(self, parser):
        parser.add_argument(
            '--employee-id',
            type=int,
            help='Employee ID to test onboarding delivery',
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Test email address',
        )
        parser.add_argument(
            '--phone',
            type=str,
            help='Test phone number (format: 08123456789 or 628123456789)',
        )
        parser.add_argument(
            '--create-test-employee',
            action='store_true',
            help='Create a test employee for testing',
        )

    def handle(self, *args, **options):
        if options['create_test_employee']:
            self.create_test_employee()
            return

        employee_id = options.get('employee_id')
        test_email = options.get('email')
        test_phone = options.get('phone')

        if not employee_id:
            self.stdout.write(
                self.style.ERROR('Please provide --employee-id or use --create-test-employee')
            )
            return

        try:
            employee = Employee.objects.get(employee_id=employee_id)
        except Employee.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Employee with ID {employee_id} not found')
            )
            return

        # Create or get onboarding record
        onboarding, created = EmployeeOnboarding.objects.get_or_create(
            employee=employee,
            defaults={
                'expires_at': timezone.now() + timedelta(days=3)
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Created new onboarding record for {employee.name}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Using existing onboarding record for {employee.name}')
            )

        # Use provided email/phone or employee's contact info
        email = test_email or employee.private_mail
        phone = test_phone or employee.phone

        if not email and not phone:
            self.stdout.write(
                self.style.ERROR('No email or phone number available for testing')
            )
            return

        self.stdout.write(f'Testing onboarding delivery for: {employee.name}')
        self.stdout.write(f'Employee ID: {employee.employee_id}')
        self.stdout.write(f'Onboarding Token: {onboarding.token}')
        
        if email:
            self.stdout.write(f'Email: {email}')
        if phone:
            self.stdout.write(f'Phone: {phone}')

        # Send onboarding links
        results = send_onboarding_links(onboarding, email=email, phone=phone)

        # Display results
        if email:
            if results['email']:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Email sent successfully to {email}')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ Failed to send email to {email}')
                )

        if phone:
            if results['whatsapp']:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ WhatsApp sent successfully to {phone}')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ Failed to send WhatsApp to {phone}')
                )

        # Show delivery records
        deliveries = onboarding.deliveries.all().order_by('-sent_at')
        if deliveries:
            self.stdout.write('\nDelivery History:')
            for delivery in deliveries:
                status = '✅' if delivery.is_success else '❌'
                self.stdout.write(
                    f'{status} {delivery.channel.upper()} to {delivery.destination} '
                    f'at {delivery.sent_at.strftime("%Y-%m-%d %H:%M:%S")}'
                )
                if not delivery.is_success and delivery.error_message:
                    self.stdout.write(f'   Error: {delivery.error_message}')

    def create_test_employee(self):
        """Create a test employee for testing purposes"""
        from datetime import date
        
        # Check if test employee already exists
        test_employee_id = 99999
        if Employee.objects.filter(employee_id=test_employee_id).exists():
            self.stdout.write(
                self.style.WARNING(f'Test employee with ID {test_employee_id} already exists')
            )
            return

        employee = Employee.objects.create(
            employee_id=test_employee_id,
            name='Test Employee',
            join_date=date.today(),
            employment_status='probation',
            private_mail='test@example.com',
            phone='08123456789',
            is_active=True
        )

        self.stdout.write(
            self.style.SUCCESS(f'Created test employee: {employee.name} (ID: {employee.employee_id})')
        )
        self.stdout.write('You can now test with:')
        self.stdout.write(f'python manage.py test_onboarding --employee-id {employee.employee_id}')
        self.stdout.write('or')
        self.stdout.write(f'python manage.py test_onboarding --employee-id {employee.employee_id} --email your-email@example.com --phone 08123456789')