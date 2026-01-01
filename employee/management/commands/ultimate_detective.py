from django.core.management.base import BaseCommand
import requests
import json
import hashlib
import time

class Command(BaseCommand):
    help = 'Ultimate detective mode - find the EXACT difference'

    def handle(self, *args, **options):
        print("🕵️ ULTIMATE DETECTIVE MODE - TIDAK AKAN MENYERAH!")
        print("=" * 60)
        
        # Let's capture EVERYTHING about both requests
        token = 'urWuiF1pMJyGM25uJEjA'
        
        print("🔍 STEP 1: CAPTURE EXACT REQUEST DETAILS")
        print("-" * 40)
        
        # Method 1: Exact copy of simple_fonnte_test
        print("📤 SIMPLE_FONNTE_TEST REQUEST:")
        
        import requests.adapters
        import urllib3
        
        # Create session to capture more details
        session1 = requests.Session()
        
        # Enable detailed logging
        import logging
        import http.client as http_client
        
        # Temporarily enable HTTP debugging
        http_client.HTTPConnection.debuglevel = 1
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True
        
        try:
            print("   Sending request...")
            response1 = session1.post('https://api.fonnte.com/send',
                                    headers={'Authorization': 'urWuiF1pMJyGM25uJEjA'},
                                    data={
                                        'target': '6283838786991',
                                        'message': 'Ultimate detective test 1',
                                        'countryCode': '62'
                                    })
            
            print(f"   Status: {response1.status_code}")
            print(f"   Headers sent: {dict(response1.request.headers)}")
            print(f"   Body sent: {response1.request.body}")
            print(f"   URL: {response1.request.url}")
            print(f"   Method: {response1.request.method}")
            print(f"   Response: {response1.text}")
            
            # Calculate hash of request
            request_hash1 = hashlib.md5(str(response1.request.headers).encode() + 
                                      (response1.request.body or b'')).hexdigest()
            print(f"   Request hash: {request_hash1}")
            
            success1 = response1.json().get('status', False) if response1.status_code == 200 else False
            
        except Exception as e:
            print(f"   Error: {e}")
            success1 = False
            request_hash1 = "error"
        
        # Disable debugging
        http_client.HTTPConnection.debuglevel = 0
        logging.getLogger().setLevel(logging.WARNING)
        
        time.sleep(3)  # Wait between requests
        
        # Method 2: Onboarding system way
        print(f"\n📤 ONBOARDING SYSTEM REQUEST:")
        
        session2 = requests.Session()
        
        try:
            # Exact replication of onboarding system
            from django.conf import settings
            
            url = getattr(settings, 'WHATSAPP_SERVICE_URL', 'https://api.fonnte.com/send')
            token_from_settings = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', '')
            
            headers = {
                'Authorization': token_from_settings,
            }
            
            data = {
                'target': '6283838786991',
                'message': 'Ultimate detective test 2',
                'countryCode': '62',
            }
            
            print(f"   URL from settings: {url}")
            print(f"   Token from settings: {token_from_settings}")
            print(f"   Headers: {headers}")
            print(f"   Data: {data}")
            
            response2 = session2.post(url, data=data, headers=headers)
            
            print(f"   Status: {response2.status_code}")
            print(f"   Headers sent: {dict(response2.request.headers)}")
            print(f"   Body sent: {response2.request.body}")
            print(f"   URL: {response2.request.url}")
            print(f"   Method: {response2.request.method}")
            print(f"   Response: {response2.text}")
            
            # Calculate hash of request
            request_hash2 = hashlib.md5(str(response2.request.headers).encode() + 
                                      (response2.request.body or b'')).hexdigest()
            print(f"   Request hash: {request_hash2}")
            
            success2 = response2.json().get('status', False) if response2.status_code == 200 else False
            
        except Exception as e:
            print(f"   Error: {e}")
            success2 = False
            request_hash2 = "error"
        
        print(f"\n🔍 STEP 2: DETAILED COMPARISON")
        print("-" * 40)
        
        print(f"Request 1 success: {success1}")
        print(f"Request 2 success: {success2}")
        print(f"Request hashes match: {request_hash1 == request_hash2}")
        
        if 'response1' in locals() and 'response2' in locals():
            # Compare every detail
            print(f"\n📊 DETAILED COMPARISON:")
            print(f"URLs match: {response1.request.url == response2.request.url}")
            print(f"Methods match: {response1.request.method == response2.request.method}")
            print(f"Bodies match: {response1.request.body == response2.request.body}")
            
            # Compare headers one by one
            headers1 = dict(response1.request.headers)
            headers2 = dict(response2.request.headers)
            
            print(f"\n🔍 HEADER COMPARISON:")
            all_headers = set(headers1.keys()) | set(headers2.keys())
            for header in sorted(all_headers):
                val1 = headers1.get(header, 'MISSING')
                val2 = headers2.get(header, 'MISSING')
                match = "✅" if val1 == val2 else "❌"
                print(f"   {header}: {match}")
                if val1 != val2:
                    print(f"      Request 1: {val1}")
                    print(f"      Request 2: {val2}")
            
            # Compare response details
            print(f"\n🔍 RESPONSE COMPARISON:")
            print(f"Status codes match: {response1.status_code == response2.status_code}")
            print(f"Response bodies match: {response1.text == response2.text}")
            
            if response1.text != response2.text:
                print(f"   Response 1: {response1.text}")
                print(f"   Response 2: {response2.text}")
        
        # Step 3: Test with IDENTICAL variables
        print(f"\n🔍 STEP 3: ABSOLUTELY IDENTICAL TEST")
        print("-" * 40)
        
        # Use exact same variables for both
        test_url = 'https://api.fonnte.com/send'
        test_token = 'urWuiF1pMJyGM25uJEjA'
        test_headers = {'Authorization': test_token}
        test_data = {
            'target': '6283838786991',
            'message': 'Identical test',
            'countryCode': '62'
        }
        
        print(f"Using identical variables:")
        print(f"URL: {test_url}")
        print(f"Token: {test_token}")
        print(f"Headers: {test_headers}")
        print(f"Data: {test_data}")
        
        # Test A
        try:
            resp_a = requests.post(test_url, headers=test_headers, data=test_data)
            success_a = resp_a.json().get('status', False) if resp_a.status_code == 200 else False
            print(f"Test A: {success_a} - {resp_a.text}")
        except Exception as e:
            print(f"Test A error: {e}")
            success_a = False
        
        time.sleep(2)
        
        # Test B
        try:
            resp_b = requests.post(test_url, headers=test_headers, data=test_data)
            success_b = resp_b.json().get('status', False) if resp_b.status_code == 200 else False
            print(f"Test B: {success_b} - {resp_b.text}")
        except Exception as e:
            print(f"Test B error: {e}")
            success_b = False
        
        # Step 4: Check if it's a timing/race condition
        print(f"\n🔍 STEP 4: TIMING/RACE CONDITION TEST")
        print("-" * 40)
        
        # Send multiple requests quickly
        results = []
        for i in range(5):
            try:
                resp = requests.post(test_url, headers=test_headers, data={
                    'target': '6283838786991',
                    'message': f'Timing test {i+1}',
                    'countryCode': '62'
                })
                success = resp.json().get('status', False) if resp.status_code == 200 else False
                results.append(success)
                print(f"   Test {i+1}: {success}")
                time.sleep(1)
            except Exception as e:
                print(f"   Test {i+1}: Error - {e}")
                results.append(False)
        
        success_rate = sum(results) / len(results) * 100
        print(f"Success rate: {success_rate}%")
        
        # Final analysis
        print(f"\n🎯 ULTIMATE ANALYSIS:")
        print("=" * 40)
        
        if success1 and not success2:
            print("🚨 CONFIRMED: Simple test works, onboarding fails")
            print("   → There IS a difference we haven't found yet")
        elif success1 and success2:
            print("🤔 BOTH WORK: The issue is elsewhere")
            print("   → Maybe it's in the Django view or database logging")
        elif not success1 and not success2:
            print("❌ BOTH FAIL: Account or connection issue")
        else:
            print("🔄 INCONSISTENT: Timing or race condition")
        
        print(f"\n💡 NEXT INVESTIGATION:")
        if success1 and success2:
            print("1. Check if the issue is in Django views")
            print("2. Check if OnboardingDelivery records are created")
            print("3. Check if there's a database transaction issue")
            print("4. Check if there's middleware interfering")
        else:
            print("1. There's still a difference in the API calls")
            print("2. Need to check character encoding")
            print("3. Need to check if there are hidden characters")
            print("4. Need to check network/proxy differences")
        
        print(f"\n🔥 CHALLENGE ACCEPTED - WE WILL FIND THIS BUG!")
        print("The mystery continues... 🕵️‍♂️")