from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.urls import reverse
from task_manager.status.models import Status
from task_manager.status import forms


class CreateStatus(View):

    def get(self, request, *args, **kwargs):
        form = forms.StatusCreateForm()
        return render(request, 'status/create_status.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.StatusCreateForm(request.POST)
        if form.is_valid():
            status = form.save(commit=False)
            status.save()
            messages.success(request, 'Статус успешно создан')
            return redirect(reverse('statuses_list'))
        return render(request, 'status/create_status.html', {'form': form})


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
                      'status/update_status.html',
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
        return render(request, 'status/update_status.html', {'form': form})


class DeleteStatus(View):

    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        if not request.user.id:
            messages.warning(request, 'Вы не авторизованы! '
                                      'Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        deleted_status = Status.objects.get(id=status_id)
        return render(request, 'status/delete_status.html',
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


class StatusesListView(View):

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        return render(request, 'status/status_list.html', context={
            'statuses': statuses
        })
