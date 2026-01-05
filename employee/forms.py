from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date

from .models import (
    Employee, EmployeeAddress, EmployeeFamily, 
    EmployeeStudied, EmployeeHistory, Unit, 
    Department, Subdepartment, Position, EmployeeWorkExperience
)


class EmployeeCreateForm(forms.ModelForm):
    """Form for creating new employee"""
    
    class Meta:
        model = Employee
        fields = [
            'employee_id', 'name', 'join_date', 'employment_status',
            'place_of_birth', 'date_of_birth', 'religion', 'sex', 
            'marital_status', 'national_id_number', 'family_card_number',
            'phone', 'private_mail', 'company_mail', 'blood_type', 'photo'
        ]
        widgets = {
            'join_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'employee_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'employment_status': forms.Select(attrs={'class': 'form-control'}),
            'place_of_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'religion': forms.Select(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            'national_id_number': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '16'}),
            'family_card_number': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '16'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'private_mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'company_mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'blood_type': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
    
    def clean_employee_id(self):
        employee_id = self.cleaned_data.get('employee_id')
        if Employee.objects.filter(employee_id=employee_id).exists():
            raise ValidationError("Employee ID already exists.")
        return employee_id
    
    def clean_join_date(self):
        join_date = self.cleaned_data.get('join_date')
        if join_date and join_date > timezone.now().date():
            raise ValidationError("Join date cannot be in the future.")
        return join_date
    
    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            # Check file size (5MB max)
            if photo.size > 5 * 1024 * 1024:
                raise ValidationError("Image file too large. Maximum size is 5MB.")
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if photo.content_type not in allowed_types:
                raise ValidationError("Invalid file type. Please upload JPG, PNG, or GIF.")
        
        return photo
    
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth:
            today = timezone.now().date()
            age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            if age < 17:
                raise ValidationError("Employee must be at least 17 years old.")
            if age > 65:
                raise ValidationError("Employee age cannot exceed 65 years.")
        return date_of_birth


class EmployeeUpdateForm(forms.ModelForm):
    """Form for updating employee information"""
    
    class Meta:
        model = Employee
        fields = [
            'name', 'employment_status', 'permanent_date',
            'place_of_birth', 'date_of_birth', 'religion', 'sex', 
            'marital_status', 'national_id_number', 'family_card_number',
            'bpjs_employment', 'bpjs_health', 'tax_id', 'blood_type',
            'phone', 'private_mail', 'company_mail', 'photo'
        ]
        widgets = {
            'permanent_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'employment_status': forms.Select(attrs={'class': 'form-control'}),
            'place_of_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'religion': forms.Select(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            'national_id_number': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '16'}),
            'family_card_number': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '16'}),
            'bpjs_employment': forms.TextInput(attrs={'class': 'form-control'}),
            'bpjs_health': forms.TextInput(attrs={'class': 'form-control'}),
            'tax_id': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'private_mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'company_mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'blood_type': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
    
    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            # Check file size (5MB max)
            if photo.size > 5 * 1024 * 1024:
                raise ValidationError("Image file too large. Maximum size is 5MB.")
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if photo.content_type not in allowed_types:
                raise ValidationError("Invalid file type. Please upload JPG, PNG, or GIF.")
        
        return photo


class EmployeeSearchForm(forms.Form):
    """Form for searching employees"""
    
    STATUS_CHOICES = [
        ('', 'All Status'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, ID, or email...'
        })
    )
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    unit = forms.ModelChoiceField(
        queryset=Unit.objects.all(),
        required=False,
        empty_label="All Units",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class EmployeeAddressForm(forms.ModelForm):
    """Form for employee address"""
    
    class Meta:
        model = EmployeeAddress
        fields = ['address_type', 'address', 'village', 'district', 'city', 'province']
        widgets = {
            'address_type': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'village': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'province': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EmployeeFamilyForm(forms.ModelForm):
    """Form for employee family member"""
    
    class Meta:
        model = EmployeeFamily
        fields = ['name', 'sex', 'relationship', 'date_of_birth']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'relationship': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class EmployeeEducationForm(forms.ModelForm):
    """Form for employee education"""
    
    class Meta:
        model = EmployeeStudied
        fields = ['institution_name', 'graduation_year', 'major', 'degree']
        widgets = {
            'institution_name': forms.TextInput(attrs={'class': 'form-control'}),
            'graduation_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'major': forms.TextInput(attrs={'class': 'form-control'}),
            'degree': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EmployeeHistoryForm(forms.ModelForm):
    """Form for employee position history"""
    
    class Meta:
        model = EmployeeHistory
        fields = ['subdepartment', 'position', 'grade', 'start_date']
        widgets = {
            'subdepartment': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    
    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date and start_date > timezone.now().date():
            raise ValidationError("Start date cannot be in the future.")
        return start_date


# Formsets for handling multiple related objects
from django.forms import inlineformset_factory

EmployeeAddressFormSet = inlineformset_factory(
    Employee, 
    EmployeeAddress, 
    form=EmployeeAddressForm,
    extra=1,
    can_delete=True
)

EmployeeFamilyFormSet = inlineformset_factory(
    Employee, 
    EmployeeFamily, 
    form=EmployeeFamilyForm,
    extra=1,
    can_delete=True
)

EmployeeEducationFormSet = inlineformset_factory(
    Employee, 
    EmployeeStudied, 
    form=EmployeeEducationForm,
    extra=1,
    can_delete=True
)

class EmployeeWorkExperienceForm(forms.ModelForm):
    """Form for employee work experience"""
    
    class Meta:
        model = EmployeeWorkExperience
        fields = [
            'company_name', 'position', 'department', 'start_date', 'end_date',
            'job_description', 'reason_for_leaving', 'salary_range',
            'supervisor_name', 'supervisor_contact'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama perusahaan'
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Posisi/jabatan'
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Departemen/divisi'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'job_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Deskripsi pekerjaan dan tanggung jawab'
            }),
            'reason_for_leaving': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Alasan meninggalkan pekerjaan'
            }),
            'salary_range': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Range gaji (opsional)'
            }),
            'supervisor_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama atasan langsung'
            }),
            'supervisor_contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email/telepon atasan'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if start_date >= end_date:
                raise ValidationError({
                    'end_date': 'Tanggal selesai harus setelah tanggal mulai'
                })
            
            # Validasi tidak boleh di masa depan
            today = date.today()
            if start_date > today:
                raise ValidationError({
                    'start_date': 'Tanggal mulai tidak boleh di masa depan'
                })
            if end_date > today:
                raise ValidationError({
                    'end_date': 'Tanggal selesai tidak boleh di masa depan'
                })
        
        return cleaned_data


# Formset untuk multiple work experience entries
EmployeeWorkExperienceFormSet = forms.modelformset_factory(
    EmployeeWorkExperience,
    form=EmployeeWorkExperienceForm,
    extra=1,  # Satu form kosong tambahan
    max_num=3,  # Maksimal 3 pengalaman kerja
    validate_max=True,
    can_delete=True
)