# 🔧 Troubleshooting Employee Onboarding

## ❌ Error: "OnboardingDelivery() got unexpected keyword arguments: 'is_success'"

### **Penyebab:**
Ada typo dalam model `OnboardingDelivery` dimana field bernama `is_succces` (dengan typo) tapi kode menggunakan `is_success`.

### **Solusi:**

#### **Option 1: Jalankan Migration (Recommended)**
```bash
# Aktifkan virtual environment dulu
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows

# Jalankan migration
python manage.py migrate employee
```

#### **Option 2: Fix Manual dengan Management Command**
```bash
python manage.py fix_onboarding_typo
```

#### **Option 3: Fix Manual Database (SQLite)**
```sql
-- Jika menggunakan SQLite browser atau command line
ALTER TABLE employee_onboardingdelivery RENAME COLUMN is_succces TO is_success;
```

### **Verifikasi Fix:**
```bash
# Test onboarding setelah fix
python manage.py test_onboarding --create-test-employee
python manage.py test_onboarding --employee-id 99999 --email test@example.com
```

---

## ❌ Error: "No module named 'django'"

### **Penyebab:**
Virtual environment belum diaktifkan atau Django belum terinstall.

### **Solusi:**
```bash
# Aktifkan virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies jika belum
pip install django djangorestframework requests
```

---

## ❌ Error: Email tidak terkirim

### **Troubleshooting:**

#### **1. Cek Konfigurasi Email**
```python
# Di Django shell
python manage.py shell
>>> from django.conf import settings
>>> print(settings.EMAIL_BACKEND)
>>> print(settings.EMAIL_HOST_USER)
```

#### **2. Test SMTP Connection**
```python
# Di Django shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
```

#### **3. Cek .env File**
```bash
# Pastikan .env file ada dan berisi:
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

#### **4. Gmail App Password**
- Bukan password biasa Gmail
- Harus enable 2FA dulu
- Generate di: https://myaccount.google.com/apppasswords

---

## ❌ Error: WhatsApp tidak terkirim

### **Troubleshooting:**

#### **1. Cek Konfigurasi WhatsApp**
```python
# Di Django shell
>>> from django.conf import settings
>>> print(settings.WHATSAPP_SERVICE_URL)
>>> print(settings.WHATSAPP_SERVICE_TOKEN)
```

#### **2. Test API Connection**
```python
# Di Django shell
>>> import requests
>>> response = requests.post(
...     'https://api.fonnte.com/send',
...     data={'target': '628123456789', 'message': 'test'},
...     headers={'Authorization': 'your-token'}
... )
>>> print(response.json())
```

#### **3. Cek Token Validity**
- Login ke dashboard provider (Fonnte/Wablas)
- Pastikan token masih aktif
- Cek saldo/quota

---

## ❌ Error: "CSRF verification failed"

### **Penyebab:**
CSRF token tidak valid dalam form.

### **Solusi:**
```html
<!-- Pastikan ada di template form -->
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

---

## ❌ Error: Template tidak ditemukan

### **Penyebab:**
Template path tidak sesuai atau app tidak terdaftar.

### **Solusi:**
```python
# Di settings.py, pastikan:
INSTALLED_APPS = [
    # ...
    'employee.apps.EmployeeConfig',  # atau 'employee'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,  # Penting!
        # ...
    },
]
```

---

## 🔍 Debug Mode

### **Enable Detailed Logging:**
```python
# Di settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'employee.services.onboarding_delivery': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### **Check Database Records:**
```python
# Di Django shell
>>> from employee.models import *
>>> 
>>> # Cek employee
>>> Employee.objects.all()
>>> 
>>> # Cek onboarding records
>>> EmployeeOnboarding.objects.all()
>>> 
>>> # Cek delivery records
>>> OnboardingDelivery.objects.all()
>>> 
>>> # Cek failed deliveries
>>> OnboardingDelivery.objects.filter(is_success=False)
```

---

## 📞 Bantuan Lebih Lanjut

Jika masih ada masalah:

1. **Cek log file**: `logs/onboarding.log`
2. **Jalankan test command**: `python manage.py test_onboarding --create-test-employee`
3. **Cek database**: Gunakan Django admin atau shell
4. **Verify settings**: Pastikan semua environment variables benar