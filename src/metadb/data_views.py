from django.views import View
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.utils.translation import get_language
from django.shortcuts import get_object_or_404, render

from .data_forms import (DataForm, get_resolutions, get_scenarios,
                         get_timesteps, get_levelsgroups, get_levels)

from .models import (Data, Dataset, LevelI18N, LevelsGroup, ParameterI18N, Resolution,
                     Scenario, SpecificParameter, TimeStepI18N, UnitsI18N)


def load_dataset_resolutions(request):
    ''' Get a list of resolutions for a given collection '''
    template_name = 'metadb/hr/dropdown_list_options.html'
    collection_id = request.GET.get('collectionId')
    resolutions = {}
    if collection_id:
        resolutions = get_resolutions(collection_id)
    ctx = {'data': resolutions}
    return render(request, template_name, ctx)

def load_dataset_scenarios(request):
    ''' Get a list of scenarios for a given collection and a resolution '''
    template_name = 'metadb/hr/dropdown_list_options.html'
    collection_id = request.GET.get('collectionId')
    resolution_id = request.GET.get('resolutionId')
    scenarios = {}
    if collection_id and resolution_id:
        scenarios = get_scenarios(collection_id, resolution_id)
    ctx = {'data': scenarios}
    return render(request, template_name, ctx)

def load_parameter_timesteps(request):
    ''' Get a list of time steps for a given parameter '''
    template_name = 'metadb/hr/dropdown_list_options.html'
    parameteri18n_id = request.GET.get('parameteri18nId')
    timesteps = {}
    if parameteri18n_id:
        parameter_id = ParameterI18N.objects.get(pk=parameteri18n_id).parameter_id
        timesteps = get_timesteps(parameter_id)
    ctx = {'data': timesteps}
    return render(request, template_name, ctx)

def load_parameter_lvsgroups(request):
    ''' Get a list of levels groups for a given parameter and a time step '''
    template_name = 'metadb/hr/dropdown_list_options.html'
    parameteri18n_id = request.GET.get('parameteri18nId')
    timestepi18n_id = request.GET.get('timestepi18nId')
    lvsgroups = {}
    if parameteri18n_id and timestepi18n_id:
        parameter_id = ParameterI18N.objects.get(pk=parameteri18n_id).parameter_id
        time_step_id = TimeStepI18N.objects.get(pk=timestepi18n_id).time_step_id
        lvsgroups = get_levelsgroups(parameter_id, time_step_id)
    ctx = {'data': lvsgroups}
    return render(request, template_name, ctx)

def load_parameter_lvsnames(request):
    ''' Get a list of levels in a given levels group '''
    lvsgroup_id = request.GET.get('lvsgroupId')
    levels = ''
    if lvsgroup_id:
        levels = get_levels(lvsgroup_id)
    return HttpResponse(levels)


class DataBaseView(View):
    form_class = DataForm
    model = Data

    def save_form(self, request, form, template_name):
        ''' Saves the form '''
        data = dict()
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

        ctx = {'form': form}
        data['html_form'] = render_to_string(template_name, ctx, request)
        return JsonResponse(data)


class DataCreateView(DataBaseView):
    template_name = 'metadb/includes/data_create_form.html'

    def get(self, request):
        form = self.form_class()

        ctx = {'form': form, 'form_class': 'js-data-create-form'}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request):
        form = self.form_class(request.POST)
        
        return self.save_form(request, form, self.template_name)


class DataUpdateView(DataBaseView):
    template_name = 'metadb/includes/data_update_form.html'

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(instance=obj)

        ctx = {'form': form, 'form_class': 'js-data-update-form'}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(request.POST, instance=obj)
        return self.save_form(request, form, self.template_name)


class DataDeleteView(DataBaseView):
    template_name = 'metadb/includes/data_delete_form.html'

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)

        ctx = {'data': obj}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        obj.delete()
        return JsonResponse({'html_form': None, 'form_is_valid': True})
