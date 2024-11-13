# forms.py

from django import forms
from .models import CallbackRequest

class CallbackRequestForm(forms.ModelForm):
    class Meta:
        model = CallbackRequest
        fields = ['name', 'phone_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш номер телефона'}),
        }
