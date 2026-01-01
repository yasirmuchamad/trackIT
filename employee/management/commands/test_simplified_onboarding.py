from django.core.management.base import BaseCommand
import requests

class Command(BaseCommand):
    help = 'Test simplified onboarding message without link'

    def handle(self, *args, **options):
        print("🧪 TEST PESAN ONBOARDING YANG DISEDERHANAKAN")
        print("=" * 50)
        
        token = 'urWuiF1pMJyGM25uJEjA'
        target = '6283838786991'
        
        # Test different versions of onboarding message
        test_messages = [
            {
                'name': 'Original Simple (Working)',
                'message': 'Test simple'
            },
            {
                'name': 'Simple Onboarding',
                'message': 'Halo! Selamat bergabung di perusahaan kami. Silakan hubungi HR untuk onboarding.'
            },
            {
                'name': 'With Emoji Only',
                'message': 'Halo! 👋 Selamat bergabung di perusahaan kami. Terima kasih! 🙏'
            },
            {
                'name': 'With Link Only',
                'message': 'Silakan klik link berikut: http://localhost:8000/onboarding/test/'
            },
            {
                'name': 'Multi-line No Link',
                'message': '''Halo Test User!

Selamat bergabung di perusahaan kami!

Silakan hubungi HR untuk melengkapi data onboarding.

Terima kasih!'''
            },
            {
                'name': 'Full Original (Problematic)',
                'message': '''Halo Test User! 👋

Selamat bergabung di perusahaan kami! 

Silakan lengkapi data onboarding Anda melalui link berikut:
http://localhost:8000/onboarding/test-token/

Link ini berlaku hingga: 02 January 2026, 07:11

Jika ada pertanyaan, silakan hubungi HR.

Terima kasih! 🙏'''
            }
        ]
        
        results = []
        
        for i, test in enumerate(test_messages, 1):
            print(f"\n{i}️⃣ {test['name']}")
            print("-" * 30)
            print(f"Panjang: {len(test['message'])} karakter")
            print(f"Baris: {test['message'].count(chr(10)) + 1}")
            print(f"Link: {'http' in test['message']}")
            print(f"Emoji: {'👋' in test['message'] or '🙏' in test['message']}")
            
            try:
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
                    
                    print(f"Success: {success}")
                    print(f"Message ID: {message_id}")
                    
                    results.append({
                        'name': test['name'],
                        'length': len(test['message']),
                        'lines': test['message'].count('\n') + 1,
                        'has_link': 'http' in test['message'],
                        'has_emoji': '👋' in test['message'] or '🙏' in test['message'],
                        'success': success,
                        'message_id': message_id
                    })
                    
                    if success:
                        print("✅ SUCCESS")
                    else:
                        print("❌ FAILED")
                        print(f"Response: {response.text}")
                else:
                    print(f"❌ HTTP Error: {response.status_code}")
                    results.append({
                        'name': test['name'],
                        'length': len(test['message']),
                        'lines': test['message'].count('\n') + 1,
                        'has_link': 'http' in test['message'],
                        'has_emoji': '👋' in test['message'] or '🙏' in test['message'],
                        'success': False,
                        'message_id': None
                    })
                
            except Exception as e:
                print(f"❌ Error: {e}")
                results.append({
                    'name': test['name'],
                    'length': len(test['message']),
                    'lines': test['message'].count('\n') + 1,
                    'has_link': 'http' in test['message'],
                    'has_emoji': '👋' in test['message'] or '🙏' in test['message'],
                    'success': False,
                    'message_id': None
                })
        
        # Analysis
        print("\n📊 ANALISIS HASIL")
        print("=" * 50)
        print(f"{'Test':<25} {'Len':<4} {'Line':<4} {'Link':<4} {'Emoji':<5} {'Success'}")
        print("-" * 50)
        
        for r in results:
            link = "Yes" if r['has_link'] else "No"
            emoji = "Yes" if r['has_emoji'] else "No"
            success = "✅" if r['success'] else "❌"
            
            print(f"{r['name']:<25} {r['length']:<4} {r['lines']:<4} {link:<4} {emoji:<5} {success}")
        
        # Find patterns
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        print(f"\n🎯 POLA YANG DITEMUKAN:")
        print(f"✅ Berhasil: {len(successful)}/{len(results)}")
        print(f"❌ Gagal: {len(failed)}/{len(results)}")
        
        if successful and failed:
            print(f"\n📏 Panjang rata-rata:")
            print(f"   Berhasil: {sum(r['length'] for r in successful) / len(successful):.0f} karakter")
            print(f"   Gagal: {sum(r['length'] for r in failed) / len(failed):.0f} karakter")
            
            print(f"\n🔗 Link:")
            success_with_link = sum(1 for r in successful if r['has_link'])
            failed_with_link = sum(1 for r in failed if r['has_link'])
            print(f"   Berhasil dengan link: {success_with_link}/{len(successful)}")
            print(f"   Gagal dengan link: {failed_with_link}/{len(failed)}")
            
            print(f"\n😀 Emoji:")
            success_with_emoji = sum(1 for r in successful if r['has_emoji'])
            failed_with_emoji = sum(1 for r in failed if r['has_emoji'])
            print(f"   Berhasil dengan emoji: {success_with_emoji}/{len(successful)}")
            print(f"   Gagal dengan emoji: {failed_with_emoji}/{len(failed)}")
        
        print(f"\n💡 KESIMPULAN:")
        if all(r['success'] for r in results):
            print("✅ Semua test berhasil - masalah BUKAN di content pesan")
            print("   → Masalah di device Fonnte atau delivery ke WhatsApp")
        else:
            print("❌ Ada pola kegagalan berdasarkan content:")
            for r in failed:
                factors = []
                if r['length'] > 100:
                    factors.append("panjang")
                if r['has_link']:
                    factors.append("link")
                if r['has_emoji']:
                    factors.append("emoji")
                if r['lines'] > 3:
                    factors.append("multi-line")
                
                print(f"   - {r['name']}: {', '.join(factors) if factors else 'unknown'}")
        
        print(f"\n🔧 REKOMENDASI:")
        if failed:
            print("1. Gunakan pesan yang lebih sederhana untuk onboarding")
            print("2. Hindari link langsung dalam pesan WhatsApp")
            print("3. Kurangi penggunaan emoji")
            print("4. Buat pesan lebih pendek")
        else:
            print("1. Cek dashboard Fonnte untuk delivery status")
            print("2. Verifikasi device WhatsApp Business online")
            print("3. Cek quota dan balance akun")