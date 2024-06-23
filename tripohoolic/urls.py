
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tripohoolic.common.urls')),
    path('accounts/', include('tripohoolic.accounts.urls')),
    path('trips/', include('tripohoolic.trips.urls')),
    path('agencies/', include('tripohoolic.agencies.urls')),

    #Enable browsable API of Django Rest Framework
    path('api-auth/', include('rest_framework.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)