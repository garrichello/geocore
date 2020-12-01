from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm

from .models import DataKind


class DataKindForm(ModelForm):

    class Meta:
        model = DataKind
        fields = ['name']
        labels = {
            'name': _('Data kind name'),
        }