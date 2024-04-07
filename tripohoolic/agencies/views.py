from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from tripohoolic.agencies.models import Agencies
from tripohoolic.trips.models import Trips


@login_required
def index_agencies(request):
    agencies = Agencies.objects.all()
    trips_by_agencies = Trips.objects.filter(type="Agency")

    context = {
        'agencies': agencies,
        'trips_by_agencies': trips_by_agencies,
    }

    return render(request, 'agencies/agencies.html', context)

