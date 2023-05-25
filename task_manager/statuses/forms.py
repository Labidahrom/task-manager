from django import forms
from task_manager.statuses.models import Status


class StatusCreateForm(forms.ModelForm):
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
