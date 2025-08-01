from django.test import TestCase
from django.contrib.auth.models import User
from inventory.models import Departement, Employee, Category, Item, ItemUnit
from django.utils import timezone

class ModelTestCase(TestCase):
    def setUp(self):
        # Create basic objects to reuse
        self.user = User.objects.create(username='john')
        self.departement = Departement.objects.create(name='IT', leader='Jane')
        self.employee = Employee.objects.create(
            user=self.user,
            employee_id='EMP001',
            name='John Doe',
            departement=self.departement,
            position='Developer',
            email='john@example.com',
            phone='08123456789'
        )
        self.category = Category.objects.create(name='Laptop')
        self.item = Item.objects.create(
            sku_code='SKU123',
            category=self.category,
            name='MacBook Pro',
            brand='Apple',
            model='2021',
            cpu='M1',
            ram='16GB',
            storage='512GB',
            display='13 inch',
            os='macOS',
            entry_date=timezone.now()
        )

    def test_departement_str(self):
        self.assertEqual(str(self.departement), 'IT Jane')

    def test_employee_str(self):
        self.assertEqual(str(self.employee), 'EMP001 - John Doe')

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Laptop')

    def test_item_str(self):
        self.assertEqual(str(self.item), 'MacBook Pro Apple 2021')

    def test_item_unit_creation_and_str(self):
        unit = ItemUnit.objects.create(
            asset_number='AS001',
            item=self.item,
            serial_number='SN123456',
            location='Office',
            ip_address='192.168.1.10',
            status='in_use',
            condition='good',
            current_user=self.employee
        )
        self.assertEqual(str(unit), 'SN123456')
        self.assertEqual(unit.item, self.item)
        self.assertEqual(unit.current_user.name, 'John Doe')
