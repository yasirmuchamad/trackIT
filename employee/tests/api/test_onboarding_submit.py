from rest_framework.test import APITestCase
from django.urls import reverse
from datetime import date

from employee.models import Employee, EmployeeOnboarding

class OnboardingSubmitAPITest(APITestCase):

    def setUp(self):
        self.employee = Employee.objects.create(
            employee_id=1001,
            name='Yasir',
            join_date=date(2024, 1, 1),
            employment_status='tetap',
            place_of_birth='Jakarta',
            date_of_birth=date(1995, 1, 1),
            religion='islam',
            sex='male',
            marital_status='single',
            national_id_number='1234567890123456',
            family_card_number='1234567890123456',
            bpjs_employment='123',
            bpjs_health='456',
            phone='08123456789',
        )

        self.onboarding = EmployeeOnboarding.objects.create(
            employee=self.employee
        )

        self.url=reverse(
            "onboarding-submit",
            args=[self.onboarding.token]
        )

    def test_onboarding_submit_success(self):
        payload = {
            "employee":{
                "place_of_birth":"Jakarta",
                "date_of_birth":"1993-01-01",
                "phone":"0876523487682"
            }
        }

        response = self.client.post(self.url, payload, format="json")
        
        self.assertEqual(response.status_code, 200)

        self.employee.refresh_from_db()
        self.onboarding.refresh_from_db()

        self.assertEqual(self.employee.place_of_birth, "Jakarta")
        self.assertTrue(self.onboarding.is_completed)

    def test_onboarding_cannot_be_submitted_twice(self):
        self.onboarding.is_completed = True
        self.onboarding.save()

        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(response.status_code, 400)
