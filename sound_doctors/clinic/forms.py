from django import forms
from . import models
from django.utils.translation import gettext_lazy as _

class RegularServiceOrderForm(forms.ModelForm):
    class Meta:
        model = models.ServiceOrder
        fields = ['doctor', 'regular_service', "instrument"]

    def __init__(self, *args, **kwargs):
        super(RegularServiceOrderForm, self).__init__(*args, **kwargs)
        self.fields['doctor'].queryset = models.Doctor.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        regular_service = cleaned_data.get('regular_service')

        if not regular_service:
            raise forms.ValidationError(_('Please select a regular service.'))
        return cleaned_data

class CustomServiceOrderForm(forms.ModelForm):
    custom_text = forms.CharField(
        label=_("Custom Text"),
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False
    )

    class Meta:
        model = models.ServiceOrder
        fields = ['doctor', 'instrument', 'custom_text']

    def clean(self):
        cleaned_data = super().clean()
        custom_service = cleaned_data.get('custom_service')
        custom_text = cleaned_data.get('custom_text')

        if not custom_service and not custom_text:
            raise forms.ValidationError(_('Please select a custom service or provide custom details.'))
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