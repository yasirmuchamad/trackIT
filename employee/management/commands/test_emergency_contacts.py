from django.core.management.base import BaseCommand
from employee.models import Employee, EmployeeFamily


class Command(BaseCommand):
    help = 'Test emergency contact functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--employee-id',
            type=int,
            help='Employee ID to test emergency contacts',
        )

    def handle(self, *args, **options):
        employee_id = options.get('employee_id')
        
        if not employee_id:
            self.stdout.write(
                self.style.ERROR('Please provide --employee-id')
            )
            return

        try:
            employee = Employee.objects.get(employee_id=employee_id)
        except Employee.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Employee with ID {employee_id} not found')
            )
            return

        self.stdout.write(f'Testing emergency contacts for: {employee.name}')
        self.stdout.write(f'Employee ID: {employee.employee_id}')
        
        # Check if has emergency contacts
        if employee.has_emergency_contact():
            self.stdout.write(self.style.SUCCESS('✅ Employee has emergency contacts'))
            
            # Get all emergency contacts
            emergency_contacts = employee.get_emergency_contacts()
            self.stdout.write(f'\n📞 Emergency Contacts ({emergency_contacts.count()}):\n')
            
            for i, contact in enumerate(emergency_contacts, 1):
                self.stdout.write(f'{i}. {contact.name}')
                self.stdout.write(f'   Relationship: {contact.get_relationship_display()}')
                self.stdout.write(f'   Phone: {contact.phone or "Not provided"}')
                self.stdout.write(f'   Priority: {contact.emergency_priority}')
                self.stdout.write('')
            
            # Get primary emergency contact
            primary = employee.get_primary_emergency_contact()
            if primary:
                self.stdout.write(self.style.SUCCESS(f'🚨 Primary Emergency Contact: {primary.name}'))
                self.stdout.write(f'   Phone: {primary.phone or "Not provided"}')
                self.stdout.write(f'   Relationship: {primary.get_relationship_display()}')
        else:
            self.stdout.write(self.style.WARNING('⚠️ Employee has no emergency contacts'))
        
        # Show all family members
        all_family = employee.families.all()
        if all_family:
            self.stdout.write(f'\n👨‍👩‍👧‍👦 All Family Members ({all_family.count()}):\n')
            
            for family in all_family:
                emergency_indicator = " 🚨" if family.is_emergency_contact else ""
                self.stdout.write(f'• {family.name} ({family.get_relationship_display()}){emergency_indicator}')
                if family.phone:
                    self.stdout.write(f'  📞 {family.phone}')
        else:
            self.stdout.write('\n👨‍👩‍👧‍👦 No family members recorded')
        
        # Recommendations
        self.stdout.write('\n💡 Recommendations:')
        if not employee.has_emergency_contact():
            self.stdout.write('   - Add at least one emergency contact')
            self.stdout.write('   - Emergency contacts should have phone numbers')
        
        emergency_without_phone = emergency_contacts.filter(phone='') if employee.has_emergency_contact() else []
        if emergency_without_phone:
            self.stdout.write('   - Some emergency contacts are missing phone numbers:')
            for contact in emergency_without_phone:
                self.stdout.write(f'     * {contact.name} ({contact.get_relationship_display()})')
        
        if employee.has_emergency_contact() and emergency_contacts.count() == 1:
            self.stdout.write('   - Consider adding a backup emergency contact')
        
        self.stdout.write('\n✅ Emergency contact test completed')