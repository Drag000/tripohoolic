from django.contrib import admin

from tripohoolic.trips.models import Trips


# Register your models here.

@admin.register(Trips)
class TripsAdmin(admin.ModelAdmin):
    pass
