from django import forms

class FlightSearchForm(forms.Form):
    origin = forms.CharField(label="مبدا", max_length=3)
    destination = forms.CharField(label="مقصد", max_length=3)
    departing = forms.CharField(label="تاریخ رفت (YYYY-MM-DD)")
    returning = forms.CharField(label="تاریخ برگشت (اختیاری)", required=False)
    adults = forms.IntegerField(label="تعداد بزرگسال", min_value=1, initial=1)
