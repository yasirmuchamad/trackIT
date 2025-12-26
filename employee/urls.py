from django.urls import path
from .views import *
from employee.api.onboarding import OnboardingSubmitAPIView

app_name = 'employees'
urlpatterns = [
    # API URLs
    path("api/onboarding/submit/<uuid:token>/", 
         OnboardingSubmitAPIView.as_view(),
         name="onboarding-submit"),
    
    # AJAX URLs
    path('ajax/departments/', get_departments, name='get_departments'),
    path('ajax/subdepartments/', get_subdepartments, name='get_subdepartments'),
    
    # Dashboard
    path('', employee_dashboard, name='dashboard'),
    
    # Employee CRUD
    path('list/', employee_list, name='employee_list'),
    path('create/', create_employee, name='create_employee'),
    path('<int:employee_id>/', employee_detail, name='employee_detail'),
    path('<int:employee_id>/update/', update_employee, name='update_employee'),
    path('<int:employee_id>/deactivate/', deactivate_employee, name='deactivate_employee'),
    
    # Employee History
    path('<int:employee_id>/history/create/', employee_history_create, name='employee_history_create'),
    
    # Onboarding
    path('onboarding/', onboarding_list, name='onboarding_list'),
    path('onboarding/<int:onboarding_id>/resend/', resend_onboarding, name='resend_onboarding'),
]