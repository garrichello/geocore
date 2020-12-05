from .simple_views import SimpleCreateView, SimpleUpdateView, SimpleDeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from .dataset_forms import DatasetForm

from .models import Dataset


class DatasetCreateView(SimpleCreateView):
    form_class = DatasetForm
    model = Dataset
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-dataset-create-form',
        'title': _("Create a new dataset"),
        'submit_name': _("Create dataset"),
        'script': 'metadb/dataset_form.js',
        'attributes': [
            {'name': 'collections-url', 
             'value': reverse_lazy('metadb:form_load_collections')},
            {'name': 'resolutions-url', 
             'value': reverse_lazy('metadb:form_load_resolutions')},
            {'name': 'scenarios-url', 
             'value': reverse_lazy('metadb:form_load_scenarios')},
            {'name': 'datakinds-url', 
             'value': reverse_lazy('metadb:form_load_datakinds')},
            {'name': 'filetypes-url', 
             'value': reverse_lazy('metadb:form_load_filetypes')},
        ]
    }
    url_name = 'metadb:dataset_create'


class DatasetUpdateView(SimpleUpdateView):
    form_class = DatasetForm
    model = Dataset
    template_name = 'metadb/includes/dataset_form.html'
    ctx = {
        'form_class': 'js-dataset-update-form',
        'title': _("Update dataset"),
        'submit_name': _("Update dataset"),
        'script': 'metadb/dataset_form.js',
        'attributes': [
            {'name': 'collections-url', 
             'value': reverse_lazy('metadb:form_load_collections')},
            {'name': 'resolutions-url', 
             'value': reverse_lazy('metadb:form_load_resolutions')},
            {'name': 'scenarios-url', 
             'value': reverse_lazy('metadb:form_load_scenarios')},
            {'name': 'datakinds-url', 
             'value': reverse_lazy('metadb:form_load_datakinds')},
            {'name': 'filetypes-url', 
             'value': reverse_lazy('metadb:form_load_filetypes')},
        ]
    }
    url_name = 'metadb:dataset_update'

class DatasetDeleteView(SimpleDeleteView):
    form_class = DatasetForm
    model = Dataset
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-dataset-delete-form',
        'title': _('Confirm dataset delete'),
        'text': _('Are you sure you want to delete the dataset'),
        'submit_name': _('Delete dataset')
    }
    url_name = 'metadb:dataset_delete'
