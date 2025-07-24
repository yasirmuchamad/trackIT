from django import forms
from .models import *
from django.forms import DateTimeInput

class CategoryForm(forms.ModelForm):
    """Form definition for Category."""

    class Meta:
        """Meta definition for Categoryform."""

        model = Category
        fields = '__all__'

    def __init__(self, *args, **KWarg):
        super(CategoryForm, self).__init__(*args, **KWarg)
        self.fields['name'].widget.attrs.update({'id':'cat_name', 'name':'cat_name',
                'class':'form-control', 'placeholder':'Input Category Name'}) 

class DepartementForm(forms.ModelForm):
    """Form definition for Departement."""

    class Meta:
        """Meta definition for Departementform."""

        model = Departement
        fields = '__all__'

    def __init__(self, *args, **KWarg):
        super(DepartementForm, self).__init__(*args, **KWarg)
        self.fields['name'].widget.attrs.update({'id':'cat_name', 'name':'cat_name',
                'class':'form-control', 'placeholder':'Input Departement Name'}) 
        self.fields['leader'].widget.attrs.update({'id':'leader', 'name':'leader',
                'class':'form-control', 'placeholder':'Input Leader Name'}) 

class EmployeeForm(forms.ModelForm):
    """Form definition for Employee."""

    class Meta:
        """Meta definition for Employeeform."""

        model = Employee
        fields = '__all__'

    def __init__(self, *args, **KWarg):
        super(EmployeeForm, self).__init__(*args, **KWarg)
        self.fields['user'].widget.attrs.update({'id':'user', 'name':'user',
                'class':'form-control'}) 
        self.fields['employee_id'].widget.attrs.update({'id':'employee_id', 'name':'employee_id',
                'class':'form-control', 'placeholder':'Input Employee Number'}) 
        self.fields['name'].widget.attrs.update({'id':'name', 'name':'name',
                'class':'form-control', 'placeholder':'Input Employee Number'})
        self.fields['departement'].widget.attrs.update({'id':'departement', 'name':'departement',
                'class':'form-control'}) 
        self.fields['position'].widget.attrs.update({'id':'position', 'name':'position',
                'class':'form-control'})
        self.fields['email'].widget.attrs.update({'id':'email', 'name':'email',
                'class':'form-control'})
        self.fields['phone'].widget.attrs.update({'id':'phone', 'name':'phone',
                'class':'form-control'})
