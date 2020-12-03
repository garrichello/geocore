from .simple_views import SimpleCreateView, SimpleUpdateView, SimpleDeleteView
from django.utils.translation import gettext_lazy as _

from .simple_forms import PropertyForm

from .models import Property


class PropertyCreateView(SimpleCreateView):
    form_class = PropertyForm
    model = Property
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-property-create-form',
        'title': _("Create a new property"),
        'submit_name': _("Create property"),
    }
    url_name = 'metadb:property_create'


class PropertyUpdateView(SimpleUpdateView):
    form_class = PropertyForm
    model = Property
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-property-update-form',
        'title': _("Update property"),
        'submit_name': _("Update property"),
    }
    url_name = 'metadb:property_update'

class PropertyDeleteView(SimpleDeleteView):
    form_class = PropertyForm
    model = Property
    template_name = 'metadb/includes/simple_delete_form.html'
    ctx = {
        'form_class': 'js-property-delete-form',
        'title': _('Confirm property delete'),
        'text': _('Are you sure you want to delete the property'),
        'submit_name': _('Delete property')
    }
    url_name = 'metadb:property_delete'
