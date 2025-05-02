from django import forms
from django.core.exceptions import ValidationError
from datetime import date, timedelta, time
from .models import Reservation, Table


class TableForm(forms.ModelForm):
    number = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-control",
                            "placeholder": "Select available Table number"}),
        label="Table",
    )
    class Meta:
        model = Table
        fields = ['number', 'capacity']
        widgets = {
            'capacity': forms.Select(
                attrs={"class": "form-control",
                       "placeholder": "Select Table capacity",}
            ),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get all possible table numbers (1 to 20) and exclude those already in the database
        existing_numbers = Table.objects.values_list('number', flat=True)
        available_numbers = [(i, i) for i in range(1, 21) if i not in existing_numbers]
        self.fields['number'].choices = available_numbers

class ReservationStep1Form(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'start_time', 'end_time', 'total_persons', 'user_name', 'user_phone']
        widgets = {
            'date': forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "min": date.today().isoformat(),
                    "max": (date.today() + timedelta(days=6 * 30)).isoformat(),
                }
            ),
            'start_time': forms.TimeInput(attrs={"class": "form-control", "type": "time", "placeholder": "Select start time"}),
            'end_time': forms.TimeInput(attrs={"class": "form-control", "type": "time", "placeholder": "Select end time"}),
            'total_persons': forms.Select(attrs={"class": "form-control", "placeholder": "Select total persons"}),
            'user_name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your name"}),
            'user_phone': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your phone number"}),
        }
        labels = {
            'date': "Date",
            'start_time': "Start Time",
            'end_time': "End Time",
            'total_persons': "Total Persons",
            'user_name': "User Name",
            'user_phone': "User Phone",
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        # Define allowed time ranges
        min_start_time = time(9, 0)  # 09:00 AM
        max_start_time = time(20, 0)  # 08:00 PM
        min_end_time = time(10, 0)  # 10:00 AM
        max_end_time = time(22, 0)  # 10:00 PM

        # Validate start_time
        if start_time and (start_time < min_start_time or start_time > max_start_time):
            raise ValidationError(f"Start time must be between {min_start_time.strftime('%I:%M %p')} and {max_start_time.strftime('%I:%M %p')}.")

        # Validate end_time
        if end_time and (end_time < min_end_time or end_time > max_end_time):
            raise ValidationError(f"End time must be between {min_end_time.strftime('%I:%M %p')} and {max_end_time.strftime('%I:%M %p')}.")

        # Ensure start_time is at least 1 hour before end_time
        if start_time and end_time and (end_time <= (time(start_time.hour + 1, start_time.minute) if start_time.hour < 23 else time(0, 0))):
            raise ValidationError("End time must be at least 1 hour after start time.")

        return cleaned_data


class ReservationStep2Form(forms.ModelForm):
    table = forms.ModelChoiceField(
        queryset=Table.objects.none(),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Table",
    )

    class Meta:
        model = Reservation
        fields = ['table']
        labels = {
            'table': "Table",
        }

    def __init__(self, *args, **kwargs):
        available_tables = kwargs.pop("available_tables", Table.objects.none())
        super().__init__(*args, **kwargs)
        self.fields["table"].queryset = available_tables

    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get("table")
        date = self.initial.get("date")
        start_time = self.initial.get("start_time")
        end_time = self.initial.get("end_time")

        if table and date and start_time and end_time:
            # Check for overlapping reservations
            overlapping_reservations = Reservation.objects.filter(
                table=table,
                date=date,
                start_time__lt=end_time,
                end_time__gt=start_time,
            )

            if overlapping_reservations.exists():
                overlapping_reservation = overlapping_reservations.first()
                raise ValidationError(
                    f"The selected table is already booked from {overlapping_reservation.start_time.strftime('%I:%M %p')} "
                    f"to {overlapping_reservation.end_time.strftime('%I:%M %p')} on {date}."
                )

        return cleaned_data