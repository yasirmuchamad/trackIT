from django.core.management.base import BaseCommand
from django.conf import settings
import requests
import json
import time

class Command(BaseCommand):
    help = 'Deep comparison of API calls - byte by byte analysis'

    def handle(self, *args, **options):
        print("🔬 ANALISIS MENDALAM - BYTE BY BYTE COMPARISON")
        print("=" * 60)
        
        # Get exact values
        settings_token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', '')
        settings_url = getattr(settings, 'WHATSAPP_SERVICE_URL', '')
        hardcoded_token = 'urWuiF1pMJyGM25uJEjA'
        hardcoded_url = 'https://api.fonnte.com/send'
        
        print(f"🔍 PERBANDINGAN KONFIGURASI:")
        print(f"Settings URL: '{settings_url}'")
        print(f"Hardcoded URL: '{hardcoded_url}'")
        print(f"URL Match: {settings_url == hardcoded_url}")
        
        print(f"Settings Token: '{settings_token}'")
        print(f"Hardcoded Token: '{hardcoded_token}'")
        print(f"Token Match: {settings_token == hardcoded_token}")
        
        if settings_token != hardcoded_token:
            print("🚨 MASALAH DITEMUKAN: TOKEN BERBEDA!")
            print("Ini penyebab utama masalah")
            return
        
        # Test with identical parameters
        target = '6283838786991'
        message = 'Test identical call'
        
        print(f"\n🧪 TEST DENGAN PARAMETER IDENTIK:")
        print(f"Target: {target}")
        print(f"Message: {message}")
        
        # Method 1: Exact simple_fonnte_test replication
        print(f"\n1️⃣ METHOD SIMPLE_FONNTE_TEST (EXACT COPY):")
        try:
            # Exact copy from simple_fonnte_test.py
            r1 = requests.post('https://api.fonnte.com/send',
                            headers={'Authorization': 'urWuiF1pMJyGM25uJEjA'},
                            data={
                                'target': '6283838786991',
                                'message': 'Test simple',
                                'countryCode': '62'
                            })
            
            print(f"   Status: {r1.status_code}")
            print(f"   Headers: {dict(r1.headers)}")
            print(f"   Response: {r1.text}")
            
            if r1.status_code == 200:
                result1 = r1.json()
                success1 = result1.get('status', False)
                print(f"   Success: {success1}")
                print(f"   Message ID: {result1.get('id', 'None')}")
            else:
                success1 = False
                
        except Exception as e:
            print(f"   Error: {e}")
            success1 = False
        
        time.sleep(2)  # Wait between calls
        
        # Method 2: Exact onboarding system replication
        print(f"\n2️⃣ METHOD ONBOARDING SYSTEM (EXACT COPY):")
        try:
            # Exact copy from send_via_fonnte function
            url = getattr(settings, 'WHATSAPP_SERVICE_URL', 'https://api.fonnte.com/send')
            token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', '')
            
            headers = {
                'Authorization': token,
            }
            
            data = {
                'target': '6283838786991',
                'message': 'Test simple',  # Same message as method 1
                'countryCode': '62',
            }
            
            print(f"   URL: {url}")
            print(f"   Headers: {headers}")
            print(f"   Data: {data}")
            
            r2 = requests.post(url, data=data, headers=headers, timeout=30)
            
            print(f"   Status: {r2.status_code}")
            print(f"   Headers: {dict(r2.headers)}")
            print(f"   Response: {r2.text}")
            
            if r2.status_code == 200:
                result2 = r2.json()
                success2 = result2.get('status', False)
                print(f"   Success: {success2}")
                print(f"   Message ID: {result2.get('id', 'None')}")
            else:
                success2 = False
                
        except Exception as e:
            print(f"   Error: {e}")
            success2 = False
        
        # Compare responses byte by byte
        print(f"\n🔍 BYTE-BY-BYTE COMPARISON:")
        if 'r1' in locals() and 'r2' in locals():
            print(f"Response 1 length: {len(r1.text)}")
            print(f"Response 2 length: {len(r2.text)}")
            print(f"Response identical: {r1.text == r2.text}")
            
            if r1.text != r2.text:
                print("🚨 RESPONSES BERBEDA!")
                print(f"Response 1: {repr(r1.text)}")
                print(f"Response 2: {repr(r2.text)}")
        
        # Check request details
        print(f"\n🔍 REQUEST DETAILS COMPARISON:")
        
        # Method 3: Manual request building to see exact differences
        print(f"\n3️⃣ MANUAL REQUEST BUILDING:")
        
        import urllib.parse
        
        # Build request exactly like simple_fonnte_test
        simple_data = {
            'target': '6283838786991',
            'message': 'Test manual simple',
            'countryCode': '62'
        }
        simple_headers = {'Authorization': 'urWuiF1pMJyGM25uJEjA'}
        
        print(f"Simple data: {simple_data}")
        print(f"Simple headers: {simple_headers}")
        print(f"Simple encoded: {urllib.parse.urlencode(simple_data)}")
        
        # Build request exactly like onboarding
        onboarding_data = {
            'target': '6283838786991',
            'message': 'Test manual onboarding',
            'countryCode': '62',
        }
        onboarding_headers = {
            'Authorization': getattr(settings, 'WHATSAPP_SERVICE_TOKEN', ''),
        }
        
        print(f"Onboarding data: {onboarding_data}")
        print(f"Onboarding headers: {onboarding_headers}")
        print(f"Onboarding encoded: {urllib.parse.urlencode(onboarding_data)}")
        
        # Check for hidden differences
        print(f"\n🔍 HIDDEN DIFFERENCES CHECK:")
        
        # Check for extra whitespace or characters
        simple_token = 'urWuiF1pMJyGM25uJEjA'
        settings_token_clean = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', '').strip()
        
        print(f"Simple token repr: {repr(simple_token)}")
        print(f"Settings token repr: {repr(settings_token_clean)}")
        print(f"Token bytes equal: {simple_token.encode() == settings_token_clean.encode()}")
        
        # Check URL differences
        simple_url = 'https://api.fonnte.com/send'
        settings_url_clean = getattr(settings, 'WHATSAPP_SERVICE_URL', '').strip()
        
        print(f"Simple URL repr: {repr(simple_url)}")
        print(f"Settings URL repr: {repr(settings_url_clean)}")
        print(f"URL bytes equal: {simple_url.encode() == settings_url_clean.encode()}")
        
        # Final test with absolutely identical parameters
        print(f"\n4️⃣ FINAL TEST - ABSOLUTELY IDENTICAL:")
        
        # Use exact same variables
        test_url = 'https://api.fonnte.com/send'
        test_token = 'urWuiF1pMJyGM25uJEjA'
        test_target = '6283838786991'
        test_message = 'Final identical test'
        
        # Test A: Simple style
        try:
            rA = requests.post(test_url,
                            headers={'Authorization': test_token},
                            data={
                                'target': test_target,
                                'message': test_message,
                                'countryCode': '62'
                            })
            print(f"Test A Status: {rA.status_code}")
            print(f"Test A Response: {rA.text}")
            successA = rA.json().get('status', False) if rA.status_code == 200 else False
        except Exception as e:
            print(f"Test A Error: {e}")
            successA = False
        
        time.sleep(2)
        
        # Test B: Onboarding style with timeout
        try:
            rB = requests.post(test_url,
                            headers={'Authorization': test_token},
                            data={
                                'target': test_target,
                                'message': test_message,
                                'countryCode': '62'
                            },
                            timeout=30)
            print(f"Test B Status: {rB.status_code}")
            print(f"Test B Response: {rB.text}")
            successB = rB.json().get('status', False) if rB.status_code == 200 else False
        except Exception as e:
            print(f"Test B Error: {e}")
            successB = False
        
        print(f"\n🎯 FINAL RESULTS:")
        print(f"Test A (simple style): {'✅ SUCCESS' if successA else '❌ FAILED'}")
        print(f"Test B (onboarding style): {'✅ SUCCESS' if successB else '❌ FAILED'}")
        
        if successA and not successB:
            print("🚨 TIMEOUT PARAMETER MENYEBABKAN MASALAH!")
        elif not successA and successB:
            print("🚨 SIMPLE STYLE BERMASALAH!")
        elif successA and successB:
            print("✅ KEDUA STYLE BERHASIL - masalah di tempat lain")
        else:
            print("❌ KEDUA STYLE GAGAL - masalah di akun/koneksi")
        
        print(f"\n💡 NEXT STEPS:")
        print("1. Jika timeout menyebabkan masalah → hapus timeout dari onboarding")
        print("2. Jika kedua berhasil → masalah di logging atau database")
        print("3. Jika kedua gagal → masalah di akun Fonnte")
        print("4. Cek apakah ada middleware atau proxy yang interfere")