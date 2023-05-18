from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from task_manager.task.models import Task
from task_manager.task import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.views import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.list import ListView


class TasksListView(ListView):
    model = Task
    template_name = 'task/tasks_list.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = \
            forms.TaskFilter(self.request.GET, queryset=self.get_queryset(),
                             request=self.request)
        return context


class TaskDetailsView(View):
    model = Task
    template_name = 'task/tasks_list.html'
    context_object_name = 'tasks'

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = Task.objects.get(id=task_id)
        task_labels = task.labels.values_list('name', flat=True)
        return render(request, 'task/task_details.html', context={
            'task': task, 'task_labels': task_labels
        })


class CreateTask(SuccessMessageMixin, CreateView):
    form_class = forms.TaskCreateForm
    template_name = 'task/create_task.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('Task created')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTask(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Task
    form_class = forms.TaskUpdateForm
    template_name = 'task/update_task.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('Task changed')


class DeleteTask(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'task/delete_task.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('Task deleted')
