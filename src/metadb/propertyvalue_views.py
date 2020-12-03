from .simple_views import SimpleCreateView, SimpleUpdateView, SimpleDeleteView
from django.utils.translation import gettext_lazy as _

from .simple_forms import PropertyValueForm

from .models import PropertyValue


class PropertyValueCreateView(SimpleCreateView):
    form_class = PropertyValueForm
    model = PropertyValue
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-propertyvalue-create-form',
        'title': _("Create a new property value"),
        'submit_name': _("Create property value"),
    }
    url_name = 'metadb:property_value_create'


class PropertyValueUpdateView(SimpleUpdateView):
    form_class = PropertyValueForm
    model = PropertyValue
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-propertyvalue-update-form',
        'title': _("Update property value"),
        'submit_name': _("Update property value"),
    }
    url_name = 'metadb:property_value_update'

class PropertyValueDeleteView(SimpleDeleteView):
    form_class = PropertyValueForm
    model = PropertyValue
    template_name = 'metadb/includes/simple_delete_form.html'
    ctx = {
        'form_class': 'js-propertyvalue-delete-form',
        'title': _('Confirm property value delete'),
        'text': _('Are you sure you want to delete the property value'),
        'submit_name': _('Delete property value')
    }
    url_name = 'metadb:property_value_delete'
