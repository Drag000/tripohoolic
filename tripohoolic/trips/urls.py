from django.urls import path, include

from tripohoolic.trips.views import create_trip, details_trip, edit_trip, delete_trip

urlpatterns = (
    path('create/', create_trip, name='create trip'),
    path('<int:pk>/', include([
        path('details/', details_trip, name='details trip'),
        path('edit/', edit_trip, name='edit trip'),
        path('delete/', delete_trip, name='delete trip'),
    ]))
)
