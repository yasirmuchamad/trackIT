from django.core.management.base import BaseCommand
import requests

class Command(BaseCommand):
    help = 'Monkey patch requests to see what is actually being called'

    def handle(self, *args, **options):
        print("🐒 MONKEY PATCH TEST - INTERCEPT ALL REQUESTS")
        print("=" * 50)
        
        # Store original requests.post
        original_post = requests.post
        
        # Create interceptor
        call_count = 0
        intercepted_calls = []
        
        def intercepted_post(*args, **kwargs):
            nonlocal call_count, intercepted_calls
            call_count += 1
            
            print(f"\n🚨 INTERCEPTED REQUEST #{call_count}:")
            print(f"   Args: {args}")
            print(f"   Kwargs: {kwargs}")
            
            # Store the call details
            call_info = {
                'call_number': call_count,
                'args': args,
                'kwargs': kwargs
            }
            intercepted_calls.append(call_info)
            
            # Call the original function
            try:
                response = original_post(*args, **kwargs)
                print(f"   Response Status: {response.status_code}")
                print(f"   Response Text: {response.text}")
                call_info['response_status'] = response.status_code
                call_info['response_text'] = response.text
                return response
            except Exception as e:
                print(f"   Exception: {e}")
                call_info['exception'] = str(e)
                raise
        
        # Apply monkey patch
        requests.post = intercepted_post
        
        try:
            print("🧪 TESTING WITH MONKEY PATCH ACTIVE...")
            
            # Test 1: Simple direct call
            print(f"\n1️⃣ DIRECT SIMPLE CALL:")
            try:
                response1 = requests.post('https://api.fonnte.com/send',
                                        headers={'Authorization': 'urWuiF1pMJyGM25uJEjA'},
                                        data={
                                            'target': '6283838786991',
                                            'message': 'Monkey patch test 1',
                                            'countryCode': '62'
                                        })
                print(f"   Direct call completed")
            except Exception as e:
                print(f"   Direct call error: {e}")
            
            # Test 2: Through onboarding system
            print(f"\n2️⃣ THROUGH ONBOARDING SYSTEM:")
            try:
                from employee.services.onboarding_delivery import send_via_fonnte
                
                result = send_via_fonnte('6283838786991', 'Monkey patch test 2')
                print(f"   Onboarding system result: {result}")
                
            except Exception as e:
                print(f"   Onboarding system error: {e}")
                import traceback
                traceback.print_exc()
            
            # Test 3: Full onboarding flow
            print(f"\n3️⃣ FULL ONBOARDING FLOW:")
            try:
                from employee.models import EmployeeOnboarding
                from employee.services.onboarding_delivery import send_onboarding_links
                
                onboarding = EmployeeOnboarding.objects.filter(is_completed=False).first()
                
                if onboarding:
                    print(f"   Testing with: {onboarding.employee.name}")
                    
                    results = send_onboarding_links(
                        onboarding,
                        email=onboarding.employee.private_mail,
                        phone=onboarding.employee.phone,
                    )
                    
                    print(f"   Full flow results: {results}")
                else:
                    print("   No test onboarding found")
                    
            except Exception as e:
                print(f"   Full flow error: {e}")
                import traceback
                traceback.print_exc()
            
        finally:
            # Restore original function
            requests.post = original_post
        
        # Analysis
        print(f"\n📊 MONKEY PATCH ANALYSIS:")
        print("=" * 40)
        print(f"Total intercepted calls: {call_count}")
        
        if call_count == 0:
            print("🚨 NO REQUESTS INTERCEPTED!")
            print("   → The onboarding system is NOT making HTTP requests")
            print("   → There's a bug preventing the API call from happening")
        else:
            print(f"✅ {call_count} requests intercepted")
            
            for i, call in enumerate(intercepted_calls, 1):
                print(f"\n📞 Call #{i}:")
                
                # Check if it's a Fonnte call
                if len(call['args']) > 0 and 'fonnte.com' in str(call['args'][0]):
                    print("   ✅ This is a Fonnte API call")
                    
                    # Check success
                    if 'response_status' in call and call['response_status'] == 200:
                        print("   ✅ HTTP request succeeded")
                        
                        # Check Fonnte response
                        try:
                            import json
                            response_data = json.loads(call['response_text'])
                            if response_data.get('status'):
                                print("   ✅ Fonnte API returned success")
                            else:
                                print("   ❌ Fonnte API returned failure")
                                print(f"      Response: {call['response_text']}")
                        except:
                            print(f"   ⚠️ Could not parse response: {call['response_text']}")
                    else:
                        print(f"   ❌ HTTP request failed: {call.get('response_status', 'Unknown')}")
                else:
                    print("   ⚠️ This is NOT a Fonnte API call")
                    print(f"      URL: {call['args'][0] if call['args'] else 'Unknown'}")
        
        print(f"\n🎯 CONCLUSION:")
        
        if call_count == 0:
            print("🚨 MAJOR DISCOVERY: NO HTTP REQUESTS ARE BEING MADE!")
            print("   The onboarding system has a bug that prevents API calls")
            print("   Need to debug why send_via_fonnte is not calling requests.post")
        elif call_count > 0:
            fonnte_calls = [c for c in intercepted_calls if len(c['args']) > 0 and 'fonnte.com' in str(c['args'][0])]
            
            if fonnte_calls:
                print(f"✅ {len(fonnte_calls)} Fonnte API calls detected")
                print("   The system IS making API calls")
                print("   The issue is either in Fonnte's processing or response handling")
            else:
                print("⚠️ HTTP requests detected but NONE to Fonnte API")
                print("   The system is making requests to wrong endpoints")
        
        print(f"\n💡 NEXT INVESTIGATION:")
        if call_count == 0:
            print("1. Debug why send_via_fonnte doesn't call requests.post")
            print("2. Check if there are early returns or exceptions")
            print("3. Add print statements in send_via_fonnte function")
        else:
            print("1. Analyze the intercepted calls above")
            print("2. Check if Fonnte calls are successful")
            print("3. If successful, the issue is in Fonnte's backend")
        
        print(f"\n🔥 THE MYSTERY DEEPENS... BUT WE'RE GETTING CLOSER! 🕵️‍♂️")