from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'luxury-input'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'luxury-input'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'luxury-input', 'rows': 6})
    )