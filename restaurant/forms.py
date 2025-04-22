from django import forms

from .models import Review


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
            "name": forms.TextInput(attrs={"placeholder": "Enter your name", "style": "background-color: #f8f9fa;"}),
            "review_text": forms.Textarea(attrs={"placeholder": "Write your review here", "style": "background-color: #f8f9fa;"}),
            "rating": forms.Select(attrs={"placeholder": "Select rating", "style": "background-color: #f8f9fa;"}),
        }


    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "form-control"})
        self.fields["review_text"].widget.attrs.update({"class": "form-control"})
        self.fields["rating"].widget.attrs.update({"class": "form-control"})
