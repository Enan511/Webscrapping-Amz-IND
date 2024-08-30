# forms.py
from django import forms

class AmazonProductForm(forms.Form):
    url = forms.URLField(label='Amazon Product URL', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
