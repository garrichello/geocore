from .simple_views import SimpleCreateView, SimpleUpdateView, SimpleDeleteView
from django.utils.translation import gettext_lazy as _

from .dataset_forms import DatasetForm

from .models import Dataset


class DatasetCreateView(SimpleCreateView):
    form_class = DatasetForm
    model = Dataset
    template_name = 'metadb/includes/dataset_form.html'
    ctx = {
        'form_class': 'js-dataset-create-form',
        'title': _("Create a new dataset"),
        'submit_name': _("Create dataset"),
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
    }
    url_name = 'metadb:dataset_update'

class DatasetDeleteView(SimpleDeleteView):
    form_class = DatasetForm
    model = Dataset
    template_name = 'metadb/includes/simple_delete_form.html'
    ctx = {
        'form_class': 'js-dataset-delete-form',
        'title': _('Confirm dataset delete'),
        'text': _('Are you sure you want to delete the dataset'),
        'submit_name': _('Delete dataset')
    }
    url_name = 'metadb:dataset_delete'
