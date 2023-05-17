from django.shortcuts import render
from django.contrib import messages
from django.views import View
from django.urls import reverse_lazy
from task_manager.task.models import Task
from task_manager.task import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.views import LoginRequiredMixin


class TasksListView(View):

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        f = forms.TaskFilter(request.GET,
                             queryset=Task.objects.all(),
                             request=request)
        return render(request, 'task/tasks_list.html', context={
            'tasks': tasks, 'filter': f
        })


class TaskDetailsView(View):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = Task.objects.get(id=task_id)
        task_labels = task.labels.values_list('name', flat=True)
        return render(request, 'task/task_details.html', context={
            'task': task, 'task_labels': task_labels
        })


class CreateTask(CreateView):
    form_class = forms.TaskCreateForm
    template_name = 'task/create_task.html'
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Задача успешно создана')
        return super().form_valid(form)


class UpdateTask(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = forms.TaskUpdateForm
    template_name = 'task/update_task.html'
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form):
        messages.success(self.request, 'Задача успешно изменена')
        return super().form_valid(form)


class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task/delete_task.html'
    success_url = reverse_lazy('tasks_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        messages.success(request, 'Задача успешно удалена')
        return self.form_valid(form)
