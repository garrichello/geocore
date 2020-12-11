from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Collection, Dataset, Data, SpecificParameter
from django.utils.translation import get_language
from django.db.models import Q

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
