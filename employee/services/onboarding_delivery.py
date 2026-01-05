from django.conf import settings
from employee.models import OnboardingDelivery
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import requests
import logging
import json

logger = logging.getLogger(__name__)

def build_onboarding_link(token):
    """Build complete onboarding link"""
    base_url = getattr(settings, 'FRONT_END_BASE_URL', 'http://localhost:8000')
    return f"{base_url}/onboarding/{token}/"

def send_onboarding_email(onboarding, email):
    """Send onboarding link via email"""
    link = build_onboarding_link(onboarding.token)
    employee = onboarding.employee
    
    logger.info(f"Attempting to send onboarding email to {email} for {employee.name}")
    logger.info(f"Using email backend: {settings.EMAIL_BACKEND}")
    logger.info(f"SMTP host: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
    logger.info(f"From email: {settings.DEFAULT_FROM_EMAIL}")
    
    try:
        # Create HTML email content
        html_message = render_to_string('employee/emails/onboarding.html', {
            'employee': employee,
            'onboarding_link': link,
            'expires_at': onboarding.expires_at,
        })
        
        # Create plain text version
        plain_message = strip_tags(html_message)
        
        logger.info("Email content prepared, attempting to send...")
        
        send_mail(
            subject=f"Welcome to the Team - Complete Your Onboarding ({employee.name})",
            message=plain_message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', ''),
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
        logger.error(f"Exception type: {type(e).__name__}")
        
        # Additional debugging for common email issues
        if "Connection unexpectedly closed" in str(e):
            logger.error("→ This usually indicates SMTP server connection issues")
            logger.error("→ Check if SMTP server is accessible and credentials are correct")
            logger.error("→ Try using port 465 with SSL instead of 587 with TLS")
        elif "Authentication failed" in str(e):
            logger.error("→ Email credentials are incorrect")
        elif "timeout" in str(e).lower():
            logger.error("→ SMTP server is not responding (timeout)")
            
        return False

def send_onboarding_whatsapp(onboarding, phone):
    """Send onboarding link via WhatsApp"""
    print(f"🚨 DEBUG: send_onboarding_whatsapp CALLED!")
    print(f"🚨 DEBUG: employee={onboarding.employee.name}, phone={phone}")
    
    logger.info(f"send_onboarding_whatsapp called with phone: {phone}")
    
    link = build_onboarding_link(onboarding.token)
    employee = onboarding.employee
    
    # Format phone number (remove non-digits and ensure proper format)
    clean_phone = ''.join(filter(str.isdigit, phone))
    if clean_phone.startswith('0'):
        clean_phone = '62' + clean_phone[1:]  # Convert Indonesian format
    elif not clean_phone.startswith('62'):
        clean_phone = '62' + clean_phone
    
    print(f"🚨 DEBUG: clean_phone={clean_phone}")
    logger.info(f"Phone formatted: {phone} → {clean_phone}")
    
    message = f"""Halo {employee.name}! 👋

Selamat bergabung di perusahaan kami! 

Silakan lengkapi data onboarding Anda melalui link berikut:
{link}

Link ini berlaku hingga: {onboarding.expires_at.strftime('%d %B %Y, %H:%M')}

Jika ada pertanyaan, silakan hubungi HR.

Terima kasih! 🙏
    """.strip()
    
    print(f"🚨 DEBUG: message prepared, length={len(message)}")
    logger.info(f"Message prepared for {employee.name}")
    
    try:
        # Check if WhatsApp service is configured
        whatsapp_url = getattr(settings, 'WHATSAPP_SERVICE_URL', '')
        whatsapp_token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', '')
        
        if not whatsapp_url or not whatsapp_token:
            logger.info(f"[WhatsApp] Service not configured, would send to {clean_phone}: {message}")
            
            OnboardingDelivery.objects.create(
                onboarding=onboarding,
                channel="whatsapp",
                destination=clean_phone,
                is_success=True,
                error_message="WhatsApp service not configured - logged only"
            )
            return True
        
        # Call Fonnte directly
        success = send_via_fonnte(clean_phone, message)
        
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
        
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        return True
    except Exception as e:
        logger.error(f"WhatsApp API error: {str(e)}")
        return False

def send_via_whatsapp_service(phone, message):
    """Send via third-party WhatsApp service (Fonnte, Wablas, etc.)"""
    try:
        whatsapp_url = getattr(settings, 'WHATSAPP_SERVICE_URL', '')
        whatsapp_token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', '')
        
        if not whatsapp_url or not whatsapp_token:
            logger.error("WhatsApp service URL or token not configured")
            return False
        
        # Example for Fonnte.com
        if 'fonnte' in whatsapp_url.lower():
            return send_via_fonnte(phone, message)
        
        # Example for Wablas.com
        elif 'wablas' in whatsapp_url.lower():
            return send_via_wablas(phone, message)
        
        # Generic implementation
        else:
            headers = {
                'Authorization': f'Bearer {whatsapp_token}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'phone': phone,
                'message': message
            }
            
            response = requests.post(whatsapp_url, json=data, headers=headers)
            response.raise_for_status()
            
            return True
            
    except Exception as e:
        logger.error(f"WhatsApp service error: {str(e)}")
        return False

def send_via_fonnte(phone, message):
    """Send via Fonnte.com service"""
    try:
        print(f"🚨 DEBUG: send_via_fonnte CALLED!")
        print(f"🚨 DEBUG: phone={phone}, message={message[:50]}...")
        
        # Get settings - NO fallback to dummy token
        url = getattr(settings, 'WHATSAPP_SERVICE_URL', 'https://api.fonnte.com/send')
        token = getattr(settings, 'WHATSAPP_SERVICE_TOKEN', '')  # Empty default
        
        print(f"🚨 DEBUG: url={url}")
        print(f"🚨 DEBUG: token={token[:10]}...")
        
        logger.info(f"Fonnte URL from settings: {url}")
        logger.info(f"Fonnte token from settings: {token[:10]}..." if token else "Fonnte token: EMPTY")
        
        if not url or not token or url == '' or token == '':
            logger.error("Fonnte URL or token not configured properly")
            logger.error(f"URL: '{url}', Token: '{token[:10]}...' if token else 'EMPTY'")
            logger.error("Make sure WHATSAPP_SERVICE_TOKEN is set in .env file with real Fonnte token")
            return False
        
        headers = {
            'Authorization': token,
        }
        
        data = {
            'target': phone,
            'message': message,
            'countryCode': '62',  # Indonesia
        }
        
        print(f"🚨 DEBUG: About to call requests.post")
        print(f"🚨 DEBUG: headers={{'Authorization': '{token[:10]}...'}}")
        print(f"🚨 DEBUG: data={data}")
        
        logger.info(f"Sending WhatsApp via Fonnte to {phone}")
        logger.info(f"Request URL: {url}")
        logger.info(f"Request headers: Authorization: {token[:10]}...")
        logger.info(f"Request data: {data}")
        
        response = requests.post(url, data=data, headers=headers)
        
        print(f"🚨 DEBUG: requests.post completed!")
        print(f"🚨 DEBUG: response.status_code={response.status_code}")
        print(f"🚨 DEBUG: response.text={response.text}")
        
        logger.info(f"Fonnte response status: {response.status_code}")
        logger.info(f"Fonnte response headers: {dict(response.headers)}")
        logger.info(f"Fonnte response raw: {response.text}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                logger.info(f"Fonnte response JSON: {result}")
                
                # Analyze the response in detail
                success = result.get('status', False)
                
                # Log all response fields for debugging
                for key, value in result.items():
                    logger.info(f"Fonnte response field '{key}': {value}")
                
                if success:
                    logger.info(f"Fonnte API returned success: {result}")
                    
                    # Check for additional status indicators
                    if 'id' in result:
                        logger.info(f"Message ID from Fonnte: {result['id']}")
                    if 'detail' in result:
                        logger.info(f"Detail from Fonnte: {result['detail']}")
                    if 'message' in result:
                        logger.info(f"Message from Fonnte: {result['message']}")
                    
                    # Warning about delivery vs sent
                    logger.warning("⚠️ IMPORTANT: Fonnte 'success' means message was SENT to WhatsApp servers")
                    logger.warning("⚠️ It does NOT guarantee the message was DELIVERED to the recipient")
                    logger.warning("⚠️ Check Fonnte dashboard for actual delivery status")
                    
                    return True
                else:
                    logger.error(f"Fonnte API returned failure: {result}")
                    
                    # Analyze common error patterns
                    error_msg = str(result).lower()
                    if 'invalid' in error_msg:
                        logger.error("→ Possible invalid phone number or token")
                    elif 'quota' in error_msg or 'balance' in error_msg:
                        logger.error("→ Possible quota/balance issue")
                    elif 'blocked' in error_msg:
                        logger.error("→ Number might be blocked")
                    elif 'not registered' in error_msg:
                        logger.error("→ Phone number not registered in WhatsApp")
                    
                    return False
                    
            except json.JSONDecodeError as e:
                logger.error(f"Fonnte response is not valid JSON: {e}")
                logger.error(f"Raw response: {response.text}")
                return False
        else:
            logger.error(f"Fonnte HTTP error: {response.status_code} - {response.text}")
            return False
        
    except requests.exceptions.Timeout:
        logger.error("Fonnte request timeout")
        return False
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Fonnte connection error: {e}")
        return False
    except Exception as e:
        logger.error(f"Fonnte unexpected error: {str(e)}", exc_info=True)
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
        
        response = requests.post(url, json=data, headers=headers)
        result = response.json()
        
        return result.get('status', False)
        
    except Exception as e:
        logger.error(f"Wablas error: {str(e)}")
        return False

def send_onboarding_links(onboarding, email=None, phone=None):
    """Send onboarding links via email and/or WhatsApp"""
    logger.info(f"send_onboarding_links called for employee {onboarding.employee.name}")
    logger.info(f"Email parameter: {email}")
    logger.info(f"Phone parameter: {phone}")
    
    results = {'email': None, 'whatsapp': None}
    
    if email:
        logger.info(f"Attempting to send email to: {email}")
        results['email'] = send_onboarding_email(onboarding, email)
        logger.info(f"Email result: {results['email']}")

    if phone:
        logger.info(f"Attempting to send WhatsApp to: {phone}")
        results['whatsapp'] = send_onboarding_whatsapp(onboarding, phone)
        logger.info(f"WhatsApp result: {results['whatsapp']}")
    
    logger.info(f"Final results: {results}")
    return results