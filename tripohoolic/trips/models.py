from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django_countries.fields import CountryField

from tripohoolic.agencies.models import Agencies

UserModel = get_user_model()


class Trips(models.Model):
    TRIP_NAME_MIN_LENGTH = 5
    TRIP_NAME_MAX_LENGTH = 50
    TYPE_SOLO = 'Solo'
    TYPE_GROUP = 'Group'
    TYPE_AGENCY = 'Agency'

    TRIP_TYPES = (
        (TYPE_SOLO, TYPE_SOLO),
        (TYPE_GROUP, TYPE_GROUP),
        (TYPE_AGENCY, TYPE_AGENCY),
    )
    # AGENCY_CHOICES = Agencies.objects.all()
    # AGENCY_CHOICES = Agencies.objects.values_list('pk', 'agency_name')


    user = models.ForeignKey(
        UserModel,
        on_delete=models.DO_NOTHING,
    )

    trip_name = models.CharField(
        max_length=TRIP_NAME_MAX_LENGTH,
        validators=(
            validators.MinLengthValidator(TRIP_NAME_MIN_LENGTH),
        ),
    )

    type = models.CharField(
        max_length=len(TYPE_AGENCY),
        choices=TRIP_TYPES,
        verbose_name='Trip type',
        blank=False,
        null=False,
    )

    used_agency = models.ForeignKey(
        Agencies,
        on_delete=models.DO_NOTHING,
        max_length=30,
        # choices=AGENCY_CHOICES,
        blank=False,
        null=False,
    )

    country = CountryField(
        multiple=True,
        blank=False,
        null=False,
    )

    #There is a similar package as for country, called django-cities, but it works a bit differently, it has table with cities
    cities = models.CharField(
        blank=False,
        null=False,
    )

    sightseeing = models.TextField(
        blank=True,
        null=True,
    )

    activities = models.TextField(
        blank=True,
        null=True,
    )

    food_and_drinks = models.TextField(
        blank=True,
        null=True,
    )

    transport = models.TextField(
        blank=True,
        null=True,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    publication_date = models.DateField(
        # Autonow autoatically sets current date on 'save'
        auto_now=True,
        null=False,
        blank=True,
    )

    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0,
        blank=True,
    )

    photos = models.ManyToManyField(
        'Photos',
        blank=True,
    )


class Photos(models.Model):
    image = models.FileField(
        upload_to='trips_photos',
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False,
    )
