from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.urls import reverse_lazy
from task_manager.status.models import Status
from task_manager.task.models import Task
from task_manager.status import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.views import LoginRequiredMixin


class CreateStatus(CreateView):
    form_class = forms.StatusCreateForm
    template_name = 'status/create_status.html'
    success_url = reverse_lazy('statuses_list')

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно создан')
        return super().form_valid(form)


class UpdateStatus(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = forms.StatusUpdateForm
    template_name = 'status/update_status.html'
    success_url = reverse_lazy('statuses_list')

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно изменён')
        return super().form_valid(form)


class DeleteStatus(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'status/delete_status.html'
    success_url = reverse_lazy('statuses_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if Task.objects.filter(status=self.object).exists():
            messages.warning(request, 'Невозможно удалить статус,'
                                      ' потому что он используется')
            return redirect(self.get_success_url())
        messages.success(request, 'Статус успешно удалён')
        return self.form_valid(form)


class StatusesListView(View):

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        return render(request, 'status/status_list.html', context={
            'statuses': statuses
        })
