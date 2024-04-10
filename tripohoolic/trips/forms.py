from django import forms
from tripohoolic.agencies.models import Agencies
from tripohoolic.core.forms_mixin import DisabledFormMixin
from tripohoolic.trips.models import Trips, Photos


class TripBaseForm(forms.ModelForm):
    class Meta:
        model = Trips
        exclude = ('average_rating', 'user', 'photos')

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

        labels = {
            'type': "Type of trip",
            'country': 'Country',
            'cities': 'Visited cities (places)',
            'sightseeing': 'Sightseeing',
            'activities': 'Activities',
            'food_and_drinks': 'Food and drinks',
            'notes': 'Notes',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #<Make used_agency dynamic drop down list from the existing objects in Agencies model
        self.fields['used_agency'].queryset = Agencies.objects.all()

        # TODO if Solo and add Agencgy to hide/show field in the browsed (to be done dynamically) I need JavaScript because the template is executed on the server side, but the user interaction occurs on the client side.. in the browser.
        # TODO .. alternatively add None in Agencgy table and make 'used_agency' required


class TripCreateForm(TripBaseForm):
    pass


class TripEditForm(TripBaseForm):
    pass


class TripDeleteForm(DisabledFormMixin, TripBaseForm):
    disabled_fields = ['trip_name', 'type', 'used_agency', 'country', 'cities', 'sightseeing', 'activities',
                       'food_and_drinks', 'transport', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._disable_fields()

    def save(self, commit=True):
        if commit:
            super().save()
            self.instance.delete()

        return self.instance


class MultiplePhotosForm(forms.ModelForm):
    class Meta:
        model = Photos
        fields = ('image',)

    # TODO I tired to upload multiple photos with 1 form but id didn't worked.. it needs JavaSript
    image = forms.FileField(
        widget=forms.TextInput(
            attrs={
                # "name": "images",
                "type": "File",
                "class": "form-control",
                "multiple": "True",
            }
        ),
        required=False,
    ),

    delete_photos = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.trip = kwargs.pop('trip')
        super().__init__(*args, **kwargs)
        self.fields['delete_photos'].choices = [(photo.id, photo.image.url) for photo in self.trip.photos.all()]

    def clean_delete_photos(self):
        deleted_photo_ids = self.cleaned_data.get('delete_photos')
        if deleted_photo_ids:
            return [int(photo_id) for photo_id in deleted_photo_ids]
        return []
