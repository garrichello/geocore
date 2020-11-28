from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm

from .models import Resolution


class ResolutionForm(ModelForm):

    class Meta:
        model = Resolution
        fields = ['name', 'subpath1']
        labels = {
            'name': _('Resolution name'),
            'subpath1': _('Resolution subpath'),
        }