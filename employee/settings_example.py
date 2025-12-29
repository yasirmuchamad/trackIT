# Example settings for email and WhatsApp configuration
# Add these to your Django settings.py file

# =============================================================================
# EMAIL CONFIGURATION
# =============================================================================

# For Gmail SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # Your Gmail address
EMAIL_HOST_PASSWORD = 'your-app-password'  # Gmail App Password (not regular password)
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'

# For development (console backend - emails will be printed to console)
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For production with other SMTP providers
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'mail.your-domain.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'noreply@your-domain.com'
# EMAIL_HOST_PASSWORD = 'your-password'
# DEFAULT_FROM_EMAIL = 'noreply@your-domain.com'

# =============================================================================
# WHATSAPP CONFIGURATION
# =============================================================================

# Frontend URL for onboarding links
FRONT_END_BASE_URL = 'http://localhost:8000'  # Change to your domain in production

# Option 1: WhatsApp Business API (Official)
# WHATSAPP_API_URL = 'https://graph.facebook.com/v17.0/YOUR_PHONE_NUMBER_ID/messages'
# WHATSAPP_API_TOKEN = 'your-whatsapp-business-api-token'

# Option 2: Fonnte.com (Indonesian WhatsApp Gateway)
# WHATSAPP_SERVICE_URL = 'https://api.fonnte.com/send'
# WHATSAPP_SERVICE_TOKEN = 'your-fonnte-token'

# Option 3: Wablas.com (Indonesian WhatsApp Gateway)
# WHATSAPP_SERVICE_URL = 'https://console.wablas.com/api/send-message'
# WHATSAPP_SERVICE_TOKEN = 'your-wablas-token'

# Option 4: Other WhatsApp services
# WHATSAPP_SERVICE_URL = 'https://api.your-whatsapp-service.com/send'
# WHATSAPP_SERVICE_TOKEN = 'your-service-token'

# =============================================================================
# LOGGING CONFIGURATION (Optional)
# =============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'onboarding.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'employee.services.onboarding_delivery': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}