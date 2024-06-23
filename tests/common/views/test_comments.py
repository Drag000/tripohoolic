from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from tripohoolic.common.models import TripComment
from tests.helpers import _create_user, _create_agency, formset_data, VALID_USER_MODEL_DATA_1, VALID_TRIP_MODEL_DATA_1, \
    _create_trip

UserModel = get_user_model()


class CommentsViewTests(TestCase):
    def test_create_comment__when_valid__expects_comment(self):
        user = _create_user(VALID_USER_MODEL_DATA_1)
        self.client.login(**VALID_USER_MODEL_DATA_1)

        agency = _create_agency()

        trip = _create_trip(VALID_TRIP_MODEL_DATA_1, user, agency)

        response = self.client.post(
            reverse('comment trip', kwargs={'trip_id': trip.pk}),
            data={
                'text': 'My cow is blue',
            }
        )

        comment = TripComment.objects.get(trip=trip)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(TripComment.objects.count(),1)
        self.assertEqual(comment.text,'My cow is blue')
        self.assertEqual(comment.user, user)

        index_response = self.client.get(
            reverse('index')
        )
        self.assertEqual(index_response.status_code, 200)

    def test_delete_comment__when_valid__expects_no_comment(self):
        user = _create_user(VALID_USER_MODEL_DATA_1)
        self.client.login(**VALID_USER_MODEL_DATA_1)

        agency = _create_agency()

        trip = _create_trip(VALID_TRIP_MODEL_DATA_1, user, agency)

        response = self.client.post(
            reverse('comment trip', kwargs={'trip_id': trip.pk}),
            data={
                'text': 'My dog is happy',
            }
        )

        comment = TripComment.objects.get(trip=trip)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(TripComment.objects.count(),1)
        self.assertEqual(comment.text,'My dog is happy')
        self.assertEqual(comment.user, user)

        response = self.client.post(
            reverse('delete comment', kwargs={'comment_id': comment.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(TripComment.objects.count(),0)