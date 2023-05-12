from django import forms
from task_manager.models import User, Status, Task, Label
import django_filters
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


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
    # password = forms.CharField(label='Password',
    #                            widget=forms.PasswordInput())
    # password_confirmation = \
    #     forms.CharField(label='Confirm password',
    #                     widget=forms.PasswordInput())

    # class Meta:
    #     model = User
    #     fields = ['first_name', 'last_name', 'username']
    #
    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = cleaned_data.get("password")
    #     password_confirmation = \
    #         cleaned_data.get("password_confirmation")
    #
    #     if password and password_confirmation and password != \
    #             password_confirmation:
    #         raise forms.ValidationError("Passwords do not match")
    #
    #     return cleaned_data


# class LoginForm(BootstrapMixin, AuthenticationForm):
#
#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop('request', None)
#         super().__init__(*args, request=self.request, **kwargs)
#
#     username = forms.CharField(
#         label='Имя пользователя',
#         widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'})
#     )
#     password = forms.CharField(
#         label='Пароль',
#         widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'})
#     )
#
#     class Meta:
#         model = User
#         fields = ['username', 'password']


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
    assigned_to = \
        forms.ModelChoiceField(queryset=User.objects.all(),
                               widget=forms.Select(
                                   attrs={'label': 'assigned_to'}))
    status = \
        forms.ModelChoiceField(queryset=Status.objects.all(),
                               widget=forms.Select(
                                   attrs={'label': 'status'}))
    label = \
        forms.ModelMultipleChoiceField(queryset=Label.objects.all(),
                                       widget=forms.SelectMultiple(
                                       attrs={'label': 'label'}),
                                       required=False)

    class Meta:
        model = Task
        fields = ['name', 'description', 'assigned_to',
                  'status', 'label']
        widgets = {
            'name': forms.TextInput(attrs={'label': 'name'}),
            'description':
                forms.TextInput(attrs={'label': 'description'}),
            'assigned_to':
                forms.TextInput(attrs={'label': 'assigned_to'}),
            'status': forms.TextInput(attrs={'label': 'status'}),
            'label': forms.TextInput(attrs={'label': 'label'}),
        }


class TaskUpdateForm(TaskCreateForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'assigned_to', 'status',
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
        to_field_name='name'
    )
    author = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        to_field_name='username'
    )
    assigned_to = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        to_field_name='username'
    )
    is_authorized = \
        django_filters.BooleanFilter(method='filter_by_authorized',
                                     widget=forms.CheckboxInput(),
                                     label="Только свои задачи")

    class Meta:
        model = Task
        fields = ['status', 'author', 'assigned_to', 'is_authorized']

    def filter_by_authorized(self, queryset, author, value):
        authorized_user = getattr(self.request, 'user', None)

        if value:
            return queryset.filter(author=authorized_user.id)
        else:
            return queryset
