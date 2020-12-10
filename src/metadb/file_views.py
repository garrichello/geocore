from .simple_views import CommonCreateView, CommonUpdateView, CommonDeleteView
from django.utils.translation import gettext_lazy as _

from .simple_forms import FileForm

from .models import File


class FileCreateView(CommonCreateView):
    form_class = FileForm
    model = File
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-file-form',
        'title': _("Create a new file"),
        'submit_name': _("Create file"),
    }
    url_name = 'metadb:file_create'


class FileUpdateView(CommonUpdateView):
    form_class = FileForm
    model = File
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-file-form',
        'title': _("Update file"),
        'submit_name': _("Update file"),
    }
    url_name = 'metadb:file_update'

class FileDeleteView(CommonDeleteView):
    form_class = FileForm
    model = File
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-file-delete-form',
        'title': _('Confirm file delete'),
        'text': _('Are you sure you want to delete the file'),
        'submit_name': _('Delete file')
    }
    url_name = 'metadb:file_delete'
