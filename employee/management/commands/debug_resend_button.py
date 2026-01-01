from django.core.management.base import BaseCommand
from employee.models import EmployeeOnboarding
from employee.views import resend_onboarding
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.backends.db import SessionStore

class Command(BaseCommand):
    help = 'Debug resend button specifically'

    def handle(self, *args, **options):
        print("🔍 DEBUG RESEND BUTTON SPECIFICALLY")
        print("=" * 50)
        
        # Find test onboarding
        onboarding = EmployeeOnboarding.objects.filter(is_completed=False).first()
        
        if not onboarding:
            print("❌ No test onboarding found")
            return
        
        print(f"✅ Using onboarding: {onboarding.employee.name}")
        print(f"📱 Phone: {onboarding.employee.phone}")
        print(f"🆔 Onboarding ID: {onboarding.id}")
        
        # Create a proper Django request (simulating web interface)
        print(f"\n🌐 SIMULATING WEB INTERFACE REQUEST:")
        print("-" * 30)
        
        try:
            # Create request factory
            factory = RequestFactory()
            
            # Create POST request (like clicking resend button)
            request = factory.post(f'/employees/onboarding/{onboarding.id}/resend/')
            
            # Add user (required for @login_required)
            user = User.objects.first()
            if not user:
                user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
            request.user = user
            
            # Add session (required for messages framework)
            request.session = SessionStore()
            request.session.create()
            
            # Add messages storage
            messages = FallbackStorage(request)
            request._messages = messages
            
            print(f"   Request method: {request.method}")
            print(f"   Request path: {request.path}")
            print(f"   Request user: {request.user}")
            print(f"   Onboarding ID: {onboarding.id}")
            
            print(f"\n📞 CALLING resend_onboarding VIEW:")
            print("-" * 30)
            
            # Call the actual view function
            response = resend_onboarding(request, onboarding.id)
            
            print(f"   Response type: {type(response)}")
            print(f"   Response status: {getattr(response, 'status_code', 'N/A')}")
            print(f"   Response url: {getattr(response, 'url', 'N/A')}")
            
            # Check messages
            message_list = list(messages)
            print(f"   Messages generated: {len(message_list)}")
            for i, msg in enumerate(message_list):
                print(f"      {i+1}. {msg.level_tag}: {msg.message}")
            
            print(f"✅ VIEW EXECUTED SUCCESSFULLY")
            
        except Exception as e:
            print(f"❌ ERROR in view execution: {e}")
            import traceback
            traceback.print_exc()
        
        # Now test the actual web interface by making HTTP request
        print(f"\n🌍 TESTING ACTUAL HTTP REQUEST:")
        print("-" * 30)
        
        try:
            from django.test import Client
            from django.contrib.auth import get_user_model
            
            # Create test client
            client = Client()
            
            # Login (required for @login_required)
            User = get_user_model()
            user = User.objects.first()
            if user:
                client.force_login(user)
                
                # Make POST request to resend endpoint
                url = f'/employees/onboarding/{onboarding.id}/resend/'
                print(f"   Making POST request to: {url}")
                
                response = client.post(url)
                
                print(f"   Response status: {response.status_code}")
                print(f"   Response redirect: {getattr(response, 'url', 'N/A')}")
                
                if response.status_code == 302:
                    print("   ✅ Request successful (redirect response)")
                else:
                    print(f"   ⚠️ Unexpected status code: {response.status_code}")
                    if hasattr(response, 'content'):
                        print(f"   Response content: {response.content[:200]}...")
            else:
                print("   ❌ No user found for login")
                
        except Exception as e:
            print(f"❌ ERROR in HTTP request: {e}")
            import traceback
            traceback.print_exc()
        
        # Check if debug messages appear when using web interface
        print(f"\n🔍 CHECKING DEBUG OUTPUT:")
        print("-" * 30)
        print("If you see '🚨 DEBUG:' messages above, the web interface is working")
        print("If you don't see them, there's a difference between command and web execution")
        
        # Compare with direct function call
        print(f"\n🧪 DIRECT FUNCTION CALL FOR COMPARISON:")
        print("-" * 30)
        
        try:
            from employee.services.onboarding_delivery import send_onboarding_links
            
            print("Calling send_onboarding_links directly...")
            results = send_onboarding_links(
                onboarding,
                email=onboarding.employee.private_mail,
                phone=onboarding.employee.phone,
            )
            
            print(f"Direct call results: {results}")
            
        except Exception as e:
            print(f"Direct call error: {e}")
        
        print(f"\n🎯 ANALYSIS:")
        print("=" * 30)
        print("1. If web interface shows debug messages → web interface works")
        print("2. If web interface doesn't show debug messages → there's a bug in web flow")
        print("3. Compare the debug output between web interface and direct call")
        print("4. Look for differences in execution path")
        
        print(f"\n💡 NEXT STEPS:")
        print("1. Check if debug messages appear when using web interface")
        print("2. If not, there's a bug in the web request handling")
        print("3. Check Django logs for any errors")
        print("4. Verify CSRF token and form submission")