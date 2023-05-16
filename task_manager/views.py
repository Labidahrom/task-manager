from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.urls import reverse, reverse_lazy
from task_manager.models import Task
from task_manager import forms
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


class TasksListView(View):

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        f = forms.TaskFilter(request.GET,
                             queryset=Task.objects.all(),
                             request=request)
        return render(request, 'tasks_list.html', context={
            'tasks': tasks, 'filter': f
        })


class TaskDetailsView(View):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        task_labels = task.labels.values_list('name', flat=True)
        return render(request, 'task_details.html', context={
            'task': task, 'task_labels': task_labels
        })


class CreateTask(View):

    def get(self, request, *args, **kwargs):
        form = forms.TaskCreateForm()
        return render(request, 'create_task.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.TaskCreateForm(request.POST)
        if form.is_valid():
            selected_labels = form.cleaned_data['labels']
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            task.labels.set(selected_labels)

            messages.success(request, 'Задача успешно создана')
            return redirect(reverse('tasks_list'))
        return render(request, 'create_task.html', {'form': form})


class UpdateTask(View):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        if not request.user.id:
            messages.warning(request, 'Вы не авторизованы! '
                                      'Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        updated_task = Task.objects.get(id=task_id)
        form = \
            forms.TaskUpdateForm(instance=updated_task, initial={
                'labels': updated_task.labels.all()})
        return render(request, 'update_task.html',
                      {'form': form, 'updated_task': updated_task,
                       'id': task_id})

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        if not request.user.id:
            messages.warning(request, 'Вы не авторизованы! '
                                      'Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        task = Task.objects.get(id=task_id)
        form = forms.TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            selected_labels = form.cleaned_data['labels']
            task = form.save(commit=False)
            task.save()
            task.labels.set(selected_labels)
            messages.success(request, 'Задача успешно изменена')
            return redirect(reverse('tasks_list'))
        return render(request, 'update_task.html', {'form': form})


class DeleteTask(View):
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        if not request.user.id:
            messages.warning(request, 'Вы не авторизованы! Пожалуйста, '
                                      'выполните вход.')
            return redirect(reverse('login'))
        deleted_task = Task.objects.get(id=task_id)
        if request.user != deleted_task.author:
            messages.warning(request, 'Задачу может удалить '
                                      'только её автор')
            return redirect(reverse('tasks_list'))
        return render(request, 'delete_task.html',
                      {'task': deleted_task})

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        if not request.user.id:
            messages.warning(request,
                             'Вы не авторизованы! '
                             'Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        deleted_task = Task.objects.get(id=task_id)
        deleted_task.delete()
        messages.success(request, 'Задача успешно удалена')
        return redirect(reverse('tasks_list'))
