from django.contrib.auth import views as auth_views, login, get_user_model, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from tripohoolic.accounts.forms_mixins import CustomFormsMixin
from tripohoolic.accounts.models import UserProfile

UserModel = get_user_model()


class RegisterUserView(views.CreateView, CustomFormsMixin):
    template_name = 'profile/create-profile.html'
    form_class = None
    success_url = reverse_lazy('index')


class LoginUserView(auth_views.LoginView):
    template_name = 'profile/login-profile.html'


class LogoutUserView(auth_views.LogoutView, LoginRequiredMixin):
    pass


class ProfileDetailsView(views.DetailView, LoginRequiredMixin):
    template_name = 'profile/details-profile.html'
    model = UserProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch data from UserProfile model. (This is "object")
        user_profile = UserProfile.objects.get(pk=self.kwargs['pk'])
        context['user_profile'] = user_profile

        # Fetch data from User model  (take the user as an object)
        user_model = UserModel.objects.get(pk=user_profile.pk)
        context['user_model'] = user_model

        rights_to_edit = True
        if user_profile.pk != self.request.user.pk:
            rights_to_edit = False

        context['rights_to_edit'] = rights_to_edit

        return context


class ProfileEditView(views.UpdateView, LoginRequiredMixin):
    model = UserProfile
    fields = ['first_name', 'last_name', 'email', 'age', 'profile_picture']
    template_name = 'profile/edit-profile.html'

    def get_success_url(self):
        return reverse('details user', kwargs={'pk': self.object.user.pk})


class PasswordEditView(auth_views.PasswordChangeView, LoginRequiredMixin):
    model = UserModel
    template_name = 'profile/edit-password.html'

    def get_success_url(self):
        return reverse('details user', kwargs={'pk': self.request.user.pk})


class ProfileDeleteView(views.DeleteView, LoginRequiredMixin):
    model = UserModel
    template_name = 'profile/delete-profile.html'
    success_url = reverse_lazy('index')
