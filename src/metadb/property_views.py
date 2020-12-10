from .common_views import CommonCreateView, CommonUpdateView, CommonDeleteView
from django.utils.translation import gettext_lazy as _
from .simple_forms import PropertyForm
from django.urls import reverse_lazy

from .models import Property


class PropertyCreateView(CommonCreateView):
    form_class = PropertyForm
    model = Property
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-property-form',
        'title': _("Create a new property"),
        'submit_name': _("Create property"),
        'script': 'metadb/property_form.js',
        'attributes': [
            {'name': 'gui-element-url', 
             'value': reverse_lazy('metadb:form_load_guielements')},
        ],
    }
    url_name = 'metadb:property_create'


class PropertyUpdateView(CommonUpdateView):
    form_class = PropertyForm
    model = Property
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-property-form',
        'title': _("Update property"),
        'submit_name': _("Update property"),
        'script': 'metadb/property_form.js',
        'attributes': [
            {'name': 'gui-element-url', 
             'value': reverse_lazy('metadb:form_load_guielements')},
        ],
    }
    url_name = 'metadb:property_update'

class PropertyDeleteView(CommonDeleteView):
    form_class = PropertyForm
    model = Property
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-property-delete-form',
        'title': _('Confirm property delete'),
        'text': _('Are you sure you want to delete the property'),
        'submit_name': _('Delete property')
    }
    url_name = 'metadb:property_delete'
