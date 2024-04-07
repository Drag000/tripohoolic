from django.core import validators
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    FIRST_NAME_MIN_LENGTH = 2
    FIRST_NAME_MAX_LENGTH = 20
    LAST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 20
    # AGE_MIN = 16

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )

    first_name = models.CharField(
        null=False,
        blank=False,
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            validators.MinLengthValidator(FIRST_NAME_MIN_LENGTH),
        ),
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            validators.MinLengthValidator(LAST_NAME_MIN_LENGTH),
        )
    )

    age = models.PositiveIntegerField(
        null=True,
        blank=True,
        # validators=(
        #     validators.MinLengthValidator(AGE_MIN),
        # ),

    )

    # gender = models.CharField(
    #     choices=Gender.choices(),
    # )

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    profile_picture = models.ImageField(
        upload_to='profile_picture',
        null=True,
        blank=True,
    )