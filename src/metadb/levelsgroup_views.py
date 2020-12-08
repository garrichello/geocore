from .simple_views import SimpleCreateView, SimpleUpdateView, SimpleDeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from .levelsgroup_form import LevelsGroupForm

from .models import LevelsGroup


class LevelsGroupCreateView(SimpleCreateView):
    form_class = LevelsGroupForm
    model = LevelsGroup
    template_name = 'metadb/includes/levelsgroup_form.html'
    ctx = {
        'form_class': 'js-levels-group-form',
        'title': _("Create a new levels group"),
        'submit_name': _("Create levels group"),
        'script': 'metadb/levelsgroup_form.js',
        'attributes': [
            {'name': 'units-url',
             'value': reverse_lazy('metadb:form_load_units')},
        ]
    }
    url_name = 'metadb:levels_group_create'


class LevelsGroupUpdateView(SimpleUpdateView):
    form_class = LevelsGroupForm
    model = LevelsGroup
    template_name = 'metadb/includes/levelsgroup_form.html'
    ctx = {
        'form_class': 'js-levels-group-form',
        'title': _("Update levels_group"),
        'submit_name': _("Update levels group"),
        'script': 'metadb/levelsgroup_form.js',
        'attributes': [
            {'name': 'units-url',
             'value': reverse_lazy('metadb:form_load_units')},
        ]
    }
    url_name = 'metadb:levels_group_update'

class LevelsGroupDeleteView(SimpleDeleteView):
    form_class = LevelsGroupForm
    model = LevelsGroup
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-levels-group-delete-form',
        'title': _('Confirm levels group delete'),
        'text': _('Are you sure you want to delete the levels group'),
        'submit_name': _('Delete levels group')
    }
    url_name = 'metadb:levels_group_delete'
