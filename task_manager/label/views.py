from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.urls import reverse
from task_manager.label.models import Label
from task_manager.label import forms


class LabelsListView(View):

    def get(self, request, *args, **kwargs):
        labels = Label.objects.all()
        return render(request, 'label/label_list.html', context={
            'labels': labels,
        })


class CreateLabel(View):

    def get(self, request, *args, **kwargs):
        form = forms.LabelCreateForm()
        return render(request, 'label/create_label.html',
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.LabelCreateForm(request.POST)
        if form.is_valid():
            label = form.save(commit=False)
            label.save()
            messages.success(request,
                             'Метка успешно создана')
            return redirect(reverse('labels_list'))
        return render(request, 'label/create_label.html',
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
        return render(request, 'label/update_label.html',
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
            messages.success(request, 'Метка успешно изменена')
            return redirect(reverse('labels_list'))
        return render(request, 'label/update_label.html', {'form': form})


class DeleteLabel(View):
    def get(self, request, *args, **kwargs):
        label_id = kwargs.get('id')
        if not request.user.id:
            messages.warning(request, 'Вы не авторизованы! '
                                      'Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        deleted_label = Label.objects.get(id=label_id)
        return render(request, 'label/delete_label.html',
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
        messages.success(request, 'Метка успешно удалена')
        return redirect(reverse('labels_list'))
