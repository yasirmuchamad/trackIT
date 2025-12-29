from django.conf import settings
from employee.models import OnboardingDelivery
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import requests
import logging

logger = logging.getLogger(__name__)

def build_onboarding_link(token):
    """Build complete onboarding link"""
    base_url = getattr(settings, 'FRONT_END_BASE_URL', 'http://localhost:8000')
    return f"{base_url}/onboarding/{token}/"

def send_onboarding_email(onboarding, email):
    """Send onboarding link via email"""
    link = build_onboarding_link(onboarding.token)
    employee = onboarding.employee
    
    try:
        # Create HTML email content
        html_message = render_to_string('employee/emails/onboarding.html', {
            'employee': employee,
            'onboarding_link': link,
            'expires_at': onboarding.expires_at,
        })
        
        # Create plain text version
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=f"Welcome to the Team - Complete Your Onboarding ({employee.name})",
            message=plain_message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@company.com'),
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )

        OnboardingDelivery.objects.create(
            onboarding=onboarding,
            channel="email",
            destination=email,
            is_success=True,
        )
        
        logger.info(f"Onboarding email sent successfully to {email} for employee {employee.name}")
        return True
    
    except Exception as e:
        OnboardingDelivery.objects.create(
            onboarding=onboarding,
            channel="email",
            destination=email,
            is_success=False,
            error_message=str(e),
        )
        
        logger.error(f"Failed to send onboarding email to {email}: {str(e)}")
        return False

def send_onboarding_whatsapp(onboarding, phone):
    """Send onboarding link via WhatsApp"""
    link = build_onboarding_link(onboarding.token)
    employee = onboarding.employee
    
    # Format phone number (remove non-digits and ensure proper format)
    clean_phone = ''.join(filter(str.isdigit, phone))
    if clean_phone.startswith('0'):
        clean_phone = '62' + clean_phone[1:]  # Convert Indonesian format
    elif not clean_phone.startswith('62'):
        clean_phone = '62' + clean_phone
    
    message = f"""
Halo {employee.name}! 👋

Selamat bergabung di perusahaan kami! 

Silakan lengkapi data onboarding Anda melalui link berikut:
{link}

Link ini berlaku hingga: {onboarding.expires_at.strftime('%d %B %Y, %H:%M')}

Jika ada pertanyaan, silakan hubungi HR.

Terima kasih! 🙏
    """.strip()
    
    try:
        # Method 1: Using WhatsApp Business API (if configured)
        if hasattr(settings, 'WHATSAPP_API_URL') and hasattr(settings, 'WHATSAPP_API_TOKEN'):
            success = send_via_whatsapp_api(clean_phone, message)
        
        # Method 2: Using third-party service like Fonnte, Wablas, etc.
        elif hasattr(settings, 'WHATSAPP_SERVICE_URL') and hasattr(settings, 'WHATSAPP_SERVICE_TOKEN'):
            success = send_via_whatsapp_service(clean_phone, message)
        
        # Method 3: Fallback - just log (for development)
        else:
            logger.info(f"[WhatsApp] Would send to {clean_phone}: {message}")
            success = True  # Assume success for development
        
        if success:
            OnboardingDelivery.objects.create(
                onboarding=onboarding,
                channel="whatsapp",
                destination=clean_phone,
                is_success=True,
            )
            logger.info(f"Onboarding WhatsApp sent successfully to {clean_phone} for employee {employee.name}")
            return True
        else:
            raise Exception("WhatsApp service returned failure")
            
    except Exception as e:
        OnboardingDelivery.objects.create(
            onboarding=onboarding,
            channel="whatsapp",
            destination=clean_phone,
            is_success=False,
            error_message=str(e),
        )
        
        logger.error(f"Failed to send onboarding WhatsApp to {clean_phone}: {str(e)}")
        return False

def send_via_whatsapp_api(phone, message):
    """Send via official WhatsApp Business API"""
    try:
        url = settings.WHATSAPP_API_URL
        headers = {
            'Authorization': f'Bearer {settings.WHATSAPP_API_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'messaging_product': 'whatsapp',
            'to': phone,
            'type': 'text',
            'text': {'body': message}
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        
        return True
    except Exception as e:
        logger.error(f"WhatsApp API error: {str(e)}")
        return False

def send_via_whatsapp_service(phone, message):
    """Send via third-party WhatsApp service (Fonnte, Wablas, etc.)"""
    try:
        # Example for Fonnte.com
        if 'fonnte' in settings.WHATSAPP_SERVICE_URL.lower():
            return send_via_fonnte(phone, message)
        
        # Example for Wablas.com
        elif 'wablas' in settings.WHATSAPP_SERVICE_URL.lower():
            return send_via_wablas(phone, message)
        
        # Generic implementation
        else:
            headers = {
                'Authorization': f'Bearer {settings.WHATSAPP_SERVICE_TOKEN}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'phone': phone,
                'message': message
            }
            
            response = requests.post(settings.WHATSAPP_SERVICE_URL, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            
            return True
            
    except Exception as e:
        logger.error(f"WhatsApp service error: {str(e)}")
        return False

def send_via_fonnte(phone, message):
    """Send via Fonnte.com service"""
    try:
        url = settings.WHATSAPP_SERVICE_URL
        headers = {
            'Authorization': settings.WHATSAPP_SERVICE_TOKEN,
        }
        
        data = {
            'target': phone,
            'message': message,
            'countryCode': '62',  # Indonesia
        }
        
        response = requests.post(url, data=data, headers=headers, timeout=30)
        result = response.json()
        
        return result.get('status', False)
        
    except Exception as e:
        logger.error(f"Fonnte error: {str(e)}")
        return False

def send_via_wablas(phone, message):
    """Send via Wablas.com service"""
    try:
        url = settings.WHATSAPP_SERVICE_URL
        headers = {
            'Authorization': settings.WHATSAPP_SERVICE_TOKEN,
            'Content-Type': 'application/json'
        }
        
        data = {
            'phone': phone,
            'message': message
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=30)
        result = response.json()
        
        return result.get('status', False)
        
    except Exception as e:
        logger.error(f"Wablas error: {str(e)}")
        return False

def send_onboarding_links(onboarding, email=None, phone=None):
    """Send onboarding links via email and/or WhatsApp"""
    results = {'email': None, 'whatsapp': None}
    
    if email:
        results['email'] = send_onboarding_email(onboarding, email)

    if phone:
        results['whatsapp'] = send_onboarding_whatsapp(onboarding, phone)
    
    return results