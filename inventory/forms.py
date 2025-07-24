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
