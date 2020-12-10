from .simple_views import CommonCreateView, CommonUpdateView, CommonDeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.http import JsonResponse

from .specpar_forms import SpecificParameterForm

from .models import SpecificParameter


class SpecificParameterMixin():
    form_class = SpecificParameterForm
    model = SpecificParameter
    template_name = 'metadb/includes/simple_form.html'

    def save_form(self, request, template_name, ctx):
        ''' Saves the form '''
        data = dict()
        form = ctx['forms'][0]
        if form.is_valid():
            sp_obj = form.save(commit=False)  # Get data object
            sp_obj.parameter = form.cleaned_data['parameteri18n'].parameter
            sp_obj.time_step = form.cleaned_data['time_stepi18n'].time_step
            sp_obj.levels_group = form.cleaned_data['lvs_group']
            sp_obj.save()  # Save object
            form.save_m2m()  # Save many-to-many relations
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

        data['html_form'] = render_to_string(template_name, ctx, request)
        return JsonResponse(data)


class SpecificParameterCreateView(SpecificParameterMixin, CommonCreateView):
    ctx = {
        'form_class': 'js-specpar-form',
        'title': _("Create a new specific parameter"),
        'submit_name': _("Create specific parameter"),
        'script': 'metadb/specpar_form.js',
        'attributes': [
            {'name': 'parameter-url',
             'value': reverse_lazy('metadb:form_load_parameters')},
            {'name': 'time-step-url',
             'value': reverse_lazy('metadb:form_load_timesteps')},
            {'name': 'levels-group-url',
             'value': reverse_lazy('metadb:form_load_lvsgroups')},
            {'name': 'lvsgroup-lvsnames-url',
             'value': reverse_lazy('metadb:sp_form_load_lvsgroup_lvsnames')},
        ]
    }
    url_name = 'metadb:specpar_create'

    def post(self, request):
        form = self.form_class(request.POST)
        self.ctx['forms'] = [form]
        return self.save_form(request, self.template_name, self.ctx)


class SpecificParameterUpdateView(SpecificParameterMixin, CommonUpdateView):
    ctx = {
        'form_class': 'js-specpar-update-form',
        'title': _("Update specific parameter"),
        'submit_name': _("Update specific parameter"),
        'script': 'metadb/specpar_form.js',
        'attributes': [
            {'name': 'parameter-url',
             'value': reverse_lazy('metadb:form_load_parameters')},
            {'name': 'time-step-url',
             'value': reverse_lazy('metadb:form_load_timesteps')},
            {'name': 'levels-group-url',
             'value': reverse_lazy('metadb:form_load_lvsgroups')},
            {'name': 'lvsgroup-lvsnames-url',
             'value': reverse_lazy('metadb:sp_form_load_lvsgroup_lvsnames')},
        ]
    }
    url_name = 'metadb:specpar_update'

class SpecificParameterDeleteView(CommonDeleteView):
    form_class = SpecificParameterForm
    model = SpecificParameter
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-specpar-delete-form',
        'title': _('Confirm specific parameter delete'),
        'text': _('Are you sure you want to delete the specific parameter'),
        'submit_name': _('Delete specific parameter')
    }
    url_name = 'metadb:specpar_delete'
