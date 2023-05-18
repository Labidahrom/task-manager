from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from task_manager.task.models import Task
from task_manager.user.models import User
from task_manager.user import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.views import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.list import ListView


class UsersListView(ListView):
    model = User
    template_name = 'user/user_list.html'
    context_object_name = 'users'


class CreateUser(SuccessMessageMixin, CreateView):
    form_class = forms.UserCreateForm
    template_name = 'user/create_user.html'
    success_url = reverse_lazy('login')
    success_message = _('User created')


class UpdateUser(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = forms.UserUpdateForm
    template_name = 'user/update_user.html'
    success_url = reverse_lazy('users_list')
    success_message = _('User changed')

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        if user_id != request.user.id:
            messages.warning(request, _("Can't edit user"))
            return redirect(reverse('users_list'))
        return super().get(request, *args, **kwargs)


class DeleteUser(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'user/delete_user.html'
    success_url = reverse_lazy('users_list')

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        if user_id != request.user.id:
            messages.warning(request, _("Can't edit user"))
            return redirect(reverse('users_list'))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if self.object.id != self.request.user.id:
            messages.warning(request, _("Can't edit user"))
            return redirect(self.get_success_url())
        if Task.objects.filter(author=self.object).exists() or \
                Task.objects.filter(executor=self.object).exists():
            messages.warning(request, _("Can't edit used user"))
            return redirect(self.get_success_url())
        messages.success(request, _('User deleted'))
        return self.form_valid(form)
