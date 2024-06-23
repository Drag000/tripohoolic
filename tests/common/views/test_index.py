from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from tests.helpers import _create_user, _create_agency, VALID_USER_MODEL_DATA_1, VALID_TRIP_MODEL_DATA_1, _create_trip, \
    VALID_TRIP_MODEL_DATA_3

UserModel = get_user_model()


class IndexViewTests(TestCase):

    def test_index__when_get_method__expects_posts(self):
        response = self.client.get(
            reverse('index'),
        )

        context = response.context

        self.assertEqual(200, response.status_code)
        self.assertEquals(0, len(context['trips']))
        self.assertTemplateUsed(response, 'common/index.html')

    def test_index__when_single_trip__expects_single_trip(self):
        user = _create_user(VALID_USER_MODEL_DATA_1)
        agency = _create_agency()

        trip = _create_trip(VALID_TRIP_MODEL_DATA_1, user, agency)
        trip.save()

        response = self.client.get(
            reverse('index'),
        )

        context = response.context

        self.assertEquals(1, len(context['trips']))

    def test_index_search__when_search_by_existing_country__expects_match(self):
        user = _create_user(VALID_USER_MODEL_DATA_1)
        self.client.login(**VALID_USER_MODEL_DATA_1)
        agency = _create_agency()

        trip = _create_trip(VALID_TRIP_MODEL_DATA_1, user, agency)
        trip2 = _create_trip(VALID_TRIP_MODEL_DATA_3, user, agency)
        trip.save()
        trip2.save()


        response = self.client.get(
            reverse('index'),
            data={
                'country_name': 'italy',
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, trip.trip_name)
        self.assertNotContains(response, trip2.trip_name)
        self.assertEqual(len(response.context['trips']), 1)
        self.assertEqual(response.context['trips'][0].trip_name, trip.trip_name)

