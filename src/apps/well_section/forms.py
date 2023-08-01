from django import forms
from django.forms import modelformset_factory
from .models import Bird

class DynamicFieldForm(forms.Form):
    field_name = forms.CharField(max_length=100)
    
BirdFormSet = modelformset_factory(
    Bird, fields=("common_name", "scientific_name"), extra=1
)