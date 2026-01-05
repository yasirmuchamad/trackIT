from django.core.management.base import BaseCommand
import requests
import json


class Command(BaseCommand):
    help = 'Debug Fonnte API directly'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Direct Fonnte API Debug")
        
        token = 'urWuiF1pMJyGM25uJEjA'
        
        # Step 1: Check account profile
        self.stdout.write("\n📊 Checking Account Profile...")
        try:
            response = requests.get('https://api.fonnte.com/profile', 
                                  headers={'Authorization': token}, 
                                  timeout=10)
            
            self.stdout.write(f"Profile Status: {response.status_code}")
            self.stdout.write(f"Profile Response: {response.text}")
            
            if response.status_code == 200:
                try:
                    profile = response.json()
                    self.stdout.write("Account Info:")
                    for key, value in profile.items():
                        self.stdout.write(f"  {key}: {value}")
                except:
                    self.stdout.write("Non-JSON response")
            
        except Exception as e:
            self.stdout.write(f"Error: {str(e)}")
        
        # Step 2: Send test message
        self.stdout.write("\n📤 Sending Test Message...")
        try:
            url = 'https://api.fonnte.com/send'
            headers = {'Authorization': token}
            data = {
                'target': '6283838786991',
                'message': '🧪 Direct test from debug command',
                'countryCode': '62',
            }
            
            response = requests.post(url, data=data, headers=headers, timeout=30)
            
            self.stdout.write(f"Send Status: {response.status_code}")
            self.stdout.write(f"Send Response: {response.text}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get('status'):
                        self.stdout.write("✅ Message sent successfully!")
                        if 'id' in result:
                            self.stdout.write(f"Message ID: {result['id']}")
                    else:
                        self.stdout.write(f"❌ Send failed: {result}")
                except:
                    self.stdout.write("Non-JSON response")
            
        except Exception as e:
            self.stdout.write(f"Error: {str(e)}")
        
        # Step 3: Check message history
        self.stdout.write("\n📜 Checking Message History...")
        try:
            response = requests.get('https://api.fonnte.com/history', 
                                  headers={'Authorization': token}, 
                                  timeout=10)
            
            self.stdout.write(f"History Status: {response.status_code}")
            self.stdout.write(f"History Response: {response.text}")
            
        except Exception as e:
            self.stdout.write(f"Error: {str(e)}")
        
        self.stdout.write("\n🎯 Analysis:")
        self.stdout.write("1. Check if profile shows device connected")
        self.stdout.write("2. Check if send returns success with message ID")
        self.stdout.write("3. Check if message appears in history")
        self.stdout.write("4. If API works but WhatsApp doesn't receive:")
        self.stdout.write("   - Device disconnected from WhatsApp")
        self.stdout.write("   - Phone number issues")
        self.stdout.write("   - Account quota/balance issues")