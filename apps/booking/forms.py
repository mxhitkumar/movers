from django import forms
from .models import ContactSubmission

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ["name", "email", "phone", "service", "message", "botcheck"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control required", "id": "template-contactform-name"}),
            "email": forms.EmailInput(attrs={"class": "required email form-control", "id": "template-contactform-email"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "id": "template-contactform-phone"}),
            "service": forms.Select(attrs={"class": "form-select", "id": "template-contactform-service"}),
            "message": forms.Textarea(attrs={"class": "required form-control", "rows": 6, "id": "template-contactform-message"}),
            "botcheck": forms.TextInput(attrs={"class": "form-control", "id": "template-contactform-botcheck", "autocomplete": "off"}),
        }

    def clean_botcheck(self):
        value = self.cleaned_data.get("botcheck", "")
        # honeypot: humans should leave this blank
        if value:
            raise forms.ValidationError("Bot detected.")
        return value
