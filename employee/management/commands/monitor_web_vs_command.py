from django.core.management.base import BaseCommand
from employee.models import EmployeeOnboarding, OnboardingDelivery
from django.utils import timezone
from datetime import timedelta
import time


class Command(BaseCommand):
    help = 'Monitor delivery records to compare web vs command behavior'

    def add_arguments(self, parser):
        parser.add_argument(
            '--watch',
            action='store_true',
            help='Watch for new delivery records in real-time',
        )

    def handle(self, *args, **options):
        if options['watch']:
            self.watch_deliveries()
        else:
            self.show_recent_deliveries()

    def watch_deliveries(self):
        """Watch for new delivery records in real-time"""
        self.stdout.write("👀 Watching for new delivery records...")
        self.stdout.write("💡 Now click the resend button in web interface")
        self.stdout.write("💡 Press Ctrl+C to stop watching")
        
        # Get current time as baseline
        start_time = timezone.now()
        last_count = OnboardingDelivery.objects.count()
        
        try:
            while True:
                current_count = OnboardingDelivery.objects.count()
                
                if current_count > last_count:
                    # New delivery records found
                    new_deliveries = OnboardingDelivery.objects.filter(
                        sent_at__gte=start_time
                    ).order_by('-sent_at')
                    
                    self.stdout.write(f"\n🚨 {current_count - last_count} new delivery record(s) detected!")
                    
                    for delivery in new_deliveries:
                        self.show_delivery_detail(delivery)
                    
                    last_count = current_count
                    start_time = timezone.now()
                
                time.sleep(1)  # Check every second
                
        except KeyboardInterrupt:
            self.stdout.write("\n👋 Stopped watching")

    def show_recent_deliveries(self):
        """Show recent delivery records with analysis"""
        self.stdout.write("📋 Recent Delivery Records (last 10):")
        
        recent_deliveries = OnboardingDelivery.objects.all().order_by('-sent_at')[:10]
        
        if not recent_deliveries:
            self.stdout.write("   No delivery records found")
            return
        
        for delivery in recent_deliveries:
            self.show_delivery_detail(delivery)
        
        # Analysis
        self.analyze_delivery_patterns(recent_deliveries)

    def show_delivery_detail(self, delivery):
        """Show detailed information about a delivery record"""
        status = '✅' if delivery.is_success else '❌'
        
        self.stdout.write(f"\n{status} {delivery.channel.upper()} Delivery:")
        self.stdout.write(f"   Employee: {delivery.onboarding.employee.name}")
        self.stdout.write(f"   Destination: {delivery.destination}")
        self.stdout.write(f"   Time: {delivery.sent_at.strftime('%Y-%m-%d %H:%M:%S')}")
        self.stdout.write(f"   Success: {delivery.is_success}")
        
        if not delivery.is_success and delivery.error_message:
            self.stdout.write(f"   Error: {delivery.error_message}")
        
        # Check if this was recent (within last 5 minutes)
        if delivery.sent_at >= timezone.now() - timedelta(minutes=5):
            self.stdout.write("   🔥 RECENT (within 5 minutes)")
            
            # Try to determine if this was from web or command
            self.guess_delivery_source(delivery)

    def guess_delivery_source(self, delivery):
        """Try to guess if delivery was from web interface or command"""
        # Check for patterns that might indicate source
        
        # Check timing - commands often send multiple at once
        similar_time_deliveries = OnboardingDelivery.objects.filter(
            sent_at__gte=delivery.sent_at - timedelta(seconds=5),
            sent_at__lte=delivery.sent_at + timedelta(seconds=5),
            onboarding=delivery.onboarding
        ).count()
        
        if similar_time_deliveries > 1:
            self.stdout.write("   🤖 Likely from COMMAND (multiple simultaneous)")
        else:
            self.stdout.write("   🌐 Likely from WEB INTERFACE (single delivery)")
        
        # Check for email+whatsapp pair (typical of onboarding)
        email_delivery = OnboardingDelivery.objects.filter(
            onboarding=delivery.onboarding,
            channel='email',
            sent_at__gte=delivery.sent_at - timedelta(seconds=10),
            sent_at__lte=delivery.sent_at + timedelta(seconds=10)
        ).first()
        
        whatsapp_delivery = OnboardingDelivery.objects.filter(
            onboarding=delivery.onboarding,
            channel='whatsapp',
            sent_at__gte=delivery.sent_at - timedelta(seconds=10),
            sent_at__lte=delivery.sent_at + timedelta(seconds=10)
        ).first()
        
        if email_delivery and whatsapp_delivery:
            self.stdout.write("   📧📱 Part of EMAIL+WHATSAPP pair")
            
            # Compare success rates
            if email_delivery.is_success and not whatsapp_delivery.is_success:
                self.stdout.write("   ⚠️ EMAIL succeeded but WHATSAPP failed")
            elif not email_delivery.is_success and whatsapp_delivery.is_success:
                self.stdout.write("   ⚠️ WHATSAPP succeeded but EMAIL failed")
            elif email_delivery.is_success and whatsapp_delivery.is_success:
                self.stdout.write("   ✅ Both EMAIL and WHATSAPP succeeded")
            else:
                self.stdout.write("   ❌ Both EMAIL and WHATSAPP failed")

    def analyze_delivery_patterns(self, deliveries):
        """Analyze patterns in delivery records"""
        self.stdout.write("\n📊 DELIVERY ANALYSIS:")
        
        # Success rates by channel
        email_deliveries = [d for d in deliveries if d.channel == 'email']
        whatsapp_deliveries = [d for d in deliveries if d.channel == 'whatsapp']
        
        if email_deliveries:
            email_success_rate = sum(1 for d in email_deliveries if d.is_success) / len(email_deliveries) * 100
            self.stdout.write(f"   📧 Email success rate: {email_success_rate:.1f}% ({len(email_deliveries)} attempts)")
        
        if whatsapp_deliveries:
            whatsapp_success_rate = sum(1 for d in whatsapp_deliveries if d.is_success) / len(whatsapp_deliveries) * 100
            self.stdout.write(f"   📱 WhatsApp success rate: {whatsapp_success_rate:.1f}% ({len(whatsapp_deliveries)} attempts)")
            
            # Check for pattern of "success but not delivered"
            whatsapp_successes = [d for d in whatsapp_deliveries if d.is_success]
            if whatsapp_successes:
                self.stdout.write(f"   📱 WhatsApp 'successes': {len(whatsapp_successes)}")
                self.stdout.write("   💡 Remember: 'success' means sent to Fonnte, not delivered to phone")
        
        # Time patterns
        if deliveries:
            latest = deliveries[0].sent_at
            oldest = deliveries[-1].sent_at
            timespan = latest - oldest
            
            self.stdout.write(f"   ⏰ Timespan: {timespan}")
            
            if timespan.total_seconds() < 60:
                self.stdout.write("   🔥 High frequency (< 1 minute) - likely testing")
        
        # Common errors
        errors = [d.error_message for d in deliveries if not d.is_success and d.error_message]
        if errors:
            self.stdout.write("   ❌ Common errors:")
            for error in set(errors):
                count = errors.count(error)
                self.stdout.write(f"      • {error} ({count}x)")
        
        self.stdout.write("\n💡 RECOMMENDATIONS:")
        self.stdout.write("   1. Use --watch mode while testing web interface")
        self.stdout.write("   2. Compare delivery records from web vs command")
        self.stdout.write("   3. Look for timing patterns and error differences")
        self.stdout.write("   4. Check if WhatsApp 'successes' actually deliver messages")