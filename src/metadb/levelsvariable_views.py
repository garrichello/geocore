from .simple_views import SimpleCreateView, SimpleUpdateView, SimpleDeleteView
from django.utils.translation import gettext_lazy as _

from .simple_forms import LevelsVariableForm

from .models import Variable


class LevelsVariableCreateView(SimpleCreateView):
    form_class = LevelsVariableForm
    model = Variable
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-levels-variable-form',
        'title': _("Create a new levels variable"),
        'submit_name': _("Create levels variable"),
    }
    url_name = 'metadb:levels_variable_create'


class LevelsVariableUpdateView(SimpleUpdateView):
    form_class = LevelsVariableForm
    model = Variable
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-levels-variable-form',
        'title': _("Update levels variable"),
        'submit_name': _("Update levels variable"),
    }
    url_name = 'metadb:levels_variable_update'

class LevelsVariableDeleteView(SimpleDeleteView):
    form_class = LevelsVariableForm
    model = Variable
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-levels-variable-delete-form',
        'title': _('Confirm levels variable delete'),
        'text': _('Are you sure you want to delete the levels variable'),
        'submit_name': _('Delete levels variable')
    }
    url_name = 'metadb:levels_variable_delete'
