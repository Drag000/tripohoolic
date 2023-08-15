from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_forms
from django import forms

from tripohoolic.accounts.models import UserProfile

UserModel = get_user_model()


class RegisterUserForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'password1', 'password2')


class RegisterProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 'age')