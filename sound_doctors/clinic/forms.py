from django import forms
from . import models

class ServiceOrderForm(forms.ModelForm):
    class Meta:
        model = models.ServiceOrder
        fields = ['service', 'doctor']