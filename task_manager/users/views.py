from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from task_manager.users.models import User
from task_manager.users import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.mixins import LoginRequiredMixin, UserRequiredMixin
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


class UpdateUser(SuccessMessageMixin, LoginRequiredMixin,
                 UserRequiredMixin, UpdateView):
    model = User
    form_class = forms.UserUpdateForm
    template_name = 'user/update_user.html'
    success_url = reverse_lazy('users_list')
    success_message = _('User changed')
    permission_denied_message = _("Can't edit user")


class DeleteUser(LoginRequiredMixin, UserRequiredMixin, DeleteView):
    model = User
    template_name = 'user/delete_user.html'
    success_url = reverse_lazy('users_list')
    permission_denied_message = _("Can't delete user")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user_author.exists() or \
                self.object.user_assignee.exists():
            messages.warning(request, _("Can't delete used user"))
            return redirect(self.get_success_url())
        messages.success(request, _('User deleted'))
        return super().post(request, *args, **kwargs)
