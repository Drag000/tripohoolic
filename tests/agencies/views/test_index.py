from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tripohoolic.agencies.models import Agencies
from tripohoolic.trips.models import Trips
from tests.helpers import _create_user, _create_agency, formset_data, VALID_USER_MODEL_DATA_1, VALID_TRIP_MODEL_DATA_1

UserModel = get_user_model()


class AgenciesIndexViewTests(TestCase):

    def test_index__when_get_method__expects_posts(self):
        user = _create_user(VALID_USER_MODEL_DATA_1)
        self.client.login(**VALID_USER_MODEL_DATA_1)

        Agencies.objects.create(agency_name='Denita', agency_website='www.denita.bg')
        Agencies.objects.create(agency_name='Chaika', agency_website='www.chaika.bg')
        Agencies.objects.create(agency_name='TravelFree', agency_website='www.travelfree.bg')

        print(Agencies.objects.all())

        response = self.client.get(
            reverse('agencies'),
        )

        context = response.context

        self.assertEqual(200, response.status_code)
        self.assertEquals(3, len(context['agencies']))
        self.assertTemplateUsed(response, 'agencies/agencies.html',)