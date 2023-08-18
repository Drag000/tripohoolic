from django.contrib import admin

from tripohoolic.common.models import TripComment, TripRating


@admin.register(TripComment)
class TripsAdmin(admin.ModelAdmin):
    list_display = ('text', 'publication_date_and_time', 'trip', 'user',)
    list_filter = ('text', 'publication_date_and_time')
    list_per_page = 20
    ordering = ('-publication_date_and_time',)

@admin.register(TripRating)
class TripsAdmin(admin.ModelAdmin):
    list_display = ('trip', 'user', 'rate',)
    list_per_page = 20
    ordering = ('-rate',)

