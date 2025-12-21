from django.urls import path
from .views import *
from employee.api.onboarding import OnboardingSubmitAPIView

app_name = 'employees'
urlpatterns = [
    path("api/onboarding/submit/<uuid:token>/", 
         OnboardingSubmitAPIView.as_view(),
         name="onboarding-submit"),

    # path('/', CategoryListView.as_view(), name='list_category'),
    # path('category/create', CategoryCreateView.as_view(), name='create_category'),
    # path('category/update/<int:pk>', CategoryUpdateView.as_view(), name='update_category'),
    # path('category/delete/<int:pk>', CategoryDeleteView.as_view(), name='delete_category'),
    # path('category/export', categoryToExcel, name='category_to_excel'),
    
]