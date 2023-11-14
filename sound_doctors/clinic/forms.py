from django import forms
from . import models
from django.utils.translation import gettext_lazy as _

class ServiceOrderForm(forms.ModelForm):
    class Meta:
        model = models.ServiceOrder
        fields = ['service', 'doctor']


class ServiceOrderForm(forms.ModelForm):
    custom_text = forms.CharField(label=_("Custom Order Details"), required=False, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    custom_img = forms.ImageField(label=_("Image (optional)"), required=False)
    service = forms.ModelChoiceField(
        queryset=models.Service.objects.all(),
        label=_("Service"),
        required=False  # Service field is not required for a custom order
    )

    class Meta:
        model = models.ServiceOrder
        fields = ['service', 'doctor']

    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get('service')
        custom_text = cleaned_data.get('custom_text')
        custom_img = cleaned_data.get('custom_img')

        # Check if either custom_text or custom_img is provided for a custom order
        if not service and not (custom_text or custom_img):
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