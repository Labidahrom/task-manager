from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.urls import reverse_lazy
from task_manager.label.models import Label
from task_manager.task.models import TaskLabel
from task_manager.label import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.views import LoginRequiredMixin
from django.utils.translation import gettext as _


class LabelsListView(View):

    def get(self, request, *args, **kwargs):
        labels = Label.objects.all()
        return render(request, 'label/label_list.html', context={
            'labels': labels,
        })


class CreateLabel(CreateView):
    form_class = forms.LabelCreateForm
    template_name = 'label/create_label.html'
    success_url = reverse_lazy('labels_list')

    def form_valid(self, form):
        messages.success(self.request, _('Label created'))
        return super().form_valid(form)


class UpdateLabel(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = forms.LabelUpdateForm
    template_name = 'label/update_label.html'
    success_url = reverse_lazy('labels_list')

    def form_valid(self, form):
        messages.success(self.request, _('Label changed'))
        return super().form_valid(form)


class DeleteLabel(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'label/delete_label.html'
    success_url = reverse_lazy('labels_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if TaskLabel.objects.filter(label=self.object).exists():
            messages.warning(request, _("Can't delete label"))
            return redirect(self.get_success_url())
        messages.success(request, _('Label deleted'))
        return self.form_valid(form)
