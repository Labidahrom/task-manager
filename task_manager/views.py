from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.urls import reverse, reverse_lazy
from task_manager.models import User, Status, Task, Label
from task_manager import forms
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, 'index.html')


class UsersListView(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, 'user_list.html', context={
            'users': users,
        })


class CreateUser(View):

    def get(self, request, *args, **kwargs):
        form = forms.UserCreateForm()
        return render(request, 'create_user.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(request.POST.get('password'))
            user.save()
            return redirect(reverse('login'))
        return render(request, 'create_user.html', {'form': form})


class UpdateUser(View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        if not request.user.id:
            messages.warning(request, 'Вы не авторизованы! '
                                      'Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        if user_id != request.user.id:
            messages.warning(request, 'У вас нет прав для '
                                      'изменения другого пользователя.')
            return redirect(reverse('users_list'))
        updated_user = User.objects.get(id=user_id)
        form = forms.UserUpdateForm(instance=updated_user)
        return render(request, 'update_user.html',
                      {'form': form, 'updated_user': updated_user,
                       'id': user_id})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        if user_id != request.user.id:
            messages.warning(request, 'Вы не можете '
                                      'редактировать этого юзера')
            return redirect(reverse('users_list'))
        user = User.objects.get(id=user_id)
        form = forms.UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(request.POST.get('password'))
            user.save()
            return redirect(reverse('users_list'))
        return render(request, 'update_user.html', {'form': form})


class DeleteUser(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        if not request.user.id:
            messages.warning(request, 'Вы не авторизованы! '
                                      'Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        if user_id != request.user.id:
            messages.warning(request, 'У вас нет прав для изменения '
                                      'другого пользователя.')
            return redirect(reverse('users_list'))
        deleted_user = User.objects.get(id=user_id)
        return render(request, 'delete_user.html',
                      {'user': deleted_user})

    def post(self, request, *args, **kwargs):
        used_authors_id = \
            [i for i in Task.objects.values_list('author',
                                                 flat=True).distinct()]
        print('used_authors_id:', used_authors_id)
        used_assignees_id = \
            [i for i in Task.objects.values_list('assigned_to',
                                                 flat=True).distinct()]
        user_id = kwargs.get('id')
        if user_id in used_authors_id or user_id in used_assignees_id:
            messages.warning(request, 'Невозможно удалить пользователя, '
                                      'потому что он используется')
            return redirect(reverse('users_list'))
        if user_id != request.user.id:
            messages.warning(request, 'Вы не можете редактировать этого '
                                      'пользователя')
            return redirect(reverse('users_list'))
        deleted_user = User.objects.get(id=user_id)
        deleted_user.delete()
        return redirect(reverse('users_list'))


class LoginUser(LoginView):
    template_name = 'login_user.html'
    next_page = reverse_lazy('index')

    def form_valid(self, form):
        users_list = str(User.objects.all())
        messages.success(self.request, users_list)
        return super().form_valid(form)

    def form_invalid(self, form):
        users_list = str(User.objects.all())
        messages.warning(
            self.request,
            f'{users_list} - это список пользователей'
        )
        return super().form_invalid(form)


class LogoutUser(LogoutView):
    template_name = 'index.html'
    next_page = reverse_lazy('index')


class StatusesListView(View):

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        return render(request, 'status_list.html', context={
            'statuses': statuses
        })


class CreateStatus(View):

    def get(self, request, *args, **kwargs):
        form = forms.StatusCreateForm()
        return render(request, 'create_status.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.StatusCreateForm(request.POST)
        if form.is_valid():
            status = form.save(commit=False)
            status.save()
            messages.success(request, 'Статус успешно создан')
            return redirect(reverse('statuses_list'))
        return render(request, 'create_status.html', {'form': form})


class UpdateStatus(View):

    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        if not request.user.id:
            messages.warning(request, 'Вы не авторизованы! '
                                      'Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        updated_status = Status.objects.get(id=status_id)
        form = forms.StatusUpdateForm(instance=updated_status)
        return render(request,
                      'update_status.html',
                      {'form': form,
                       'updated_status': updated_status,
                       'id': status_id})

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        if not request.user.id:
            messages.warning(request, 'Вы не авторизованы! '
                                      'Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        status = Status.objects.get(id=status_id)
        form = forms.StatusUpdateForm(request.POST, instance=status)
        if form.is_valid():
            status = form.save(commit=False)
            status.save()
            messages.success(request, 'Статус успешно изменён')
            return redirect(reverse('statuses_list'))
        return render(request, 'update_status.html', {'form': form})


class DeleteStatus(View):
    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        if not request.user.id:
            messages.warning(request, 'Вы не авторизованы! '
                                      'Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        deleted_status = Status.objects.get(id=status_id)
        return render(request, 'delete_status.html',
                      {'status': deleted_status})

    def post(self, request, *args, **kwargs):
        used_statuses_id = \
            [i.id for i in Status.objects.filter(
                task__isnull=False).distinct()]
        status_id = kwargs.get('id')
        if status_id in used_statuses_id:
            messages.warning(request, 'Невозможно удалить '
                                      'статус, потому что он '
                                      'используется')
            return redirect(reverse('statuses_list'))
        if not request.user.id:
            messages.warning(request, 'Вы не авторизованы! '
                                      'Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        deleted_status = Status.objects.get(id=status_id)
        deleted_status.delete()
        messages.success(request, 'Статус успешно удалён')
        return redirect(reverse('statuses_list'))


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
            selected_labels = form.cleaned_data['label']
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
                'label': updated_task.labels.all()})
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
            selected_labels = form.cleaned_data['label']
            task = form.save(commit=False)
            task.save()
            task.labels.set(selected_labels)
            messages.success(request, 'Задача успешно отредактирована')
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


class LabelsListView(View):

    def get(self, request, *args, **kwargs):
        labels = Label.objects.all()
        return render(request, 'label_list.html', context={
            'labels': labels,
        })


class CreateLabel(View):

    def get(self, request, *args, **kwargs):
        form = forms.LabelCreateForm()
        return render(request, 'create_label.html',
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.LabelCreateForm(request.POST)
        if form.is_valid():
            label = form.save(commit=False)
            label.save()
            messages.success(request,
                             'Метка успешно создана')
            return redirect(reverse('labels_list'))
        return render(request, 'create_label.html',
                      {'form': form})


class UpdateLabel(View):

    def get(self, request, *args, **kwargs):
        label_id = kwargs.get('id')
        if not request.user.id:
            messages.warning(request, 'Вы не авторизованы! '
                                      'Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        updated_label = Label.objects.get(id=label_id)
        form = forms.LabelUpdateForm(instance=updated_label)
        return render(request, 'update_label.html',
                      {'form': form, 'updated_label': updated_label,
                       'id': label_id})

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('id')
        if not request.user.id:
            messages.warning(request, 'Вы не авторизованы! '
                                      'Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        label = Label.objects.get(id=label_id)
        form = forms.LabelUpdateForm(request.POST, instance=label)
        if form.is_valid():
            label = form.save(commit=False)
            label.save()
            messages.success(request, 'Метка успешно изменёна')
            return redirect(reverse('labels_list'))
        return render(request, 'update_label.html', {'form': form})


class DeleteLabel(View):
    def get(self, request, *args, **kwargs):
        label_id = kwargs.get('id')
        if not request.user.id:
            messages.warning(request, 'Вы не авторизованы! '
                                      'Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        deleted_label = Label.objects.get(id=label_id)
        return render(request, 'delete_label.html',
                      {'label': deleted_label})

    def post(self, request, *args, **kwargs):
        used_labels_id = \
            [i.id for i in
             Label.objects.filter(tasklabel__isnull=False).distinct()]
        label_id = kwargs.get('id')
        if label_id in used_labels_id:
            messages.warning(request, 'Невозможно удалить метку, '
                                      'потому что она используется')
            return redirect(reverse('labels_list'))
        if not request.user.id:
            messages.warning(request, 'Вы не авторизованы! '
                                      'Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        deleted_label = Label.objects.get(id=label_id)
        deleted_label.delete()
        messages.success(request, 'Метка успешно удалёна')
        return redirect(reverse('labels_list'))
