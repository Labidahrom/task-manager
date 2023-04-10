from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from django import forms
from django.urls import reverse
from task_manager.models import User, Status, Task, Label
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


class StatusCreateForm(BootstrapMixin, forms.ModelForm):

    class Meta:
        model = Status
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'label': 'name'}),
        }


class StatusUpdateForm(StatusCreateForm):

    class Meta:
        model = Status
        fields = ['name']


class TaskCreateForm(BootstrapMixin, forms.ModelForm):
    assigned_to = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'label': 'assigned_to'}))
    status = forms.ModelChoiceField(queryset=Status.objects.all(), widget=forms.Select(attrs={'label': 'status'}))
    label = forms.ModelMultipleChoiceField(queryset=Label.objects.all(), widget=forms.SelectMultiple(attrs={'label': 'label'}), required=False)

    class Meta:
        model = Task
        fields = ['name', 'description', 'assigned_to', 'status', 'label']
        widgets = {
            'name': forms.TextInput(attrs={'label': 'name'}),
            'description': forms.TextInput(attrs={'label': 'description'}),
            'assigned_to': forms.TextInput(attrs={'label': 'assigned_to'}),
            'status': forms.TextInput(attrs={'label': 'status'}),
            'label': forms.TextInput(attrs={'label': 'label'}),
        }


class TaskUpdateForm(TaskCreateForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'assigned_to', 'status', 'label']


class LabelCreateForm(BootstrapMixin, forms.ModelForm):

    class Meta:
        model = Label
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'label': 'label'}),
        }


class LabelUpdateForm(LabelCreateForm):

    class Meta:
        model = Label
        fields = ['name']
