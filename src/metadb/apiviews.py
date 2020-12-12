from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.utils.translation import get_language
from django.db.models import Q


class AccumulationModeApiListView(APIView):
    """
    Returns accumulatiob modes
    """
    def get(self, request):

        items = AccumulationMode.objects.all()
        data = []
        for item in items:
            data.append(
                {
                    'id': item.id,
                    'name': item.name,
                }
            )

        return Response(data)


class CollectionApiListView(APIView):
    """
    Returns collections
    """
    def get(self, request):
        language = get_language()

        collections = Collection.objects.all()
        collection_data = []
        for collection in collections:
            collection_data.append(
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

        return Response(collection_data)


class DataApiListView(APIView):
    """
    Returns datasets
    """
    def get(self, request):
        language = get_language()
        qlang = Q(language__code=language)
        datas = Data.objects.all()
        data_data = [
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

        return Response(data_data)


class DataKindApiListView(APIView):
    """
    Returns data kinds
    """
    def get(self, request):

        items = DataKind.objects.all()
        data = []
        for item in items:
            data.append(
                {
                    'id': item.id,
                    'name': item.name,
                }
            )

        return Response(data)


class DatasetApiListView(APIView):
    """
    Returns datasets
    """
    def get(self, request):
        datasets = Dataset.objects.all()
        dataset_data = [
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

        return Response(dataset_data)


class FileApiListView(APIView):
    """
    Returns files patterns
    """
    def get(self, request):

        items = File.objects.all()
        data = []
        for item in items:
            data.append(
                {
                    'id': item.id,
                    'name_pattern': item.name_pattern,
                }
            )

        return Response(data)


class FileTypeApiListView(APIView):
    """
    Returns file types
    """
    def get(self, request):

        items = FileType.objects.all()
        data = []
        for item in items:
            data.append(
                {
                    'id': item.id,
                    'name': item.name,
                }
            )

        return Response(data)


class GuiElementApiListView(APIView):
    """
    Returns GUI elements
    """
    def get(self, request):

        language = get_language()
        items = GuiElement.objects.all()
        data = []
        for item in items:
            data.append(
                {
                    'id': item.id,
                    'name': item.name,
                    'caption': item.guielementi18n_set.filter(language__code=language).get().caption,
                }
            )

        return Response(data)


class LanguageApiListView(APIView):
    """
    Returns languages
    """
    def get(self, request):

        items = Language.objects.all()
        data = []
        for item in items:
            data.append(
                {
                    'id': item.id,
                    'name': item.name,
                    'code': item.code,
                }
            )

        return Response(data)


class LevelApiListView(APIView):
    """
    Returns levels
    """
    def get(self, request):

        language = get_language()
        items = Level.objects.all()
        data = []
        for item in items:
            data.append(
                {
                    'id': item.id,
                    'label': item.label,
                    'name': item.leveli18n_set.filter(language__code=language).get().name,
                }
            )

        return Response(data)


class LevelsGroupApiListView(APIView):
    """
    Returns levels groups
    """
    def get(self, request):

        qlang = Q(language__code=get_language())
        items = LevelsGroup.objects.all()
        data = []
        for item in items:
            data.append(
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

        return Response(data)


class LevelsVariableApiListView(APIView):
    """
    Returns levels variables
    """
    def get(self, request):

        items = Variable.objects.all()
        data = []
        for item in items:
            data.append(
                {
                    'id': item.id,
                    'name': item.name,
                }
            )

        return Response(data)


class OrganizationApiListView(APIView):
    """
    Returns organizations
    """
    def get(self, request):

        language = get_language()
        items = Organization.objects.all()
        data = []
        for item in items:
            data.append(
                {
                    'id': item.id,
                    'url': item.url,
                    'name': item.organizationi18n_set.filter(language__code=language).get().name,
                }
            )

        return Response(data)


class ParameterApiListView(APIView):
    """
    Returns meteorological parameters
    """
    def get(self, request):

        language = get_language()
        items = Parameter.objects.all()
        data = []
        for item in items:
            data.append(
                {
                    'id': item.id,
                    'is_visible': item.is_visible,
                    'accumulation_mode': item.accumulation_mode.name,
                    'name': item.parameteri18n_set.filter(language__code=language).get().name,
                }
            )

        return Response(data)


class PropertyApiListView(APIView):
    """
    Returns properties
    """
    def get(self, request):

        language = get_language()
        items = Property.objects.all()
        data = []
        for item in items:
            data.append(
                {
                    'id': item.id,
                    'label': item.label,
                    'gui_element_name': item.gui_element.name,
                    'gui_element_caption': item.gui_element.guielementi18n_set.filter(
                        language__code=language).get().caption,
                }
            )

        return Response(data)


class PropertyValueApiListView(APIView):
    """
    Returns properties values
    """
    def get(self, request):

        items = PropertyValue.objects.all()
        data = []
        for item in items:
            data.append(
                {
                    'id': item.id,
                    'label': item.label,
                }
            )

        return Response(data)


class ResolutionApiListView(APIView):
    """
    Returns horizontal resolutions
    """
    def get(self, request):

        items = Resolution.objects.all()
        data = []
        for item in items:
            data.append(
                {
                    'id': item.id,
                    'name': item.name,
                    'subpath1': item.subpath1,
                }
            )

        return Response(data)


class RootDirApiListView(APIView):
    """
    Returns root directories
    """
    def get(self, request):

        items = RootDir.objects.all()
        data = []
        for item in items:
            data.append(
                {
                    'id': item.id,
                    'name': item.name,
                }
            )

        return Response(data)


class ScenarioApiListView(APIView):
    """
    Returns scenarios
    """
    def get(self, request):

        items = Scenario.objects.all()
        data = []
        for item in items:
            data.append(
                {
                    'id': item.id,
                    'name': item.name,
                    'subpath0': item.subpath0,
                }
            )

        return Response(data)


class SpecificParameterApiListView(APIView):
    """
    Returns specific parameters
    """
    def get(self, request):
        language = get_language()

        specpars = SpecificParameter.objects.all()
        specpar_data = [
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

        return Response(specpar_data)


class TimeStepApiListView(APIView):
    """
    Returns time steps
    """
    def get(self, request):

        language = get_language()
        items = TimeStep.objects.all()
        data = []
        for item in items:
            data.append(
                {
                    'id': item.id,
                    'label': item.label,
                    'subpath2': item.subpath2,
                    'name': item.timestepi18n_set.filter(language__code=language).get().name,
                }
            )

        return Response(data)


class UnitApiListView(APIView):
    """
    Returns units
    """
    def get(self, request):

        language = get_language()
        items = Units.objects.all()
        data = []
        for item in items:
            data.append(
                {
                    'id': item.id,
                    'name': item.unitsi18n_set.filter(language__code=language).get().name,
                }
            )

        return Response(data)


class VariableApiListView(APIView):
    """
    Returns variables
    """
    def get(self, request):

        items = Variable.objects.all()
        data = []
        for item in items:
            data.append(
                {
                    'id': item.id,
                    'name': item.name,
                }
            )

        return Response(data)
