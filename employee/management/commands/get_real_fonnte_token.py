from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Guide to get real Fonnte token'

    def handle(self, *args, **options):
        self.stdout.write("🔑 How to Get Real Fonnte Token")
        
        self.stdout.write("\n📋 Step-by-Step Guide:")
        
        self.stdout.write("\n1️⃣ Login to Fonnte Dashboard")
        self.stdout.write("   • Go to: https://console.fonnte.com")
        self.stdout.write("   • Login with your account")
        self.stdout.write("   • If no account, register first")
        
        self.stdout.write("\n2️⃣ Get Your API Token")
        self.stdout.write("   • Look for 'API Token' or 'Token' section")
        self.stdout.write("   • Copy the token (usually starts with letters/numbers)")
        self.stdout.write("   • Token format example: 'abc123def456ghi789'")
        
        self.stdout.write("\n3️⃣ Connect WhatsApp Device")
        self.stdout.write("   • Scan QR code to connect your WhatsApp")
        self.stdout.write("   • Make sure device status shows 'Connected'")
        self.stdout.write("   • Keep the phone online and WhatsApp active")
        
        self.stdout.write("\n4️⃣ Check Account Balance/Quota")
        self.stdout.write("   • Ensure you have sufficient balance")
        self.stdout.write("   • Check quota limits")
        self.stdout.write("   • Top up if necessary")
        
        self.stdout.write("\n5️⃣ Update .env File")
        self.stdout.write("   • Open .env file in your project")
        self.stdout.write("   • Find line: WHATSAPP_SERVICE_TOKEN=urWuiF1pMJyGM25uJEjA")
        self.stdout.write("   • Replace with: WHATSAPP_SERVICE_TOKEN=[YOUR_REAL_TOKEN]")
        self.stdout.write("   • Save the file")
        
        self.stdout.write("\n6️⃣ Restart and Test")
        self.stdout.write("   • Restart Django server")
        self.stdout.write("   • Run: python manage.py final_test")
        self.stdout.write("   • Check Fonnte dashboard for message history")
        
        self.stdout.write("\n🚨 IMPORTANT NOTES:")
        self.stdout.write("   • Token 'urWuiF1pMJyGM25uJEjA' is DUMMY/EXAMPLE token")
        self.stdout.write("   • It will never work with real Fonnte API")
        self.stdout.write("   • You MUST use your own Fonnte account token")
        self.stdout.write("   • Keep your real token secret and secure")
        
        self.stdout.write("\n🔍 How to Verify Token is Real:")
        self.stdout.write("   • Real token is usually longer than dummy")
        self.stdout.write("   • Real token has random letters/numbers")
        self.stdout.write("   • Real token works in Fonnte dashboard")
        self.stdout.write("   • Messages appear in Fonnte message history")
        
        self.stdout.write("\n💡 Troubleshooting:")
        self.stdout.write("   • If no Fonnte account: Create free account")
        self.stdout.write("   • If token not working: Check account status")
        self.stdout.write("   • If device disconnected: Scan QR code again")
        self.stdout.write("   • If no balance: Top up your account")
        
        self.stdout.write("\n🎯 Current Status:")
        self.stdout.write("   ❌ Using DUMMY token: urWuiF1pMJyGM25uJEjA")
        self.stdout.write("   🛠️ Need to replace with REAL Fonnte token")
        self.stdout.write("   ✅ System is ready - just need real token!")
        
        self.stdout.write("\n📞 Alternative Solutions:")
        self.stdout.write("   • Use different WhatsApp gateway (Wablas, etc.)")
        self.stdout.write("   • Use WhatsApp Business API directly")
        self.stdout.write("   • Use SMS gateway as backup")
        self.stdout.write("   • Disable WhatsApp and use email only")
        
        # Show current .env content
        self.stdout.write("\n📄 Current .env file content:")
        try:
            with open('.env', 'r') as f:
                for line_num, line in enumerate(f, 1):
                    if 'WHATSAPP_SERVICE_TOKEN' in line:
                        self.stdout.write(f"   Line {line_num}: {line.strip()}")
                        if 'urWuiF1pMJyGM25uJEjA' in line:
                            self.stdout.write("   ❌ This is the DUMMY token that needs to be replaced!")
                        break
        except:
            self.stdout.write("   ❌ Could not read .env file")
        
        self.stdout.write("\n🔄 After getting real token:")
        self.stdout.write("   1. Update .env file with real token")
        self.stdout.write("   2. Restart Django server")
        self.stdout.write("   3. Run: python manage.py final_test")
        self.stdout.write("   4. Check Fonnte dashboard")
        self.stdout.write("   5. Check WhatsApp on target phone")
        self.stdout.write("   6. Test web interface resend button")