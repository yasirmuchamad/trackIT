from django.core.management.base import BaseCommand
from django.test import Client
from django.urls import reverse
from employee.models import EmployeeOnboarding
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Test form submission programmatically'

    def handle(self, *args, **options):
        self.stdout.write("📝 Testing Form Submission")
        
        # Find onboarding record
        onboarding = EmployeeOnboarding.objects.first()
        if not onboarding:
            self.stdout.write("❌ No onboarding records found")
            return
        
        self.stdout.write(f"📋 Testing with onboarding ID: {onboarding.id}")
        self.stdout.write(f"👤 Employee: {onboarding.employee.name}")
        
        # Create test client
        client = Client()
        
        # Get or create a user for authentication
        try:
            user = User.objects.first()
            if not user:
                user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
                self.stdout.write("✅ Created test user")
            
            # Login
            client.force_login(user)
            self.stdout.write("✅ Logged in as test user")
            
        except Exception as e:
            self.stdout.write(f"❌ User setup error: {str(e)}")
            return
        
        # Test GET request to onboarding list
        try:
            list_url = reverse('employees:onboarding_list')
            response = client.get(list_url)
            
            self.stdout.write(f"\n📄 GET {list_url}")
            self.stdout.write(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                self.stdout.write("✅ Onboarding list page loads successfully")
                
                # Check if our onboarding is in the page
                if str(onboarding.id) in response.content.decode():
                    self.stdout.write(f"✅ Onboarding ID {onboarding.id} found in page")
                else:
                    self.stdout.write(f"⚠️ Onboarding ID {onboarding.id} not found in page")
                    
            else:
                self.stdout.write(f"❌ Onboarding list page failed: {response.status_code}")
                
        except Exception as e:
            self.stdout.write(f"❌ GET request error: {str(e)}")
        
        # Test POST request to resend
        try:
            resend_url = reverse('employees:resend_onboarding', args=[onboarding.id])
            
            self.stdout.write(f"\n📤 POST {resend_url}")
            
            # Get CSRF token first
            csrf_response = client.get(list_url)
            csrf_token = csrf_response.cookies.get('csrftoken')
            
            if csrf_token:
                self.stdout.write("✅ CSRF token obtained")
            else:
                self.stdout.write("⚠️ No CSRF token found")
            
            # Make POST request
            response = client.post(resend_url, {
                'csrfmiddlewaretoken': csrf_token.value if csrf_token else ''
            })
            
            self.stdout.write(f"Status: {response.status_code}")
            
            if response.status_code == 302:  # Redirect
                self.stdout.write("✅ POST request successful (redirected)")
                self.stdout.write(f"Redirect to: {response.url}")
                
                # Check if redirected to onboarding list
                if 'onboarding' in response.url:
                    self.stdout.write("✅ Redirected to onboarding list as expected")
                else:
                    self.stdout.write(f"⚠️ Unexpected redirect: {response.url}")
                    
            elif response.status_code == 200:
                self.stdout.write("✅ POST request successful (no redirect)")
                
            elif response.status_code == 403:
                self.stdout.write("❌ POST request forbidden (CSRF issue?)")
                
            elif response.status_code == 404:
                self.stdout.write("❌ POST request not found (URL issue?)")
                
            else:
                self.stdout.write(f"❌ POST request failed: {response.status_code}")
                
        except Exception as e:
            self.stdout.write(f"❌ POST request error: {str(e)}")
        
        # Check recent delivery records
        self.stdout.write(f"\n📋 Checking Delivery Records...")
        
        from django.utils import timezone
        from datetime import timedelta
        from django.db import models
        
        try:
            recent_deliveries = onboarding.deliveries.all().order_by('-sent_at')[:3]
            
            if recent_deliveries:
                self.stdout.write(f"✅ Found {recent_deliveries.count()} recent delivery records:")
                for delivery in recent_deliveries:
                    status = '✅' if delivery.is_success else '❌'
                    self.stdout.write(f"   {status} {delivery.channel.upper()} to {delivery.destination}")
            else:
                self.stdout.write("⚠️ No recent delivery records found")
        except Exception as e:
            self.stdout.write(f"⚠️ Error checking deliveries: {str(e)}")
        
        # Final diagnosis
        self.stdout.write(f"\n🎯 DIAGNOSIS:")
        self.stdout.write("If POST request succeeds here but browser doesn't work:")
        self.stdout.write("• Browser JavaScript issue")
        self.stdout.write("• Confirm dialog being cancelled")
        self.stdout.write("• Browser security blocking submission")
        self.stdout.write("• Form HTML structure issue")
        
        self.stdout.write(f"\n💡 BROWSER TEST:")
        self.stdout.write("1. Go to onboarding list page")
        self.stdout.write("2. Open Developer Tools → Network tab")
        self.stdout.write("3. Click resend button")
        self.stdout.write("4. In confirm dialog, click 'OK' (not Cancel)")
        self.stdout.write("5. Look for POST request in Network tab")
        self.stdout.write("6. If no POST request → JavaScript/confirm issue")
        self.stdout.write("7. If POST request appears → backend working")