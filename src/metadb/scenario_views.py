from .common_views import CommonCreateView, CommonUpdateView, CommonDeleteView
from django.utils.translation import gettext_lazy as _

from .simple_forms import ScenarioForm

from .models import Scenario


class ScenarioCreateView(CommonCreateView):
    form_class = ScenarioForm
    model = Scenario
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-scenario-form',
        'title': _("Create a new scenario"),
        'submit_name': _("Create scenario"),
    }
    url_name = 'metadb:scenario_create'


class ScenarioUpdateView(CommonUpdateView):
    form_class = ScenarioForm
    model = Scenario
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-scenario-form',
        'title': _("Update scenario"),
        'submit_name': _("Update scenario"),
    }
    url_name = 'metadb:scenario_update'

class ScenarioDeleteView(CommonDeleteView):
    form_class = ScenarioForm
    model = Scenario
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-scenario-delete-form',
        'title': _('Confirm scenario delete'),
        'text': _('Are you sure you want to delete the scenario'),
        'submit_name': _('Delete scenario')
    }
    url_name = 'metadb:scenario_delete'
