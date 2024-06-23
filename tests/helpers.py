from tripohoolic.accounts.models import UserProfile
from tripohoolic.agencies.models import Agencies
from tripohoolic.trips.models import Trips
from django.contrib.auth import get_user_model

UserModel = get_user_model()

VALID_TRIP_MODEL_DATA_1 = {
    'trip_name': 'Road trip in Italy',
    'type': Trips.TYPE_SOLO,
    'country': ['IT'],
    'cities': 'Rome',
    # 'used_agency': 'None'
}

VALID_TRIP_MODEL_DATA_2 = {
    'trip_name': 'Road trip in Italy 2',
    'type': Trips.TYPE_SOLO,
    'country': ['IT'],
    'cities': 'Rome',
    'used_agency': 'None'
}

VALID_TRIP_MODEL_DATA_3 = {
    'trip_name': 'Trip to Spain',
    'type': Trips.TYPE_GROUP,
    'country': ['ES'],
    'cities': 'Barcelona',
}

VALID_USER_MODEL_DATA_1 = {
    'username': 'Pesho',
    'password': 'wqeQWe123@',
}

VALID_USER_MODEL_DATA_2 = {
    'username': 'Georgi',
    'password': 'FXCDe12dsds3@',
}

VALID_PROFILE_DATA = {
    'first_name': 'Pesho',
    'last_name': 'Dachev',
    'age': 20,
    'email': 'peshov@abv.bg',
}

VALID_PROFILE_DATA_2 = {
    'first_name': 'Simeon',
    'last_name': 'Stoykov',
    'age': 30,
    'email': 's.stoykov@abv.bg',
}

VALID_AGENCY_MODEL_DATA_1 = {
    'agency_name': 'None',
    'agency_website': 'None',
}

formset_data = {
    'form-TOTAL_FORMS': '1',
    'form-INITIAL_FORMS': '0',
    'form-MIN_NUM_FORMS': '0',
    'form-MAX_NUM_FORMS': '5',
    'form-0-image': '',
}


def _create_user(user_data):
    return UserModel.objects.create_user(**user_data)


def _create_userprofile(user, data, **kwargs):
    # user = _create_user(VALID_USER_MODEL_DATA_1)
    userprofile_data = {
        'user': user,
        **data,
        **kwargs,

    }

    return UserProfile(**userprofile_data)


def _create_agency():
    return Agencies.objects.create(agency_name='None', agency_website='None')


def _create_trip(trip_data, user, agency):
    return Trips.objects.create(**trip_data, user_id=user.pk, used_agency_id=agency.pk)
