from django.contrib import admin
from django.urls import path

app_name = 'inventory'
urlpatterns = [
    path('category/', views.listCategory, name='list_category'),
]
