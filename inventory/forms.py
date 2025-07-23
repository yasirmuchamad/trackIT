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
        self.fields['name'].widget.attrs.update({'id':'name', 'name':'name',
                'class':'form-control', 'placeholder':'Input Category Name'}) 
