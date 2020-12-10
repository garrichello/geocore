from .common_views import CommonCreateView, CommonUpdateView, CommonDeleteView
from django.utils.translation import gettext_lazy as _

from .simple_forms import FileTypeForm

from .models import FileType


class FileTypeCreateView(CommonCreateView):
    form_class = FileTypeForm
    model = FileType
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-filetype-form',
        'title': _("Create a new filetype"),
        'submit_name': _("Create filetype"),
    }
    url_name = 'metadb:filetype_create'


class FileTypeUpdateView(CommonUpdateView):
    form_class = FileTypeForm
    model = FileType
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-filetype-form',
        'title': _("Update filetype"),
        'submit_name': _("Update filetype"),
    }
    url_name = 'metadb:filetype_update'

class FileTypeDeleteView(CommonDeleteView):
    form_class = FileTypeForm
    model = FileType
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-filetype-delete-form',
        'title': _('Confirm file type delete'),
        'text': _('Are you sure you want to delete the file type'),
        'submit_name': _('Delete file type')
    }
    url_name = 'metadb:filetype_delete'
