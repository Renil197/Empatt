from django import forms
from django.contrib.auth.models import User

class EmployeeForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        required=False, 
        help_text="Leave blank if updating without changing password."
    )
    # Changed 'default' to 'initial' here:
    role = forms.ChoiceField(
        choices=[('employee', 'Employee'), ('admin', 'Admin')], 
        initial='employee',  
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }