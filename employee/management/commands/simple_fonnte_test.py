from django.core.management.base import BaseCommand
import requests


class Command(BaseCommand):
    help = 'Simple Fonnte test'

    def handle(self, *args, **options):
        self.stdout.write("🧪 Simple Fonnte Test")
        
        token = 'urWuiF1pMJyGM25uJEjA'
        
        # Test 1: Profile check
        self.stdout.write("\n1. Profile Check:")
        try:
            r = requests.get('https://api.fonnte.com/profile', 
                           headers={'Authorization': token})
            self.stdout.write(f"Status: {r.status_code}")
            self.stdout.write(f"Response: {r.text}")
        except Exception as e:
            self.stdout.write(f"Error: {e}")
        
        # Test 2: Send message
        self.stdout.write("\n2. Send Message:")
        try:
            r = requests.post('https://api.fonnte.com/send',
                            headers={'Authorization': token},
                            data={
                                'target': '6283838786991',
                                'message': 'Test simple',
                                'countryCode': '62'
                            })
            self.stdout.write(f"Status: {r.status_code}")
            self.stdout.write(f"Response: {r.text}")
        except Exception as e:
            self.stdout.write(f"Error: {e}")
        
        self.stdout.write("\n💡 Check Fonnte dashboard for results")