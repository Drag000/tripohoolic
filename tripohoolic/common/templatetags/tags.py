from django import template

from tripohoolic.common.models import TripRating

register = template.Library()


@register.simple_tag(name="my_rating")
def my_rating(trip_id, user_id):
    rating = TripRating.objects.filter(trip_id=trip_id, user_id=user_id)

    return rating
