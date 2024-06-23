from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from tripohoolic.agencies.models import Agencies
from tripohoolic.trips.forms import TripCreateForm, TripEditForm, TripDeleteForm, MultiplePhotosForm
from tripohoolic.trips.models import Trips, Photos

UserModel = get_user_model()


def get_trip(pk):
    return Trips.objects.get(pk=pk)


@login_required
def create_trip(request):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    PhotoFormSet = modelformset_factory(Photos, fields=('image',), extra=5)

    if request.method == 'GET':
        form = TripCreateForm()
        formset = PhotoFormSet(queryset=Photos.objects.none())
    else:
        form = TripCreateForm(request.POST)
        formset = PhotoFormSet(request.POST, request.FILES, queryset=Photos.objects.none())

        if form.is_valid() and formset.is_valid():
            trip = form.save(commit=False)  # Create an instance of the Trip model without saving to the database
            trip.user = request.user  # Assign the authenticated user to the 'user' field
            trip.save()  # Save the instance to the database

            for photo_form in formset:
                if 'image' in photo_form.cleaned_data and photo_form.cleaned_data['image']:
                    photo = Photos(image=photo_form.cleaned_data['image'])
                    photo.save()
                    trip.photos.add(photo)

            return redirect('dashboard')

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'trips/create-trip.html', context)


@login_required
def details_trip(request, pk):
    trip = get_trip(pk)
    photos = trip.photos.all()

    rights_to_edit = True
    if request.user.pk != trip.user_id:
        rights_to_edit = False

    context = {
        'trip': trip,
        'rights_to_edit': rights_to_edit,
        'photos': photos,
    }
    return render(request, 'trips/details-trip.html', context)


@login_required
def edit_trip(request, pk):
    trip = get_trip(pk)
    agencies = Agencies.objects.all()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    if request.method == 'GET':
        form = TripEditForm(instance=trip)
        photos_form = MultiplePhotosForm(trip=trip)
    else:
        form = TripEditForm(request.POST, instance=trip)
        photos_form = MultiplePhotosForm(request.POST, request.FILES, trip=trip)

        if form.is_valid() and photos_form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()

            for image_file in request.FILES.getlist('image'):
                image_ins = Photos(image=image_file)  # Create object and save it to the model Photos
                image_ins.save()
                trip.photos.add(image_ins)  # Create connection in the through table

            photo_ids_to_delete = photos_form.cleaned_data['delete_photos']
            for id_to_delete in photo_ids_to_delete:  # deleting the selected photos by id from the model Photos
                Photos(id=id_to_delete).delete()

            def get_success_url():
                return reverse('details trip', kwargs={'pk': trip.pk})

            return redirect(get_success_url())

    context = {
        'form': form,
        'photos_form': photos_form,
        'trip': trip,
    }
    return render(request, 'trips/edit-trip.html', context)


@login_required
def delete_trip(request, pk):
    trip = get_trip(pk)

    if request.method == 'GET':
        form = TripDeleteForm(instance=trip)
    else:
        # form = TripDeleteForm(request.POST, instance=trip)
        # if form.is_valid():
        #     form.save()
        trip.delete()
        return redirect('dashboard')

    context = {
        'form': form,
        'trip': trip,
    }

    return render(request, 'trips/delete-trip.html', context)
