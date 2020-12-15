from django.utils.translation import gettext_lazy as _

from .common_views import CommonCreateView, CommonUpdateView, CommonDeleteView

from .units_forms import UnitsForm

from .models import Units, UnitsI18N


class UnitCreateView(CommonCreateView):
    form_class = UnitsForm
    model = Units
    modeli18n = UnitsI18N
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-unit-form',
        'title': _("Create a new measurement unit"),
        'submit_name': _("Create unit"),
    }
    action_url = 'metadb:unit_create'
    fk_field_name = 'units'


class UnitUpdateView(CommonUpdateView):
    form_class = UnitsForm
    model = Units
    modeli18n = UnitsI18N
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-unit-form',
        'title': _("Update measurement unit"),
        'submit_name': _("Update units"),
    }
    action_url = 'metadb:unit_update'
    fk_field_name = 'units'


class UnitDeleteView(CommonDeleteView):
    form_class = UnitsForm
    model = Units
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-unit-delete-form',
        'title': _('Confirm measurement unit delete'),
        'text': _('Are you sure you want to delete the unit'),
        'submit_name': _('Delete units')
    }
    action_url = 'metadb:unit_delete'
