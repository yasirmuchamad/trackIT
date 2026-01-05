"""
URL configuration for trackIT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from employee.views import onboarding_form

def home_redirect(request):
    """Redirect root URL to employee dashboard"""
    return redirect('employees:dashboard')

urlpatterns = [
    path('', home_redirect, name='home'),  # Add default redirect
    path('admin/', admin.site.urls),
    path('employees/', include('employee.urls')),
    path('inventory/', include('inventory.urls')),
    path('maintenance/', include('maintenance.urls')),
    
    # Public onboarding URL (no login required)
    path('onboarding/<uuid:token>/', onboarding_form, name='onboarding_form'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
