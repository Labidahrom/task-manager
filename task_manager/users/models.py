from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


# class UserManager(BaseUserManager):
#
#     def create_superuser(self, username, password, first_name=None,
#                          last_name=None, **extra_fields):
#         extra_fields['is_stuff'] = True
#         return self.create_user(username, password, first_name,
#                                 last_name, **extra_fields)
#
#     def get_by_natural_key(self, username):
#         return self.get(**{self.model.USERNAME_FIELD: username})
#
#     def _is_superuser(self, extra_fields):
#         return extra_fields.get('is_stuff')


class User(AbstractUser):
    # objects = UserManager()

    def __str__(self):
        return self.get_full_name()
