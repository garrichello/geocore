from .simple_views import CommonCreateView, CommonUpdateView, CommonDeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from .dataset_forms import DatasetForm

from .models import Dataset


class DatasetCreateView(CommonCreateView):
    form_class = DatasetForm
    model = Dataset
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-dataset-form',
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


class DatasetUpdateView(CommonUpdateView):
    form_class = DatasetForm
    model = Dataset
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-dataset-form',
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

class DatasetDeleteView(CommonDeleteView):
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
