from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator


def index(request):
    return render(request, 'index.html')


class LoginUser(LoginView):
    template_name = 'login_user.html'
    next_page = reverse_lazy('index')

    def form_valid(self, form):
        messages.success(self.request, 'Вы залогинены')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(
            self.request,
            'Пожалуйста, введите правильные имя пользователя и пароль.'
            ' Оба поля могут быть чувствительны к регистру.'
        )
        return super().form_invalid(form)


class LogoutUser(LogoutView):
    template_name = 'index.html'
    next_page = reverse_lazy('index')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, 'Вы разлогинены')
        return super().dispatch(request, *args, **kwargs)
