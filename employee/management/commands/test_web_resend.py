from django.core.management.base import BaseCommand
from django.test import Client
from django.contrib.auth.models import User
from employee.models import EmployeeOnboarding

class Command(BaseCommand):
    help = 'Test web resend button with HTTP client'

    def handle(self, *args, **options):
        print("🌐 TEST WEB RESEND BUTTON")
        print("=" * 40)
        
        # Find test onboarding
        onboarding = EmployeeOnboarding.objects.filter(is_completed=False).first()
        
        if not onboarding:
            print("❌ No test onboarding found")
            return
        
        print(f"✅ Using onboarding: {onboarding.employee.name}")
        print(f"🆔 Onboarding ID: {onboarding.id}")
        
        # Create test client
        client = Client()
        
        # Get or create user
        user = User.objects.first()
        if not user:
            user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
            print("✅ Created test user")
        
        # Login
        client.force_login(user)
        print("✅ Logged in")
        
        # Test GET request first (to see the page)
        print(f"\n1️⃣ TESTING GET REQUEST:")
        print("-" * 20)
        
        try:
            get_url = '/employees/onboarding/'
            get_response = client.get(get_url)
            print(f"   GET {get_url}")
            print(f"   Status: {get_response.status_code}")
            
            if get_response.status_code == 200:
                print("   ✅ Onboarding list page accessible")
            else:
                print(f"   ❌ Cannot access onboarding list: {get_response.status_code}")
                
        except Exception as e:
            print(f"   ❌ GET request error: {e}")
        
        # Test POST request (resend button)
        print(f"\n2️⃣ TESTING POST REQUEST (RESEND BUTTON):")
        print("-" * 20)
        
        try:
            post_url = f'/employees/onboarding/{onboarding.id}/resend/'
            print(f"   POST {post_url}")
            
            # Make POST request (simulating resend button click)
            post_response = client.post(post_url)
            
            print(f"   Status: {post_response.status_code}")
            
            if post_response.status_code == 302:
                print(f"   ✅ Redirect response (normal)")
                print(f"   Redirect to: {post_response.url}")
            elif post_response.status_code == 200:
                print(f"   ⚠️ 200 response (unexpected)")
            else:
                print(f"   ❌ Error response: {post_response.status_code}")
                if hasattr(post_response, 'content'):
                    print(f"   Content: {post_response.content[:200]}...")
            
            print(f"\n📋 LOOK FOR DEBUG MESSAGES ABOVE!")
            print("If you see '🚨 DEBUG: resend_onboarding VIEW CALLED!' then the view is working")
            print("If you see '🚨 DEBUG: send_onboarding_whatsapp CALLED!' then the service is working")
            
        except Exception as e:
            print(f"   ❌ POST request error: {e}")
            import traceback
            traceback.print_exc()
        
        # Test direct URL access
        print(f"\n3️⃣ TESTING DIRECT URL ACCESS:")
        print("-" * 20)
        
        try:
            # Test if the URL pattern is correct
            from django.urls import reverse
            
            try:
                reverse_url = reverse('employees:resend_onboarding', args=[onboarding.id])
                print(f"   Reverse URL: {reverse_url}")
                
                direct_response = client.post(reverse_url)
                print(f"   Direct POST status: {direct_response.status_code}")
                
            except Exception as reverse_error:
                print(f"   ❌ URL reverse error: {reverse_error}")
                
        except Exception as e:
            print(f"   ❌ Direct URL test error: {e}")
        
        print(f"\n🎯 ANALYSIS:")
        print("=" * 20)
        print("Look at the output above:")
        print("1. If you see '🚨 DEBUG: resend_onboarding VIEW CALLED!' → View is executed")
        print("2. If you see '🚨 DEBUG: send_onboarding_whatsapp CALLED!' → Service is executed")
        print("3. If you see neither → There's a routing or authentication issue")
        print("4. If you see view debug but not service debug → Issue in view logic")
        
        print(f"\n💡 NEXT STEPS:")
        print("1. Check the debug messages above")
        print("2. If no debug messages → Check URL routing and authentication")
        print("3. If view debug but no service debug → Check view logic")
        print("4. If both debug messages appear → Check why message doesn't reach Fonnte history")
        
        print(f"\n🌐 MANUAL TEST:")
        print("Now try clicking the resend button in your browser and see if debug messages appear in Django console")