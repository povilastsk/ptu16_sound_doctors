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

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError("Review content cannot be empty.")
        return content
    

class AlbumReviewForm(forms.ModelForm):
    class Meta:
        model = models.AlbumReview
        fields = ('content', 'album', 'reviewer')
        widgets = {
            'album': forms.HiddenInput(),
            'reviewer': forms.HiddenInput(),
        }
        labels = {
            'content': '',
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError("Review content cannot be empty.")
        return content