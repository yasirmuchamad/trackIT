from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Fix typo in OnboardingDelivery table column name'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            try:
                # Check if old column exists
                cursor.execute("PRAGMA table_info(employee_onboardingdelivery)")
                columns = [row[1] for row in cursor.fetchall()]
                
                if 'is_succces' in columns and 'is_success' not in columns:
                    self.stdout.write('Fixing typo: renaming is_succces to is_success...')
                    
                    # For SQLite, we need to recreate the table
                    cursor.execute("""
                        CREATE TABLE employee_onboardingdelivery_new (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            channel VARCHAR(10) NOT NULL,
                            destination VARCHAR(255) NOT NULL,
                            sent_at DATETIME NOT NULL,
                            is_success BOOLEAN NOT NULL DEFAULT 1,
                            error_message TEXT NOT NULL,
                            onboarding_id CHAR(32) NOT NULL REFERENCES employee_employeeonboarding(id)
                        )
                    """)
                    
                    # Copy data from old table to new table
                    cursor.execute("""
                        INSERT INTO employee_onboardingdelivery_new 
                        (id, channel, destination, sent_at, is_success, error_message, onboarding_id)
                        SELECT id, channel, destination, sent_at, is_succces, error_message, onboarding_id
                        FROM employee_onboardingdelivery
                    """)
                    
                    # Drop old table and rename new table
                    cursor.execute("DROP TABLE employee_onboardingdelivery")
                    cursor.execute("ALTER TABLE employee_onboardingdelivery_new RENAME TO employee_onboardingdelivery")
                    
                    self.stdout.write(
                        self.style.SUCCESS('Successfully fixed typo in OnboardingDelivery table')
                    )
                elif 'is_success' in columns:
                    self.stdout.write(
                        self.style.SUCCESS('Column is_success already exists, no fix needed')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING('OnboardingDelivery table not found or has different structure')
                    )
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error fixing typo: {str(e)}')
                )
                self.stdout.write(
                    self.style.WARNING('You may need to run: python manage.py migrate employee')
                )