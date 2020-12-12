from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from .common_views import CommonCreateView, CommonUpdateView, CommonDeleteView

from .data_forms import DataForm

from .models import (Data, Dataset, SpecificParameter)


class DataMixin():
    form_class = DataForm
    model = Data

    def save_form(self, request, template_name, ctx):
        ''' Saves the form '''
        data = dict()
        form = ctx['forms'][0]
        if form.is_valid():
            data_obj = form.save(commit=False)  # Get data object
            # Find and attach dataset object to the data object
            dataset_obj = Dataset.objects.filter(
                collection=form.cleaned_data['collection'],
                resolution=form.cleaned_data['resolution'],
                scenario=form.cleaned_data['scenario']
            ).get()
            data_obj.dataset = dataset_obj
            # Find and attach specific parameter object to the data object
            sp_obj = SpecificParameter.objects.filter(
                parameter=form.cleaned_data['parameteri18n'].parameter,
                time_step=form.cleaned_data['time_stepi18n'].time_step,
                levels_group=form.cleaned_data['levels_group']
            ).get()
            data_obj.specific_parameter = sp_obj
            # Get and sttach units object to the data object
            data_obj.units = form.cleaned_data['unitsi18n'].units

            data_obj.save()  # Save object
            form.save_m2m()  # Save many-to-many relations
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

        data['html_form'] = render_to_string(template_name, ctx, request)
        return JsonResponse(data)


class DataCreateView(DataMixin, CommonCreateView):
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-data-form',
        'title': _("Create a new data"),
        'submit_name': _("Create data"),
        'script': 'metadb/data_form.js',
        'attributes': [
            {'name': 'dataset-resolutions-url',
             'value': reverse_lazy('metadb:form_load_dataset_resolutions')},
            {'name': 'dataset-scenario-url',
             'value': reverse_lazy('metadb:form_load_dataset_scenarios')},
            {'name': 'parameter-timesteps-url',
             'value': reverse_lazy('metadb:form_load_parameter_timesteps')},
            {'name': 'parameter-lvsgroups-url',
             'value': reverse_lazy('metadb:form_load_parameter_lvsgroups')},
            {'name': 'lvsgroup-lvsnames-url',
             'value': reverse_lazy('metadb:form_load_lvsgroup_lvsnames')},
            {'name': 'levels-variables-url',
             'value': reverse_lazy('metadb:form_load_lvsvars')},
            {'name': 'variables-url',
             'value': reverse_lazy('metadb:form_load_variables')},
            {'name': 'units-url',
             'value': reverse_lazy('metadb:form_load_units')},
            {'name': 'properties-url',
             'value': reverse_lazy('metadb:form_load_properties')},
            {'name': 'property-values-url',
             'value': reverse_lazy('metadb:form_load_propvals')},
            {'name': 'root-dirs-url',
             'value': reverse_lazy('metadb:form_load_rootdirs')},
            {'name': 'files-url',
             'value': reverse_lazy('metadb:form_load_files')},
        ]
    }
    action_url = 'metadb:data_create'


class DataUpdateView(DataMixin, CommonUpdateView):
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-data-form',
        'title': _("Update data"),
        'submit_name': _("Update data"),
        'script': 'metadb/data_form.js',
        'attributes': [
            {'name': 'dataset-resolutions-url',
             'value': reverse_lazy('metadb:form_load_dataset_resolutions')},
            {'name': 'dataset-scenario-url',
             'value': reverse_lazy('metadb:form_load_dataset_scenarios')},
            {'name': 'parameter-timesteps-url',
             'value': reverse_lazy('metadb:form_load_parameter_timesteps')},
            {'name': 'parameter-lvsgroups-url',
             'value': reverse_lazy('metadb:form_load_parameter_lvsgroups')},
            {'name': 'parameter-lvsnames-url',
             'value': reverse_lazy('metadb:form_load_lvsgroup_lvsnames')},
            {'name': 'levels-variables-url',
             'value': reverse_lazy('metadb:form_load_lvsvars')},
            {'name': 'variables-url',
             'value': reverse_lazy('metadb:form_load_variables')},
            {'name': 'units-url',
             'value': reverse_lazy('metadb:form_load_units')},
            {'name': 'properties-url',
             'value': reverse_lazy('metadb:form_load_properties')},
            {'name': 'property-values-url',
             'value': reverse_lazy('metadb:form_load_propvals')},
            {'name': 'root-dirs-url',
             'value': reverse_lazy('metadb:form_load_rootdirs')},
            {'name': 'files-url',
             'value': reverse_lazy('metadb:form_load_files')},
        ]
    }
    action_url = 'metadb:data_update'


class DataDeleteView(CommonDeleteView):
    form_class = DataForm
    model = Data
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-data-delete-form',
        'title': _('Confirm data delete'),
        'text': _('Are you sure you want to delete the data record'),
        'submit_name': _('Delete data')
    }
    action_url = 'metadb:data_delete'
