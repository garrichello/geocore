from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm

from .models import FileType


class FileTypeForm(ModelForm):

    class Meta:
        model = FileType
        fields = ['name']
        labels = {
            'name': _('File type name'),
        }