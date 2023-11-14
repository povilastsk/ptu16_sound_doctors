from django import forms
from . import models
from django.utils.translation import gettext_lazy as _

class RegularServiceOrderForm(forms.ModelForm):
    class Meta:
        model = models.ServiceOrder
        fields = ['doctor', 'regular_service', 'status']
        

class CustomServiceOrderForm(forms.ModelForm):
    instrument = forms.ModelChoiceField(
        queryset= models.Instrument.objects.all(),
        label=_("Instrument"),
        required=False
    )

    class Meta:
        model = models.ServiceOrder
        fields = ['doctor', 'custom_service', 'instrument', 'status']

    def clean(self):
        cleaned_data = super().clean()
        custom_service = cleaned_data.get('custom_service')
        custom_text = cleaned_data.get('custom_text')
        custom_img = cleaned_data.get('custom_img')

        # Check if either custom_text or custom_img is provided for a custom order
        if not custom_service and not (custom_text or custom_img):
            raise forms.ValidationError(_('Either select a regular service or provide custom details for a custom order.'))
        return cleaned_data


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