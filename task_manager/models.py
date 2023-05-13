from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, first_name=None,
                    last_name=None, **extra_fields):
        if not username:
            raise ValueError('username пользователя '
                             'обязательно для заполнения')

        if self._is_superuser(extra_fields):
            first_name = None
            last_name = None
        else:
            if not first_name:
                raise ValueError('first_name пользователя обязательно '
                                 'для заполнения')
            if not last_name:
                raise ValueError('last_name пользователя обязательно '
                                 'для заполнения')

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            created_at=timezone.now(),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, first_name=None,
                         last_name=None, **extra_fields):
        extra_fields['is_admin'] = True
        return self.create_user(username, password, first_name,
                                last_name, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})

    def _is_superuser(self, extra_fields):
        return extra_fields.get('is_admin')


class User(AbstractUser):
    # username = models.CharField(max_length=30, unique=True)
    # first_name = models.CharField(max_length=30, null=True)
    # last_name = models.CharField(max_length=30, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin


class Status(models.Model):
    name = models.CharField(_('Name'), max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class TaskLabel(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    label = models.ForeignKey('Label', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('task', 'label')


class Label(models.Model):
    name = models.CharField(_('Name'), max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.tasks.exists():
            raise Exception('Cannot delete Label object '
                            'with associated tasks')
        super().delete(*args, **kwargs)


class Task(models.Model):
    name = models.CharField(_('Name'), max_length=100, unique=True)
    description = models.TextField(_('Description'),)
    author = models.ForeignKey(User, on_delete=models.PROTECT,
                               related_name='user_author')
    assigned_to = models.ForeignKey(User, on_delete=models.PROTECT,
                                    related_name='user_assignee')
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    labels = models.ManyToManyField(Label, through=TaskLabel,
                                    related_name='tasks')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
