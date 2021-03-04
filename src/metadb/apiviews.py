from rest_framework.response import Response
from rest_framework.renderers import *
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from django.utils.translation import get_language, gettext_lazy as _
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from collections import defaultdict
import json

from .models import *
from .serializers import *


class BaseViewSet(viewsets.ModelViewSet):
    """
    Abstract base class for all REST API viewsets
    """
    queryset = None
    serializer_class = None
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = ''
    action_url = ''

    table_headers = []

    ctx_create = {
        'form_class': '',
        'method': 'POST',
        'title': _(''),
        'submit_name': _(''),
        'script': '',
        'attributes': [],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'form_class': '',
        'method': 'PUT',
        'title': _(''),
        'submit_name': _(''),
        'script': '',
        'attributes': [],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'form_class': '',
        'method': 'DELETE',
        'title': _(''),
        'text': _(''),
        'submit_name': _(''),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    def list(self, request):
        http_action = request.META.get('HTTP_ACTION')
        serializer = self.get_serializer(self.get_queryset(), many=True)
        ctx = {'data': serializer.data}

        if http_action == 'options_list' or request.GET.get('format') == 'html':
            result = render(request, self.options_template_name, ctx)
        else:
            if isinstance(request.accepted_renderer, JSONRenderer):
                ctx['headers'] = self.table_headers
            result = Response(ctx)

        return result

    def retrieve(self, request, pk=None):
        http_action = request.META.get('HTTP_ACTION')
        if http_action == 'create':
            instance = None
        elif http_action == 'update' or http_action == 'delete' or pk is not None:
            instance = self.get_queryset().filter(pk=pk).first()
        else:
            raise MethodNotAllowed(http_action, detail='Unknown action')
        serializer = self.get_serializer(instance)

        if isinstance(request.accepted_renderer, BrowsableAPIRenderer) or http_action == 'json':
            response = Response({'data': serializer.data})
        else:
            if http_action == 'create':
                ctx = self.ctx_create
                ctx['action'] = reverse(self.list_url)
            elif http_action == 'update':
                ctx = self.ctx_update
                ctx['action'] = reverse(self.action_url, kwargs={'pk': pk})
            elif http_action == 'delete':
                ctx = self.ctx_delete
                ctx['label'] = getattr(instance, 'label', instance.pk)
                ctx['action'] = reverse(self.action_url, kwargs={'pk': pk})
            else:
                ctx = {'style': {'template_pack': 'rest_framework/vertical/'}}
            ctx['form'] = serializer
            html_form = render_to_string(self.template_name, ctx, request)
            response = JsonResponse({'html_form': html_form})

        return response

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        is_valid = serializer.is_valid()
        if is_valid:
            serializer.save()

        if isinstance(request.accepted_renderer, BrowsableAPIRenderer):
            response = Response({'data': serializer.data})
        else:
            self.ctx_create['form'] = serializer
            html_form = render_to_string(self.template_name, self.ctx_create, request)
            response = JsonResponse({'html_form': html_form, 'form_is_valid': is_valid})

        return response

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data, instance=instance)
        is_valid = serializer.is_valid()
        if is_valid:
            serializer.save()
        if isinstance(request.accepted_renderer, BrowsableAPIRenderer):
            response = Response({'data': serializer.data})
        else:
            self.ctx_update['form'] = serializer
            html_form = render_to_string(self.template_name, self.ctx_update, request)
            response = JsonResponse({'html_form': html_form, 'form_is_valid': is_valid})

        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return JsonResponse({'html_form': None, 'form_is_valid': True})

#==============================================================================================

class AccumulationModeViewSet(BaseViewSet):
    """
    Returns accumulation modes
    """
    queryset = AccumulationMode.objects.all().order_by('name')
    serializer_class = AccumulationModeSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:accumulationmode-list'
    action_url = 'metadb:accumulationmode-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Name'), 'field': 'name'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-accmode-form',
        'title': _("Create a new accumulation mode"),
        'submit_name': _("Create accumulation mode"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-accmode-form',
        'title': _("Update accumulation mode"),
        'submit_name': _("Update accumulation mode"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-accmode-delete-form',
        'title': _('Confirm accumulation mode delete'),
        'text': _('Are you sure you want to delete the accumulation mode'),
        'submit_name': _('Delete accumulation mode'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class CollectionViewSet(BaseViewSet):
    """
    Returns collections
    """
    queryset = Collection.objects.all().order_by('label')
    serializer_class = CollectionSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:collection-list'
    action_url = 'metadb:collection-detail'

    table_headers = [
        ('head_none', 'Id'),
        ('head_select', _('Collection label')),
        ('head_select', _('Collection name')),
        ('head_text', _('Collection description')),
        ('head_select', _('Organization')),
        ('head_text', _('Organization URL')),
        ('head_text', _('Collection URL'))
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-collection-form',
        'title': _("Create a new collection"),
        'submit_name': _("Create collection"),
        'script': 'metadb/collection_form.js',
        'attributes': [
            {'name': 'organizations-url',
             'value': reverse_lazy('metadb:organization-list')}
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-collection-form',
        'title': _("Update collection"),
        'submit_name': _("Update collection"),
        'script': 'metadb/collection_form.js',
        'attributes': [
            {'name': 'organizations-url',
             'value': reverse_lazy('metadb:organization-list')}
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-collection-delete-form',
        'title': _('Confirm collection delete'),
        'text': _('Are you sure you want to delete the collection'),
        'submit_name': _('Delete collection'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class ComputingModuleViewSet(BaseViewSet):
    """
    Returns computing modules
    """
    queryset = ComputingModule.objects.all().order_by('name')
    serializer_class = ComputingModuleSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:computingmodule-list'
    action_url = 'metadb:computingmodule-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Name'), 'field': 'name'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-computingmodule-form',
        'title': _("Create a new computing module"),
        'submit_name': _("Create computing module"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-computingmodule-form',
        'title': _("Update computing module"),
        'submit_name': _("Update computing module"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-computingmodule-delete-form',
        'title': _('Confirm computing module delete'),
        'text': _('Are you sure you want to delete the computing module'),
        'submit_name': _('Delete computing module'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class ConveyorViewSet(BaseViewSet):
    """
    Returns conveyors
    """
    queryset = Conveyor.objects.all()
    serializer_class = ConveyorSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    template_name = 'metadb/includes/conveyor_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:conveyor-list'
    action_url = 'metadb:conveyor-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Label'), 'field': 'label'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-conveyor-form',
        'title': _("Create a new conveyor"),
        'submit_name': _("Create conveyor"),
        'script': 'metadb/conveyor_form.js',
        'attributes': [
            {'name': 'vertices-url',
             'value': reverse_lazy('metadb:vertex-list')},
            {'name': 'datavariables-url',
             'value': reverse_lazy('metadb:datavariable-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-conveyor-form',
        'title': _("Update conveyor"),
        'submit_name': _("Update conveyor"),
        'script': 'metadb/conveyor_form.js',
        'attributes': [
            {'name': 'vertices-url',
             'value': reverse_lazy('metadb:vertex-list')},
            {'name': 'datavariables-url',
             'value': reverse_lazy('metadb:datavariable-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-conveyor-delete-form',
        'title': _('Confirm conveyor delete'),
        'text': _('Are you sure you want to delete the conveyor'),
        'submit_name': _('Delete conveyor'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    def sort_dict(self, in_dict: dict):
        out_dict = {}
        for key in sorted(in_dict.keys()):
            out_dict[key] = in_dict[key]
        return out_dict

    @action(methods=['GET'], detail=True)
    def retrieve_graph(self, request, pk=None):
        edges = Edge.objects.filter(conveyor__id=pk).all()
        vertices = defaultdict(dict)
        links = {}
        link_id = 0
        for edge in edges:
            vertices[edge.from_vertex]['downlinks'] = vertices[edge.from_vertex].get('downlinks', [])
            vertices[edge.from_vertex]['downlinks'].append({'output': edge.from_output, 'vertex': edge.to_vertex})
            vertices[edge.to_vertex]['uplinks'] = vertices[edge.to_vertex].get('uplinks', [])
            vertices[edge.to_vertex]['uplinks'].append({'input': edge.to_input, 'vertex': edge.from_vertex})
            links[str(link_id)] = {
                'fromOperator': f'vertex_{edge.from_vertex.id}',
                'fromConnector': f'output_{edge.from_output}',
                'fromSubConnector': 0,
                'toOperator': f'vertex_{edge.to_vertex.id}',
                'toConnector': f'input_{edge.to_input}',
                'toSubConnector': 0,
                'label': edge.data_variable.label,
                'datavariable_id': edge.data_variable.id,
            }
            link_id += 1
        operators = {}
        top = 10
        left = 10
        d_left = 100
        for vertex, data in vertices.items():
            op_key = f'vertex_{vertex.id}'
            coords = ConveyorHasVertex.objects.filter(conveyor__pk=pk, vertex=vertex).get()
            if coords.vertex_position_top is not None:
                top = coords.vertex_position_top
            if coords.vertex_position_left is not None:
                left = coords.vertex_position_left
            operators[op_key] = {
                'top': top,
                'left': left,
                'properties': {},
            }
            inputs = {}
            for uplink in data.get('uplinks', {}):
                input_key = f"input_{uplink['input']}"
                inputs[input_key] = {
                    'label': input_key if uplink['input'] != 0 else "options"
                }
            outputs = {}
            for downlink in data.get('downlinks', {}):
                output_key = f"output_{downlink['output']}"
                outputs[output_key] = {
                    'label': output_key if downlink['output'] != 0 else "options"
                }
            operators[op_key]['properties'] = {
                'title': vertex.computing_module.name,
                'inputs': inputs, #self.sort_dict(inputs),
                'outputs': outputs, #self.sort_dict(outputs),
                'condition_option': vertex.condition_option.label,
                'condition_value': vertex.condition_value.label,
            }
            left += d_left

        result = {'operators': operators, 'links': links}
        response = JsonResponse(result)
        return response

    @action(methods=['POST'], detail=False)
    def create_graph(self, request):

        data = json.loads(request.data['data'])

        conveyor_label = data['conveyorLabel']
        operators = data['operators']
        links = data['links']
        all_links_has_ids = all(['datavariable_id' in v for v in links.values()])

        form_is_valid = True
        if not conveyor_label or not operators or not links or not all_links_has_ids:
            form_is_valid = False
        else:
            # Create a new conveyor instance
            conveyor_serializer = self.get_serializer(data={'label': conveyor_label})
            if conveyor_serializer.is_valid():
                conveyor = conveyor_serializer.save()
                # Link conveyor to vertices
                for operator in operators.values():
                    chv = ConveyorHasVertex()
                    chv.conveyor = conveyor
                    chv.vertex_id = operator['properties']['vertex_id']
                    chv.vertex_position_top = operator['top']
                    chv.vertex_position_left = operator['left']
                    chv.save()
                # Add edges
                for link in links.values():
                    edge = Edge()
                    edge.conveyor = conveyor
                    edge.from_vertex_id = link['fromOperator'].split('_')[1]
                    edge.from_output = link['fromConnector'].split('_')[1]
                    edge.to_vertex_id = link['toOperator'].split('_')[1]
                    edge.to_input = link['toConnector'].split('_')[1]
                    edge.data_variable_id = link['datavariable_id']
                    edge.save()
            else:
                form_is_valid = False

        result = {'data': {'form_is_valid': form_is_valid}}
        response = JsonResponse(result)
        return response

    @action(methods=['PUT'], detail=True)
    def update_graph(self, request, pk=None):

        data = json.loads(request.data['data'])

        conveyor_label = data['conveyorLabel']
        operators = data['operators']
        links = data['links']
        all_links_has_ids = all(['datavariable_id' in v for v in links.values()])

        form_is_valid = True
        if not conveyor_label or not operators or not links or not all_links_has_ids:
            form_is_valid = False
        else:
            # Use an existing conveyor instance
            instance = self.get_object()
            conveyor_serializer = self.get_serializer(data={'label': conveyor_label}, instance=instance)
            if conveyor_serializer.is_valid():
                conveyor = conveyor_serializer.save()
                # Link conveyor to vertices
                for operator in operators.values():
                    chv = ConveyorHasVertex()
                    chv.conveyor = conveyor
                    chv.vertex_id = operator['properties']['vertex_id']
                    chv.vertex_position_top = operator['top']
                    chv.vertex_position_left = operator['left']
                    chv.save()
                # Add edges
                for link in links.values():
                    edge = Edge()
                    edge.conveyor = conveyor
                    edge.from_vertex_id = link['fromOperator'].split('_')[1]
                    edge.from_output = link['fromConnector'].split('_')[1]
                    edge.to_vertex_id = link['toOperator'].split('_')[1]
                    edge.to_input = link['toConnector'].split('_')[1]
                    edge.data_variable_id = link['datavariable_id']
                    edge.save()
            else:
                form_is_valid = False
            

        result = {'data': {'form_is_valid': form_is_valid}}
        response = JsonResponse(result)
        return response

class DataViewSet(BaseViewSet):
    """
    Returns data
    """
    queryset = Data.objects.all()
    serializer_class = DataSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:data-list'
    action_url = 'metadb:data-detail'

    table_headers = [
        ('head_none', 'Id'),
        ('head_none', _('Dataset visibility')),
        ('head_select', _('Collection label')),
        ('head_select', _('Resolution')),
        ('head_select', _('Scenario')),
        ('head_none', _('Parameter visibility')),
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

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-data-form',
        'title': _("Create a new data"),
        'submit_name': _("Create data"),
        'script': 'metadb/data_form.js',
        'attributes': [
            {'name': 'datasets-url',
             'value': reverse_lazy('metadb:dataset-list')},
            {'name': 'parameters-url',
             'value': reverse_lazy('metadb:parameter-list')},
            {'name': 'timesteps-url',
             'value': reverse_lazy('metadb:timestep-list')},
            {'name': 'levelsgroups-url',
             'value': reverse_lazy('metadb:levelsgroup-list')},
            {'name': 'levels-variables-url',
             'value': reverse_lazy('metadb:levelsvariable-list')},
            {'name': 'variables-url',
             'value': reverse_lazy('metadb:variable-list')},
            {'name': 'units-url',
             'value': reverse_lazy('metadb:units-list')},
            {'name': 'properties-url',
             'value': reverse_lazy('metadb:property-list')},
            {'name': 'property-values-url',
             'value': reverse_lazy('metadb:propertyvalue-list')},
            {'name': 'root-dirs-url',
             'value': reverse_lazy('metadb:rootdir-list')},
            {'name': 'files-url',
             'value': reverse_lazy('metadb:file-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-data-form',
        'title': _("Update data"),
        'submit_name': _("Update data"),
        'script': 'metadb/data_form.js',
        'attributes': [
            {'name': 'datasets-url',
             'value': reverse_lazy('metadb:dataset-list')},
            {'name': 'parameters-url',
             'value': reverse_lazy('metadb:parameter-list')},
            {'name': 'timesteps-url',
             'value': reverse_lazy('metadb:timestep-list')},
            {'name': 'levelsgroups-url',
             'value': reverse_lazy('metadb:levelsgroup-list')},
            {'name': 'levels-variables-url',
             'value': reverse_lazy('metadb:levelsvariable-list')},
            {'name': 'variables-url',
             'value': reverse_lazy('metadb:variable-list')},
            {'name': 'units-url',
             'value': reverse_lazy('metadb:units-list')},
            {'name': 'properties-url',
             'value': reverse_lazy('metadb:property-list')},
            {'name': 'property-values-url',
             'value': reverse_lazy('metadb:propertyvalue-list')},
            {'name': 'root-dirs-url',
             'value': reverse_lazy('metadb:rootdir-list')},
            {'name': 'files-url',
             'value': reverse_lazy('metadb:file-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-data-delete-form',
        'title': _('Confirm data delete'),
        'text': _('Are you sure you want to delete the data record'),
        'submit_name': _('Delete data'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class DataKindViewSet(BaseViewSet):
    """
    Returns data kinds
    """
    queryset = DataKind.objects.all().order_by('name')
    serializer_class = DataKindSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:datakind-list'
    action_url = 'metadb:datakind-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Name'), 'field': 'name'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-datakind-form',
        'title': _("Create a new datakind"),
        'submit_name': _("Create datakind"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-datakind-form',
        'title': _("Update datakind"),
        'submit_name': _("Update datakind"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-datakind-delete-form',
        'title': _('Confirm data kind delete'),
        'text': _('Are you sure you want to delete the data kind'),
        'submit_name': _('Delete data kind'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class DatasetViewSet(BaseViewSet):
    """
    Returns datasets
    """
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:dataset-list'
    action_url = 'metadb:dataset-detail'

    table_headers = [
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

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-dataset-form',
        'title': _("Create a new dataset"),
        'submit_name': _("Create dataset"),
        'script': 'metadb/dataset_form.js',
        'attributes': [
            {'name': 'collections-url',
             'value': reverse_lazy('metadb:collection-list')},
            {'name': 'resolutions-url',
             'value': reverse_lazy('metadb:resolution-list')},
            {'name': 'scenarios-url',
             'value': reverse_lazy('metadb:scenario-list')},
            {'name': 'datakinds-url',
             'value': reverse_lazy('metadb:datakind-list')},
            {'name': 'filetypes-url',
             'value': reverse_lazy('metadb:filetype-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-dataset-form',
        'title': _("Update dataset"),
        'submit_name': _("Update dataset"),
        'script': 'metadb/dataset_form.js',
        'attributes': [
            {'name': 'collections-url',
             'value': reverse_lazy('metadb:collection-list')},
            {'name': 'resolutions-url',
             'value': reverse_lazy('metadb:resolution-list')},
            {'name': 'scenarios-url',
             'value': reverse_lazy('metadb:scenario-list')},
            {'name': 'datakinds-url',
             'value': reverse_lazy('metadb:datakind-list')},
            {'name': 'filetypes-url',
             'value': reverse_lazy('metadb:filetype-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-dataset-delete-form',
        'title': _('Confirm dataset delete'),
        'text': _('Are you sure you want to delete the dataset'),
        'submit_name': _('Delete dataset'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class DataVariableViewSet(BaseViewSet):
    """
    Returns data variables
    """
    queryset = DataVariable.objects.all()
    serializer_class = DataVariableSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:datavariable-list'
    action_url = 'metadb:datavariable-detail'

    table_headers = [
        ('head_none', 'Id'),
        ('head_text', _('Data variable label')),
        ('head_select', _('Units')),
        ('head_text', _('Data variable description')),
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-datavariable-form',
        'title': _("Create a new data variable"),
        'submit_name': _("Create data variable"),
        'script': 'metadb/datavariable_form.js',
        'attributes': [
            {'name': 'units-url',
             'value': reverse_lazy('metadb:units-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-datavariable-form',
        'title': _("Update data variable"),
        'submit_name': _("Update data variable"),
        'script': 'metadb/datavariable_form.js',
        'attributes': [
            {'name': 'units-url',
             'value': reverse_lazy('metadb:units-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-datavariable-delete-form',
        'title': _('Confirm data variable delete'),
        'text': _('Are you sure you want to delete the data variable'),
        'submit_name': _('Delete data variable'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }
    def __init__(self, *args, **kwargs):
        self.queryset = self.queryset.order_by('label')

class EdgeViewSet(BaseViewSet):
    """
    Returns edges
    """
    queryset = Edge.objects.all()
    serializer_class = EdgeSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:edge-list'
    action_url = 'metadb:edge-detail'

    table_headers = [
        ('head_select', _('Conveyor id')),
        ('head_none', _('Edge id')),
        ('head_none', _('Source vertex id')),
        ('head_select', _('Source module')),
        ('head_select', _('Source condition option')),
        ('head_select', _('Source condition value')),
        ('head_text', _('Source module output')),
        ('head_none', _('Target vertex id')),
        ('head_select', _('Target module')),
        ('head_select', _('Target condition option')),
        ('head_select', _('Target condition value')),
        ('head_text', _('Target module input')),
        ('head_select', _('Data label')),
        ('head_text', _('Data description')),
        ('head_select', _('Data units')),
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-edge-form',
        'title': _("Create a new edge"),
        'submit_name': _("Create edge"),
        'script': 'metadb/edge_form.js',
        'attributes': [
            {'name': 'conveyors-url',
             'value': reverse_lazy('metadb:conveyor-list')},
            {'name': 'vertices-url',
             'value': reverse_lazy('metadb:vertex-list')},
            {'name': 'vertices-url',
             'value': reverse_lazy('metadb:vertex-list')},
            {'name': 'datavariables-url',
             'value': reverse_lazy('metadb:datavariable-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-edge-form',
        'title': _("Update edge"),
        'submit_name': _("Update edge"),
        'script': 'metadb/edge_form.js',
        'attributes': [
            {'name': 'conveyors-url',
             'value': reverse_lazy('metadb:conveyor-list')},
            {'name': 'vertices-url',
             'value': reverse_lazy('metadb:vertex-list')},
            {'name': 'vertices-url',
             'value': reverse_lazy('metadb:vertex-list')},
            {'name': 'datavariables-url',
             'value': reverse_lazy('metadb:datavariable-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-edge-delete-form',
        'title': _('Confirm edge delete'),
        'text': _('Are you sure you want to delete the edge'),
        'submit_name': _('Delete edge'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class FileViewSet(BaseViewSet):
    """
    Returns file name patterns
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:file-list'
    action_url = 'metadb:file-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('File name pattern'), 'field': 'name_pattern'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-file-form',
        'title': _("Create a new file"),
        'submit_name': _("Create file"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-file-form',
        'title': _("Update file"),
        'submit_name': _("Update file"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-file-delete-form',
        'title': _('Confirm file delete'),
        'text': _('Are you sure you want to delete the file'),
        'submit_name': _('Delete file'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }



class FileTypeViewSet(BaseViewSet):
    """
    Returns file types
    """
    queryset = FileType.objects.all().order_by('name')
    serializer_class = FileTypeSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:filetype-list'
    action_url = 'metadb:filetype-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Name'), 'field': 'name'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-filetype-form',
        'title': _("Create a new file type"),
        'submit_name': _("Create file type"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-filetype-form',
        'title': _("Update file type"),
        'submit_name': _("Update file type"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-filetype-delete-form',
        'title': _('Confirm file type delete'),
        'text': _('Are you sure you want to delete the file type'),
        'submit_name': _('Delete file type'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class GuiElementViewSet(BaseViewSet):
    """
    Returns GUI elements
    """
    queryset = GuiElement.objects.all().order_by('name')
    serializer_class = GuiElementSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:guielement-list'
    action_url = 'metadb:guielement-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Name'), 'field': 'name'},
        {'type': 'head_text', 'caption': _('Caption'), 'field': 'guielementi18n.caption'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-gui-element-form',
        'title': _("Create a new GUI element"),
        'submit_name': _("Create GUI element"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-gui-element-form',
        'title': _("Update GUI element"),
        'submit_name': _("Update GUI element"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-gui-element-delete-form',
        'title': _('Confirm GUI element delete'),
        'text': _('Are you sure you want to delete the GUI element'),
        'submit_name': _('Delete GUI element'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class LanguageViewSet(BaseViewSet):
    """
    Returns languages
    """
    queryset = Language.objects.all().order_by('name')
    serializer_class = LanguageSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:language-list'
    action_url = 'metadb:language-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Name'), 'field': 'name'},
        {'type': 'head_text', 'caption': _('Code'), 'field': 'code'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-language-form',
        'title': _("Create a new language"),
        'submit_name': _("Create language"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-language-form',
        'title': _("Update language"),
        'submit_name': _("Update language"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-language-delete-form',
        'title': _('Confirm language delete'),
        'text': _('Are you sure you want to delete the language'),
        'submit_name': _('Delete language'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class LevelViewSet(BaseViewSet):
    """
    Returns levels
    """
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:level-list'
    action_url = 'metadb:level-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Label'), 'field': 'label'},
        {'type': 'head_text', 'caption': _('Name'), 'field': 'leveli18n.name'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-level-form',
        'title': _("Create a new level"),
        'submit_name': _("Create level"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-level-form',
        'title': _("Update level"),
        'submit_name': _("Update level"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-level-delete-form',
        'title': _('Confirm level delete'),
        'text': _('Are you sure you want to delete the level'),
        'submit_name': _('Delete level'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    def __init__(self, *args, **kwargs):
        self.queryset = self.queryset.filter(
            language__code=get_language()).order_by('leveli18n__name')


class LevelsGroupViewSet(BaseViewSet):
    """
    Returns levels groups
    """
    queryset = LevelsGroup.objects.all()
    serializer_class = LevelsGroupSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:levelsgroup-list'
    action_url = 'metadb:levelsgroup-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Description'), 'field': 'description'},
        {'type': 'head_text', 'caption': _('Measurement unit'), 'field': 'units.unitsi18n.name'},
        {'type': 'head_text', 'caption': _('Levels'), 'field': 'levels', 'subfield': 'leveli18n.name'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-levels-group-form',
        'title': _("Create a new levels group"),
        'submit_name': _("Create levels group"),
        'script': 'metadb/levelsgroup_form.js',
        'attributes': [
            {'name': 'units-url',
             'value': reverse_lazy('metadb:units-list')},
            {'name': 'levels-url',
             'value': reverse_lazy('metadb:level-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-levels-group-form',
        'title': _("Update levels_group"),
        'submit_name': _("Update levels group"),
        'script': 'metadb/levelsgroup_form.js',
        'attributes': [
            {'name': 'units-url',
             'value': reverse_lazy('metadb:units-list')},
            {'name': 'levels-url',
             'value': reverse_lazy('metadb:level-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-levels-group-delete-form',
        'title': _('Confirm levels group delete'),
        'text': _('Are you sure you want to delete the levels group'),
        'submit_name': _('Delete levels group'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    def list(self, request):
        http_action = request.META.get('HTTP_ACTION')
        qset = self.get_queryset()
        parameter_id = request.GET.get('parameterId')
        time_step_id = request.GET.get('timestepId')
        if parameter_id and time_step_id:
            qset = qset.filter(specificparameter__parameter_id=parameter_id,
                               specificparameter__time_step_id=time_step_id)
        serializer = self.get_serializer(qset, many=True)
        ctx = {'data': serializer.data}

        if http_action == 'options_list' or request.GET.get('format') == 'html':
            result = render(request, self.options_template_name, ctx)
        else:
            if isinstance(request.accepted_renderer, JSONRenderer):
                ctx['headers'] = self.table_headers
            result = Response(ctx)

        return result


class LevelsVariableViewSet(BaseViewSet):
    """
    Returns levels variables
    """
    queryset = Variable.objects.all()
    serializer_class = LevelsVariableSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:levelsvariable-list'
    action_url = 'metadb:levelsvariable-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Name'), 'field': 'name'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-levels-variable-form',
        'title': _("Create a new levels variable"),
        'submit_name': _("Create levels variable"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-levels-variable-form',
        'title': _("Update levels variable"),
        'submit_name': _("Update levels variable"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-levels-variable-delete-form',
        'title': _('Confirm levels variable delete'),
        'text': _('Are you sure you want to delete the levels variable'),
        'submit_name': _('Delete levels variable'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class OptionViewSet(BaseViewSet):
    """
    Returns options
    """
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:option-list'
    action_url = 'metadb:option-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Label'), 'field': 'label'},
        {'type': 'head_text', 'caption': _('GUI element name'), 'field': 'gui_element.name'},
        {'type': 'head_text', 'caption': _('GUI element caption'), 'field': 'gui_element.guielementi18n.caption'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-option-form',
        'title': _("Create a new option"),
        'submit_name': _("Create option"),
        'script': 'metadb/option_form.js',
        'attributes': [
            {'name': 'gui-element-url',
             'value': reverse_lazy('metadb:guielement-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-option-form',
        'title': _("Update option"),
        'submit_name': _("Update option"),
        'script': 'metadb/option_form.js',
        'attributes': [
            {'name': 'gui-element-url',
             'value': reverse_lazy('metadb:guielement-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-option-delete-form',
        'title': _('Confirm option delete'),
        'text': _('Are you sure you want to delete the option'),
        'submit_name': _('Delete option'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class OptionValueViewSet(BaseViewSet):
    """
    Returns option values
    """
    queryset = OptionValue.objects.order_by('label')
    serializer_class = OptionValueSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:optionvalue-list'
    action_url = 'metadb:optionvalue-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Label'), 'field': 'label'},
        {'type': 'head_text', 'caption': _('Name'), 'field': 'optionvaluei18n.name'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-optionvalue-form',
        'title': _("Create a new option value"),
        'submit_name': _("Create option value"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-optionvalue-form',
        'title': _("Update option value"),
        'submit_name': _("Update option value"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-optionvalue-delete-form',
        'title': _('Confirm level option value'),
        'text': _('Are you sure you want to delete the option value'),
        'submit_name': _('Delete option value'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class OrganizationViewSet(BaseViewSet):
    """
    Returns organizations
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:organization-list'
    action_url = 'metadb:organization-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Name'), 'field': 'organizationi18n.name'},
        {'type': 'head_text', 'caption': _('URL'), 'field': 'url'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-organization-form',
        'title': _("Create a new organization"),
        'submit_name': _("Create organization"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-organization-form',
        'title': _("Update organization"),
        'submit_name': _("Update organization"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-organization-delete-form',
        'title': _('Confirm organization delete'),
        'text': _('Are you sure you want to delete the organization'),
        'submit_name': _('Delete organization'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    def __init__(self, *args, **kwargs):
        self.queryset = self.queryset.filter(
            language__code=get_language()).order_by('organizationi18n__name')


class ParameterViewSet(BaseViewSet):
    """
    Returns parameters
    """
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:parameter-list'
    action_url = 'metadb:parameter-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_select', 'caption': _('Is visible'), 'field': 'is_visible'},
        {'type': 'head_text', 'caption': _('Accumulation mode'), 'field': 'accumulation_mode'},
        {'type': 'head_text', 'caption': _('Name'), 'field': 'parameteri18n.name'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-parameter-form',
        'title': _("Create a new meteorological parameter"),
        'submit_name': _("Create parameter"),
        'script': 'metadb/parameter_form.js',
        'attributes': [
            {'name': 'accmodes-url',
             'value': reverse_lazy('metadb:accumulationmode-list')}
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-parameter-form',
        'title': _("Update meteorological parameter"),
        'submit_name': _("Update parameter"),
        'script': 'metadb/parameter_form.js',
        'attributes': [
            {'name': 'accmodes-url',
             'value': reverse_lazy('metadb:accumulationmode-list')}
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-parameter-delete-form',
        'title': _('Confirm meteorological parameter delete'),
        'text': _('Are you sure you want to delete the parameter'),
        'submit_name': _('Delete parameter'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    def __init__(self, *args, **kwargs):
        self.queryset = self.queryset.filter(
            language__code=get_language()).order_by('parameteri18n__name')


class PropertyViewSet(BaseViewSet):
    """
    Returns properties
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:property-list'
    action_url = 'metadb:property-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Label'), 'field': 'label'},
        {'type': 'head_text', 'caption': _('GUI element name'), 'field': 'gui_element.name'},
        {'type': 'head_text', 'caption': _('GUI element caption'), 'field': 'gui_element.guielementi18n.caption'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-property-form',
        'title': _("Create a new property"),
        'submit_name': _("Create property"),
        'script': 'metadb/property_form.js',
        'attributes': [
            {'name': 'gui-element-url',
             'value': reverse_lazy('metadb:form_load_guielements')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-property-form',
        'title': _("Update property"),
        'submit_name': _("Update property"),
        'script': 'metadb/property_form.js',
        'attributes': [
            {'name': 'gui-element-url',
             'value': reverse_lazy('metadb:form_load_guielements')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-property-delete-form',
        'title': _('Confirm property delete'),
        'text': _('Are you sure you want to delete the property'),
        'submit_name': _('Delete property'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class PropertyValueViewSet(BaseViewSet):
    """
    Returns property values
    """
    queryset = PropertyValue.objects.all()
    serializer_class = PropertyValueSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:propertyvalue-list'
    action_url = 'metadb:propertyvalue-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Label'), 'field': 'label'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-property-value-form',
        'title': _("Create a new property value"),
        'submit_name': _("Create property value"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-property-value-form',
        'title': _("Update property value"),
        'submit_name': _("Update property value"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-property-value-delete-form',
        'title': _('Confirm property value delete'),
        'text': _('Are you sure you want to delete the property value'),
        'submit_name': _('Delete property value'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class ResolutionViewSet(BaseViewSet):
    """
    Returns resolutions
    """
    queryset = Resolution.objects.all().order_by('name')
    serializer_class = ResolutionSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:resolution-list'
    action_url = 'metadb:resolution-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Name'), 'field': 'name'},
        {'type': 'head_text', 'caption': _('Subpath'), 'field': 'subpath1'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-resolution-form',
        'title': _("Create a new resolution"),
        'submit_name': _("Create resolution"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-resolution-form',
        'title': _("Update resolution"),
        'submit_name': _("Update resolution"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-resolution-delete-form',
        'title': _('Confirm resolution delete'),
        'text': _('Are you sure you want to delete the resolution'),
        'submit_name': _('Delete resolution'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class RootDirViewSet(BaseViewSet):
    """
    Returns root directory names
    """
    queryset = RootDir.objects.all()
    serializer_class = RootDirSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:rootdir-list'
    action_url = 'metadb:rootdir-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Name'), 'field': 'name'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-root-dir-form',
        'title': _("Create a new root directory"),
        'submit_name': _("Create root directory"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-root-dir-form',
        'title': _("Update root directory"),
        'submit_name': _("Update root directory"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-root-dir-delete-form',
        'title': _('Confirm root directory delete'),
        'text': _('Are you sure you want to delete the root directory'),
        'submit_name': _('Delete root directory'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class ScenarioViewSet(BaseViewSet):
    """
    Returns scenarios
    """
    queryset = Scenario.objects.all().order_by('name')
    serializer_class = ScenarioSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:scenario-list'
    action_url = 'metadb:scenario-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Name'), 'field': 'name'},
        {'type': 'head_text', 'caption': _('Subpath'), 'field': 'subpath0'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-scenario-form',
        'title': _("Create a new scenario"),
        'submit_name': _("Create scenario"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-scenario-form',
        'title': _("Update scenario"),
        'submit_name': _("Update scenario"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-scenario-delete-form',
        'title': _('Confirm scenario delete'),
        'text': _('Are you sure you want to delete the scenario'),
        'submit_name': _('Delete scenario'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class SpecificParameterViewSet(BaseViewSet):
    """
    Returns specific parameters
    """
    queryset = SpecificParameter.objects.all()
    serializer_class = SpecificParameterSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:specificparameter-list'
    action_url = 'metadb:specificparameter-detail'

    table_headers = [
        ('head_none', 'Id'),
        ('head_none', _('Visible')),
        ('head_select', _('Parameter')),
        ('head_select', _('Accumulation mode')),
        ('head_select', _('Time step')),
        ('head_none', _('Time step label')),
        ('head_none', _('Time step subpath')),
        ('head_select', _('Levels group measurement unit')),
        ('head_text', _('Levels group description')),
        ('head_text', _('Levels names')),
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-specpar-form',
        'title': _("Create a new specific parameter"),
        'submit_name': _("Create specific parameter"),
        'script': 'metadb/specpar_form.js',
        'attributes': [
            {'name': 'parameter-url',
             'value': reverse_lazy('metadb:parameter-list')},
            {'name': 'time-step-url',
             'value': reverse_lazy('metadb:timestep-list')},
            {'name': 'levels-group-url',
             'value': reverse_lazy('metadb:levelsgroup-list')},
            {'name': 'lvsgroup-lvsnames-url',
             'value': reverse_lazy('metadb:levelsgroup-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-specpar-update-form',
        'title': _("Update specific parameter"),
        'submit_name': _("Update specific parameter"),
        'script': 'metadb/specpar_form.js',
        'attributes': [
            {'name': 'parameter-url',
             'value': reverse_lazy('metadb:parameter-list')},
            {'name': 'time-step-url',
             'value': reverse_lazy('metadb:timestep-list')},
            {'name': 'levels-group-url',
             'value': reverse_lazy('metadb:levelsgroup-list')},
            {'name': 'lvsgroup-lvsnames-url',
             'value': reverse_lazy('metadb:levelsgroup-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-specpar-delete-form',
        'title': _('Confirm specific parameter delete'),
        'text': _('Are you sure you want to delete the specific parameter'),
        'submit_name': _('Delete specific parameter'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class TimeStepViewSet(BaseViewSet):
    """
    Returns time step
    """
    queryset = TimeStep.objects.all()
    serializer_class = TimeStepSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:timestep-list'
    action_url = 'metadb:timestep-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Label'), 'field': 'label'},
        {'type': 'head_text', 'caption': _('Subpath'), 'field': 'subpath2'},
        {'type': 'head_text', 'caption': _('Name'), 'field': 'timestepi18n.name'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-timestep-form',
        'title': _("Create a new time step"),
        'submit_name': _("Create time step"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-unit-form',
        'title': _("Update measurement unit"),
        'submit_name': _("Update units"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-timestep-delete-form',
        'title': _('Confirm time step delete'),
        'text': _('Are you sure you want to delete the time step'),
        'submit_name': _('Delete time step'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    def __init__(self, *args, **kwargs):
        self.queryset = self.queryset.filter(
            language__code=get_language()).order_by('timestepi18n__name')


    def list(self, request):
        http_action = request.META.get('HTTP_ACTION')
        qset = self.get_queryset()
        parameter_id = request.GET.get('parameterId')
        if parameter_id:
            qset = qset.filter(specificparameter__parameter_id=parameter_id).distinct()
        serializer = self.get_serializer(qset, many=True)
        ctx = {'data': serializer.data}

        if http_action == 'options_list' or request.GET.get('format') == 'html':
            result = render(request, self.options_template_name, ctx)
        else:
            if isinstance(request.accepted_renderer, JSONRenderer):
                ctx['headers'] = self.table_headers
            result = Response(ctx)

        return result


class UnitsViewSet(BaseViewSet):
    """
    Returns units
    """
    queryset = Units.objects.all()
    serializer_class = UnitsSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:units-list'
    action_url = 'metadb:units-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Name'), 'field': 'unitsi18n.name'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-unit-form',
        'title': _("Create a new measurement unit"),
        'submit_name': _("Create unit"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-unit-form',
        'title': _("Update measurement unit"),
        'submit_name': _("Update unit"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-unit-delete-form',
        'title': _('Confirm measurement unit delete'),
        'text': _('Are you sure you want to delete the unit'),
        'submit_name': _('Delete unit'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    def __init__(self, *args, **kwargs):
        self.queryset = self.queryset.filter(
            language__code=get_language()).order_by('unitsi18n__name')


class VariableViewSet(BaseViewSet):
    """
    Returns variables
    """
    queryset = Variable.objects.all()
    serializer_class = VariableSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:variable-list'
    action_url = 'metadb:variable-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Name'), 'field': 'name'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-variable-form',
        'title': _("Create a new variable"),
        'submit_name': _("Create variable"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-variable-form',
        'title': _("Update variable"),
        'submit_name': _("Update variable"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-variable-delete-form',
        'title': _('Confirm variable delete'),
        'text': _('Are you sure you want to delete the variable'),
        'submit_name': _('Delete variable'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class VertexViewSet(BaseViewSet):
    """
    Returns vertices
    """
    queryset = Vertex.objects.all()
    serializer_class = VertexSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/list_vertex_items.html'
    list_url = 'metadb:vertex-list'
    action_url = 'metadb:vertex-detail'

    table_headers = [
        ('head_none', 'Id'),
        ('head_select', _('Computing module')),
        ('head_select', _('Option label')),
        ('head_select', _('GUI element')),
        ('head_none', _('Option value')),
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-vertex-form',
        'title': _("Create a new vertex"),
        'submit_name': _("Create vertex"),
        'script': 'metadb/vertex_form.js',
        'attributes': [
            {'name': 'computingmodules-url',
             'value': reverse_lazy('metadb:computingmodule-list')},
            {'name': 'options-url',
             'value': reverse_lazy('metadb:option-list')},
            {'name': 'optionvalues-url',
             'value': reverse_lazy('metadb:optionvalue-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-vertex-form',
        'title': _("Update vertex"),
        'submit_name': _("Update vertex"),
        'script': 'metadb/specpar_form.js',
        'attributes': [
            {'name': 'computingmodules-url',
             'value': reverse_lazy('metadb:computingmodule-list')},
            {'name': 'options-url',
             'value': reverse_lazy('metadb:option-list')},
            {'name': 'optionvalues-url',
             'value': reverse_lazy('metadb:optionvalue-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-vertex-delete-form',
        'title': _('Confirm vertex delete'),
        'text': _('Are you sure you want to delete the vertex'),
        'submit_name': _('Delete vertex'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    # This action allows to get only essential properties of the vertices. Fast.
    @action(methods=['GET'], detail=False)
    def light(self, request, pk=None):
        vertices = self.get_queryset()
        if pk is not None:
            vertices = vertices.filter(pk=pk)

        data = []
        for vertex in vertices:
            data.append({'id': vertex.id,
                         'computing_module': {'name': vertex.computing_module.name},
                         'condition_option': {'label': vertex.condition_option.label},
                         'condition_value': {'label': vertex.condition_value.label},
                        })

        result = {'data': data}
        response = JsonResponse(result)
        return response

    def __init__(self, *args, **kwargs):
        self.queryset = self.queryset.order_by('computing_module__name')
