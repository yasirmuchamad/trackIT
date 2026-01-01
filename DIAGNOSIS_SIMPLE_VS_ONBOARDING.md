# Diagnosis: Simple Test Works vs Onboarding Fails

## Situasi Saat Ini
- ✅ `simple_whatsapp_test` → WhatsApp sampai
- ✅ `debug_fonnte` → WhatsApp sampai  
- ❌ Sistem onboarding → WhatsApp tidak sampai (meski log sukses)

## Kemungkinan Penyebab

### 1. **Perbedaan Format Pesan**

**Simple Test Message:**
```
🧪 Test dari TrackIT System

Waktu: 2025-12-30 21:30:00
Nomor: 6283838786991

Jika Anda menerima pesan ini, konfigurasi WhatsApp berhasil!
```

**Onboarding Message:**
```
Halo [Employee Name]! 👋

Selamat bergabung di perusahaan kami! 

Silakan lengkapi data onboarding Anda melalui link berikut:
http://localhost:8000/onboarding/[token]/

Link ini berlaku hingga: [date]

Jika ada pertanyaan, silakan hubungi HR.

Terima kasih! 🙏
```

**Kemungkinan masalah:**
- Pesan onboarding lebih panjang
- Mengandung link URL
- Format yang lebih "promotional"
- WhatsApp menganggap spam

### 2. **Perbedaan Phone Number Formatting**

**Simple Test:**
```python
phone = '6283838786991'  # Hardcoded
```

**Onboarding System:**
```python
clean_phone = ''.join(filter(str.isdigit, phone))
if clean_phone.startswith('0'):
    clean_phone = '62' + clean_phone[1:]
elif not clean_phone.startswith('62'):
    clean_phone = '62' + clean_phone
```

**Kemungkinan masalah:**
- Format berbeda menghasilkan nomor berbeda
- Salah satu format tidak valid

### 3. **Perbedaan Request Parameters**

**Simple Test:**
```python
data = {
    'target': phone,
    'message': message,
    'countryCode': '62',
}
```

**Onboarding (via send_via_fonnte):**
```python
data = {
    'target': phone,
    'message': message,
    'countryCode': '62',
}
```

Seharusnya sama, tapi perlu diverifikasi.

### 4. **Perbedaan Timing/Rate Limiting**

- Simple test: sekali kirim
- Onboarding: mungkin ada multiple requests
- WhatsApp rate limiting
- Fonnte quota per menit

## Langkah Debugging

### Step 1: Test Message Content
```bash
python manage.py compare_messages --phone 083838786991
```

Ini akan mengirim:
1. Simple message (seperti debug_fonnte)
2. Full onboarding message
3. Onboarding tanpa link
4. Onboarding sangat sederhana

### Step 2: Test Phone Formats
```bash
python manage.py test_phone_formats --phone 083838786991
```

Ini akan test berbagai format nomor:
- 083838786991
- 6283838786991
- +6283838786991
- dll

### Step 3: Monitor Real-time
```bash
tail -f logs/onboarding.log
```

Lalu jalankan onboarding resend dan bandingkan dengan simple test.

### Step 4: Direct Comparison
Buat test yang menggunakan PERSIS parameter yang sama:

```python
# Test A: Simple (working)
requests.post(url, data={
    'target': '6283838786991',
    'message': 'Simple test',
    'countryCode': '62'
}, headers={'Authorization': token})

# Test B: Onboarding (not working)  
requests.post(url, data={
    'target': formatted_phone,
    'message': onboarding_message,
    'countryCode': '62'
}, headers={'Authorization': token})
```

## Hipotesis Utama

### Hipotesis 1: Message Content Issue
WhatsApp memblokir pesan onboarding karena:
- Mengandung link
- Terlalu panjang
- Format promotional
- Kata-kata trigger spam

**Test:** Kirim onboarding message tanpa link

### Hipotesis 2: Phone Format Issue
Format nomor berbeda antara simple test vs onboarding:
- Simple: hardcoded '6283838786991'
- Onboarding: hasil formatting dari '083838786991'

**Test:** Pastikan kedua menggunakan format yang sama

### Hipotesis 3: Rate Limiting
Onboarding sering dipanggil berulang, menyebabkan rate limit.

**Test:** Tunggu beberapa menit antara test

### Hipotesis 4: Context/Environment
Ada perbedaan environment saat command vs web request.

**Test:** Jalankan simulate_resend_button command

## Action Plan

1. **Jalankan compare_messages** - identifikasi apakah masalah di content
2. **Jalankan test_phone_formats** - identifikasi apakah masalah di format nomor
3. **Bandingkan log detail** - lihat perbedaan request parameters
4. **Test dengan nomor berbeda** - pastikan bukan masalah nomor spesifik

## Expected Results

Jika **compare_messages** menunjukkan:
- Simple works, onboarding fails → **Content issue**
- Simple works, onboarding no-link works → **Link issue**  
- All fail → **Configuration issue**
- All work → **Timing/rate limiting issue**

Jika **test_phone_formats** menunjukkan:
- Multiple formats work → **Not phone format issue**
- Only one format works → **Phone formatting issue**
- None work → **Number/account issue**