from django.contrib import admin

from tripohoolic.accounts.models import UserProfile


@admin.register(UserProfile)
class TripsAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'age', 'email')
    list_filter = ('first_name', 'first_name', 'age')
    search_fields = ('first_name', 'last_name','email', 'age')
    list_per_page = 20