from django import forms
from task_manager.labels.models import Label
from task_manager.forms import BootstrapMixin


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
