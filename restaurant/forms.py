from django import forms

from .models import Review, Service, Personnel


class PersonnelForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = ["name", "position", "description", "quote", "photo"]
        labels = {
            "name": "Name",
            "position": "Position",
            "description": "Description",
            "quote": "Quote",
            "photo": "Photo",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter person's full name",
                    "style": "background-color: #f8f9fa;",
                }
            ),
            "position": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Enter position", "style": "background-color: #f8f9fa;"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter description",
                    "style": "background-color: #f8f9fa;",
                }
            ),
            "quote": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Enter quote", "style": "background-color: #f8f9fa;"}
            ),
            "photo": forms.ClearableFileInput(
                attrs={"class": "form-control", "placeholder": "Choose photo", "style": "background-color: #f8f9fa;"}
            ),
        }


class ServiceForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = ["name", "description", "image"]
        labels = {"name": "Name", "description": "Description", "image": "Image"}
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter service name",
                    "style": "background-color: #f8f9fa;",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter description",
                    "style": "background-color: #f8f9fa;",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={"class": "form-control", "placeholder": "Choose image", "style": "background-color: #f8f9fa;"}
            ),
        }


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["name", "review_text", "rating"]
        labels = {
            "name": "Name",
            "review_text": "Review",
            "rating": "Rating",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your name",
                    "style": "background-color: #f8f9fa;",
                }
            ),
            "review_text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write your review here",
                    "style": "background-color: #f8f9fa;",
                }
            ),
            "rating": forms.RadioSelect(
                choices=[(i, str(i)) for i in range(1, 6)],
                attrs={"class": "form-check-input d-inline-block me-2"},
            ),
        }
