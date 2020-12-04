from django.shortcuts import get_object_or_404, render
from django.utils.translation import get_language
from django.http import HttpResponse

from time import sleep

from .models import (Collection, OrganizationI18N, Resolution, Scenario, 
                     DataKind, FileType, ParameterI18N, TimeStepI18N,
                     Variable, UnitsI18N, Property, PropertyValue,
                     RootDir, File, GuiElement)
from .data_forms import (get_resolutions, get_scenarios,
                         get_timesteps, get_levelsgroups, get_levels)


def load_organizations(request):
    template_name = 'metadb/hr/dropdown_list_options.html'
    sleep(0.1)  # Have to wait for DB to arrange things.
    organizations = OrganizationI18N.objects.filter(
        language__code=get_language()
    ).order_by('name').all()
    ctx = {'data': organizations}
    return render(request, template_name, ctx)


def load_collections(request):
    template_name = 'metadb/hr/dropdown_list_options.html'
    sleep(0.1)  # Have to wait for DB to arrange things.
    collections = Collection.objects.order_by('label').all()
    ctx = {'data': collections}
    return render(request, template_name, ctx)


def load_resolutions(request):
    template_name = 'metadb/hr/dropdown_list_options.html'
    sleep(0.1)  # Have to wait for DB to arrange things.
    resolutions = Resolution.objects.order_by('name').all()
    ctx = {'data': resolutions}
    return render(request, template_name, ctx)


def load_scenarios(request):
    template_name = 'metadb/hr/dropdown_list_options.html'
    sleep(0.1)  # Have to wait for DB to arrange things.
    scenarios = Scenario.objects.order_by('name').all()
    ctx = {'data': scenarios}
    return render(request, template_name, ctx)


def load_datakinds(request):
    template_name = 'metadb/hr/dropdown_list_options.html'
    sleep(0.1)  # Have to wait for DB to arrange things.
    datakinds = DataKind.objects.order_by('name').all()
    ctx = {'data': datakinds}
    return render(request, template_name, ctx)


def load_filetypes(request):
    template_name = 'metadb/hr/dropdown_list_options.html'
    sleep(0.1)  # Have to wait for DB to arrange things.
    filetypes = FileType.objects.order_by('name').all()
    ctx = {'data': filetypes}
    return render(request, template_name, ctx)

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

def load_lvsvars(request):
    template_name = 'metadb/hr/dropdown_list_options.html'
    sleep(0.1)  # Have to wait for DB to arrange things.
    data = Variable.objects.order_by('name').all()
    ctx = {'data': data}
    return render(request, template_name, ctx)


def load_variables(request):
    template_name = 'metadb/hr/dropdown_list_options.html'
    sleep(0.1)  # Have to wait for DB to arrange things.
    data = Variable.objects.order_by('name').all()
    ctx = {'data': data}
    return render(request, template_name, ctx)

def load_units(request):
    template_name = 'metadb/hr/dropdown_list_options.html'
    sleep(0.1)  # Have to wait for DB to arrange things.
    data = UnitsI18N.objects.filter(
        language__code=get_language()).order_by('name').all()
    ctx = {'data': data}
    return render(request, template_name, ctx)

def load_properties(request):
    template_name = 'metadb/hr/dropdown_list_options.html'
    sleep(0.1)  # Have to wait for DB to arrange things.
    data = Property.objects.order_by('label').all()
    ctx = {'data': data}
    return render(request, template_name, ctx)

def load_propvals(request):
    template_name = 'metadb/hr/dropdown_list_options.html'
    sleep(0.1)  # Have to wait for DB to arrange things.
    data = PropertyValue.objects.order_by('label').all()
    ctx = {'data': data}
    return render(request, template_name, ctx)

def load_rootdirs(request):
    template_name = 'metadb/hr/dropdown_list_options.html'
    sleep(0.1)  # Have to wait for DB to arrange things.
    data = RootDir.objects.order_by('name').all()
    ctx = {'data': data}
    return render(request, template_name, ctx)

def load_files(request):
    template_name = 'metadb/hr/dropdown_list_options.html'
    sleep(0.1)  # Have to wait for DB to arrange things.
    data = File.objects.order_by('name_pattern').all()
    ctx = {'data': data}
    return render(request, template_name, ctx)

def load_guielements(request):
    template_name = 'metadb/hr/dropdown_list_options.html'
    sleep(0.1)  # Have to wait for DB to arrange things.
    data = GuiElement.objects.order_by('name').all()
    ctx = {'data': data}
    return render(request, template_name, ctx)
