from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from tripohoolic.trips.models import Trips
from tests.helpers import _create_user, _create_agency, formset_data, VALID_USER_MODEL_DATA_1, VALID_TRIP_MODEL_DATA_1

UserModel = get_user_model()


class TripsCreateViewTests(TestCase):

    def test_create_trip__when_valid__expects_to_be_created(self):
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

        # print(f"User logged in: {logged_in}")
        print(f"Response status code: {response.status_code}")
        # print(f"Response content: {response.content.decode()}")
        # print(f"Trips count: {Trips.objects.count()}")
        # print(
        #     f"Form errors: {response.context.get('form').errors if 'form' in response.context else 'No form in context'}")
        # print(
        #     f"Formset errors: {response.context.get('formset').errors if 'formset' in response.context else 'No formset in context'}")

        print(response.context)
        print(response.status_code)
        print(Trips.objects.all())
        trip = Trips.objects.get()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
        self.assertEqual(Trips.objects.count(), 1)
        self.assertEqual(trip.user, user)
        self.assertEqual(trip.trip_name, 'Road trip in Italy')

    def test_create__when_anonymous_user__expect_302_with_redirect_to_login(self):
        response = self.client.get(
            reverse('create trip'),
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('login user')}?next={reverse('create trip')}"
        )
