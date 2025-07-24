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
]
