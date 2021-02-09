from django import forms

from .models import Shift

# classes needed for the widget to get the right format of thw input_type
class DateInput(forms.DateInput):
    input_type = 'date'

# classes needed for the widget to get the right format of thw input_type
class DateTimeInput(forms.DateTimeInput):
    input_type = 'time'

class ShiftForm(forms.ModelForm):
    # simple classed based form with widgets i.e date calendat, time picker
    class Meta:
        model = Shift
        fields = [
            'date',
            "start_time",
            'end_time',
            'tip',
        ]
        widgets = {'date': DateInput(),'start_time':DateTimeInput(),'end_time':DateTimeInput()}
