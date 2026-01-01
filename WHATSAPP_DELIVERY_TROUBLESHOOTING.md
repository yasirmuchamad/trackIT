# WhatsApp Delivery Troubleshooting Guide

## Masalah: Log Sukses tapi WhatsApp Tidak Masuk

### Status Saat Ini ✅
- ✅ Konfigurasi Fonnte benar
- ✅ API call berhasil (status 200)
- ✅ Fonnte response "success: true"
- ❌ WhatsApp tidak sampai ke penerima

### Penyebab Umum

#### 1. **Device WhatsApp Business Tidak Terhubung**
Fonnte memerlukan device WhatsApp Business yang selalu online.

**Cek:**
```bash
python manage.py check_fonnte_account
```

**Solusi:**
- Login ke dashboard Fonnte
- Pastikan device status "Connected"
- Scan QR code jika perlu reconnect

#### 2. **Nomor Penerima Bermasalah**
- Nomor tidak terdaftar WhatsApp
- Nomor memblokir WhatsApp Business Anda
- Format nomor salah

**Test dengan nomor lain:**
```bash
python manage.py check_fonnte_account --phone 08123456789
```

#### 3. **Quota/Balance Habis**
Meskipun API return success, pesan tidak dikirim jika quota habis.

**Cek di dashboard Fonnte:**
- Sisa quota
- Balance account
- Package limits

#### 4. **WhatsApp Policy Violation**
WhatsApp memblokir pesan yang melanggar policy:
- Spam content
- Promotional messages tanpa opt-in
- Pesan terlalu panjang
- Link suspicious

#### 5. **Timing dan Rate Limiting**
- Terlalu banyak pesan dalam waktu singkat
- WhatsApp rate limiting
- Server delay

### Langkah Debugging

#### Step 1: Cek Account Status
```bash
python manage.py check_fonnte_account
```

Perhatikan:
- Device status: harus "connect"
- Quota: harus > 0
- Balance: harus sufficient

#### Step 2: Test dengan Nomor Berbeda
Test dengan nomor yang pasti aktif WhatsApp:
```bash
python manage.py check_fonnte_account --phone [nomor_anda_sendiri]
```

#### Step 3: Cek Dashboard Fonnte
Login ke https://console.fonnte.com:
- Lihat message history
- Cek delivery status
- Lihat error logs

#### Step 4: Test Message Content
Coba dengan pesan sederhana:
```bash
python manage.py debug_fonnte --phone [nomor_test]
```

#### Step 5: Monitor Real-time
```bash
tail -f logs/onboarding.log
```
Lalu kirim pesan dan lihat response detail.

### Response Fonnte yang Normal

#### Success Response:
```json
{
  "status": true,
  "id": "msg_12345",
  "detail": "Message sent successfully"
}
```

#### Error Response:
```json
{
  "status": false,
  "reason": "Invalid phone number"
}
```

### Solusi Berdasarkan Penyebab

#### Jika Device Disconnect:
1. Login dashboard Fonnte
2. Reconnect WhatsApp device
3. Scan QR code baru
4. Test ulang

#### Jika Quota Habis:
1. Top up balance di Fonnte
2. Upgrade package jika perlu
3. Monitor usage

#### Jika Nomor Bermasalah:
1. Test dengan nomor lain
2. Pastikan format +62xxx
3. Cek apakah nomor aktif WhatsApp

#### Jika Policy Violation:
1. Simplify message content
2. Remove promotional language
3. Shorten message
4. Remove suspicious links

### Monitoring dan Prevention

#### 1. Setup Monitoring
```python
# Tambah di settings.py
LOGGING = {
    'loggers': {
        'employee.services.onboarding_delivery': {
            'level': 'DEBUG',
            'handlers': ['file'],
        }
    }
}
```

#### 2. Implement Retry Logic
```python
def send_with_retry(phone, message, max_retries=3):
    for attempt in range(max_retries):
        if send_via_fonnte(phone, message):
            return True
        time.sleep(2 ** attempt)  # Exponential backoff
    return False
```

#### 3. Validate Phone Numbers
```python
def validate_whatsapp_number(phone):
    # Check if number is registered in WhatsApp
    # Use WhatsApp Business API check endpoint
    pass
```

#### 4. Dashboard Monitoring
- Setup alerts untuk quota rendah
- Monitor delivery rate
- Track failed messages

### Testing Checklist

- [ ] Account status connected
- [ ] Quota sufficient
- [ ] Test dengan nomor sendiri
- [ ] Test dengan pesan sederhana
- [ ] Cek dashboard Fonnte
- [ ] Monitor logs real-time
- [ ] Test dengan nomor berbeda
- [ ] Verify message content policy

### Emergency Fallback

Jika WhatsApp tetap tidak bisa:

1. **Email Backup**: Pastikan email selalu terkirim
2. **SMS Gateway**: Implement SMS sebagai backup
3. **Manual Process**: Notify admin untuk follow up manual
4. **Alternative Provider**: Siapkan provider WhatsApp alternatif

### Kesimpulan

Masalah "log sukses tapi WA tidak masuk" biasanya disebabkan oleh:
1. **Device disconnect** (paling umum)
2. **Quota habis** 
3. **Nomor penerima bermasalah**
4. **Policy violation**

Jalankan `check_fonnte_account` command untuk diagnosis lengkap.