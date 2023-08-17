from django import forms

from tripohoolic.common.models import TripComment, TripRating


class TripCommentForm(forms.ModelForm):
    class Meta:
        model = TripComment
        fields = ('text',)
        widgets = {
            'text': forms.TextInput(
                attrs={
                    'placeholder': 'Please enter your comment',
                },
            ),
        }

        labels = {
            'text': "Comment",
        }


class TripRatingForm(forms.ModelForm):
    class Meta:
        model = TripRating
        fields = ('rate',)


class SearchCountryForm(forms.Form):
    country_name = forms.CharField(
        max_length=20,
        required=False,
    )


class SearchCityForm(forms.Form):
    city_name = forms.CharField(
        max_length=20,
        required=False,
    )
