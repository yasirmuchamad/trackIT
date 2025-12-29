# 📧 Konfigurasi 163.com SMTP - Multiple Options

## 🔧 Option 1: Port 587 + TLS (Recommended)

### .env Configuration:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtphz.qiye.163.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=muchamad.yasir@goldenteks.id
EMAIL_HOST_PASSWORD=$FdSfa%xMq3ZRj31
DEFAULT_FROM_EMAIL=muchamad.yasir@goldenteks.id
```

## 🔧 Option 2: Port 465 + SSL

### .env Configuration:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtphz.qiye.163.com
EMAIL_PORT=465
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
EMAIL_HOST_USER=muchamad.yasir@goldenteks.id
EMAIL_HOST_PASSWORD=$FdSfa%xMq3ZRj31
DEFAULT_FROM_EMAIL=muchamad.yasir@goldenteks.id
```

## 🔧 Option 3: Port 25 + TLS (Fallback)

### .env Configuration:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtphz.qiye.163.com
EMAIL_PORT=25
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=muchamad.yasir@goldenteks.id
EMAIL_HOST_PASSWORD=$FdSfa%xMq3ZRj31
DEFAULT_FROM_EMAIL=muchamad.yasir@goldenteks.id
```

## 🔧 Option 4: Alternative SMTP Server

### .env Configuration:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.qiye.163.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=muchamad.yasir@goldenteks.id
EMAIL_HOST_PASSWORD=$FdSfa%xMq3ZRj31
DEFAULT_FROM_EMAIL=muchamad.yasir@goldenteks.id
```

## 🔐 163.com Authorization Code Setup

### Jika password biasa tidak work:

1. **Login ke 163.com webmail**: https://mail.163.com
2. **Masuk dengan akun**: muchamad.yasir@goldenteks.id
3. **Settings → POP3/SMTP/IMAP**
4. **Enable SMTP service**
5. **Generate Authorization Code** (bukan password biasa)
6. **Gunakan Authorization Code** sebagai EMAIL_HOST_PASSWORD

## 🧪 Testing Commands

### Test setiap konfigurasi:
```bash
# Update .env dengan salah satu option di atas
# Restart Django server
python manage.py runserver

# Test di terminal baru
python manage.py test_email --to muchamad.yasir@goldenteks.id
```

## 🔍 Manual SMTP Test

### Test langsung dengan Python:
```python
import smtplib
from email.mime.text import MIMEText

# Test SSL (Port 465)
try:
    server = smtplib.SMTP_SSL('smtphz.qiye.163.com', 465)
    server.login('muchamad.yasir@goldenteks.id', '$FdSfa%xMq3ZRj31')
    print("SSL connection successful!")
    server.quit()
except Exception as e:
    print(f"SSL failed: {e}")

# Test TLS (Port 587)
try:
    server = smtplib.SMTP('smtphz.qiye.163.com', 587)
    server.starttls()
    server.login('muchamad.yasir@goldenteks.id', '$FdSfa%xMq3ZRj31')
    print("TLS connection successful!")
    server.quit()
except Exception as e:
    print(f"TLS failed: {e}")
```

## 🚨 Common Issues

### "Connection unexpectedly closed"
- **Cause**: Wrong SSL/TLS configuration
- **Solution**: Try Option 1 (Port 587 + TLS)

### "Authentication failed"
- **Cause**: Wrong password or SMTP not enabled
- **Solution**: Generate Authorization Code from webmail

### "Network unreachable"
- **Cause**: Firewall/network blocking
- **Solution**: Try different network or contact IT

### "Timeout"
- **Cause**: Network connectivity
- **Solution**: Check internet connection

## 📋 Recommended Testing Order

1. **Try Option 1** (Port 587 + TLS) - Most common
2. **Try Option 4** (Alternative server) - Different server
3. **Try Option 3** (Port 25) - Fallback
4. **Generate Authorization Code** - If password issue
5. **Contact IT** - If all fail