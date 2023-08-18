from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from tripohoolic.accounts.views import LoginUserView, LogoutUserView, RegisterUserView, ProfileDetailsView, \
    ProfileEditView, ProfileDeleteView, PasswordEditView

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login user'),
    path('logout/', LogoutUserView.as_view(), name='logout user'),
    path('register/', RegisterUserView.as_view(), name='register user'),
    path('profile/<int:pk>/', include([
        path('details/', ProfileDetailsView.as_view(), name='details user'),
        path('edit-profile/', ProfileEditView.as_view(), name='edit profile'),
        path('edit-password/', PasswordEditView.as_view(), name='edit password'),
        path('delete/', ProfileDeleteView.as_view(), name='delete user'),
    ]))]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
