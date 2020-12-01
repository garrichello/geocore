from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm

from .models import Scenario


class ScenarioForm(ModelForm):

    class Meta:
        model = Scenario
        fields = ['name', 'subpath0']
        labels = {
            'name': _('Scenario name'),
            'subpath0': _('Scenario subpath'),
        }