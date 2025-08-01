from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from inventory.models import Category, Departement, Employee, Item, ItemUnit
from django.utils import timezone

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='admin', password='pass')
        self.client.force_login(self.user)

        self.category = Category.objects.create(name='Electronics')
        self.departement = Departement.objects.create(name='HR', leader='John Smith')
        self.employee = Employee.objects.create(
            user=self.user,
            employee_id='EMP002',
            name='Alice',
            departement=self.departement,
            position='Manager',
            email='alice@example.com'
        )
        self.item = Item.objects.create(
            sku_code='ITEM001',
            category=self.category,
            name='Laptop',
            brand='HP',
            model='Elitebook',
            entry_date=timezone.now()
        )
        self.item_unit = ItemUnit.objects.create(
            asset_number='AS123',
            item=self.item,
            serial_number='SN001',
            location='IT Room',
            status='in_use',
            condition='good',
            current_user=self.employee
        )

    def test_category_list_view(self):
        response = self.client.get(reverse('inventory:list_category'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'List Category')
        self.assertContains(response, self.category.name)

    def test_departement_list_view(self):
        response = self.client.get(reverse('inventory:list_departement'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.departement.name)

    def test_employee_list_view(self):
        response = self.client.get(reverse('inventory:list_employee'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.employee.name)

    def test_item_list_view(self):
        response = self.client.get(reverse('inventory:list_item'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.name)

    def test_item_unit_list_view(self):
        response = self.client.get(reverse('inventory:list_item_unit'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item_unit.asset_number)

    def test_category_excel_export(self):
        response = self.client.get(reverse('inventory:category_to_excel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    def test_departement_excel_export(self):
        response = self.client.get(reverse('inventory:departement_to_excel'))
        self.assertEqual(response.status_code, 200)

    def test_employee_excel_export(self):
        response = self.client.get(reverse('inventory:list_employee'))
        self.assertEqual(response.status_code, 200)

    def test_item_excel_export(self):
        response = self.client.get(reverse('inventory:item_to_excel'))
        self.assertEqual(response.status_code, 200)

    def test_item_unit_excel_export(self):
        response = self.client.get(reverse('inventory:item_unit_to_excel'))
        self.assertEqual(response.status_code, 200)
