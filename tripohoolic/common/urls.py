from django.urls import path

from tripohoolic.common.views import index, dashboard, comment_trip, rate_trip, delete_comment

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('comment/<int:trip_id>/', comment_trip, name='comment trip'),
    path('rate/<int:trip_id>/', rate_trip, name='rate trip'),
    path('comment/delete/<int:comment_id>/', delete_comment, name='delete comment'),

]