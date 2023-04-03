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
        widgets = {
            'first_name': forms.TextInput(attrs={'label': 'first_name'}),
            'last_name': forms.TextInput(attrs={'label': 'last_name'}),
            'username': forms.TextInput(attrs={'label': 'username'}),
            'password': forms.PasswordInput(attrs={'label': 'username'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


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


class LoginForm(UserCreateForm, BootstrapMixin):
    class Meta:
        model = User
        fields = ['username', 'password']


def index(request):
    return render(request, 'base.html')
