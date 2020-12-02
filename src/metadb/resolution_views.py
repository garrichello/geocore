from .simple_views import SimpleCreateView, SimpleUpdateView, SimpleDeleteView
from django.utils.translation import gettext_lazy as _

from .simple_forms import ResolutionForm

from .models import Resolution


class ResolutionCreateView(SimpleCreateView):
    form_class = ResolutionForm
    model = Resolution
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-resolution-create-form',
        'title': _("Create a new resolution"),
        'submit_name': _("Create resolution"),
    }
    url_name = 'metadb:resolution_create'


class ResolutionUpdateView(SimpleUpdateView):
    form_class = ResolutionForm
    model = Resolution
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-resolution-update-form',
        'title': _("Update resolution"),
        'submit_name': _("Update resolution"),
    }
    url_name = 'metadb:resolution_update'

class ResolutionDeleteView(SimpleDeleteView):
    form_class = ResolutionForm
    model = Resolution
    template_name = 'metadb/includes/simple_delete_form.html'
    ctx = {
        'form_class': 'js-resolution-delete-form',
        'title': _('Confirm resolution delete'),
        'text': _('Are you sure you want to delete the resolution'),
        'submit_name': _('Delete resolution')
    }
    url_name = 'metadb:resolution_delete'
