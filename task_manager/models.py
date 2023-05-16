from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from task_manager.status.models import Status
from task_manager.label.models import Label
from task_manager.user.models import User


class TaskLabel(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    label = models.ForeignKey('label.Label', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('task', 'label')


class Task(models.Model):
    name = models.CharField(_('Name'), max_length=100, unique=True)
    description = models.TextField(_('Description'), )
    author = models.ForeignKey(User, on_delete=models.PROTECT,
                               related_name='user_author')
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    executor = models.ForeignKey(User, on_delete=models.PROTECT,
                                 related_name='user_assignee')
    labels = models.ManyToManyField(Label, through=TaskLabel,
                                    related_name='tasks')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
