from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from tripohoolic.trips.models import Trips
from tests.helpers import _create_user, _create_agency, formset_data, VALID_USER_MODEL_DATA_1, VALID_TRIP_MODEL_DATA_1, \
    _create_trip, VALID_USER_MODEL_DATA_2

UserModel = get_user_model()


class TripsDetailsViewTests(TestCase):

    def test_trip_details__when_has_rights_to_edit__expects_to_be_edited(self):
        user = _create_user(VALID_USER_MODEL_DATA_1)
        self.client.login(**VALID_USER_MODEL_DATA_1)
        agency = _create_agency()

        trip = _create_trip(VALID_TRIP_MODEL_DATA_1, user, agency)
        trip.save()

        response = self.client.post(
            reverse('details trip', kwargs={
                'pk': trip.pk,
            }),
        )

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'trips/details-trip.html')
        self.assertEqual(Trips.objects.count(), 1)
        self.assertContains(response, trip.trip_name)

    def test_trip_details__when_has_not_rights_to_edit__expects_not_to_be_edited(self):
        user = _create_user(VALID_USER_MODEL_DATA_1)
        self.client.login(**VALID_USER_MODEL_DATA_1)
        agency = _create_agency()

        trip = _create_trip(VALID_TRIP_MODEL_DATA_1, user, agency)
        trip.save()

        self.client.logout()

        session = self.client.session
        self.assertNotIn('_auth_user_id', session)

        user2 = _create_user(VALID_USER_MODEL_DATA_2)
        self.client.login(**VALID_USER_MODEL_DATA_2)

        session = self.client.session
        self.assertEqual(session['_auth_user_id'], str(user2.pk))

        response = self.client.post(
            reverse('details trip', kwargs={
                'pk': trip.pk,
            }),
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(response.context['rights_to_edit'], False)
