from django import forms
from . import models

class ServiceOrderForm(forms.ModelForm):
    class Meta:
        model = models.ServiceOrder
        fields = ['service', 'doctor']

class ServiceReviewForm(forms.ModelForm):
    class Meta:
        model = models.ServiceReview
        fields = ('content', 'service', 'reviewer')
        widgets = {
            'service': forms.HiddenInput(),
            'reviewer': forms.HiddenInput(),
        }
        labels = {
            'content': '',
        }