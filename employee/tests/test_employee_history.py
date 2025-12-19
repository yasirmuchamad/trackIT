from django.test import TestCase
from django.db import IntegrityError
from datetime import date

from employee.models import *

class EmployeeHistoryConstrainstTest(TestCase):
    def setUp(self):
        self.unit = Unit.objects.create(name='office')
        self.department = Department.objects.create(
            name= 'IT',
            unit=self.unit
        )
        self.subdepartment = Subdepartment.objects.create(
            name='Infrastructure',
            department=self.department
        )
        self.position = Position.objects.create(
            name='Staff'
        )
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

    def test_first_history_can_be_active(self):
        history = EmployeeHistory.objects.create(
            employee=self.employee,
            subdepartment=self.subdepartment,
            position=self.position,
            start_date=date(2024, 1, 1),
            is_active=True,
        )

        self.assertTrue(history.is_active)
        self.assertIsNone(history.end_date)

    def test_new_history_deactivates_previous_one(self):
        old_history=EmployeeHistory.objects.create(
            employee = self.employee,
            subdepartment=self.subdepartment,
            position=self.position,
            start_date=date(2024, 1, 1),
            is_active=True,
        )

        new_history=EmployeeHistory.objects.create(
            employee=self.employee,
            subdepartment=self.subdepartment,
            position=self.position,
            start_date=date(2024, 6, 1),
            is_active=True,
        )

        old_history.refresh_from_db()

        self.assertFalse(old_history.is_active)
        self.assertEqual(old_history.end_date, date(2024, 6, 1))
        self.assertTrue(new_history.is_active)

        def test_database_constrainst_prevents_multiple_active_history(self):
            EmployeeHistory.objects.create(
                employee=self.employee,
                subdepartment=self.subdepartment,
                position=self.position,
                start_date=date(2024, 6, 1),
                is_active=True,
            )

            with self.assertRaises(IntegrityError):
                EmployeeHistory.objects.create(
                    employee=self.employee,
                    subdepartment=self.subdepartment,
                    position=self.position,
                    start_date=date(2024, 2, 1),
                    is_active=True,
                )

class SmokeTest(TestCase):
    def test_it_works(self):
        self.assertTrue(True)