from django.test import TesctCase
from django.db import IntegrityError
from datetime import date

from employee.models import *

class EmployeeHistoryConstrainsTest(TesctCase):
    def setUp(self):
        self.unit = Unit.objects.create(name='office')
        self.department = Department.objects.create(
            name= 'IT',
            unit=self.unit
        )
        self.subdepartment = Subdepartment.objects.create(
            name='Infrastructure',
            departement=self.department
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
                subdepartment=self.subdepartements,
                position=self.position,
                start_date=date(2024, 1, 1),
                is_active=True,
            )

            self.assertTrue(history.is_active)
            self.assertIsNone(history.end_date)