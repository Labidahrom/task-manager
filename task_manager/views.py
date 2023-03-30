from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from django import forms
from django.urls import reverse
from task_manager.models import User
from django.contrib.auth import authenticate, login, logout


class BootstrapMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class UserCreateForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']


class UserUpdateForm(UserCreateForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    password_confirmation = forms.CharField(label='Confirm password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


class LoginForm(UserCreateForm):
    class Meta:
        model = User
        fields = ['username', 'password']


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
        form = UserCreateForm()
        return render(request, 'create_user.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Создаем объект user, но не сохраняем его в базе данных
            user.set_password(request.POST.get('password'))  # Устанавливаем зашифрованный пароль
            user.save()
            return redirect('/')
        return render(request, 'create_user.html', {'form': form})


class UpdateUser(View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        if user_id != request.user.id:
            messages.error(request, 'Вы не можете редактировать этого юзера')
            return redirect(reverse('users_list'))
        updated_user = User.objects.get(id=user_id)
        form = UserUpdateForm(instance=updated_user)
        return render(request, 'update_user.html', {'form': form, 'updated_user': updated_user, 'id': user_id})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)  # Создаем объект user, но не сохраняем его в базе данных
            user.set_password(request.POST.get('password'))  # Устанавливаем зашифрованный пароль
            user.save()
            return redirect(reverse('users_list'))
        return render(request, 'update_user.html', {'form': form})


class DeleteUser(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        if user_id != request.user.id:
            messages.error(request, 'Вы не можете редактировать этого юзера')
            return redirect(reverse('users_list'))
        deleted_user = User.objects.get(id=user_id)
        return render(request, 'delete_user.html', {'user': deleted_user})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        if user_id != request.user.id:
            messages.error(request, 'Вы не можете редактировать этого юзера')
            return redirect(reverse('users_list'))
        deleted_user = User.objects.get(id=user_id)
        deleted_user.delete()
        return redirect(reverse('users_list'))


class LoginUser(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'login_user.html', {'form': form})

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_authenticated:
                messages.success(request, 'Юзер аутенфицирован')
            return redirect(reverse('users_list'))
        else:
            messages.error(request, 'Неправильное имя пользователя или пароль')
            print(f"Ошибка аутентификации для пользователя {username}.")
            return render(request, 'login_user.html', {'form': LoginForm()})


class LogoutUser(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('users_list'))
