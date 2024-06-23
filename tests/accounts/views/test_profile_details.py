from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tests.helpers import _create_userprofile, VALID_PROFILE_DATA, _create_user, VALID_USER_MODEL_DATA_1, \
    VALID_USER_MODEL_DATA_2, VALID_PROFILE_DATA_2
from tripohoolic.accounts.models import UserProfile

UserModel = get_user_model()


class ProfileDetailsTests(TestCase):
    def test_profile_details__when_get_method__expects_post(self):
        user = _create_user(VALID_USER_MODEL_DATA_1)
        userprofile = _create_userprofile(user, VALID_PROFILE_DATA)
        userprofile.full_clean()
        userprofile.save()

        response = self.client.get(
            reverse('details user', kwargs={'pk': userprofile.pk}),
        )

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'profile/details-profile.html')
        self.assertContains(response, userprofile.last_name)

