from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from employee.forms import EmployeeCreateForm
from employee.models import EmployeeOnboarding
from employee.services.onboarding_delivery import send_onboarding_links


# Create your views here.
@login_required
def create_employee(request):
    if request.method == "POST":
        form = EmployeeCreateForm(request.POST)

        if form.is_valid():
            employee = form.save()

            onboarding = EmployeeOnboarding.create_for_employee(employee)

            send_onboarding_links(
                onboarding,
                email=employee.private_mail,
                phone=employee.phone,
            )

            messages.is_succces(
                request,
                "Employee created and onboarding link sent."
            )
            return redirect("employee_liast")
        
    else:
        form = EmployeeCreateForm()

    return render(
        request,
        "employee/hr/create_employee.html",
        {"form":form}
    )
