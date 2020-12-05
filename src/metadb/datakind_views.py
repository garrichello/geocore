from .simple_views import SimpleCreateView, SimpleUpdateView, SimpleDeleteView
from django.utils.translation import gettext_lazy as _

from .simple_forms import DataKindForm

from .models import DataKind


class DataKindCreateView(SimpleCreateView):
    form_class = DataKindForm
    model = DataKind
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-datakind-create-form',
        'title': _("Create a new datakind"),
        'submit_name': _("Create datakind"),
    }
    url_name = 'metadb:datakind_create'


class DataKindUpdateView(SimpleUpdateView):
    form_class = DataKindForm
    model = DataKind
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-datakind-update-form',
        'title': _("Update datakind"),
        'submit_name': _("Update datakind"),
    }
    url_name = 'metadb:datakind_update'

class DataKindDeleteView(SimpleDeleteView):
    form_class = DataKindForm
    model = DataKind
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-datakind-delete-form',
        'title': _('Confirm data kind delete'),
        'text': _('Are you sure you want to delete the data kind'),
        'submit_name': _('Delete data kind')
    }
    url_name = 'metadb:datakind_delete'
