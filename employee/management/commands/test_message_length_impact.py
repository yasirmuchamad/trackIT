from django.core.management.base import BaseCommand
import requests
import time

class Command(BaseCommand):
    help = 'Test if message length or content affects delivery to Fonnte history'

    def handle(self, *args, **options):
        print("🔍 TEST DAMPAK PANJANG PESAN TERHADAP DELIVERY")
        print("=" * 60)
        
        token = 'urWuiF1pMJyGM25uJEjA'
        target = '6283838786991'
        
        # Test messages with increasing complexity
        test_messages = [
            {
                'name': 'Simple Short',
                'message': 'Test simple'
            },
            {
                'name': 'Medium Text',
                'message': 'Halo! Ini adalah test pesan dengan panjang sedang untuk melihat apakah ada perbedaan.'
            },
            {
                'name': 'Long Text No Link',
                'message': '''Halo Test User! 👋

Selamat bergabung di perusahaan kami! 

Silakan lengkapi data onboarding Anda.

Jika ada pertanyaan, silakan hubungi HR.

Terima kasih! 🙏'''
            },
            {
                'name': 'Long Text With Link',
                'message': '''Halo Test User! 👋

Selamat bergabung di perusahaan kami! 

Silakan lengkapi data onboarding Anda melalui link berikut:
http://localhost:8000/onboarding/test-token/

Link ini berlaku hingga: 2026-01-02

Jika ada pertanyaan, silakan hubungi HR.

Terima kasih! 🙏'''
            },
            {
                'name': 'Exact Onboarding Format',
                'message': '''Halo Abe Ryan Anwar! 👋

Selamat bergabung di perusahaan kami! 

Silakan lengkapi data onboarding Anda melalui link berikut:
http://localhost:8000/onboarding/53c44e3f-b4cf-40d7-922a-aa10ad5a5278/

Link ini berlaku hingga: 02 January 2026, 07:11

Jika ada pertanyaan, silakan hubungi HR.

Terima kasih! 🙏'''
            }
        ]
        
        results = []
        
        for i, test in enumerate(test_messages, 1):
            print(f"\n{i}️⃣ TEST: {test['name']}")
            print("-" * 30)
            print(f"Panjang pesan: {len(test['message'])} karakter")
            print(f"Jumlah baris: {test['message'].count(chr(10)) + 1}")
            print(f"Ada link: {'http' in test['message']}")
            
            try:
                # Send message
                response = requests.post(
                    'https://api.fonnte.com/send',
                    headers={'Authorization': token},
                    data={
                        'target': target,
                        'message': test['message'],
                        'countryCode': '62'
                    }
                )
                
                print(f"Status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    success = result.get('status', False)
                    message_id = result.get('id', [])
                    
                    print(f"API Success: {success}")
                    print(f"Message ID: {message_id}")
                    print(f"Response: {response.text}")
                    
                    results.append({
                        'test': test['name'],
                        'length': len(test['message']),
                        'has_link': 'http' in test['message'],
                        'api_success': success,
                        'message_id': message_id,
                        'response': result
                    })
                    
                    if success:
                        print("✅ API mengembalikan SUCCESS")
                    else:
                        print("❌ API mengembalikan FAILED")
                else:
                    print(f"❌ HTTP Error: {response.status_code}")
                    print(f"Response: {response.text}")
                    
                    results.append({
                        'test': test['name'],
                        'length': len(test['message']),
                        'has_link': 'http' in test['message'],
                        'api_success': False,
                        'message_id': None,
                        'response': response.text
                    })
                
                # Wait between requests to avoid rate limiting
                if i < len(test_messages):
                    print("⏳ Menunggu 3 detik...")
                    time.sleep(3)
                    
            except Exception as e:
                print(f"❌ Error: {e}")
                results.append({
                    'test': test['name'],
                    'length': len(test['message']),
                    'has_link': 'http' in test['message'],
                    'api_success': False,
                    'message_id': None,
                    'response': str(e)
                })
        
        # Summary
        print("\n📊 RINGKASAN HASIL")
        print("=" * 60)
        print(f"{'Test':<20} {'Length':<8} {'Link':<6} {'API Success':<12} {'Message ID'}")
        print("-" * 60)
        
        for result in results:
            link_status = "Yes" if result['has_link'] else "No"
            api_status = "✅ Yes" if result['api_success'] else "❌ No"
            msg_id = str(result['message_id']) if result['message_id'] else "None"
            
            print(f"{result['test']:<20} {result['length']:<8} {link_status:<6} {api_status:<12} {msg_id}")
        
        # Analysis
        print("\n🎯 ANALISIS")
        print("-" * 30)
        
        successful_tests = [r for r in results if r['api_success']]
        failed_tests = [r for r in results if not r['api_success']]
        
        print(f"✅ Berhasil: {len(successful_tests)}/{len(results)} test")
        print(f"❌ Gagal: {len(failed_tests)}/{len(results)} test")
        
        if successful_tests:
            avg_length_success = sum(r['length'] for r in successful_tests) / len(successful_tests)
            print(f"📏 Rata-rata panjang pesan yang berhasil: {avg_length_success:.0f} karakter")
            
            link_success = sum(1 for r in successful_tests if r['has_link'])
            print(f"🔗 Pesan dengan link yang berhasil: {link_success}/{len(successful_tests)}")
        
        if failed_tests:
            avg_length_failed = sum(r['length'] for r in failed_tests) / len(failed_tests)
            print(f"📏 Rata-rata panjang pesan yang gagal: {avg_length_failed:.0f} karakter")
            
            link_failed = sum(1 for r in failed_tests if r['has_link'])
            print(f"🔗 Pesan dengan link yang gagal: {link_failed}/{len(failed_tests)}")
        
        print("\n💡 KESIMPULAN:")
        if all(r['api_success'] for r in results):
            print("✅ Semua test berhasil - masalah BUKAN di panjang pesan atau link")
            print("   → Masalah kemungkinan di device Fonnte atau delivery ke WhatsApp")
        elif any(not r['api_success'] for r in results):
            print("❌ Ada test yang gagal - analisis pola kegagalan:")
            for result in failed_tests:
                print(f"   - {result['test']}: {result['response']}")
        
        print("\n🔍 LANGKAH SELANJUTNYA:")
        print("1. Cek dashboard Fonnte untuk melihat apakah pesan muncul di history")
        print("2. Jika muncul di history tapi tidak terkirim, masalah di device WhatsApp")
        print("3. Jika tidak muncul di history, masalah di API atau konfigurasi")
        print("4. Bandingkan hasil ini dengan log sistem onboarding")