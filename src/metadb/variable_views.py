from .simple_views import SimpleCreateView, SimpleUpdateView, SimpleDeleteView
from django.utils.translation import gettext_lazy as _

from .simple_forms import VariableForm

from .models import Variable


class VariableCreateView(SimpleCreateView):
    form_class = VariableForm
    model = Variable
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-variable-form',
        'title': _("Create a new variable"),
        'submit_name': _("Create variable"),
    }
    url_name = 'metadb:variable_create'


class VariableUpdateView(SimpleUpdateView):
    form_class = VariableForm
    model = Variable
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-variable-form',
        'title': _("Update variable"),
        'submit_name': _("Update variable"),
    }
    url_name = 'metadb:variable_update'

class VariableDeleteView(SimpleDeleteView):
    form_class = VariableForm
    model = Variable
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-variable-delete-form',
        'title': _('Confirm variable delete'),
        'text': _('Are you sure you want to delete the variable'),
        'submit_name': _('Delete variable')
    }
    url_name = 'metadb:variable_delete'
