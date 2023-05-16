from django import forms
from task_manager.models import Status
from task_manager.forms import BootstrapMixin


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
