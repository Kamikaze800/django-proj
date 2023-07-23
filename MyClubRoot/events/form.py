from django import forms
from django.forms import ModelForm
from .models import Venue

class VenueForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Venue
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        web = cleaned_data.get('web')
        email = cleaned_data.get('email')
        if not(web or email):
            raise forms.ValidationError(
                'You must enter either web or email, or both'
            )