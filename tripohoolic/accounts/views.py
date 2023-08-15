from django.contrib.auth import views as auth_views, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import BaseUpdateView, ModelFormMixin, ProcessFormView

from tripohoolic.accounts.forms import RegisterUserForm, RegisterProfileForm
from tripohoolic.accounts.models import UserProfile

UserModel = get_user_model()


class CustomFormsMixin(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    def get(self, request, *args, **kwargs):
        user_form = RegisterUserForm()
        profile_form = RegisterProfileForm()
        return self.render_to_response(context={'user_form': user_form, 'profile_form': profile_form})

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

            # Redirect or handle success
            return redirect('index')
        else:
            return redirect('index')


class RegisterUserView(views.CreateView, CustomFormsMixin):
    template_name = 'profile/create-profile.html'
    form_class = None
    success_url = reverse_lazy('index')

    # след регистрация да се логва автом
    def form_valid(self, user_form):
        result = super().form_valid(user_form)
        user = self.object

        login(self.request, user)

        return result


class LoginUserView(auth_views.LoginView):
    template_name = 'profile/login-profile.html'


class LogoutUserView(auth_views.LogoutView, LoginRequiredMixin):
    pass


class ProfileDetailsView(views.DetailView, LoginRequiredMixin):
    template_name = 'profile/details-profile.html'
    model = UserProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch data from UserProfile model.. това си е "object." ....
        user_profile = UserProfile.objects.get(pk=self.kwargs['pk'])
        context['user_profilee'] = user_profile

        # Fetch data from User model
        asd = UserModel.objects.get(pk=user_profile.pk)
        context['userr'] = asd

        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     # Get the current User instance associated with the view
    #     user_instance = self.request.user
    #
    #     try:
    #         # Try to retrieve the associated UserProfile instance for the User
    #         user_profile = UserProfile.objects.get(user=user_instance)
    #         # Add the UserProfile pk as context data
    #         context['user_profile_pk'] = user_profile.pk
    #     except UserProfile.DoesNotExist:
    #         # Handle the case where UserProfile does not exist for the current User
    #         context['user_profile_pk'] = None
    #
    #     return context


# class ProfileEditView(views.UpdateView):
#     model = UserProfile
#     fields = ['first_name', 'last_name', 'age', 'profile_picture', 'username']
#     template_name = 'profile/edit-profile.html'
#     success_url = reverse_lazy('index')
#
#     def get_initial(self):
#         initial = super().get_initial()
#         user_profile = self.get_object()  # Get the UserProfile object for the current instance
#         initial['username'] = user_profile.user.username
#         initial['first_name'] = user_profile.first_name
#         initial['first_name'] = user_profile.user.username
#         initial['last_name'] = user_profile.last_name
#         initial['age'] = user_profile.age
#         initial['profile_picture'] = user_profile.profile_picture
#
#         return initial

# class ProfileEditView(views.UpdateView):
#     model = UserProfile
#     fields = ['first_name', 'last_name', 'age', 'profile_picture']
#     template_name = 'profile/edit-profile.html'
#     success_url = reverse_lazy('index')


class ProfileEditView(views.UpdateView,LoginRequiredMixin):
    model = UserProfile
    fields = ['first_name', 'last_name', 'age', 'profile_picture']
    template_name = 'profile/edit-profile.html'
    success_url = reverse_lazy('index')


class PasswordEditView(auth_views.PasswordChangeView,LoginRequiredMixin):
    model = UserModel
    # fields = ['email', 'password']
    template_name = 'profile/edit-password.html'
    success_url = reverse_lazy('index')


class ProfileDeleteView(views.DeleteView, LoginRequiredMixin):
    model = UserModel
    template_name = 'profile/delete-profile.html'
    success_url = reverse_lazy('index')