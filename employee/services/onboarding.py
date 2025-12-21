from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from employee.models import *


@transaction.atomic
def submit_onboarding(token, payload):
    """
    Submit employee onboarding using token
    """
    
    try:
        onboarding = EmployeeOnboarding.objects.select_related(
            'employee'
        ).get(token=token)
    except EmployeeOnboarding.DoesNotExist:
        raise ValidationError("Invalid onboarding token")
    

    if onboarding.is_completed:
        raise ValidationError("Onboarding already completed")

    if onboarding.is_expired():
        raise ValidationError("Onboarding token has expired")
    
    employee = onboarding.employee

    
    
    # ====================================
    # Update personal data employee
    # ====================================
    employee_data = payload.get("employee", {})

    allowed_fields = [                  # hanya field ini yang diijinkan diubah
        "place_of_birth",
        "date_of_birth",
        "religion",
        "sex",
        "marital_status",
        "blood_type",
        "national_id_number",
        "family_card_number",
        "bpjs_employment",
        "bpjs_health",
        "tax_id",
        "phone",
        "private_mail",
    ]

    required_fields = [
        "place_of_birth",
        "date_of_birth",
        "religion",
        "sex",
        "marital_status",
        "national_id_number",
        "family_card_number",
        "phone"
    ]

    for field in required_fields:
        if not employee_data.get(field):
            raise ValidationError(f"{field} is required")

    for field in allowed_fields:                # Ulangi satu persatu field yang diijinkan
        if field in employee_data:              # apakah form mengirim field ini?
            setattr(employee, field, employee_data[field])      # setattr(employee, "phone", "0838")

    employee.full_clean()
    employee.save()

    # =======================================
    # replace employee data
    # =======================================
    EmployeeAddress.objects.filter(employee=employee).delete()
    EmployeeFamily.objects.filter(employee=employee).delete()
    EmployeeStudied.objects.filter(employee=employee).delete()

    # Addresses
    for address in payload.get("addresses", []):
        EmployeeAddress.objects.create(
            employee=employee,
            **address
        )

    # Families
    for family in payload.get("families", []):
        EmployeeFamily.objects.create(
            employee=employee,
            **family
        )

    # Education
    for education in payload.get("educations", []):
        EmployeeStudied.objects.create(
            employee=employee,
            **education
        )

    # =========================================
    # Finalize
    #  ==========================================
    onboarding.is_completed = True
    onboarding.completed_at = timezone.now()
    onboarding.save()

    return employee
