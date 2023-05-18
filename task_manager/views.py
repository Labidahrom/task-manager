from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import AccessMixin
from django.utils.translation import gettext as _
from django.contrib.messages.views import SuccessMessageMixin


def index(request):
    return render(request, 'index.html')


class LoginUser(SuccessMessageMixin, LoginView):
    template_name = 'login_user.html'
    next_page = reverse_lazy('index')
    success_message = _('You logged in')

    def form_invalid(self, form):
        messages.warning(
            self.request,
            _('Enter your username and password')
        )
        return super().form_invalid(form)


class LogoutUser(SuccessMessageMixin, LogoutView):
    template_name = 'index.html'
    next_page = reverse_lazy('index')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, _('You logged out'))
        return super().dispatch(request, *args, **kwargs)


class LoginRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, _('You are not logged in'))
            return redirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)
