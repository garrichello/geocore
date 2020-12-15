from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from .common_views import CommonCreateView, CommonUpdateView, CommonDeleteView

from .parameter_forms import ParameterForm

from .models import Parameter, ParameterI18N


class ParameterCreateView(CommonCreateView):
    form_class = ParameterForm
    model = Parameter
    modeli18n = ParameterI18N
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-parameter-form',
        'title': _("Create a new meteorological parameter"),
        'submit_name': _("Create parameter"),
        'script': 'metadb/parameter_form.js',
        'attributes': [
            {'name': 'accmodes-url',
             'value': reverse_lazy('metadb:form_load_accmodes')}
        ]
    }
    action_url = 'metadb:parameter_create'
    fk_field_name = 'parameter'

class ParameterUpdateView(CommonUpdateView):
    form_class = ParameterForm
    model = Parameter
    modeli18n = ParameterI18N
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-parameter-form',
        'title': _("Update meteorological parameter"),
        'submit_name': _("Update parameter"),
        'script': 'metadb/parameter_form.js',
        'attributes': [
            {'name': 'accmodes-url',
             'value': reverse_lazy('metadb:form_load_accmodes')}
        ]
    }
    action_url = 'metadb:parameter_update'
    fk_field_name = 'parameter'


class ParameterDeleteView(CommonDeleteView):
    form_class = ParameterForm
    model = Parameter
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-parameter-delete-form',
        'title': _('Confirm meteorological parameter delete'),
        'text': _('Are you sure you want to delete the parameter'),
        'submit_name': _('Delete parameter')
    }
    action_url = 'metadb:parameter_delete'
