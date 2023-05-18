from django import forms
from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User
import django_filters
from django.utils.translation import gettext as _
from task_manager.forms import BootstrapMixin


class TaskCreateForm(BootstrapMixin, forms.ModelForm):
    executor = \
        forms.ModelChoiceField(queryset=User.objects.all(),
                               label=_('Executor'),
                               widget=forms.Select(
                                   attrs={'label': 'executor'}))
    status = \
        forms.ModelChoiceField(queryset=Status.objects.all(),
                               label=_('Status'),
                               widget=forms.Select(
                                   attrs={'label': 'status'}))
    labels = \
        forms.ModelMultipleChoiceField(queryset=Label.objects.all(),
                                       label=_('Labels'),
                                       widget=forms.SelectMultiple(
                                           attrs={'label': 'labels'}),
                                       required=False)

    class Meta:
        model = Task
        fields = ['name', 'description', 'executor',
                  'status', 'labels']
        widgets = {
            'name': forms.TextInput(attrs={'label': 'name'}),
            'description':
                forms.TextInput(attrs={'label': 'description'}),
            'executor':
                forms.TextInput(attrs={'label': 'executor'}),
            'status': forms.TextInput(attrs={'label': 'status'}),
            'labels': forms.TextInput(attrs={'label': 'labels'}),
        }


class TaskUpdateForm(TaskCreateForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'executor', 'status',
                  'labels']


class TaskFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('request', None)
        super().__init__(*args, **kwargs)

    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        to_field_name='name',
        label=_('Status'),
        label_suffix=''
    )
    author = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        to_field_name='username',
        label=_('Author'),
        label_suffix=''
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        to_field_name='username',
        label=_('Executor'),
        label_suffix=''
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        to_field_name='name',
        label=_('Label'),
        label_suffix=''
    )
    self_tasks = \
        django_filters.BooleanFilter(method='filter_by_authorized',
                                     widget=forms.CheckboxInput(),
                                     label="Только свои задачи",
                                     label_suffix='')

    class Meta:
        model = Task
        fields = ['status', 'author', 'executor', 'self_tasks', 'labels']

    def filter_by_authorized(self, queryset, author, value):
        authorized_user = getattr(self.request, 'user', None)

        if value:
            return queryset.filter(author=authorized_user.id)
        else:
            return queryset
