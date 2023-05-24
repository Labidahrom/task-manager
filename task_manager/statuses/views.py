from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from task_manager.statuses.models import Status
from task_manager.statuses import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.list import ListView


class StatusesListView(ListView):
    model = Status
    template_name = 'status/status_list.html'
    context_object_name = 'statuses'


class CreateStatus(SuccessMessageMixin, CreateView):
    form_class = forms.StatusCreateForm
    template_name = 'status/create_status.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('Status created')


class UpdateStatus(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Status
    form_class = forms.StatusUpdateForm
    template_name = 'status/update_status.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('Status changed')


class DeleteStatus(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'status/delete_status.html'
    success_url = reverse_lazy('statuses_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.task_set.exists():
            messages.warning(request, _("Can't delete status"))
            return redirect(self.get_success_url())
        messages.success(request, _('Status deleted'))
        return super().post(request, *args, **kwargs)
