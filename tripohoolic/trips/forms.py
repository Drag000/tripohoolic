from django import forms

from tripohoolic.core.forms_mixin import DisabledFormMixin
from tripohoolic.trips.models import Trips


class TripBaseForm(forms.ModelForm):
    class Meta:
        model = Trips
        fields = ('trip_name', 'type', 'used_agency', 'country', 'cities')
        # exclude = ('user',)

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
            # placeholder.. сивият текст в полето
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


class TripCreateForm(TripBaseForm):
    pass


class TripEditForm(TripBaseForm):
    pass


class TripDeleteForm(TripBaseForm):
    # disabled_fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__set_disabled_fields()

    def save(self,
             commit=True):  # казваме какво да стане при save() за да не променяме логиката и да е еднаква във всики форми.. ( ако не pet  .delete()_
        if commit:  # commit дали искаме да се прати към ДБ
            self.instance.delete()

        return self.instance

    def __set_disabled_fields(self):
        for _, field in self.fields.items():
            field.widget.attrs['readonly'] = 'readonly'
