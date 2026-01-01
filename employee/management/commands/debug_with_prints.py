from django.core.management.base import BaseCommand
from employee.models import EmployeeOnboarding
from employee.services.onboarding_delivery import send_onboarding_whatsapp, send_via_fonnte

class Command(BaseCommand):
    help = 'Debug with print statements to see execution flow'

    def handle(self, *args, **options):
        print("🔍 DEBUG WITH PRINT STATEMENTS")
        print("=" * 50)
        
        # Test 1: Direct send_via_fonnte
        print("\n1️⃣ TESTING send_via_fonnte DIRECTLY:")
        print("-" * 30)
        
        try:
            result = send_via_fonnte('6283838786991', 'Debug test direct')
            print(f"✅ send_via_fonnte result: {result}")
        except Exception as e:
            print(f"❌ send_via_fonnte error: {e}")
            import traceback
            traceback.print_exc()
        
        # Test 2: send_onboarding_whatsapp
        print("\n2️⃣ TESTING send_onboarding_whatsapp:")
        print("-" * 30)
        
        onboarding = EmployeeOnboarding.objects.filter(is_completed=False).first()
        
        if onboarding:
            print(f"Using onboarding: {onboarding.employee.name}")
            
            try:
                result = send_onboarding_whatsapp(onboarding, onboarding.employee.phone)
                print(f"✅ send_onboarding_whatsapp result: {result}")
            except Exception as e:
                print(f"❌ send_onboarding_whatsapp error: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("❌ No test onboarding found")
        
        # Test 3: Full onboarding flow
        print("\n3️⃣ TESTING FULL ONBOARDING FLOW:")
        print("-" * 30)
        
        if onboarding:
            try:
                from employee.services.onboarding_delivery import send_onboarding_links
                
                results = send_onboarding_links(
                    onboarding,
                    email=onboarding.employee.private_mail,
                    phone=onboarding.employee.phone,
                )
                
                print(f"✅ send_onboarding_links results: {results}")
                
            except Exception as e:
                print(f"❌ send_onboarding_links error: {e}")
                import traceback
                traceback.print_exc()
        
        print(f"\n🎯 LOOK FOR DEBUG MESSAGES ABOVE!")
        print("If you see '🚨 DEBUG:' messages, the functions are being called")
        print("If you don't see them, there's a bug preventing function execution")
        
        print(f"\n💡 NEXT STEPS:")
        print("1. Check if you see the debug print statements above")
        print("2. If yes, the issue is in the API call or response handling")
        print("3. If no, there's a bug in the function call chain")
        print("4. Try the web interface and see if debug messages appear in console")