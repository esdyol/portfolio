from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", "email", "subject", "message")
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Votre nom", "autocomplete": "name"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Votre email", "autocomplete": "email"}
            ),
            "subject": forms.TextInput(attrs={"placeholder": "Votre sujet"}),
            "message": forms.Textarea(attrs={"placeholder": "Votre message"}),
        }
