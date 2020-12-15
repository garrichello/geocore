from django.utils.translation import gettext_lazy as _

from .common_views import CommonCreateView, CommonUpdateView, CommonDeleteView

from .timestep_forms import TimeStepForm

from .models import TimeStep, TimeStepI18N


class TimeStepCreateView(CommonCreateView):
    form_class = TimeStepForm
    model = TimeStep
    modeli18n = TimeStepI18N
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-timestep-form',
        'title': _("Create a new time step"),
        'submit_name': _("Create time step"),
    }
    action_url = 'metadb:time_step_create'
    fk_field_name = 'time_step'


class TimeStepUpdateView(CommonUpdateView):
    form_class = TimeStepForm
    model = TimeStep
    modeli18n = TimeStepI18N
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-timestep-form',
        'title': _("Update time step"),
        'submit_name': _("Update time step"),
    }
    action_url = 'metadb:time_step_update'
    fk_field_name = 'time_step'


class TimeStepDeleteView(CommonDeleteView):
    form_class = TimeStepForm
    model = TimeStep
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-timestep-delete-form',
        'title': _('Confirm time step delete'),
        'text': _('Are you sure you want to delete the time step'),
        'submit_name': _('Delete time step')
    }
    action_url = 'metadb:time_step_delete'
