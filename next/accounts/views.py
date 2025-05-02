from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, View
from next.accounts.forms import AppUserCreationForm, ProfileEditForm
from next.accounts.models import Profile


class AppUserRegisterView(CreateView):
    model = get_user_model()
    form_class = AppUserCreationForm
    template_name = 'accounts/register.html'

    def get_success_url(self):
        return reverse('profile-details', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class AppUserLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid email or password')
        return super().form_invalid(form)


class ProfileDetailsView(DetailView):
    model = Profile
    template_name = 'accounts/profile-details.html'
    context_object_name = 'profile'


class ProfileEditView(UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, pk=self.kwargs.get('pk'))

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.object.pk})


class ProfileDeleteView(LoginRequiredMixin, View):
    template_name = 'accounts/profile-delete.html'
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'user': request.user})

    def post(self, request, *args, **kwargs):
        user = request.user
        logout(request)
        user.delete()
        return redirect(self.success_url)


class AppUserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'accounts/password-change.html'
    success_message = 'Your password has been successfully changed!'
    success_url = reverse_lazy('password-change')
