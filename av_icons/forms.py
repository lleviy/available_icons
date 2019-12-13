import datetime

from django import forms

from av_icons.models import License


def get_first_date():
    return datetime.datetime.now().date() + datetime.timedelta(weeks=4)


def get_second_date():
    return datetime.datetime.now().date() + datetime.timedelta(weeks=12)


first_date = get_first_date()
second_date = get_second_date()
DATE_SELECTION = (
        (first_date, "4 weeks"),
        (second_date, "12 weeks"),
    )


class LicenseForm(forms.ModelForm):
    date_ended = forms.DateField(input_formats=["%Y-%m-%d"], widget=forms.Select(choices=DATE_SELECTION))

    class Meta:
        model = License
        fields = ['date_ended']