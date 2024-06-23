from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model

from tests.helpers import VALID_TRIP_MODEL_DATA_3, VALID_USER_MODEL_DATA_1, \
    VALID_TRIP_MODEL_DATA_1, VALID_USER_MODEL_DATA_2, _create_agency, _create_user, _create_trip
from tripohoolic.agencies.models import Agencies
from tripohoolic.common.models import TripRating
from tripohoolic.trips.models import Trips

UserModel = get_user_model()


class CommonTests(TestCase):

    def _create_triprating(self, rate, user, trip):
        # user = UserModel.objects.create(**self.VALID_USER_MODEL_DATA)
        # agency = Agencies.objects.create(agency_name='None', agency_website='www.ags.com')
        # trip = Trips.objects.create(**self.VALID_TRIP_MODEL_DATA, user_id=user.pk, used_agency_id=agency.pk)

        triprating_data = {
            'rate': rate,
            'user': user,
            'trip': trip,
        }

        return TripRating(**triprating_data)

    def test_create_triprating__when_valid__expects_to_be_created(self):
        user = _create_user(VALID_USER_MODEL_DATA_1)
        agency = _create_agency()
        trip = _create_trip(VALID_TRIP_MODEL_DATA_1, user, agency)

        triprating = self._create_triprating(TripRating.RATES[0][0], user, trip)
        triprating.full_clean()
        triprating.save()

        self.assertIsNotNone(triprating.pk)

    def test_update_rating__when_user_rerate_same_trip__expects_to_change_the_rating(self):
        user_1 = _create_user(VALID_USER_MODEL_DATA_1)
        agency = _create_agency()
        trip = _create_trip(VALID_TRIP_MODEL_DATA_3, user_1, agency)

        triprating = self._create_triprating(TripRating.RATES[0][0], user_1, trip)
        triprating.full_clean()
        triprating.save()

        user_2 = _create_user(VALID_USER_MODEL_DATA_2)
        triprating = self._create_triprating(TripRating.RATES[4][0], user_2, trip)
        triprating.full_clean()
        triprating.save()

        result = trip.average_rating
        expected_result = (TripRating.RATES[0][0] + TripRating.RATES[4][0]) / 2

        self.assertEqual(result, expected_result)
