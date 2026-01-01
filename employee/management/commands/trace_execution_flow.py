from django.core.management.base import BaseCommand
from employee.models import EmployeeOnboarding, OnboardingDelivery
from employee.services.onboarding_delivery import send_onboarding_links
import logging

class Command(BaseCommand):
    help = 'Trace exact execution flow of onboarding system'

    def handle(self, *args, **options):
        print("🔍 TRACE EXECUTION FLOW - STEP BY STEP")
        print("=" * 50)
        
        # Find test onboarding
        onboarding = EmployeeOnboarding.objects.filter(is_completed=False).first()
        
        if not onboarding:
            print("❌ No test onboarding found")
            return
        
        print(f"✅ Using onboarding: {onboarding.employee.name}")
        print(f"📧 Email: {onboarding.employee.private_mail}")
        print(f"📱 Phone: {onboarding.employee.phone}")
        
        # Clear previous delivery records for this test
        print(f"\n🧹 CLEARING PREVIOUS DELIVERY RECORDS...")
        old_count = OnboardingDelivery.objects.filter(onboarding=onboarding).count()
        print(f"Found {old_count} old delivery records")
        
        # Add detailed logging to trace execution
        logger = logging.getLogger('employee.services.onboarding_delivery')
        logger.setLevel(logging.DEBUG)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        print(f"\n📞 CALLING send_onboarding_links...")
        print("-" * 30)
        
        try:
            # Call the exact same function as the web interface
            results = send_onboarding_links(
                onboarding,
                email=onboarding.employee.private_mail,
                phone=onboarding.employee.phone,
            )
            
            print(f"\n📊 RESULTS FROM send_onboarding_links:")
            print(f"   Email result: {results.get('email', 'N/A')}")
            print(f"   WhatsApp result: {results.get('whatsapp', 'N/A')}")
            
        except Exception as e:
            print(f"❌ ERROR in send_onboarding_links: {e}")
            import traceback
            traceback.print_exc()
            results = {'email': False, 'whatsapp': False}
        
        # Check what was actually created in database
        print(f"\n💾 DATABASE RECORDS CREATED:")
        print("-" * 30)
        
        new_deliveries = OnboardingDelivery.objects.filter(onboarding=onboarding).order_by('-created_at')[:5]
        
        if new_deliveries:
            for delivery in new_deliveries:
                print(f"   📨 {delivery.channel.upper()}: {delivery.destination}")
                print(f"      Success: {delivery.is_success}")
                print(f"      Created: {delivery.created_at}")
                if delivery.error_message:
                    print(f"      Error: {delivery.error_message}")
                print()
        else:
            print("   ❌ NO DELIVERY RECORDS CREATED!")
            print("   This means the function didn't reach the database logging part")
        
        # Test direct function calls
        print(f"\n🧪 DIRECT FUNCTION TESTS:")
        print("-" * 30)
        
        # Test 1: Direct WhatsApp function
        print("1️⃣ Testing send_onboarding_whatsapp directly:")
        try:
            from employee.services.onboarding_delivery import send_onboarding_whatsapp
            
            whatsapp_result = send_onboarding_whatsapp(onboarding, onboarding.employee.phone)
            print(f"   Result: {whatsapp_result}")
            
        except Exception as e:
            print(f"   Error: {e}")
            import traceback
            traceback.print_exc()
        
        # Test 2: Direct Fonnte function
        print(f"\n2️⃣ Testing send_via_fonnte directly:")
        try:
            from employee.services.onboarding_delivery import send_via_fonnte
            
            fonnte_result = send_via_fonnte('6283838786991', 'Direct fonnte test')
            print(f"   Result: {fonnte_result}")
            
        except Exception as e:
            print(f"   Error: {e}")
            import traceback
            traceback.print_exc()
        
        # Test 3: Check if the issue is in the web view
        print(f"\n3️⃣ SIMULATING WEB VIEW CALL:")
        print("-" * 30)
        
        try:
            # Simulate exactly what the web view does
            from employee.views import resend_onboarding
            from django.http import HttpRequest
            from django.contrib.auth.models import User
            
            # Create fake request
            request = HttpRequest()
            request.method = 'POST'
            request.user = User.objects.first() or User(username='test')
            
            print(f"   Simulating resend_onboarding view...")
            print(f"   Onboarding ID: {onboarding.id}")
            
            # This would normally redirect, but we can catch any errors
            try:
                response = resend_onboarding(request, onboarding.id)
                print(f"   View response: {response}")
            except Exception as view_error:
                print(f"   View error: {view_error}")
                import traceback
                traceback.print_exc()
                
        except Exception as e:
            print(f"   Setup error: {e}")
        
        # Final check - compare with simple test
        print(f"\n4️⃣ FINAL COMPARISON WITH SIMPLE TEST:")
        print("-" * 30)
        
        import requests
        
        try:
            # Simple test that we know works
            simple_response = requests.post('https://api.fonnte.com/send',
                                          headers={'Authorization': 'urWuiF1pMJyGM25uJEjA'},
                                          data={
                                              'target': '6283838786991',
                                              'message': 'Simple comparison test',
                                              'countryCode': '62'
                                          })
            
            simple_success = simple_response.json().get('status', False) if simple_response.status_code == 200 else False
            print(f"   Simple test success: {simple_success}")
            print(f"   Simple test response: {simple_response.text}")
            
        except Exception as e:
            print(f"   Simple test error: {e}")
        
        print(f"\n🎯 EXECUTION FLOW ANALYSIS:")
        print("=" * 40)
        
        if results.get('whatsapp') and new_deliveries:
            print("✅ Function executed successfully AND database records created")
            print("   → The issue might be in Fonnte's internal processing")
            print("   → Or the message is being filtered/blocked somewhere")
        elif results.get('whatsapp') and not new_deliveries:
            print("⚠️ Function claims success but NO database records")
            print("   → There's an exception after the API call but before DB save")
        elif not results.get('whatsapp'):
            print("❌ Function reports failure")
            print("   → The API call itself is failing")
        else:
            print("🤔 Inconsistent state - need more investigation")
        
        print(f"\n💡 NEXT STEPS:")
        print("1. Check the detailed logs above for exact failure point")
        print("2. If API succeeds but no DB records → exception handling issue")
        print("3. If API fails → configuration or network issue")
        print("4. If everything succeeds → Fonnte internal issue")
        
        # Clean up logger
        logger.removeHandler(console_handler)