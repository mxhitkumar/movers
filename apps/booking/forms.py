from django import forms
from .models import ContactSubmission, MovingRequest

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

class MovingRequestForm(forms.ModelForm):
    class Meta:
        model = MovingRequest
        fields = [
            "location_from",
            "location_to",
            "name",
            "email",
            "phone",
            "date",
            "botcheck",
        ]
        widgets = {
            "location_from": forms.TextInput(attrs={"placeholder": "Location From"}),
            "location_to": forms.TextInput(attrs={"placeholder": "Location To"}),
            "name": forms.TextInput(attrs={"placeholder": "Your Full Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Your Email", "type": "email"}),
            "phone": forms.TextInput(attrs={"placeholder": "Your Phone Number", "type": "number"}),
            "date": forms.TextInput(attrs={"placeholder": "Your Date", "class": "home-date"}),
            "botcheck": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add the same classes as your original inputs
        for field_name in ["location_from", "location_to", "name", "email", "phone", "date"]:
            field = self.fields[field_name]
            css = "form-control required"
            # preserve any class passed in widget attrs (e.g. home-date)
            existing = field.widget.attrs.get("class", "")
            classes = f"{existing} {css}".strip()
            field.widget.attrs["class"] = classes

    def clean_botcheck(self):
        data = self.cleaned_data.get("botcheck", "")
        if data:
            raise ValidationError("Bot detected.")
        return data