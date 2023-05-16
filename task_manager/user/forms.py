from task_manager.user.models import User
from task_manager.forms import BootstrapMixin
from django.contrib.auth.forms import UserCreationForm


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
