from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from django import forms
from django.urls import reverse
from task_manager.models import User
from task_manager import forms
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, 'base.html')


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
            messages.warning(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        if user_id != request.user.id:
            messages.warning(request, 'У вас нет прав для изменения другого пользователя.')
            return redirect(reverse('users_list'))
        updated_user = User.objects.get(id=user_id)
        form = forms.UserUpdateForm(instance=updated_user)
        return render(request, 'update_user.html', {'form': form, 'updated_user': updated_user, 'id': user_id})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        if user_id != request.user.id:
            messages.warning(request, 'Вы не можете редактировать этого юзера')
            return redirect(reverse('users_list'))
        user = User.objects.get(id=user_id)
        form = forms.UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)  # Создаем объект user, но не сохраняем его в базе данных
            user.set_password(request.POST.get('password'))  # Устанавливаем зашифрованный пароль
            user.save()
            return redirect(reverse('users_list'))
        return render(request, 'update_user.html', {'form': form})


class DeleteUser(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        if not request.user.id:
            messages.warning(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        if user_id != request.user.id:
            messages.warning(request, 'У вас нет прав для изменения другого пользователя.')
            return redirect(reverse('users_list'))
        deleted_user = User.objects.get(id=user_id)
        return render(request, 'delete_user.html', {'user': deleted_user})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        if user_id != request.user.id:
            messages.warning(request, 'Вы не можете редактировать этого юзера')
            return redirect(reverse('users_list'))
        deleted_user = User.objects.get(id=user_id)
        deleted_user.delete()
        return redirect(reverse('users_list'))


class LoginUser(View):

    def get(self, request, *args, **kwargs):
        form = forms.LoginForm()
        return render(request, 'login_user.html', {'form': form})

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_authenticated:
                messages.success(request, 'Вы залогинены')
            return redirect(reverse('users_list'))
        else:
            messages.warning(request, 'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.')
            return render(request, 'login_user.html', {'form': forms.LoginForm()})


class LogoutUser(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('index'))
