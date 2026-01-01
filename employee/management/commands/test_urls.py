from django.core.management.base import BaseCommand
from django.urls import reverse
from employee.models import EmployeeOnboarding


class Command(BaseCommand):
    help = 'Test URL routing for resend functionality'

    def handle(self, *args, **options):
        self.stdout.write("🔗 Testing URL Routing")
        
        # Find an onboarding record
        onboarding = EmployeeOnboarding.objects.first()
        
        if not onboarding:
            self.stdout.write("❌ No onboarding records found")
            return
        
        self.stdout.write(f"📋 Testing with onboarding ID: {onboarding.id}")
        self.stdout.write(f"👤 Employee: {onboarding.employee.name}")
        
        # Test URL generation
        try:
            resend_url = reverse('employees:resend_onboarding', args=[onboarding.id])
            self.stdout.write(f"✅ Resend URL: {resend_url}")
            
            onboarding_list_url = reverse('employees:onboarding_list')
            self.stdout.write(f"✅ Onboarding List URL: {onboarding_list_url}")
            
        except Exception as e:
            self.stdout.write(f"❌ URL generation error: {str(e)}")
            return
        
        # Test form action URL
        self.stdout.write(f"\n📝 Form should have:")
        self.stdout.write(f"   action=\"{resend_url}\"")
        self.stdout.write(f"   method=\"post\"")
        
        # Manual test instructions
        self.stdout.write(f"\n🧪 MANUAL TESTS:")
        self.stdout.write(f"1. Go to: http://localhost:8000{onboarding_list_url}")
        self.stdout.write(f"2. Find employee: {onboarding.employee.name}")
        self.stdout.write(f"3. Right-click 'Resend' button → Inspect Element")
        self.stdout.write(f"4. Check form action URL matches: {resend_url}")
        self.stdout.write(f"5. Check CSRF token is present")
        
        self.stdout.write(f"\n🔍 BROWSER DEBUGGING:")
        self.stdout.write("When you click Resend button:")
        self.stdout.write("1. Check JavaScript Console for errors")
        self.stdout.write("2. Check if confirm dialog appears")
        self.stdout.write("3. Click 'OK' in confirm dialog")
        self.stdout.write("4. Check Network tab for POST request")
        self.stdout.write("5. If no POST request → JavaScript/form issue")
        self.stdout.write("6. If POST request fails → backend issue")
        
        self.stdout.write(f"\n🎯 EXPECTED BEHAVIOR:")
        self.stdout.write("1. Click 'Resend' button")
        self.stdout.write("2. Confirm dialog: 'Resend onboarding link to [name]?'")
        self.stdout.write("3. Click 'OK'")
        self.stdout.write(f"4. POST request to: {resend_url}")
        self.stdout.write("5. Page redirects back to onboarding list")
        self.stdout.write("6. Success/error message appears")
        
        # Test direct URL access
        self.stdout.write(f"\n🌐 DIRECT URL TEST:")
        self.stdout.write(f"Try accessing this URL directly:")
        self.stdout.write(f"http://localhost:8000{resend_url}")
        self.stdout.write("Expected: Should show 'Method Not Allowed' or redirect")
        self.stdout.write("(Because it expects POST, not GET)")
        
        # Common issues
        self.stdout.write(f"\n⚠️ COMMON ISSUES:")
        self.stdout.write("• JavaScript disabled in browser")
        self.stdout.write("• CSRF token missing or invalid")
        self.stdout.write("• Form inside another form (invalid HTML)")
        self.stdout.write("• Bootstrap/jQuery conflicts")
        self.stdout.write("• Browser blocking form submission")
        self.stdout.write("• Ad blocker interfering")
        
        self.stdout.write(f"\n💡 QUICK FIXES:")
        self.stdout.write("• Try different browser")
        self.stdout.write("• Try incognito/private mode")
        self.stdout.write("• Disable browser extensions")
        self.stdout.write("• Check browser security settings")
        self.stdout.write("• Clear browser cache/cookies")