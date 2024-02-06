from django import forms
from .models import User

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

# class LoginForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['Email', 'Password']