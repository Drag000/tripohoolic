from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from tests.helpers import VALID_USER_MODEL_DATA_1, VALID_PROFILE_DATA, _create_user, _create_userprofile
from tripohoolic.accounts.models import UserProfile

UserModel = get_user_model()


class UserProfileTests(TestCase):

    def test_create_userprofile__when_valid__expects_to_be_created(self):
        user = _create_user(VALID_USER_MODEL_DATA_1)
        userprofile = _create_userprofile(user,VALID_PROFILE_DATA)
        userprofile.full_clean()
        userprofile.save()

        self.assertIsNotNone(userprofile.pk)

    def test_create__when_first_name_has_1_more_than_valid_characters__expect_validation_error(self):
        user = _create_user(VALID_USER_MODEL_DATA_1)
        userprofile = _create_userprofile(user,VALID_PROFILE_DATA,
                                          first_name='P' * UserProfile.FIRST_NAME_MAX_LENGTH + 'P')

        with self.assertRaises(ValidationError):
            userprofile.full_clean()

    def test_create__when_last_name_has_1_less_than_valid_characters__expect_validation_error(self):
        user = _create_user(VALID_USER_MODEL_DATA_1)
        userprofile = _create_userprofile(user,VALID_PROFILE_DATA, last_name='P')

        with self.assertRaises(ValidationError):
            userprofile.full_clean()

    def test_login_user(self):
        user = _create_user(VALID_USER_MODEL_DATA_1)

        response = self.client.post(reverse('login user'), {
            'username': VALID_USER_MODEL_DATA_1['username'],
            'password': VALID_USER_MODEL_DATA_1['password'],
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

        session = self.client.session
        self.assertEqual(int(session['_auth_user_id']), user.pk)
