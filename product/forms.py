# forms.py
from django import forms


class AmazonURLForm(forms.Form):
    url = forms.URLField(label='Amazon Product URL', max_length=200,
                         widget=forms.TextInput(attrs={'class': 'form-control'}))
