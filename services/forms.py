from django import forms

from .models import Meal, MealCategory


class MealCategoryForm(forms.ModelForm):

    class Meta:
        model = MealCategory
        fields = ["name", "description", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
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
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
        labels = {
            "name": "Name",
            "description": "Description",
            "price": "Price",
            "category": "Category",
            "image": "Image",
        }
