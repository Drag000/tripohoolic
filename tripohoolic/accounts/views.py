from django.contrib.auth import views as auth_views, login, get_user_model, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import BaseUpdateView, ModelFormMixin, ProcessFormView

from tripohoolic.accounts.forms import RegisterUserForm, RegisterProfileForm
from tripohoolic.accounts.models import UserProfile

UserModel = get_user_model()


class CustomFormsMixin(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    # overwriting get() to have the 2 forms
    def get(self, request, *args, **kwargs):
        user_form = RegisterUserForm()
        profile_form = RegisterProfileForm()
        return self.render_to_response(
            context={'user_form': user_form,
                     'profile_form': profile_form
                     }
        )

    # validating the 2 forms and save them
    def post(self, request, *args, **kwargs):
        user_form = RegisterUserForm(request.POST)
        profile_form = RegisterProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save data to User model
            user_instance = user_form.save()

            # Save data to UserProfile model (linking to the User model)
            profile_instance = profile_form.save(commit=False)
            profile_instance.user = user_instance
            profile_instance.save()

            # Login auutomatically after registration
            login(self.request, user_instance)

            return redirect('index')
        else:
            return redirect('index')


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

        # Fetch data from UserProfile model.. това си е "object." ...
        user_profile = UserProfile.objects.get(pk=self.kwargs['pk'])
        context['user_profilee'] = user_profile

        # Fetch data from User model  (take the user as an object)
        asd = UserModel.objects.get(pk=user_profile.pk)
        context['userr'] = asd

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
