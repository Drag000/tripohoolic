from django.urls import path

from tripohoolic.agencies.views import index_agencies

urlpatterns = [
    path("", index_agencies, name='agencies'),
]
