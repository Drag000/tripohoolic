from django import forms

from tripohoolic.core.forms_mixin import DisabledFormMixin
from tripohoolic.trips.models import Trips


class TripBaseForm(forms.ModelForm):
    class Meta:
        model = Trips
        # fields = '__all__'
        # fields = ('trip_name', 'type', 'used_agency', 'country', 'cities')
        exclude = ('average_rating', 'user')


class TripCreateForm(TripBaseForm):

    labels = {
        'type': "Type of trip",
        'country': 'Country',
        'cities': 'Visited cities (places)',
        'sightseeing': 'Sightseeing',
        'activities': 'Activities',
        'food_and_drinks': 'Food and drinks',
        'notes': 'Notes',
    }

    widgets = {
        'cities': forms.TextInput(
            attrs={
                'placeholder': 'Please describe which cities / places did you visit', }
        ),

        'sightseeing': forms.TextInput(
            attrs={
                'placeholder': 'Please tell us which attractions did you see', }
        ),

        'activities': forms.TextInput(
            attrs={
                'placeholder': 'Please share with us what did you do', }
        ),

        'food_and_drinks': forms.TextInput(
            attrs={
                'placeholder': 'Please tell us what did you eat and drink', }
        ),

        'transport': forms.TextInput(
            attrs={
                'placeholder': 'Please share any interesting or useful information', }
        ),
    }


class TripEditForm(TripBaseForm):
    pass


class TripDeleteForm(DisabledFormMixin, TripBaseForm):
    disabled_fields = ['trip_name', 'type', 'used_agency', 'country', 'cities', 'sightseeing', 'activities', 'food_and_drinks', 'transport', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._disable_fields()

    def save(self, commit=True):
        if commit:
            super().save()
            self.instance.delete()

        return self.instance


