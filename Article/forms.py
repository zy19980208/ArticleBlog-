from django import forms

class Register(forms.Form):
    name = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32)

