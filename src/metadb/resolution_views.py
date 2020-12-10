from .common_views import CommonCreateView, CommonUpdateView, CommonDeleteView
from django.utils.translation import gettext_lazy as _

from .simple_forms import ResolutionForm

from .models import Resolution


class ResolutionCreateView(CommonCreateView):
    form_class = ResolutionForm
    model = Resolution
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-resolution-form',
        'title': _("Create a new resolution"),
        'submit_name': _("Create resolution"),
    }
    url_name = 'metadb:resolution_create'


class ResolutionUpdateView(CommonUpdateView):
    form_class = ResolutionForm
    model = Resolution
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-resolution-form',
        'title': _("Update resolution"),
        'submit_name': _("Update resolution"),
    }
    url_name = 'metadb:resolution_update'

class ResolutionDeleteView(CommonDeleteView):
    form_class = ResolutionForm
    model = Resolution
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-resolution-delete-form',
        'title': _('Confirm resolution delete'),
        'text': _('Are you sure you want to delete the resolution'),
        'submit_name': _('Delete resolution')
    }
    url_name = 'metadb:resolution_delete'
