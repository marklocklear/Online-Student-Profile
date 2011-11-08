from django import forms

input_format = ["%m/%d/%Y"]
class DateRangeForm(forms.Form):
    from_date = forms.DateTimeField(input_formats=input_format, required=True)
    to_date = forms.DateTimeField(input_formats=input_format, required=True)
