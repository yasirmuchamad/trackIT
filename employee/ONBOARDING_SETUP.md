# Setup Onboarding Email dan WhatsApp

Panduan lengkap untuk mengatur pengiriman email dan WhatsApp untuk sistem onboarding employee.

## 📧 Setup Email

### 1. Gmail SMTP (Recommended untuk Development)

1. **Enable 2-Factor Authentication** di akun Gmail Anda
2. **Generate App Password**:
   - Buka [Google Account Settings](https://myaccount.google.com/)
   - Security → 2-Step Verification → App passwords
   - Generate password untuk "Mail"
3. **Tambahkan ke settings.py**:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-16-digit-app-password'  # Bukan password biasa!
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

### 2. SMTP Provider Lain

```python
# Untuk hosting/domain sendiri
EMAIL_HOST = 'mail.your-domain.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'noreply@your-domain.com'
EMAIL_HOST_PASSWORD = 'your-password'
DEFAULT_FROM_EMAIL = 'noreply@your-domain.com'
```

### 3. Development Mode (Console)

```python
# Email akan ditampilkan di console/terminal
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## 📱 Setup WhatsApp

### Option 1: WhatsApp Business API (Official)

1. **Daftar di Meta for Developers**
2. **Setup WhatsApp Business API**
3. **Dapatkan Phone Number ID dan Access Token**
4. **Tambahkan ke settings.py**:

```python
WHATSAPP_API_URL = 'https://graph.facebook.com/v17.0/YOUR_PHONE_NUMBER_ID/messages'
WHATSAPP_API_TOKEN = 'your-whatsapp-business-api-token'
```

### Option 2: Fonnte.com (Indonesian Service)

1. **Daftar di [Fonnte.com](https://fonnte.com)**
2. **Dapatkan API Token**
3. **Tambahkan ke settings.py**:

```python
WHATSAPP_SERVICE_URL = 'https://api.fonnte.com/send'
WHATSAPP_SERVICE_TOKEN = 'your-fonnte-token'
```

### Option 3: Wablas.com (Indonesian Service)

1. **Daftar di [Wablas.com](https://wablas.com)**
2. **Dapatkan API Token**
3. **Tambahkan ke settings.py**:

```python
WHATSAPP_SERVICE_URL = 'https://console.wablas.com/api/send-message'
WHATSAPP_SERVICE_TOKEN = 'your-wablas-token'
```

## 🔧 Konfigurasi Tambahan

### Frontend URL

```python
# URL untuk link onboarding (ganti dengan domain production)
FRONT_END_BASE_URL = 'http://localhost:8000'  # Development
# FRONT_END_BASE_URL = 'https://your-domain.com'  # Production
```

### Logging (Optional)

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'onboarding.log',
        },
    },
    'loggers': {
        'employee.services.onboarding_delivery': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 🧪 Testing

### 1. Buat Test Employee

```bash
python manage.py test_onboarding --create-test-employee
```

### 2. Test Pengiriman

```bash
# Test dengan data employee yang ada
python manage.py test_onboarding --employee-id 12345

# Test dengan email/phone custom
python manage.py test_onboarding --employee-id 12345 --email test@example.com --phone 08123456789
```

### 3. Test Manual di Django Shell

```python
python manage.py shell

from employee.models import Employee, EmployeeOnboarding
from employee.services.onboarding_delivery import send_onboarding_links
from django.utils import timezone
from datetime import timedelta

# Ambil employee
employee = Employee.objects.get(employee_id=12345)

# Buat onboarding
onboarding = EmployeeOnboarding.create_for_employee(employee)

# Test kirim
results = send_onboarding_links(
    onboarding, 
    email='test@example.com', 
    phone='08123456789'
)

print(results)
```

## 🔍 Troubleshooting

### Email Issues

1. **Gmail "Less secure app access"**: Gunakan App Password, bukan password biasa
2. **SMTP Authentication Error**: Periksa username/password
3. **Connection refused**: Periksa EMAIL_HOST dan EMAIL_PORT
4. **TLS/SSL Error**: Pastikan EMAIL_USE_TLS = True untuk port 587

### WhatsApp Issues

1. **Phone Number Format**: Sistem otomatis format ke +62xxx
2. **API Rate Limits**: Periksa limit dari provider
3. **Invalid Token**: Pastikan token masih valid
4. **Network Timeout**: Periksa koneksi internet

### General Issues

1. **Check Logs**: Lihat file `onboarding.log` atau console output
2. **Check Database**: Lihat tabel `OnboardingDelivery` untuk history
3. **Test Connection**: Gunakan management command untuk testing

## 📋 Checklist Setup

- [ ] Email SMTP dikonfigurasi
- [ ] WhatsApp service dipilih dan dikonfigurasi
- [ ] FRONT_END_BASE_URL diset
- [ ] Template email tersedia
- [ ] Test employee dibuat
- [ ] Test pengiriman berhasil
- [ ] Logging dikonfigurasi (optional)

## 🚀 Production Considerations

1. **Use Environment Variables** untuk sensitive data:
   ```python
   import os
   EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
   WHATSAPP_SERVICE_TOKEN = os.environ.get('WHATSAPP_TOKEN')
   ```

2. **Rate Limiting**: Implementasi rate limiting untuk mencegah spam

3. **Queue System**: Gunakan Celery untuk pengiriman async di production

4. **Monitoring**: Setup monitoring untuk delivery failures

5. **Backup**: Backup delivery logs untuk audit trail