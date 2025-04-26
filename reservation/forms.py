from django import forms
from django.core.exceptions import ValidationError

from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["table", "date", "start_time", "end_time", "total_persons"]
        labels = {
            "table": "Table",
            "date": "Date",
            "start_time": "Start Time",
            "end_time": "End Time",
            "total_persons": "Total Persons",
        }
        widgets = {
            "table": forms.Select(attrs={"placeholder": "Select table", "style": "background-color: #f8f9fa;"}),
            "customer": forms.TextInput(attrs={"placeholder": "Enter customer name", "style": "background-color: #f8f9fa;"}),
            "date": forms.DateInput(attrs={"placeholder": "Select date", "style": "background-color: #f8f9fa;", 'type': 'date'}),
            "start_time": forms.TimeInput(attrs={"placeholder": "Select start time", "style": "background-color: #f8f9fa;", 'type': 'time'}),
            "end_time": forms.TimeInput(attrs={"placeholder": "Select end time", "style": "background-color: #f8f9fa;", 'type': 'time'}),
            "total_persons": forms.NumberInput(attrs={"placeholder": "Enter total persons", "style": "background-color: #f8f9fa;"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get("table")
        total_persons = cleaned_data.get("total_persons")

        if table and total_persons and total_persons > table.capacity:
            raise ValidationError(
                f"Total persons ({total_persons}) cannot exceed the table's capacity ({table.capacity}).")

        return cleaned_data