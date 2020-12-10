from .common_views import CommonCreateView, CommonUpdateView, CommonDeleteView
from django.utils.translation import gettext_lazy as _

from .simple_forms import DataKindForm

from .models import DataKind


class DataKindCreateView(CommonCreateView):
    form_class = DataKindForm
    model = DataKind
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-datakind-form',
        'title': _("Create a new datakind"),
        'submit_name': _("Create datakind"),
    }
    url_name = 'metadb:datakind_create'


class DataKindUpdateView(CommonUpdateView):
    form_class = DataKindForm
    model = DataKind
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-datakind-form',
        'title': _("Update datakind"),
        'submit_name': _("Update datakind"),
    }
    url_name = 'metadb:datakind_update'

class DataKindDeleteView(CommonDeleteView):
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
