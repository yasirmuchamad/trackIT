from django.conf import settings
from employee.models import OnboardingDelivery
from django.core.mail import send_mail

def build_onboarding_link(token):
    return f"{settings.FRONT_END_BASE_URL}/onboarding/{token}/"

def send_onboarding_email(onboarding, email):
    link = build_onboarding_link(onboarding.token)

    try:
        send_mail(
            subject="Employee Onboarding",
            message=f"Silahkan lengkapi data diri anda:\n{link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        OnboardingDelivery.objects.create(
            onboarding=onboarding,
            channel="email",
            destination=email,
            is_succes=True,
        )
    
    except Exception as e:
        OnboardingDelivery.objects.create(
            onboarding=onboarding,
            channel="email",
            destination=email,
            is_success=False,
            error_message=str(e),
        )

def send_onboarding_whatsapp(onboarding, phone):
    link = build_onboarding_link(onboarding.token)

    try:
        # TODO: integrate real WA API
        print(f"[WA] Send to {phone}: {link}")

        OnboardingDelivery.objects.create(
            onboarding=onboarding,
            channel="whatsapp",
            destination=phone,
            is_success=True,
        )
    except Exception as e:
        OnboardingDelivery.objects.create(
            onboarding=onboarding,
            channel="whatsapp",
            destination=phone,
            is_success=False,
            error_message=str(e),
        )

    def send_onboarding_link(onboarding, email=None, phone=None):
        if email:
            send_onboarding_email(onboarding, email)

        if phone:
            send_onboarding_whatsapp(onboarding, phone)