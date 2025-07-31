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

class ItemForm(forms.ModelForm):
    """Form definition for Iteme."""

    class Meta:
        """Meta definition for Itemeform."""

        model = Item
        # fields = '__all__'
        exclude = ('entry_date',)

    def __init__(self, *args, **KWarg):
        super(ItemForm, self).__init__(*args, **KWarg)
        self.fields['sku_code'].widget.attrs.update({'id':'sku_code', 'name':'sku_code',
                'class':'form-control', 'placeholder':'example : pc-thtf-e500'}) 
        self.fields['category'].widget.attrs.update({'id':'category', 'name':'category',
                'class':'form-control'}) 
        self.fields['name'].widget.attrs.update({'id':'name', 'name':'name',
                'class':'form-control', 'placeholder':'Input Item Name'})
        self.fields['brand'].widget.attrs.update({'id':'brand', 'name':'brand',
                'class':'form-control', 'placeholder':'Input Brand'}) 
        self.fields['model'].widget.attrs.update({'id':'model', 'name':'model',
                'class':'form-control', 'placeholder':'example : Laserjet'})
        self.fields['cpu'].widget.attrs.update({'id':'cpu', 'name':'cpu',
                'class':'form-control', 'placeholder':'Input Processor'})
        self.fields['ram'].widget.attrs.update({'id':'phone', 'name':'phone',
                'class':'form-control', 'placeholder':'Input Memory Capacity'})
        self.fields['storage'].widget.attrs.update({'id':'ram', 'name':'ram',
                'class':'form-control', 'placeholder':'Input Storage'})
        self.fields['display'].widget.attrs.update({'id':'display', 'name':'display',
                'class':'form-control', 'placeholder':'Input Display Resolution'})
        self.fields['os'].widget.attrs.update({'id':'os', 'name':'os',
                'class':'form-control', 'placeholder':'Input Operating System'})
        

class ItemUnitForm(forms.ModelForm):
    """Form definition for Iteme."""

    class Meta:
        """Meta definition for Itemeform."""

        model = ItemUnit
        fields = '__all__'
        # exclude = ('entry_date',)

    def __init__(self, *args, **KWarg):
        super(ItemUnitForm, self).__init__(*args, **KWarg)
        self.fields['item'].widget.attrs.update({'id':'item', 'name':'item',
                'class':'form-control'}) 
        self.fields['serial_number'].widget.attrs.update({'id':'serial_number', 'name':'serial_number',
                'class':'form-control', 'placeholder':'Input serial number'}) 
        self.fields['location'].widget.attrs.update({'id':'location', 'name':'location',
                'class':'form-control', 'placeholder':'Input Location'})
        self.fields['ip_address'].widget.attrs.update({'id':'ip_address', 'name':'ip_address',
                'class':'form-control', 'placeholder':'Input IP Address'}) 
        self.fields['status'].widget.attrs.update({'id':'status', 'name':'status',
                'class':'form-control'})
        self.fields['condition'].widget.attrs.update({'id':'condition', 'name':'condition',
                'class':'form-control'})
        self.fields['current_user'].widget.attrs.update({'id':'current_user', 'name':'current_user',
                'class':'form-control'})