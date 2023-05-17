from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.urls import reverse
from task_manager.task.models import Task
from task_manager.user.models import User
from task_manager.user import forms


class UsersListView(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, 'user/user_list.html', context={
            'users': users,
        })


class CreateUser(View):

    def get(self, request, *args, **kwargs):
        form = forms.UserCreateForm()
        return render(request, 'user/create_user.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(request.POST.get('password1'))
            user.save()
            messages.success(request, 'Пользователь успешно зарегистрирован')
            return redirect(reverse('login'))
        return render(request, 'user/create_user.html', {'form': form})


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
        return render(request, 'user/update_user.html',
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
            user.set_password(request.POST.get('password1'))
            user.save()
            messages.success(request, 'Пользователь успешно изменён')
            return redirect(reverse('users_list'))
        messages.warning(request, 'ошибка')
        return render(request, 'user/update_user.html', {'form': form})


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
        return render(request, 'user/delete_user.html',
                      {'user': deleted_user})

    def post(self, request, *args, **kwargs):
        used_authors_id = \
            [i for i in Task.objects.values_list('author',
                                                 flat=True).distinct()]
        print('used_authors_id:', used_authors_id)
        used_assignees_id = \
            [i for i in Task.objects.values_list('executor',
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
        messages.success(request, 'Пользователь успешно удалён')
        return redirect(reverse('users_list'))
