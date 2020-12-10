from .simple_views import SimpleCreateView, SimpleUpdateView, SimpleDeleteView
from django.utils.translation import gettext_lazy as _

from .simple_forms import AccumulationModeForm

from .models import AccumulationMode


class AccumulationModeCreateView(SimpleCreateView):
    form_class = AccumulationModeForm
    model = AccumulationMode
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-accmode-form',
        'title': _("Create a new accumulation mode"),
        'submit_name': _("Create accumulation mode"),
    }
    url_name = 'metadb:accmode_create'


class AccumulationModeUpdateView(SimpleUpdateView):
    form_class = AccumulationModeForm
    model = AccumulationMode
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-accmode-form',
        'title': _("Update accumulation mode"),
        'submit_name': _("Update accumulation mode"),
    }
    url_name = 'metadb:accmode_update'

class AccumulationModeDeleteView(SimpleDeleteView):
    form_class = AccumulationModeForm
    model = AccumulationMode
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-accmode-delete-form',
        'title': _('Confirm accumulation mode delete'),
        'text': _('Are you sure you want to delete the accumulation mode'),
        'submit_name': _('Delete accumulation mode')
    }
    url_name = 'metadb:accmode_delete'
