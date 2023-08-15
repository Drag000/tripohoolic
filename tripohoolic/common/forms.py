from django import forms

from tripohoolic.common.models import TripComment, TripRating


class TripCommentForm(forms.ModelForm):
    class Meta:
        model = TripComment
        fields = ('text',)
        widget = {
            'text': forms.Textarea(
                attrs={
                    'cols': 40,
                    'rows': 10,
                    'placeholder': 'Please add your comment',
                },
            ),
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
