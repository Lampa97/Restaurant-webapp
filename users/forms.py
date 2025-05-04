from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter your email"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter your password"})
    )


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "full_name", "phone_number", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Enter your email", "style": "background-color: #f5deb3;"})
        self.fields["full_name"].widget.attrs.update({"class": "form-control", "placeholder": "Enter your full name", "style": "background-color: #f5deb3;"})
        self.fields["phone_number"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter your phone number", "style": "background-color: #f5deb3;"}
        )
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Enter your password", "style": "background-color: #f5deb3;"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Confirm your password", "style": "background-color: #f5deb3;"})


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-control", "style": "background-color: #f5deb3;"})


class PasswordResetConfirmForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, label="New Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "form-control", "style": "background-color: #f5deb3;"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "style": "background-color: #f5deb3;"})

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["full_name", "phone_number",]
        labels = {
            "full_name": "Full Name",
            "phone_number": "Phone number",
        }
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your full name",
                    "style": "background-color: #f5deb3;",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your phone_number", "style": "background-color: #f5deb3;"}
            )}