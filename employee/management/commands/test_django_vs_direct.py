from django.core.management.base import BaseCommand
import requests
import subprocess
import sys
import os

class Command(BaseCommand):
    help = 'Test if Django context affects API calls'

    def handle(self, *args, **options):
        print("🔍 TEST: DJANGO CONTEXT vs DIRECT PYTHON")
        print("=" * 50)
        
        # Test 1: From Django management command (current context)
        print("1️⃣ DARI DJANGO MANAGEMENT COMMAND:")
        try:
            response = requests.post(
                'https://api.fonnte.com/send',
                headers={'Authorization': 'urWuiF1pMJyGM25uJEjA'},
                data={
                    'target': '6283838786991',
                    'message': 'Test from Django command',
                    'countryCode': '62'
                }
            )
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                django_success = result.get('status', False)
                print(f"   Success: {django_success}")
            else:
                django_success = False
        except Exception as e:
            print(f"   Error: {e}")
            django_success = False
        
        # Test 2: Create standalone Python script and run it
        print(f"\n2️⃣ DARI STANDALONE PYTHON SCRIPT:")
        
        standalone_script = '''
import requests
import json

try:
    response = requests.post(
        'https://api.fonnte.com/send',
        headers={'Authorization': 'urWuiF1pMJyGM25uJEjA'},
        data={
            'target': '6283838786991',
            'message': 'Test from standalone script',
            'countryCode': '62'
        }
    )
    
    result = {
        'status_code': response.status_code,
        'response_text': response.text,
        'success': response.json().get('status', False) if response.status_code == 200 else False
    }
    
    print(json.dumps(result))
    
except Exception as e:
    print(json.dumps({'error': str(e), 'success': False}))
'''
        
        # Write standalone script
        script_path = 'temp_standalone_test.py'
        with open(script_path, 'w') as f:
            f.write(standalone_script)
        
        try:
            # Run standalone script
            result = subprocess.run([sys.executable, script_path], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                try:
                    standalone_result = eval(result.stdout.strip())  # Safe since we control the output
                    print(f"   Status: {standalone_result.get('status_code', 'Unknown')}")
                    print(f"   Response: {standalone_result.get('response_text', 'Unknown')}")
                    standalone_success = standalone_result.get('success', False)
                    print(f"   Success: {standalone_success}")
                except:
                    print(f"   Raw output: {result.stdout}")
                    standalone_success = False
            else:
                print(f"   Error: {result.stderr}")
                standalone_success = False
                
        except Exception as e:
            print(f"   Error running standalone: {e}")
            standalone_success = False
        finally:
            # Clean up
            if os.path.exists(script_path):
                os.remove(script_path)
        
        # Test 3: Check environment differences
        print(f"\n3️⃣ ENVIRONMENT COMPARISON:")
        
        print(f"   Python version: {sys.version}")
        print(f"   Requests version: {requests.__version__}")
        
        # Check if there are any Django-specific settings affecting requests
        import django
        from django.conf import settings as django_settings
        
        print(f"   Django version: {django.get_version()}")
        print(f"   Django DEBUG: {getattr(django_settings, 'DEBUG', 'Unknown')}")
        
        # Check for proxy settings
        print(f"   HTTP_PROXY: {os.environ.get('HTTP_PROXY', 'Not set')}")
        print(f"   HTTPS_PROXY: {os.environ.get('HTTPS_PROXY', 'Not set')}")
        
        # Test 4: Check if there's a difference in request session
        print(f"\n4️⃣ SESSION vs NO SESSION:")
        
        # Without session
        try:
            resp_no_session = requests.post(
                'https://api.fonnte.com/send',
                headers={'Authorization': 'urWuiF1pMJyGM25uJEjA'},
                data={
                    'target': '6283838786991',
                    'message': 'Test no session',
                    'countryCode': '62'
                }
            )
            no_session_success = resp_no_session.json().get('status', False) if resp_no_session.status_code == 200 else False
            print(f"   No session success: {no_session_success}")
        except Exception as e:
            print(f"   No session error: {e}")
            no_session_success = False
        
        # With session
        try:
            session = requests.Session()
            resp_with_session = session.post(
                'https://api.fonnte.com/send',
                headers={'Authorization': 'urWuiF1pMJyGM25uJEjA'},
                data={
                    'target': '6283838786991',
                    'message': 'Test with session',
                    'countryCode': '62'
                }
            )
            with_session_success = resp_with_session.json().get('status', False) if resp_with_session.status_code == 200 else False
            print(f"   With session success: {with_session_success}")
        except Exception as e:
            print(f"   With session error: {e}")
            with_session_success = False
        
        # Analysis
        print(f"\n🎯 ANALYSIS:")
        print(f"Django command: {'✅ SUCCESS' if django_success else '❌ FAILED'}")
        print(f"Standalone script: {'✅ SUCCESS' if standalone_success else '❌ FAILED'}")
        print(f"No session: {'✅ SUCCESS' if no_session_success else '❌ FAILED'}")
        print(f"With session: {'✅ SUCCESS' if with_session_success else '❌ FAILED'}")
        
        if django_success and not standalone_success:
            print("🚨 STANDALONE SCRIPT GAGAL - masalah di environment")
        elif not django_success and standalone_success:
            print("🚨 DJANGO CONTEXT MENYEBABKAN MASALAH!")
            print("   → Ada middleware atau setting Django yang interfere")
        elif all([django_success, standalone_success, no_session_success, with_session_success]):
            print("✅ SEMUA METHOD BERHASIL")
            print("   → Masalah BUKAN di cara pemanggilan API")
            print("   → Kemungkinan masalah di:")
            print("     - Timing/race condition")
            print("     - Fonnte internal processing")
            print("     - Database logging issue")
        else:
            print("❌ ADA INKONSISTENSI - perlu investigasi lebih lanjut")
        
        print(f"\n💡 REKOMENDASI:")
        if django_success:
            print("1. API call dari Django berhasil")
            print("2. Masalah mungkin di logging atau database")
            print("3. Cek apakah OnboardingDelivery record tersimpan")
            print("4. Cek apakah ada error di level aplikasi")
        else:
            print("1. Ada masalah di level Django")
            print("2. Cek middleware yang mungkin interfere")
            print("3. Cek proxy atau network settings")
            print("4. Cek Django logging configuration")