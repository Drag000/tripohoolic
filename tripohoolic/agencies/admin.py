from django.contrib import admin

from tripohoolic.agencies.models import Agencies


@admin.register(Agencies)
class TripsAdmin(admin.ModelAdmin):
    list_display = ('agency_name', 'agency_website',)
    search_fields = ('agency_name', 'agency_website')
    list_per_page = 15