from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_forms
from django import forms
from django.forms import modelformset_factory

from tripohoolic.accounts.models import UserProfile
from tripohoolic.trips.models import Photos

UserModel = get_user_model()


class RegisterUserForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'password1', 'password2')


class RegisterProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 'age')


class PhotosForm(forms.ModelForm):
    class Meta:
        model = Photos
        fields = ('image',)


PhotoFormSet = modelformset_factory(Photos, form=PhotosForm, extra=3)
