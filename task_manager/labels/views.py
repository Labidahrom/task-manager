from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from task_manager.labels.models import Label
from task_manager.tasks.models import TaskLabel
from task_manager.labels import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.list import ListView


class LabelsListView(ListView):
    model = Label
    template_name = 'label/label_list.html'
    context_object_name = 'labels'


class CreateLabel(SuccessMessageMixin, CreateView):

    form_class = forms.LabelCreateForm
    template_name = 'label/create_label.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Label created')


class UpdateLabel(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Label
    form_class = forms.LabelUpdateForm
    template_name = 'label/update_label.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Label changed')


class DeleteLabel(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'label/delete_label.html'
    success_url = reverse_lazy('labels_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if self.object.tasklabel_set.exists():
            messages.warning(request, _("Can't delete label"))
            return redirect(self.get_success_url())
        messages.success(request, _('Label deleted'))
        return self.form_valid(form)
