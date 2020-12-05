from .simple_views import SimpleCreateView, SimpleUpdateView, SimpleDeleteView
from django.utils.translation import gettext_lazy as _

from .simple_forms import RootDirForm

from .models import RootDir


class RootDirCreateView(SimpleCreateView):
    form_class = RootDirForm
    model = RootDir
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-root-dir-create-form',
        'title': _("Create a new root directory"),
        'submit_name': _("Create root directory"),
    }
    url_name = 'metadb:root_dir_create'


class RootDirUpdateView(SimpleUpdateView):
    form_class = RootDirForm
    model = RootDir
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-root-dir-update-form',
        'title': _("Update root directory"),
        'submit_name': _("Update root directory"),
    }
    url_name = 'metadb:root_dir_update'

class RootDirDeleteView(SimpleDeleteView):
    form_class = RootDirForm
    model = RootDir
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-root-dir-delete-form',
        'title': _('Confirm root directory delete'),
        'text': _('Are you sure you want to delete the root directory'),
        'submit_name': _('Delete root directory')
    }
    url_name = 'metadb:root_dir_delete'
