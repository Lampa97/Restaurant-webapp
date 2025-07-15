from django import forms

from .models import Meal, MealCategory


class MealCategoryForm(forms.ModelForm):

    class Meta:
        model = MealCategory
        fields = ["name", "description", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "style": "background-color: #f5deb3;"}),
            "description": forms.Textarea(attrs={"class": "form-control", "style": "background-color: #f5deb3;"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control", "style": "background-color: #f5deb3;"}),
        }
        labels = {
            "name": "Name",
            "description": "Description",
            "image": "Image",
        }


class MealForm(forms.ModelForm):

    class Meta:
        model = Meal
        fields = ["name", "description", "price", "category", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "style": "background-color: #f5deb3;"}),
            "description": forms.Textarea(attrs={"class": "form-control", "style": "background-color: #f5deb3;"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "style": "background-color: #f5deb3;"}),
            "category": forms.Select(attrs={"class": "form-control", "style": "background-color: #f5deb3;"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control", "style": "background-color: #f5deb3;"}),
        }
        labels = {
            "name": "Name",
            "description": "Description",
            "price": "Price",
            "category": "Category",
            "image": "Image",
        }
