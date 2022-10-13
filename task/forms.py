from django import forms
from .models import modelTask
# This class is a form that is based on the modelTask model, and it has three fields: title,
# description, and important.
class taskForm(forms.ModelForm):
    class Meta:
        model = modelTask
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }