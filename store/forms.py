from django import forms
from .models import CommissionOffering

class ContactForm(forms.Form):
    INQUIRY_CHOICES = (
        ("commission", "Commission enquiry"),
        ("artwork", "Artwork question"),
        ("business", "Business or collaboration"),
        ("general", "Other / general enquiry"),
    )

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "luxury-input",
            "autocomplete": "name",
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "luxury-input",
            "autocomplete": "email",
        })
    )
    inquiry_type = forms.ChoiceField(
        choices=INQUIRY_CHOICES,
        label="What is your enquiry about?",
        widget=forms.Select(attrs={"class": "luxury-input"}),
        initial="general",
    )
    commission_offering = forms.ModelChoiceField(
        queryset=CommissionOffering.objects.filter(is_active=True),
        required=False,
        empty_label="Choose an offering (optional)",
        label="Commission type",
        widget=forms.Select(attrs={"class": "luxury-input"}),
    )
    project_size = forms.CharField(
        max_length=120,
        required=False,
        label="Preferred size or format (optional)",
        widget=forms.TextInput(attrs={"class": "luxury-input"}),
    )
    budget = forms.CharField(
        max_length=120,
        required=False,
        label="Approximate budget (optional)",
        widget=forms.TextInput(attrs={"class": "luxury-input"}),
    )
    timeframe = forms.CharField(
        max_length=120,
        required=False,
        label="Ideal timeframe (optional)",
        widget=forms.TextInput(attrs={"class": "luxury-input"}),
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={"class": "luxury-input", "rows": 6})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self:
            if field.errors:
                field.field.widget.attrs.update({
                    "aria-invalid": "true",
                    "aria-describedby": f"{field.auto_id}-errors",
                })