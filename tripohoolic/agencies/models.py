from django.core import validators
from django.db import models


class Agencies(models.Model):
    AGENCY_NAME_MIN_LENGTH = 3
    AGENCY_NAME_MAX_LENGTH = 50

    agency_name = models.CharField(
        max_length=AGENCY_NAME_MAX_LENGTH,
        validators=(
            validators.MinLengthValidator(AGENCY_NAME_MIN_LENGTH),
        ),
        blank=False,
        null=False,
    )

    agency_website = models.URLField(
        blank=False,
        null=False,
    )

