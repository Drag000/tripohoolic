from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from tests.helpers import _create_user, _create_agency, formset_data, VALID_USER_MODEL_DATA_1, VALID_TRIP_MODEL_DATA_1
from tripohoolic.agencies.models import Agencies
from tripohoolic.trips.models import Trips

UserModel = get_user_model()


class TripsDeleteViewTests(TestCase):

    def test_delete_trip__when_valid__expects_to_be_deleted(self):
        user = _create_user(VALID_USER_MODEL_DATA_1)
        self.client.login(**VALID_USER_MODEL_DATA_1)

        agency = _create_agency()

        response = self.client.post(
            reverse('create trip'),
            data={
                **VALID_TRIP_MODEL_DATA_1,
                'used_agency': agency.pk,
                'user_id': user.pk,
                **formset_data,
            }
        )
        trip = Trips.objects.get()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
        self.assertEqual(Trips.objects.count(), 1)
        self.assertEqual(trip.user, user)
        self.assertEqual(trip.trip_name, 'Road trip in Italy')

        response2 = self.client.post(
            reverse('delete trip',
                    kwargs={
                        'pk': trip.pk,
                    }),
        )

        self.assertEqual(Trips.objects.count(), 0)
