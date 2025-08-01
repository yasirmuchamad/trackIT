from django.urls import path
from .views import *

app_name = 'inventory'
urlpatterns = [
    path('category/', CategoryListView.as_view(), name='list_category'),
    path('category/create', CategoryCreateView.as_view(), name='create_category'),
    path('category/update/<int:pk>', CategoryUpdateView.as_view(), name='update_category'),
    path('category/delete/<int:pk>', CategoryDeleteView.as_view(), name='delete_category'),
    path('category/export', categoryToExcel, name='category_to_excel'),

    path('departement/', DepartementListView.as_view(), name='list_departement'),
    path('departement/create', DepartementCreateView.as_view(), name='create_departement'),
    path('departement/update/<int:pk>', DepartementUpdateView.as_view(), name='update_departement'),
    path('departement/delete/<int:pk>', DepartementDeleteView.as_view(), name='delete_departement'),
    path('departement/export', departementToExcel, name='departement_to_excel'),

    path('employee/', EmployeeListView.as_view(), name='list_employee'),
    path('employee/create', EmployeeCreateView.as_view(), name='create_employee'),
    path('employee/update/<int:pk>', EmployeeUpdateView.as_view(), name='update_employee'),
    path('employee/delete/<int:pk>', EmployeeDeleteView.as_view(), name='delete_employee'),
    path('employee/export', employeeToExcel, name='employee_to_excel'),

    path('item/', ItemListView.as_view(), name='list_item'),
    path('item/create', ItemCreateView.as_view(), name='create_item'),
    path('item/update/<int:pk>', ItemUpdateView.as_view(), name='update_item'),
    path('item/delete/<int:pk>', ItemDeleteView.as_view(), name='delete_item'),
    path('item/export', itemToExcel, name='item_to_excel'),

    path('item_unit/', ItemUnitListView.as_view(), name='list_item_unit'),
    path('item_unit/create', ItemUnitCreateView.as_view(), name='create_item_unit'),
    path('item_unit/update/<int:pk>', ItemUnitUpdateView.as_view(), name='update_item_unit'),
    path('item_unit/delete/<int:pk>', ItemUnitDeleteView.as_view(), name='delete_item_unit'),
    path('item_unit/export', itemunitToExcel, name='item_unit_to_excel'),
]
