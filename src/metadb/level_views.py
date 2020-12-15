from django.utils.translation import gettext_lazy as _

from .common_views import CommonCreateView, CommonUpdateView, CommonDeleteView

from .level_forms import LevelForm

from .models import Level, LevelI18N


class LevelCreateView(CommonCreateView):
    form_class = LevelForm
    model = Level
    modeli18n = LevelI18N
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-level-form',
        'title': _("Create a new level"),
        'submit_name': _("Create level"),
    }
    action_url = 'metadb:level_create'
    fk_field_name = 'level'


class LevelUpdateView(CommonUpdateView):
    form_class = LevelForm
    model = Level
    modeli18n = LevelI18N
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-level-form',
        'title': _("Update level"),
        'submit_name': _("Update level"),
    }
    action_url = 'metadb:level_update'
    fk_field_name = 'level'


class LevelDeleteView(CommonDeleteView):
    form_class = LevelForm
    model = Level
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-level-delete-form',
        'title': _('Confirm level delete'),
        'text': _('Are you sure you want to delete the level'),
        'submit_name': _('Delete level')
    }
    action_url = 'metadb:level_delete'
