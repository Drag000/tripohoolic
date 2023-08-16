

def trip_rating(trip_id, user_id):
    rating = TripRating.objects.filter(trip_id=trip_id, user_id=user_id)
