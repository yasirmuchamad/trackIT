from django.core.management.base import BaseCommand
from django.conf import settings
from employee.services.onboarding_delivery import send_via_fonnte
import os
import requests


class Command(BaseCommand):
    help = 'Check if we are using real Fonnte config or fallback values'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Checking Real Configuration vs Fallback...")
        
        # Check what send_via_fonnte actually uses
        self.stdout.write("\n📋 What send_via_fonnte function sees:")
        
        # This is exactly what send_via_fonnte does
        url = getattr(settings, 'WHATSAPP_SERVICE_URL', 'https://api.fonnte.com/send')
        token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', 'urWuiF1pMJyGM25uJEjA')
        
        self.stdout.write(f"   URL: {url}")
        self.stdout.write(f"   Token: {token}")
        
        # Check if these are fallback values
        if url == 'https://api.fonnte.com/send':
            self.stdout.write("   ⚠️ Using FALLBACK URL (not from .env)")
        else:
            self.stdout.write("   ✅ Using CUSTOM URL (from .env)")
            
        if token == 'urWuiF1pMJyGM25uJEjA':
            self.stdout.write("   ⚠️ Using FALLBACK TOKEN (not from .env)")
        else:
            self.stdout.write("   ✅ Using CUSTOM TOKEN (from .env)")
        
        # Check .env file directly
        self.stdout.write("\n📁 Direct .env file check:")
        
        try:
            with open('.env', 'r') as f:
                content = f.read()
                
            if 'WHATSAPP_SERVICE_URL=' in content:
                # Extract URL from .env
                for line in content.split('\n'):
                    if line.startswith('WHATSAPP_SERVICE_URL='):
                        env_url = line.split('=', 1)[1].strip()
                        self.stdout.write(f"   .env URL: {env_url}")
                        break
            else:
                self.stdout.write("   ❌ WHATSAPP_SERVICE_URL not found in .env")
                
            if 'WHATSAPP_SERVICE_TOKEN=' in content:
                # Extract token from .env
                for line in content.split('\n'):
                    if line.startswith('WHATSAPP_SERVICE_TOKEN='):
                        env_token = line.split('=', 1)[1].strip()
                        self.stdout.write(f"   .env Token: {env_token}")
                        break
            else:
                self.stdout.write("   ❌ WHATSAPP_SERVICE_TOKEN not found in .env")
                
        except FileNotFoundError:
            self.stdout.write("   ❌ .env file not found")
        except Exception as e:
            self.stdout.write(f"   ❌ Error reading .env: {str(e)}")
        
        # Test with both tokens
        self.stdout.write("\n🧪 Testing Both Configurations:")
        
        # Test 1: Fallback token
        self.stdout.write("\n📤 Test 1: Fallback Token")
        self.test_token('https://api.fonnte.com/send', 'urWuiF1pMJyGM25uJEjA', 'Fallback')
        
        # Test 2: Real token from .env
        try:
            with open('.env', 'r') as f:
                content = f.read()
                
            real_url = None
            real_token = None
            
            for line in content.split('\n'):
                if line.startswith('WHATSAPP_SERVICE_URL='):
                    real_url = line.split('=', 1)[1].strip()
                elif line.startswith('WHATSAPP_SERVICE_TOKEN='):
                    real_token = line.split('=', 1)[1].strip()
            
            if real_url and real_token:
                self.stdout.write("\n📤 Test 2: Real Token from .env")
                self.test_token(real_url, real_token, 'Real')
            else:
                self.stdout.write("\n⚠️ Test 2: Skipped - Real config not found in .env")
                
        except Exception as e:
            self.stdout.write(f"\n❌ Test 2: Error - {str(e)}")
        
        # Diagnosis
        self.stdout.write("\n🎯 DIAGNOSIS:")
        
        if url == 'https://api.fonnte.com/send' and token == 'urWuiF1pMJyGM25uJEjA':
            self.stdout.write("   ❌ PROBLEM: System is using FALLBACK values, not real Fonnte config!")
            self.stdout.write("   → This explains why dashboard shows no history")
            self.stdout.write("   → Fallback token is probably invalid/demo token")
            self.stdout.write("   → Need to fix Django settings to read .env properly")
        else:
            self.stdout.write("   ✅ System is using real configuration from .env")
            self.stdout.write("   → If dashboard still empty, check token validity")

    def test_token(self, url, token, label):
        """Test a specific token configuration"""
        try:
            headers = {'Authorization': token}
            data = {
                'target': '6283838786991',
                'message': f'Test {label} token - {self.get_current_time()}',
                'countryCode': '62',
            }
            
            self.stdout.write(f"   Sending with {label} config...")
            self.stdout.write(f"   URL: {url}")
            self.stdout.write(f"   Token: {token[:10]}...")
            
            response = requests.post(url, data=data, headers=headers, timeout=10)
            
            self.stdout.write(f"   Status: {response.status_code}")
            self.stdout.write(f"   Response: {response.text}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get('status'):
                        self.stdout.write(f"   ✅ {label} token: SUCCESS")
                        if 'id' in result:
                            self.stdout.write(f"   Message ID: {result['id']}")
                    else:
                        self.stdout.write(f"   ❌ {label} token: API ERROR - {result}")
                except:
                    self.stdout.write(f"   ⚠️ {label} token: Non-JSON response")
            else:
                self.stdout.write(f"   ❌ {label} token: HTTP ERROR")
                
        except Exception as e:
            self.stdout.write(f"   ❌ {label} token: EXCEPTION - {str(e)}")

    def get_current_time(self):
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")