from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg

from tripohoolic.trips.models import Trips

UserModel = get_user_model()


class TripComment(models.Model):
    MAX_TEXT_LENGTH = 333

    text = models.CharField(
        max_length=MAX_TEXT_LENGTH,
        null=False,
        blank=False,
    )

    publication_date_and_time = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=False,
    )

    trip = models.ForeignKey(
        Trips,
        on_delete=models.CASCADE,
        null=False,
        blank=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.DO_NOTHING,
    )


class TripRating(models.Model):
    RATES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    trip = models.ForeignKey(
        Trips,
        on_delete=models.CASCADE,
        null=False,
        blank=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.DO_NOTHING,
    )

    rate = models.PositiveIntegerField(
        choices=RATES,
    )

    #Create a new field in the model Trips 'average_rating' (here in model TripsRating)
    #Data for the calculation is here (TripRating) and the field is in Trips
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Calculate and update the average rating in the related Trips instance
        average_rating = TripRating.objects.filter(trip=self.trip).aggregate(Avg('rate'))['rate__avg']
        self.trip.average_rating = average_rating
        self.trip.save()

