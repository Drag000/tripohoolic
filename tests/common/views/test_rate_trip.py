from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from tripohoolic.common.models import TripRating, Trips
from tests.helpers import _create_user, _create_agency, formset_data, VALID_USER_MODEL_DATA_1, VALID_TRIP_MODEL_DATA_1, \
    _create_trip, VALID_USER_MODEL_DATA_2

UserModel = get_user_model()


class RateTripViewTests(TestCase):
    def test_rate_trip__when_valid__expects_rate(self):
        user = _create_user(VALID_USER_MODEL_DATA_1)
        self.client.login(**VALID_USER_MODEL_DATA_1)

        agency = _create_agency()

        trip = _create_trip(VALID_TRIP_MODEL_DATA_1, user, agency)

        response = self.client.post(
            reverse('rate trip', kwargs={'trip_id': trip.pk}),
            data={
                'rate': 3,
            }
        )

        rate = TripRating.objects.get(trip=trip)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(TripRating.objects.count(), 1)
        self.assertEqual(rate.rate, 3)
        self.assertEqual(rate.user, user)

    def test_change_rate_trip__when_valid__expects_new_rate_not_average(self):
        user = _create_user(VALID_USER_MODEL_DATA_1)
        self.client.login(**VALID_USER_MODEL_DATA_1)

        agency = _create_agency()

        trip = _create_trip(VALID_TRIP_MODEL_DATA_1, user, agency)

        response1 = self.client.post(
            reverse('rate trip', kwargs={'trip_id': trip.pk}),
            data={
                'rate': 1,
            }
        )

        rate1 = TripRating.objects.get(trip=trip, user=user)

        self.assertEqual(response1.status_code, 302)
        self.assertRedirects(response1, reverse('index'))
        self.assertEqual(TripRating.objects.count(), 1)
        self.assertEqual(rate1.rate, 1)
        self.assertEqual(rate1.user, user)

        response2 = self.client.post(
            reverse('rate trip', kwargs={'trip_id': trip.pk}),
            data={
                'rate': 2,
            }
        )

        rate2 = TripRating.objects.get(trip=trip, user=user)

        self.assertEqual(response2.status_code, 302)
        self.assertRedirects(response2, reverse('index'))
        self.assertEqual(TripRating.objects.count(), 1)
        self.assertEqual(rate2.rate, 2)
        self.assertEqual(rate2.user, user)

    def test_2_users_rate_one_trip__when_valid__expects_average_rate(self):
        user1 = _create_user(VALID_USER_MODEL_DATA_1)
        self.client.login(**VALID_USER_MODEL_DATA_1)

        agency = _create_agency()

        trip = _create_trip(VALID_TRIP_MODEL_DATA_1, user1, agency)

        response_user1 = self.client.post(
            reverse('rate trip', kwargs={'trip_id': trip.pk}),
            data={
                'rate': 5,
            }
        )

        rate_user1 = TripRating.objects.get(trip=trip, user=user1)

        self.assertEqual(response_user1.status_code, 302)
        self.assertRedirects(response_user1, reverse('index'))
        self.assertEqual(TripRating.objects.count(), 1)
        self.assertEqual(rate_user1.rate, 5)
        self.assertEqual(rate_user1.user, user1)

        self.client.logout()

        session = self.client.session
        self.assertNotIn('_auth_user_id', session)

        user2 = _create_user(VALID_USER_MODEL_DATA_2)
        self.client.login(**VALID_USER_MODEL_DATA_2)

        session = self.client.session
        self.assertEqual(session['_auth_user_id'], str(user2.pk))

        response_user2 = self.client.post(
            reverse('rate trip', kwargs={'trip_id': trip.pk}),
            data={
                'rate': 4,
            }
        )

        rate_user2 = TripRating.objects.get(trip=trip, user=user2)

        self.assertEqual(response_user2.status_code, 302)
        self.assertRedirects(response_user1, reverse('index'))
        self.assertEqual(TripRating.objects.count(), 2)
        self.assertEqual(rate_user2.rate, 4)
        self.assertEqual(rate_user2.user, user2)

        trip.refresh_from_db()
        expected_average = (rate_user1.rate + rate_user2.rate) / 2
        self.assertEqual(float(trip.average_rating), expected_average)
