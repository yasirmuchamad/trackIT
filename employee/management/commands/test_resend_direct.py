from django.core.management.base import BaseCommand
from employee.models import EmployeeOnboarding
from employee.views import resend_onboarding
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.backends.db import SessionStore

class Command(BaseCommand):
    help = 'Test resend function directly (bypass HTTP issues)'

    def handle(self, *args, **options):
        print("🔍 TEST RESEND FUNCTION DIRECTLY")
        print("=" * 40)
        
        # Find test onboarding
        onboarding = EmployeeOnboarding.objects.filter(is_completed=False).first()
        
        if not onboarding:
            print("❌ No test onboarding found")
            return
        
        print(f"✅ Using onboarding: {onboarding.employee.name}")
        print(f"🆔 Onboarding ID: {onboarding.id}")
        
        # Create a mock request object
        print(f"\n📞 CREATING MOCK REQUEST:")
        print("-" * 20)
        
        try:
            # Create mock request
            request = HttpRequest()
            request.method = 'POST'
            request.path = f'/employees/onboarding/{onboarding.id}/resend/'
            
            # Add user
            user = User.objects.first()
            if not user:
                user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
            request.user = user
            
            # Add session
            request.session = SessionStore()
            request.session.create()
            
            # Add messages
            request._messages = FallbackStorage(request)
            
            print(f"   ✅ Mock request created")
            print(f"   Method: {request.method}")
            print(f"   User: {request.user}")
            print(f"   Path: {request.path}")
            
            print(f"\n📞 CALLING resend_onboarding VIEW DIRECTLY:")
            print("-" * 20)
            
            # Call the view function directly
            response = resend_onboarding(request, onboarding.id)
            
            print(f"   ✅ View executed successfully")
            print(f"   Response type: {type(response)}")
            print(f"   Response status: {getattr(response, 'status_code', 'N/A')}")
            
            # Check messages
            messages = list(request._messages)
            print(f"   Messages: {len(messages)}")
            for msg in messages:
                print(f"      - {msg.level_tag}: {msg.message}")
            
        except Exception as e:
            print(f"   ❌ Error calling view: {e}")
            import traceback
            traceback.print_exc()
        
        print(f"\n🔍 ANALYSIS:")
        print("=" * 20)
        print("Look for debug messages above:")
        print("1. '🚨 DEBUG: resend_onboarding VIEW CALLED!' → View function executed")
        print("2. '🚨 DEBUG: send_onboarding_whatsapp CALLED!' → WhatsApp service called")
        print("3. '🚨 DEBUG: requests.post completed!' → API call made")
        
        print(f"\n💡 COMPARISON:")
        print("- Command line test: Works and appears in Fonnte history")
        print("- Web interface test: Check if debug messages appear above")
        print("- If web test shows debug messages → Web interface works")
        print("- If web test doesn't show debug messages → There's a bug in web flow")
        
        print(f"\n🌐 NEXT: TEST REAL WEB INTERFACE")
        print("Now click the resend button in your browser and watch Django console")
        print("You should see the same debug messages if web interface works")