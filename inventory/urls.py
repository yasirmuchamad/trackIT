from django.urls import path
from .views import *

app_name = 'inventory'
urlpatterns = [
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/create', CategoryCreateView.as_view(), name='create_category'),
    path('category/update/<int:pk>', CategoryUpdateView.as_view(), name='create_category'),
]
