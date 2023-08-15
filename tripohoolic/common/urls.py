from django.urls import path

from tripohoolic.common.views import index, dashboard, comment_trip, rate_trip

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('comment/<int:trip_id>/', comment_trip, name='comment trip'),
    path('rate/<int:trip_id>/', rate_trip, name='rate trip'),

]