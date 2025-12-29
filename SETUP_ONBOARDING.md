# 🚀 Setup Onboarding Email & WhatsApp - Production Ready

## 📁 Struktur File

```
trackIT/
├── .env.example          # Template environment variables (COMMIT ini)
├── .env                  # Actual environment variables (JANGAN commit)
├── trackIT/settings.py   # Main settings dengan environment variables
├── employee/
│   ├── settings_example.py    # Contoh konfigurasi (COMMIT ini)
│   └── ONBOARDING_SETUP.md   # Dokumentasi detail
└── logs/                 # Folder untuk log files
```

## 🔧 Quick Setup

### 1. **Copy Environment Template**
```bash
cp .env.example .env
```

### 2. **Edit `.env` dengan Data Anda**
```bash
# Development (Email ke console)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Production (Real email)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# WhatsApp (pilih salah satu)
WHATSAPP_SERVICE_URL=https://api.fonnte.com/send
WHATSAPP_SERVICE_TOKEN=your-fonnte-token
```

### 3. **Install Dependencies**
```bash
pip install requests
```

### 4. **Test Setup**
```bash
# Buat test employee
python manage.py test_onboarding --create-test-employee

# Test pengiriman
python manage.py test_onboarding --employee-id 99999 --email test@example.com
```

## 🌍 Environment-Based Configuration

### **Development** (`.env`)
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
FRONT_END_BASE_URL=http://localhost:8000
```

### **Staging** (`.env`)
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_USER=staging@company.com
EMAIL_HOST_PASSWORD=staging-password
FRONT_END_BASE_URL=https://staging.company.com
WHATSAPP_SERVICE_URL=https://api.fonnte.com/send
WHATSAPP_SERVICE_TOKEN=staging-token
```

### **Production** (Environment Variables di Server)
```bash
export EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
export EMAIL_HOST_USER=noreply@company.com
export EMAIL_HOST_PASSWORD=production-password
export FRONT_END_BASE_URL=https://company.com
export WHATSAPP_SERVICE_URL=https://api.fonnte.com/send
export WHATSAPP_SERVICE_TOKEN=production-token
```

## 📧 Email Providers

### **Gmail** (Recommended untuk Development)
1. Enable 2FA di Gmail
2. Generate App Password: [Google Account Settings](https://myaccount.google.com/apppasswords)
3. Gunakan App Password (16 digit), bukan password biasa

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=abcd-efgh-ijkl-mnop  # App Password
```

### **Custom SMTP** (Production)
```env
EMAIL_HOST=mail.your-domain.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@your-domain.com
EMAIL_HOST_PASSWORD=your-password
```

## 📱 WhatsApp Providers

### **Fonnte.com** (Recommended untuk Indonesia)
1. Daftar di [fonnte.com](https://fonnte.com)
2. Dapatkan token dari dashboard
3. Setup:
```env
WHATSAPP_SERVICE_URL=https://api.fonnte.com/send
WHATSAPP_SERVICE_TOKEN=your-fonnte-token
```

### **Wablas.com** (Alternative Indonesia)
```env
WHATSAPP_SERVICE_URL=https://console.wablas.com/api/send-message
WHATSAPP_SERVICE_TOKEN=your-wablas-token
```

## 🔒 Security Best Practices

### **1. Environment Variables**
- ✅ Gunakan `.env` untuk development
- ✅ Gunakan server environment variables untuk production
- ❌ JANGAN hardcode credentials di code
- ❌ JANGAN commit `.env` ke Git

### **2. File Permissions**
```bash
# Set proper permissions untuk .env
chmod 600 .env
```

### **3. Production Deployment**
```bash
# Set environment variables di server
export EMAIL_HOST_PASSWORD="your-secure-password"
export WHATSAPP_SERVICE_TOKEN="your-secure-token"

# Atau gunakan systemd environment file
# /etc/systemd/system/your-app.service.d/environment.conf
```

## 🧪 Testing Commands

```bash
# Test dengan console email (development)
python manage.py test_onboarding --employee-id 12345

# Test dengan real email
python manage.py test_onboarding --employee-id 12345 --email your-test@gmail.com

# Test dengan WhatsApp
python manage.py test_onboarding --employee-id 12345 --phone 08123456789

# Test keduanya
python manage.py test_onboarding --employee-id 12345 --email test@gmail.com --phone 08123456789
```

## 📊 Monitoring & Logs

### **Log Files**
- `logs/onboarding.log` - Detailed delivery logs
- Console output - Real-time status

### **Database Monitoring**
```python
# Check delivery status
from employee.models import OnboardingDelivery
failed_deliveries = OnboardingDelivery.objects.filter(is_success=False)
```

## 🚨 Troubleshooting

### **Email Issues**
```bash
# Test SMTP connection
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
```

### **WhatsApp Issues**
- Check token validity
- Verify phone number format
- Check API rate limits
- Review logs for detailed errors

## 📋 Deployment Checklist

- [ ] `.env.example` committed to Git
- [ ] `.env` added to `.gitignore`
- [ ] Production environment variables set
- [ ] Email provider configured and tested
- [ ] WhatsApp provider configured and tested
- [ ] Log directory created with proper permissions
- [ ] Test employee created and tested
- [ ] Monitoring setup for failed deliveries

## 🔄 Migration dari Development ke Production

1. **Copy environment template**:
   ```bash
   cp .env.example .env.production
   ```

2. **Update production values**:
   ```bash
   nano .env.production
   ```

3. **Load environment in production**:
   ```bash
   source .env.production
   python manage.py runserver
   ```

4. **Verify configuration**:
   ```bash
   python manage.py test_onboarding --employee-id test-id
   ```