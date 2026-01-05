from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from employee.models import EmployeeOnboarding

class Command(BaseCommand):
    help = 'Cleanup expired onboarding records and send notifications'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Delete onboarding records expired for more than X days (default: 30)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting'
        )
        parser.add_argument(
            '--notify-expiring',
            action='store_true',
            help='Send notifications for onboarding expiring in 24 hours'
        )

    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']
        notify_expiring = options['notify_expiring']
        
        self.stdout.write("🧹 ONBOARDING CLEANUP TOOL")
        self.stdout.write("=" * 50)
        
        # 1. Find expired onboarding records
        cutoff_date = timezone.now() - timedelta(days=days)
        expired_onboardings = EmployeeOnboarding.objects.filter(
            expires_at__lt=cutoff_date,
            is_completed=False
        )
        
        self.stdout.write(f"\n📊 EXPIRED ONBOARDING RECORDS:")
        self.stdout.write(f"   Cutoff date: {cutoff_date.strftime('%Y-%m-%d %H:%M')}")
        self.stdout.write(f"   Found: {expired_onboardings.count()} records")
        
        if expired_onboardings.exists():
            for onboarding in expired_onboardings:
                self.stdout.write(f"   • {onboarding.employee.name} - Expired: {onboarding.expires_at}")
            
            if not dry_run:
                deleted_count = expired_onboardings.count()
                expired_onboardings.delete()
                self.stdout.write(self.style.SUCCESS(f"✅ Deleted {deleted_count} expired records"))
            else:
                self.stdout.write(self.style.WARNING("🔍 DRY RUN: No records deleted"))
        else:
            self.stdout.write("   No expired records found")
        
        # 2. Find onboarding expiring soon (24 hours)
        if notify_expiring:
            tomorrow = timezone.now() + timedelta(hours=24)
            expiring_soon = EmployeeOnboarding.objects.filter(
                expires_at__lt=tomorrow,
                expires_at__gt=timezone.now(),
                is_completed=False
            )
            
            self.stdout.write(f"\n⏰ ONBOARDING EXPIRING SOON:")
            self.stdout.write(f"   Found: {expiring_soon.count()} records")
            
            if expiring_soon.exists():
                from employee.services.onboarding_delivery import send_onboarding_links
                
                for onboarding in expiring_soon:
                    employee = onboarding.employee
                    self.stdout.write(f"   • {employee.name} - Expires: {onboarding.expires_at}")
                    
                    if not dry_run:
                        try:
                            # Send reminder notification
                            results = send_onboarding_links(
                                onboarding,
                                email=employee.private_mail,
                                phone=employee.phone
                            )
                            
                            success_channels = []
                            if employee.private_mail and results.get('email'):
                                success_channels.append('email')
                            if employee.phone and results.get('whatsapp'):
                                success_channels.append('WhatsApp')
                            
                            if success_channels:
                                self.stdout.write(f"     ✅ Reminder sent via: {', '.join(success_channels)}")
                            else:
                                self.stdout.write(f"     ❌ Failed to send reminder")
                                
                        except Exception as e:
                            self.stdout.write(f"     ❌ Error: {str(e)}")
                    else:
                        self.stdout.write("     🔍 DRY RUN: No reminder sent")
            else:
                self.stdout.write("   No records expiring soon")
        
        # 3. Statistics
        self.stdout.write(f"\n📈 ONBOARDING STATISTICS:")
        
        total_onboardings = EmployeeOnboarding.objects.count()
        completed_onboardings = EmployeeOnboarding.objects.filter(is_completed=True).count()
        pending_onboardings = EmployeeOnboarding.objects.filter(is_completed=False).count()
        currently_expired = EmployeeOnboarding.objects.filter(
            expires_at__lt=timezone.now(),
            is_completed=False
        ).count()
        
        self.stdout.write(f"   Total onboardings: {total_onboardings}")
        self.stdout.write(f"   Completed: {completed_onboardings}")
        self.stdout.write(f"   Pending: {pending_onboardings}")
        self.stdout.write(f"   Currently expired: {currently_expired}")
        
        # 4. Recommendations
        self.stdout.write(f"\n💡 RECOMMENDATIONS:")
        
        if currently_expired > 0:
            self.stdout.write(f"   • {currently_expired} onboarding(s) are currently expired")
            self.stdout.write("   • Consider regenerating tokens for these employees")
        
        if pending_onboardings > 10:
            self.stdout.write(f"   • {pending_onboardings} pending onboardings (high number)")
            self.stdout.write("   • Consider following up with employees")
        
        completion_rate = (completed_onboardings / total_onboardings * 100) if total_onboardings > 0 else 0
        self.stdout.write(f"   • Completion rate: {completion_rate:.1f}%")
        
        if completion_rate < 80:
            self.stdout.write("   • Low completion rate - consider improving onboarding process")
        
        self.stdout.write(f"\n✨ Cleanup completed!")
        
        if dry_run:
            self.stdout.write(self.style.WARNING("🔍 This was a dry run. Use --no-dry-run to actually perform actions."))
        
        # Usage examples
        self.stdout.write(f"\n📚 USAGE EXAMPLES:")
        self.stdout.write("   python manage.py cleanup_expired_onboarding --days 30")
        self.stdout.write("   python manage.py cleanup_expired_onboarding --notify-expiring")
        self.stdout.write("   python manage.py cleanup_expired_onboarding --dry-run")