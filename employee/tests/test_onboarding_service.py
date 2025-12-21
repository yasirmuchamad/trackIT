from django.test import TestCase
from django.utils import timezone
from datetime import timedelta, date

from employee.models import *

from employee.services.onboarding import submit_onboarding

class SubmitOnboardingTest(TestCase):

    def setUp(self):
        self.employee = Employee.objects.create(
            employee_id=10001,
            name="yasir",
            join_date=date(2024, 1, 1),
            employment_status="probation"
        )

        self.onboarding = EmployeeOnboarding.objects.create(
            employee = self.employee,
            expires_at=timezone.now() + timedelta(days=1)
        )

    def test_submit_onboarding_success(self):
        payload = {
            "employee": {
                "place_of_birth":"Jakarta",
                "date_of_birth":"1993-01-01",
                "religion":"islam",
                "sex":"male",
                "marital_status":"married",
                "phone":"08647388362",
                "national_id_number":"7939342222342314",
                "family_card_number":"9219071227987912",
            },
            "addresses":[
                {
                    "address_type":"current",
                    "address":"Jl.Sudirman",
                    "village":"Setiabudi",
                    "district":"Setiabudi",
                    "city":"Jakarta",
                    "province":"DKI Jakarta",
                }
            ]
        }

        submit_onboarding(self.onboarding.token, payload)

        self.employee.refresh_from_db()
        self.onboarding.refresh_from_db()

        self.assertEqual(self.employee.place_of_birth, 'Jakarta')
        self.assertTrue(self.onboarding.is_completed)
        self.assertEqual(EmployeeAddress.objects.count(), 1)

    
    def test_expired_token_rejected(self):
        # atur token menjadi expired
        self.onboarding.expires_at = timezone.now() - timedelta(days=1)
        # timezone.now() -> waktu sekarang
        # - timedelda(days=1) -> dikurangi 1 hari yang lalu
        #  jadi token sudah kadaluarsa 
        self.onboarding.save()

        with self.assertRaises(ValidationError):
            submit_onboarding(self.onboarding.token, {})

    def test_employee_id_cannot_be_modified(self):
        payload = {
            "employee":{
                "employee_id":9999,
                "place_of_birth":"Jakarta",
                "date_of_birth":"1993-01-01",
                "religion":"islam",
                "sex":"male",
                "marital_status":"married",
                "phone":"08647388362",
                "national_id_number":"7939342222342314",
                "family_card_number":"9219071227987912",
            },
        }

        submit_onboarding(self.onboarding.token, payload)

        self.employee.refresh_from_db()
        self.assertEqual(self.employee.employee_id, 10001)