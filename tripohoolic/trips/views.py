from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from tripohoolic.trips.forms import TripCreateForm, TripEditForm, TripDeleteForm
from tripohoolic.trips.models import Trips

UserModel = get_user_model()


def get_trip(pk):
    return Trips.objects.get(pk=pk)


@login_required
def create_trip(request):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the 'required' attribute of the 'used_agency' field's widget to False
        self.fields['used_agency'].widget.attrs['required'] = False

    if request.method == 'GET':
        form = TripCreateForm()
    else:
        form = TripCreateForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)  # Create an instance of the Trip model without saving to the database
            trip.user = request.user  # Assign the authenticated user to the 'user' field
            trip.save()  # Save the instance to the database
            return redirect('dashboard')

    context = {
        'form': form,
    }
    return render(request, 'trips/create-trip.html', context)


@login_required
def details_trip(request, pk):
    trip = get_trip(pk)

    rights_to_edit = True
    if request.user.pk != trip.user_id:
        rights_to_edit = False

    context = {
        'trip': trip,
        'rights_to_edit': rights_to_edit,
    }
    return render(request, 'trips/details-trip.html', context)


@login_required
def edit_trip(request, pk):
    trip = get_trip(pk)



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the 'required' attribute of the 'used_agency' field's widget to False
        self.fields['used_agency'].widget.attrs['required'] = False

    if request.method == 'GET':
        form = TripEditForm(instance=trip)
    else:
        form = TripEditForm(request.POST, instance=trip)
        if form.is_valid():
            # form.save()
            trip = form.save(commit=False)
            trip.user = request.user

            # Perform the additional validation for used_agency field here
            if trip.type == Trips.TYPE_AGENCY and not trip.used_agency:
                form.add_error('used_agency', 'This field is required for agency trips.')
                return render(request, 'trips/create-trip.html', {'form': form})

            trip.save()
            return redirect('dashboard')

    context = {
        'form': form,
        'trip': trip,
    }
    return render(request, 'trips/edit-trip.html', context)


@login_required
def delete_trip(request, pk):
    trip = get_trip(pk)

    if request.method == 'GET':
        form = TripDeleteForm(instance=trip)
    else:
        form = TripDeleteForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {
        'form': form,
        'trip': trip,
    }

    return render(request, 'trips/delete-trip.html', context)
