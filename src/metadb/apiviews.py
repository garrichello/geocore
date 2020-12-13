from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import get_language, gettext_lazy as _
from django.db.models import Q

from .models import *


class AccumulationModeApiListView(APIView):
    """
    Returns accumulatiob modes
    """
    def get(self, request):

        items = AccumulationMode.objects.all()
        data = {}
        data['data'] = [
            { 'id': item.id,
              'name': item.name
            } for item in items
        ]
        data['headers'] = [
            _('Id'),
            _('Name'),
        ]

        return Response(data)


class CollectionApiListView(APIView):
    """
    Returns collections
    """
    def get(self, request):
        language = get_language()

        collections = Collection.objects.all()
        collection_data = {'data': []}
        for collection in collections:
            collection_data['data'].append(
                {
                    'id': collection.id,
                    'label': collection.label,
                    'name': collection.collectioni18n_set.filter(language__code=language).get().name,
                    'description': collection.collectioni18n_set.filter(language__code=language).get().description,
                    'organization': collection.organization.organizationi18n_set.filter(language__code=language).get().name,
                    'organization_url': collection.organization.url,
                    'url': collection.url,
                }
            )
        collection_data['headers'] = [
            ('head_none', 'Id'),
            ('head_select', _('Collection label')),
            ('head_select', _('Collection name')),
            ('head_text', _('Collection description')),
            ('head_select', _('Organization')),
            ('head_text', _('Organization URL')),
            ('head_text', _('Collection URL'))
        ]

        return Response(collection_data)


class DataApiListView(APIView):
    """
    Returns datasets
    """
    def get(self, request):
        language = get_language()
        qlang = Q(language__code=language)
        datas = Data.objects.all()
        data_data = {}
        data_data['data'] = [
            {
                'id': data.id,
                'is_visible': data.specific_parameter.parameter.is_visible,
                'collection_label': data.dataset.collection.label,
                'scenario_name': data.dataset.scenario.name,
                'resolution_name': data.dataset.resolution.name,
                'parameter_name': data.specific_parameter.parameter.parameteri18n_set.filter(qlang).get().name,
                'time_step': data.specific_parameter.time_step.timestepi18n_set.filter(qlang).get().name,
                'variable_name': data.variable.name,
                'units_name': data.units.unitsi18n_set.filter(qlang).get().name,
                'levels': '; '.join(
                    sorted([ level.leveli18n_set.filter(qlang).get().name
                    for level in data.specific_parameter.levels_group.level.all() ])
                ),
                'levels_group': '{} [{}]'.format(
                    data.specific_parameter.levels_group.description,
                    data.specific_parameter.levels_group.units.unitsi18n_set.filter(qlang).get().name
                ),
                'levels_variable':
                    data.levels_variable.name if data.levels_variable else None,
                'property_label': data.property.label,
                'property_value': data.property_value.label,
                'root_dir': data.root_dir.name,
                'subpath0': data.dataset.scenario.subpath0,
                'subpath1': data.dataset.resolution.subpath1,
                'subpath2': data.specific_parameter.time_step.subpath2,
                'file_pattern': data.file.name_pattern,
                'scale': data.scale,
                'offset': data.offset,
            }
            for data in datas
        ]
        data_data['headers'] = [
            ('head_none', 'Id'),
            ('head_none', _('Visible')),
            ('head_select', _('Collection label')),
            ('head_select', _('Resolution')),
            ('head_select', _('Scenario')),
            ('head_select', _('Parameter')),
            ('head_select', _('Time step')),
            ('head_text', _('Levels group')),
            ('head_text', _('Levels names')),
            ('head_none', _('Levels variable')),
            ('head_select', _('Variable name')),
            ('head_select', _('Units')),
            ('head_none', _('Propery label')),
            ('head_none', _('Property value')),
            ('head_text', _('Root directory')),
            ('head_text', _('Scenario subpath')),
            ('head_text', _('Resolution subpath')),
            ('head_text', _('Time step subpath')),
            ('head_none', _('File name pattern')),
            ('head_none', _('Scale')),
            ('head_none', _('Offset')),
        ]

        return Response(data_data)


class DataKindApiListView(APIView):
    """
    Returns data kinds
    """
    def get(self, request):

        items = DataKind.objects.all()
        data = {'data': []}
        for item in items:
            data['data'].append(
                {
                    'id': item.id,
                    'name': item.name,
                }
            )
        data['headers'] = [
            _('Id'), 
            _('Name'),
        ]

        return Response(data)


class DatasetApiListView(APIView):
    """
    Returns datasets
    """
    def get(self, request):
        datasets = Dataset.objects.all()
        dataset_data = {}
        dataset_data['data'] = [
            {
                'id': dataset.id,
                'is_visible': dataset.is_visible,
                'collection_label': dataset.collection.label,
                'scenario_name': dataset.scenario.name,
                'resolution_name': dataset.resolution.name,
                'data_kind_name': dataset.data_kind.name,
                'file_type_name': dataset.file_type.name,
                'time_start': dataset.time_start,
                'time_end': dataset.time_end,
                'description': dataset.description,
            }
            for dataset in datasets
        ]
        dataset_data['headers'] = [
            ('head_none', 'Id'),
            ('head_none', _('Visible')),
            ('head_select', _('Collection label')),
            ('head_select', _('Resolution')),
            ('head_select', _('Scenario')),
            ('head_select', _('Data kind')),
            ('head_select', _('File type')),
            ('head_none', _('Time start')),
            ('head_none', _('Time end')),
            ('head_text', _('Dataset description')),
        ]

        return Response(dataset_data)


class FileApiListView(APIView):
    """
    Returns files patterns
    """
    def get(self, request):

        items = File.objects.all()
        data = {'data': []}
        for item in items:
            data['data'].append(
                {
                    'id': item.id,
                    'name_pattern': item.name_pattern,
                }
            )
        data['headers'] = [
            _('Id'),
            _('File name pattern'),
        ]

        return Response(data)


class FileTypeApiListView(APIView):
    """
    Returns file types
    """
    def get(self, request):

        items = FileType.objects.all()
        data = {'data': []}
        for item in items:
            data['data'].append(
                {
                    'id': item.id,
                    'name': item.name,
                }
            )
        data['headers'] = [
            _('Id'), 
            _('Name'),
        ]

        return Response(data)


class GuiElementApiListView(APIView):
    """
    Returns GUI elements
    """
    def get(self, request):

        language = get_language()
        items = GuiElement.objects.all()
        data = {'data': []}
        for item in items:
            data['data'].append(
                {
                    'id': item.id,
                    'name': item.name,
                    'caption': item.guielementi18n_set.filter(language__code=language).get().caption,
                }
            )
        data['headers'] = [
            _('Id'), 
            _('Name'),
            _('Caption'),
        ]

        return Response(data)


class LanguageApiListView(APIView):
    """
    Returns languages
    """
    def get(self, request):

        items = Language.objects.all()
        data = {'data': []}
        for item in items:
            data['data'].append(
                {
                    'id': item.id,
                    'name': item.name,
                    'code': item.code,
                }
            )
        data['headers'] = [
            _('Id'),
            _('Name'),
            _('Code'),
        ]

        return Response(data)


class LevelApiListView(APIView):
    """
    Returns levels
    """
    def get(self, request):

        language = get_language()
        items = Level.objects.all()
        data = {'data': []}
        for item in items:
            data['data'].append(
                {
                    'id': item.id,
                    'label': item.label,
                    'name': item.leveli18n_set.filter(language__code=language).get().name,
                }
            )
        data['headers'] = [
            _('Id'),
            _('Label'),
            _('Name'),
        ]

        return Response(data)


class LevelsGroupApiListView(APIView):
    """
    Returns levels groups
    """
    def get(self, request):

        qlang = Q(language__code=get_language())
        items = LevelsGroup.objects.all()
        data = {'data': []}
        for item in items:
            data['data'].append(
                {
                    'id': item.id,
                    'description': item.description,
                    'unit': item.units.unitsi18n_set.filter(qlang).get().name,
                    'levels': '; '.join(
                        sorted([ 
                            level.leveli18n_set.filter(qlang).get().name
                            for level in item.level.all()
                        ])
                    ),
                }
            )
        data['headers'] = [
            _('Id'),
            _('Description'),
            _('Measurement unit'),
            _('Levels'),
        ]

        return Response(data)


class LevelsVariableApiListView(APIView):
    """
    Returns levels variables
    """
    def get(self, request):

        items = Variable.objects.all()
        data = {'data': []}
        for item in items:
            data['data'].append(
                {
                    'id': item.id,
                    'name': item.name,
                }
            )
        data['headers'] = [
            _('Id'),
            _('Name'),
        ]

        return Response(data)


class OrganizationApiListView(APIView):
    """
    Returns organizations
    """
    def get(self, request):

        language = get_language()
        items = Organization.objects.all()
        data = {'data': []}
        for item in items:
            data['data'].append(
                {
                    'id': item.id,
                    'url': item.url,
                    'name': item.organizationi18n_set.filter(language__code=language).get().name,
                }
            )
        data['headers'] = [
            _('Id'),
            _('URL'),
            _('Name'),
        ]

        return Response(data)


class ParameterApiListView(APIView):
    """
    Returns meteorological parameters
    """
    def get(self, request):

        language = get_language()
        items = Parameter.objects.all()
        data = {'data': []}
        for item in items:
            data['data'].append(
                {
                    'id': item.id,
                    'is_visible': item.is_visible,
                    'accumulation_mode': item.accumulation_mode.name,
                    'name': item.parameteri18n_set.filter(language__code=language).get().name,
                }
            )
        data['headers'] = [
            _('Id'),
            _('Is visible'),
            _('Accumulation mode'),
            _('Name'),
        ]

        return Response(data)


class PropertyApiListView(APIView):
    """
    Returns properties
    """
    def get(self, request):

        language = get_language()
        items = Property.objects.all()
        data = {'data': []}
        for item in items:
            data['data'].append(
                {
                    'id': item.id,
                    'label': item.label,
                    'gui_element_name': item.gui_element.name,
                    'gui_element_caption': item.gui_element.guielementi18n_set.filter(
                        language__code=language).get().caption,
                }
            )
        data['headers'] = [
            _('Id'),
            _('Label'),
            _('GUI element name'),
            _('GUI element caption'),
        ]

        return Response(data)


class PropertyValueApiListView(APIView):
    """
    Returns properties values
    """
    def get(self, request):

        items = PropertyValue.objects.all()
        data = {'data': []}
        for item in items:
            data['data'].append(
                {
                    'id': item.id,
                    'label': item.label,
                }
            )
        data['headers'] = [
            _('Id'),
            _('Label'),
        ]

        return Response(data)


class ResolutionApiListView(APIView):
    """
    Returns horizontal resolutions
    """
    def get(self, request):

        items = Resolution.objects.all()
        data = {'data': []}
        for item in items:
            data['data'].append(
                {
                    'id': item.id,
                    'name': item.name,
                    'subpath1': item.subpath1,
                }
            )
        data['headers'] = [
            _('Id'),
            _('Name'),
            _('Subpath'),
        ]

        return Response(data)


class RootDirApiListView(APIView):
    """
    Returns root directories
    """
    def get(self, request):

        items = RootDir.objects.all()
        data = {'data': []}
        for item in items:
            data['data'].append(
                {
                    'id': item.id,
                    'name': item.name,
                }
            )
        data['headers'] = [
            _('Id'),
            _('Name'),
        ]

        return Response(data)


class ScenarioApiListView(APIView):
    """
    Returns scenarios
    """
    def get(self, request):

        items = Scenario.objects.all()
        data = {'data': []}
        for item in items:
            data['data'].append(
                {
                    'id': item.id,
                    'name': item.name,
                    'subpath0': item.subpath0,
                }
            )
        data['headers'] = [
            _('Id'),
            _('Name'),
            _('Subpath'),
        ]

        return Response(data)


class SpecificParameterApiListView(APIView):
    """
    Returns specific parameters
    """
    def get(self, request):
        language = get_language()

        specpars = SpecificParameter.objects.all()
        specpar_data = {}
        specpar_data['data'] = [
            {
                'id': specpar.id,
                'is_visible': specpar.parameter.is_visible,
                'parameter_name': specpar.parameter.parameteri18n_set.filter(
                    language__code=language).get().name,
                'acc_mode_name': specpar.parameter.accumulation_mode.name,
                'time_step_name': specpar.time_step.timestepi18n_set.filter(
                    language__code='en').get().name,
                'time_step_label': specpar.time_step.label,
                'time_step_subpath': specpar.time_step.subpath2,
                'levels_group': '{} [{}]'.format(
                    specpar.levels_group.description,
                    specpar.levels_group.units.unitsi18n_set.filter(
                        language__code=language).get().name
                ),
                'levels_group_desc': specpar.levels_group.description,
                'levels': '; '.join(
                    sorted([ level.leveli18n_set.filter(language__code=language).get().name
                        for level in specpar.levels_group.level.all() ])
                    ),
            }
            for specpar in specpars
        ]
        specpar_data['headers'] = [
            ('head_none', 'Id'),
            ('head_none', _('Visible')),
            ('head_select', _('Parameter')),
            ('head_select', _('Accumulation mode')),
            ('head_select', _('Time step')),
            ('head_none', _('Time step label')),
            ('head_none', _('Time step subpath')),
            ('head_select', _('Levels group')),
            ('head_text', _('Levels group description')),
            ('head_text', _('Levels names')),
        ]

        return Response(specpar_data)


class TimeStepApiListView(APIView):
    """
    Returns time steps
    """
    def get(self, request):

        language = get_language()
        items = TimeStep.objects.all()
        data = {'data': []}
        for item in items:
            data['data'].append(
                {
                    'id': item.id,
                    'label': item.label,
                    'subpath2': item.subpath2,
                    'name': item.timestepi18n_set.filter(language__code=language).get().name,
                }
            )
        data['headers'] = [
            _('Id'), 
            _('Label'),
            _('Subpath'),
            _('Name'),
        ]

        return Response(data)


class UnitApiListView(APIView):
    """
    Returns units
    """
    def get(self, request):

        language = get_language()
        items = Units.objects.all()
        data = {'data': []}
        for item in items:
            data['data'].append(
                {
                    'id': item.id,
                    'name': item.unitsi18n_set.filter(language__code=language).get().name,
                }
            )
        data['headers'] = [
            _('Id'),
            _('Name'),
        ]

        return Response(data)


class VariableApiListView(APIView):
    """
    Returns variables
    """
    def get(self, request):

        items = Variable.objects.all()
        data = {'data': []}
        for item in items:
            data['data'].append(
                {
                    'id': item.id,
                    'name': item.name,
                }
            )
        data['headers'] = [
            _('Id'), 
            _('Name'),
        ]

        return Response(data)
