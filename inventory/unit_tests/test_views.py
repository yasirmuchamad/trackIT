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

class ItemUnitViewTests(TestCase):
    def setUp(self):
        # Buat user login dulu jika viewnya pakai @login_required
        self.user = User.objects.create_user(username='tester', password='pass')
        self.client.login(username='tester', password='pass')
         # Buat kategori dulu karena item membutuhkan category
        self.category = Category.objects.create(name='Laptop')
        
        # Buat item dulu karena ItemUnit membutuhkan foreign key item
        self.item = Item.objects.create(
            name='Lenovo ThinkPad',
            # barcode='123456789',
            category=self.category,
        )
        self.item_unit = ItemUnit.objects.create(
            asset_number='GTI-PC-0033',
            item=self.item,
            location='Compleks', 
            status='in_use',
            condition= 'good',
        )

    def test_create_item_unit(self):
        url = reverse('inventory:create_item_unit')  # sesuaikan dengan urls.py
        data = {'asset_number': 'GTI-PC-0029', 'item':self.item.id, 'location':'Compleks', 'status':'in_use', 'condition': 'good',}
        response = self.client.post(url, data)
        if response.status_code == 200:
            print("CREATE FORM ERRORS:", response.context['form'].errors)
        self.assertEqual(response.status_code, 302)  # redirect sukses
        self.assertTrue(ItemUnit.objects.filter(asset_number='GTI-PC-0029').exists())

    def test_update_item_unit(self):
        url = reverse('inventory:update_item_unit', args=[self.item_unit.pk])
        data = {'asset_number': 'GTI-PC-0029', 'item':self.item.id, 'location':'Compleks', 'status':'in_use', 'condition': 'good',}
        response = self.client.post(url, data)
        if response.status_code == 200:
            print("CREATE FORM ERRORS:", response.context['form'].errors)
        self.assertEqual(response.status_code, 302)
        self.item_unit.refresh_from_db()
        self.assertEqual(self.item_unit.asset_number, 'GTI-PC-0029')