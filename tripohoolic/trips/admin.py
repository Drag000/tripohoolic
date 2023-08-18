from django.contrib import admin

from tripohoolic.trips.models import Trips


# Register your models here.

@admin.register(Trips)
class TripsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'trip_name', 'type', 'used_agency', 'average_rating')
    search_fields = ('trip_name', 'type', 'used_agency','average_rating', 'publication_date','country', 'cities',)
    list_filter = ('type', 'average_rating', 'publication_date', 'used_agency', 'country', 'cities',)
    list_per_page = 20
    ordering = ('-average_rating',)