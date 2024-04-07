from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import render, redirect

from tripohoolic.common.forms import TripCommentForm, TripRatingForm, SearchCountryForm, SearchCityForm
from tripohoolic.common.models import TripComment, TripRating
from tripohoolic.trips.models import Trips
from django_countries import countries

UserModel = get_user_model()


def map_country_name(name, to_abbreviation=True):
    if to_abbreviation:
        for code, country_name in countries:
            if country_name.lower() == name.lower():
                return code
    else:
        for code, country_name in countries:
            if code.lower() == name.lower():
                return country_name

    print(f"No abbreviation found for country: {name}")
    return None


def index(request):
    trips = Trips.objects.all()

    search_form_country = SearchCountryForm(request.GET)
    search_pattern = None
    if search_form_country.is_valid():
        search_pattern = search_form_country.cleaned_data['country_name']

    if search_pattern:
        # Convert the full country name to abbreviation
        country_abbreviation = map_country_name(search_pattern)
        if country_abbreviation:
            trips = trips.filter(country__icontains=country_abbreviation)

    # search_form_city = SearchCityForm(request.GET)
    # search_pattern = None
    # if search_form_city.is_valid():
    #     search_pattern = search_form_city.cleaned_data['city_name']
    #
    # if search_pattern:
    #     trips = trips.filter(city__icontains=search_pattern)

    authenticaed_user = request.user.is_authenticated

    context = {
        'trips': trips,
        'comments_form': TripCommentForm(),
        'rate_form': TripRatingForm(),
        'search_form_country': SearchCountryForm(),
        'search_form_city': SearchCityForm(),
        'authenticaed_user': authenticaed_user,
    }
    return render(request, 'common/index.html', context)


@login_required
def dashboard(request):
    logged_in_user = request.user
    trips = Trips.objects.all().filter(user=logged_in_user)

    context = {
        "profile": logged_in_user,
        'trips': trips,
    }
    return render(request, 'common/dashboard.html', context)


@login_required
def comment_trip(request, trip_id):
    trip = Trips.objects.get(pk=trip_id)

    form = TripCommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)  # Does not persist to DB ... Do not save it to DB
        comment.trip = trip  # Takes trip by trip_in
        comment.user_id = request.user.id
        comment.save()

    return redirect('index')


@login_required
def delete_comment(request, comment_id):
    TripComment.objects.get(pk=comment_id).delete()
    return redirect('index')


@login_required
def rate_trip(request, trip_id):
    rating_trip = Trips.objects.get(pk=trip_id)

    try:
        existing_rating = TripRating.objects.get(trip_id=trip_id, user_id=request.user.id)
        existing_rating.delete()
    except TripRating.DoesNotExist:
        pass

    form = TripRatingForm(request.POST)

    if form.is_valid():
        rate = form.save(commit=False)
        rate.trip_id = rating_trip.pk
        rate.user_id = request.user.id
        rate.save()

    return redirect('index')
