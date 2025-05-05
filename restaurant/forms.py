from django import forms

from .models import Personnel, Review, Service


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
                    "style": "background-color: #f5deb3;",
                }
            ),
            "position": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Enter position", "style": "background-color: #f5deb3;"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter description",
                    "style": "background-color: #f5deb3;",
                }
            ),
            "quote": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Enter quote", "style": "background-color: #f5deb3;"}
            ),
            "photo": forms.ClearableFileInput(
                attrs={"class": "form-control", "placeholder": "Choose photo", "style": "background-color: #f5deb3;"}
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
                    "style": "background-color: #f5deb3;",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter description",
                    "style": "background-color: #f5deb3;",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={"class": "form-control", "placeholder": "Choose image", "style": "background-color: #f5deb3;"}
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
                    "style": "background-color: #f5deb3; ",
                }
            ),
            "review_text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write your review here",
                    "style": "background-color: #f5deb3;",
                }
            ),
            "rating": forms.RadioSelect(
                choices=[(i, str(i)) for i in range(1, 6)],
                attrs={
                    "class": "form-check-input d-inline-block me-2",
                },
            ),
        }
