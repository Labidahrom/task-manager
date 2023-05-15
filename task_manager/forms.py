from django import forms
from task_manager.models import User, Status, Task, Label
import django_filters
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _


class BootstrapMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for field in self.fields:
            self.fields[field].widget.\
                attrs.update({'class': 'form-control mb-3'})


class UserCreateForm(BootstrapMixin, UserCreationForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")


class UserUpdateForm(UserCreateForm):
    pass


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


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.first_name + " " + obj.last_name


class TaskCreateForm(BootstrapMixin, forms.ModelForm):
    executor = \
        UserModelChoiceField(queryset=User.objects.all(),
                               label=_('Executor'),
                               widget=forms.Select(
                                   attrs={'label': 'executor', 'name': 'executor'}))
    status = \
        forms.ModelChoiceField(queryset=Status.objects.all(),
                               label=_('Status'),
                               widget=forms.Select(
                                   attrs={'label': 'status'}))
    label = \
        forms.ModelMultipleChoiceField(queryset=Label.objects.all(),
                                       label=_('Label'),
                                       widget=forms.SelectMultiple(
                                       attrs={'label': 'label'}),
                                       required=False)

    class Meta:
        model = Task
        fields = ['name', 'description', 'executor',
                  'status', 'label']
        widgets = {
            'name': forms.TextInput(attrs={'label': 'name'}),
            'description':
                forms.TextInput(attrs={'label': 'description'}),
            'executor':
                forms.TextInput(attrs={'label': 'executor'}),
            'status': forms.TextInput(attrs={'label': 'status'}),
            'label': forms.TextInput(attrs={'label': 'label'}),
        }


class TaskUpdateForm(TaskCreateForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'executor', 'status',
                  'label']


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


class TaskFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('request', None)
        super().__init__(*args, **kwargs)

    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        to_field_name='name',
        label_suffix=''
    )
    author = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        to_field_name='username'
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        to_field_name='username'
    )
    self_tasks = \
        django_filters.BooleanFilter(method='filter_by_authorized',
                                     widget=forms.CheckboxInput(),
                                     label="Только свои задачи",
                                     label_suffix='')

    class Meta:
        model = Task
        fields = ['status', 'author', 'executor', 'self_tasks']

    def filter_by_authorized(self, queryset, author, value):
        authorized_user = getattr(self.request, 'user', None)

        if value:
            return queryset.filter(author=authorized_user.id)
        else:
            return queryset
