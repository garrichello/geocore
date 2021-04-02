import json
from collections import defaultdict

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

from .models import *
from .serializers import LanguageSerializer
from .serializers_collection import *
from .serializers_dataset import *
from .serializers_specparam import *
from .serializers_data import *
from .serializers_conveyor import *
from .serializers_processor import *

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


class ArgumentsGroupViewSet(BaseViewSet):
    """
    Returns arguments groups
    """
    queryset = ArgumentsGroup.objects.all().order_by('name')
    serializer_class = ArgumentsGroupSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:argumentsgroup-list'
    action_url = 'metadb:argumentsgroup-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Name'), 'field': 'name'},
        {'type': 'head_text', 'caption': _('Description'), 'field': 'description'},
        {'type': 'head_select', 'caption': _('Argument type'), 'field': 'argument_type.label'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-arggroup-form',
        'title': _("Create a new arguments group"),
        'submit_name': _("Create arguments group"),
        'script': 'metadb/arggroup_form.js',
        'attributes': [
            {'name': 'argtypes-url',
             'value': reverse_lazy('metadb:argumenttype-list')}
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-arggroup-form',
        'title': _("Update arguments group"),
        'submit_name': _("Update arguments group"),
        'script': 'metadb/arggroup_form.js',
        'attributes': [
            {'name': 'argtypes-url',
             'value': reverse_lazy('metadb:argumenttype-list')}
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-arggroup-delete-form',
        'title': _('Confirm arguments group delete'),
        'text': _('Are you sure you want to delete the arguments group'),
        'submit_name': _('Delete arguments group'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class ArgumentsGroupFullViewSet(BaseViewSet):
    """
    Returns arguments groups full info
    """
    queryset = ArgumentsGroup.objects.all().order_by('name')
    serializer_class = ArgumentsGroupFullSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:fullargumentsgroup-list'
    action_url = 'metadb:fullargumentsgroup-detail'

    table_headers = [
#        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
#        {'type': 'head_text', 'caption': _('Name'), 'field': 'name'},
#        {'type': 'head_text', 'caption': _('Description'), 'field': 'description'},
#        {'type': 'head_select', 'caption': _('Argument type'), 'field': 'argument_type.label'},
#        {'type': 'head_select', 'caption': _('Processor'), 'field': 'processor',
#                                                           'subfield': 'processor.processori18n.name'},
#        {'type': 'head_select', 'caption': _('Specific parameter'), 'field': 'specific_parameter',
#                                                                    'subfield': 'string'},
        ('head_none', 'Id'),
        ('head_text', _('Name')),
        ('head_text', _('Description')),
        ('head_select', _('Argument type')),
        ('head_text', _('Processor')),
        ('head_text', _('Specific parameter')),
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-arggroupfull-form',
        'title': _("Create a new arguments group"),
        'submit_name': _("Create arguments group"),
        'script': 'metadb/arggroupfull_form.js',
        'attributes': [
            {'name': 'argtypes-url',
             'value': reverse_lazy('metadb:argumenttype-list')},
            {'name': 'processors-url',
             'value': reverse_lazy('metadb:processor-list')},
            {'name': 'specificparameters-url',
             'value': reverse_lazy('metadb:specificparameter-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-arggroupfull-form',
        'title': _("Update arguments group"),
        'submit_name': _("Update arguments group"),
        'script': 'metadb/arggroupfull_form.js',
        'attributes': [
            {'name': 'argtypes-url',
             'value': reverse_lazy('metadb:argumenttype-list')},
            {'name': 'processors-url',
             'value': reverse_lazy('metadb:processor-list')},
            {'name': 'specificparameters-url',
             'value': reverse_lazy('metadb:specificparameter-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-arggroupfull-delete-form',
        'title': _('Confirm arguments group delete'),
        'text': _('Are you sure you want to delete the arguments group'),
        'submit_name': _('Delete arguments group'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class ArgumentsGroupHasProcessorViewSet(BaseViewSet):
    """
    Returns arguments groups
    """
    queryset = ArgumentsGroupHasProcessor.objects.all()
    serializer_class = ArgumentsGroupHasProcessorSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:argumentsgrouphasprocessor-list'
    action_url = 'metadb:argumentsgrouphasprocessor-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Name'), 'field': 'name'},
        {'type': 'head_select', 'caption': _('Processor'), 'field': 'processor'},
        {'type': 'head_select', 'caption': _('Override combinations'), 'field': 'override_combination'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-arggrouphasproc-form',
        'title': _("Create a new link arguments group - processor"),
        'submit_name': _("Create link"),
        'script': 'metadb/arggrouphasproc_form.js',
        'attributes': [
            {'name': 'processors-url',
             'value': reverse_lazy('metadb:processor-list')},
            {'name': 'combinations-url',
             'value': reverse_lazy('metadb:combination-list')}
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-arggrouphasproc-form',
        'title': _("Update the link arguments group - processor"),
        'submit_name': _("Update link"),
        'script': 'metadb/arggrouphasproc_form.js',
        'attributes': [
            {'name': 'processors-url',
             'value': reverse_lazy('metadb:processor-list')},
            {'name': 'combinations-url',
             'value': reverse_lazy('metadb:combination-list')}
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-arggrouphasproc-delete-form',
        'title': _('Confirm arguments group - processor link delete'),
        'text': _('Are you sure you want to delete the link arguments group - processor'),
        'submit_name': _('Delete link'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class ArgumentTypeViewSet(BaseViewSet):
    """
    Returns argument types
    """
    queryset = ArgumentType.objects.all().order_by('label')
    serializer_class = ArgumentTypeSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:argumenttype-list'
    action_url = 'metadb:argumenttype-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Label'), 'field': 'label'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-argtype-form',
        'title': _("Create a new argument type"),
        'submit_name': _("Create argument type"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-argtype-form',
        'title': _("Update argument type"),
        'submit_name': _("Update argument type"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-argtype-delete-form',
        'title': _('Confirm argument type delete'),
        'text': _('Are you sure you want to delete the argument type'),
        'submit_name': _('Delete argument type'),
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


class CombinationViewSet(BaseViewSet):
    """
    Returns option-value combinations
    """
    queryset = Combination.objects.order_by('option__label')
    serializer_class = CombinationSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:combination-list'
    action_url = 'metadb:combination-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_select', 'caption': _('Option label'), 'field': 'option.label'},
        {'type': 'head_select', 'caption': _('Option value label'), 'field': 'option_value.label'},
        {'type': 'head_select', 'caption': _('Condition option'), 'field': 'condition.option.label'},
        {'type': 'head_select', 'caption': _('Condition value'), 'field': 'condition.option_value.label'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-combination-form',
        'title': _("Create a new option-value combination"),
        'submit_name': _("Create combination"),
        'script': 'metadb/combination_form.js',
        'attributes': [
            {'name': 'options-url',
             'value': reverse_lazy('metadb:option-list')},
            {'name': 'optionvalues-url',
             'value': reverse_lazy('metadb:optionvalue-list')},
            {'name': 'conditions-url',
             'value': reverse_lazy('metadb:combination-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-combination-form',
        'title': _("Update option-value combination"),
        'submit_name': _("Update combination"),
        'script': 'metadb/combination_form.js',
        'attributes': [
            {'name': 'options-url',
             'value': reverse_lazy('metadb:option-list')},
            {'name': 'optionvalues-url',
             'value': reverse_lazy('metadb:optionvalue-list')},
            {'name': 'conditions-url',
             'value': reverse_lazy('metadb:combination-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-combination-delete-form',
        'title': _('Confirm option-value combination delete'),
        'text': _('Are you sure you want to delete the option-value combination'),
        'submit_name': _('Delete combination'),
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
        {'type': 'head_text', 'caption': _('Number of inputs'), 'field': 'number_of_inputs'},
        {'type': 'head_text', 'caption': _('Number of inputs'), 'field': 'number_of_outputs'},
        {'type': 'head_text', 'caption': _('Description'), 'field': 'description'},
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

    def _sort_dict(self, in_dict: dict):
        out_dict = {}
        for key in sorted(in_dict.keys()):
            out_dict[key] = in_dict[key]
        return out_dict

    def _num(self, numbered_name: str) -> int:
        ''' Cut off number of a name given in a form: name_#. '''
        return int(numbered_name.split('_')[1])

    def _retrieve_graph(self, request, pk=None):
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
                'vertex_id': vertex.id,
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
                'inputs': inputs, #self._sort_dict(inputs),
                'outputs': outputs, #self._sort_dict(outputs),
                'condition_option': vertex.condition_combination.option.label if vertex.condition_combination else None,
                'condition_value': vertex.condition_combination.option_value.label if vertex.condition_combination else None,
            }
            left += d_left

        result = {'operators': operators, 'links': links}
        response = JsonResponse(result)
        return response

    def retrieve(self, request, pk=None):
        http_action = request.META.get('HTTP_ACTION')
        if http_action == 'graph':
            result = self._retrieve_graph(request, pk)
        else:
            result = super().retrieve(request, pk)

        return result

    def create(self, request, *args, **kwargs):
        data = json.loads(request.data['data'])

        conveyor_label = data['conveyorLabel']
        operators = data['operators']
        links = data['links']
        all_links_has_ids = True
        for link in links.values():
            if 'datavariable_id' not in link:
                all_links_has_ids = False
                link['color'] = "#ff0000"

        form_is_valid = False
        errors = []

        # Create a new conveyor instance
        conveyor_serializer = self.get_serializer(data={'label': conveyor_label})
        if conveyor_serializer.is_valid():
            if not operators:
                errors.append(_('Graph may not be empty'))
            elif not links:
                errors.append(_('Graph must be connected'))
            elif not all_links_has_ids:
                errors.append(_('All links must be assigned to data variables'))
            else:
                conveyor = conveyor_serializer.save()
                # Link conveyor to vertices
                for operator in operators.values():
                    chv = ConveyorHasVertex()
                    chv.conveyor = conveyor
                    chv.vertex_id = operator['vertex_id']
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

                form_is_valid = True
        else:
            errors.append(_("Conveyor label may not be blank!"))

        result = {'data': data, 'form_is_valid': form_is_valid, 'errors': errors}
        response = JsonResponse(result)
        return response

    def update(self, request, *args, **kwargs):
        data = json.loads(request.data['data'])

        conveyor_label = data['conveyorLabel']
        operators = data['operators']
        links = data['links']
        all_links_has_ids = True
        for link in links.values():
            if 'datavariable_id' not in link:
                all_links_has_ids = False
                link['color'] = "#ff0000"

        form_is_valid = False
        errors = []

        # Use an existing conveyor instance
        instance = self.get_object()
        conveyor_serializer = self.get_serializer(data={'label': conveyor_label}, instance=instance)
        if conveyor_serializer.is_valid():
            if not operators:
                errors.append(_('Graph may not be empty'))
            elif not links:
                errors.append(_('Graph must be connected'))
            elif not all_links_has_ids:
                errors.append(_('All links must be assigned to data variables'))
            else:
                # Update conveyor
                conveyor_serializer.save()
                # Get lists of vertices in db and modified graph
                vertices_in_db_set = set([obj.vertex for obj in ConveyorHasVertex.objects.filter(conveyor=instance)])
                vertices_in_graph = {Vertex.objects.get(pk=op['vertex_id']): {'top': op['top'],
                                                                              'left': op['left']
                                                                             } for op in operators.values()}
                vertices_in_graph_set = set(vertices_in_graph.keys())
                # Delete removed vertices from db
                vertices_to_delete = vertices_in_db_set - vertices_in_graph_set
                for vertex in vertices_to_delete:
                    ConveyorHasVertex.objects.filter(conveyor=instance,
                                                     vertex=vertex).delete()
                # Add inserted vertices into db
                vertices_to_insert = vertices_in_graph_set - vertices_in_db_set
                for vertex in vertices_to_insert:
                    chv = ConveyorHasVertex()
                    chv.conveyor = instance
                    chv.vertex = vertex
                    chv.vertex_position_top = vertices_in_graph[vertex]['top']
                    chv.vertex_position_left = vertices_in_graph[vertex]['left']
                    chv.save()
                # Update remaining vertices in db
                vertices_to_update = vertices_in_graph_set & vertices_in_db_set
                for vertex in vertices_to_update:
                    chv = ConveyorHasVertex.objects.filter(conveyor=instance,
                                                           vertex=vertex).get()
                    chv.vertex_position_top = vertices_in_graph[vertex]['top']
                    chv.vertex_position_left = vertices_in_graph[vertex]['left']
                    chv.save()
                # Get edges in db and modified graph
                edges_in_graph = {(self._num(link['fromOperator']),
                                       self._num(link['fromConnector']),
                                       self._num(link['toOperator']),
                                       self._num(link['toConnector'])): {
                                           'data_variable_id': link['datavariable_id']
                                       } for link in links.values()}
                edges_in_graph_set = set(edges_in_graph.keys())
                edges_in_db = {(edge.from_vertex_id,
                                edge.from_output,
                                edge.to_vertex_id,
                                edge.to_input): edge for edge in Edge.objects.filter(conveyor=instance)}
                edges_in_db_set = set(edges_in_db.keys())
                # Delete removed edges from db
                edges_to_delete = edges_in_db_set - edges_in_graph_set
                for edge in edges_to_delete:
                    edges_in_db[edge].delete()
                # Add inserted vertices into db
                edges_to_insert = edges_in_graph_set - edges_in_db_set
                for edge in edges_to_insert:
                    new_edge = Edge()
                    new_edge.conveyor = instance
                    new_edge.from_vertex_id = edge[0]
                    new_edge.from_output = edge[1]
                    new_edge.to_vertex_id = edge[2]
                    new_edge.to_input = edge[3]
                    new_edge.data_variable_id = edges_in_graph[edge]['data_variable_id']
                    new_edge.save()
                # Update remaining edges in db
                edges_to_update = edges_in_graph_set & edges_in_db_set
                for edge in edges_to_update:
                    edges_in_db[edge].data_variable_id = edges_in_graph[edge]['data_variable_id']
                    edges_in_db[edge].save()

                form_is_valid = True
        else:
            errors.append(_("Conveyor label may not be blank! (Or DB is damaged)"))

        result = {'data': data, 'form_is_valid': form_is_valid, 'errors': errors}
        response = JsonResponse(result)
        return response


class ConveyorFullViewSet(BaseViewSet):
    """
    Returns conveyors with edges
    """
    queryset = Conveyor.objects.all()
    serializer_class = ConveyorFullSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:fullconveyor-list'
    action_url = 'metadb:fullconveyor-detail'


class DataArgumentsGroupViewSet(BaseViewSet):
    """
    Returns data arguments groups info
    """
    queryset = ArgumentsGroup.objects.filter(argument_type__label='data').order_by('name')
    serializer_class = DataArgumentsGroupSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:dataargumentsgroup-list'
    action_url = 'metadb:dataargumentsgroup-detail'

    table_headers = [
#        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
#        {'type': 'head_text', 'caption': _('Name'), 'field': 'name'},
#        {'type': 'head_text', 'caption': _('Description'), 'field': 'description'},
#        {'type': 'head_select', 'caption': _('Argument type'), 'field': 'argument_type.label'},
#        {'type': 'head_select', 'caption': _('Processor'), 'field': 'processor',
#                                                           'subfield': 'processor.processori18n.name'},
#        {'type': 'head_select', 'caption': _('Specific parameter'), 'field': 'specific_parameter',
#                                                                    'subfield': 'string'},
        ('head_none', 'Id'),
        ('head_text', _('Group name')),
        ('head_text', _('Group description')),
        ('head_text', _('Specific parameter')),
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-dataarggroup-form',
        'title': _("Create a new data arguments group"),
        'submit_name': _("Create data arguments group"),
        'script': 'metadb/dataarggroup_form.js',
        'attributes': [
            {'name': 'specificparameters-url',
             'value': reverse_lazy('metadb:specificparameter-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-dataarggroup-form',
        'title': _("Update data arguments group"),
        'submit_name': _("Update data arguments group"),
        'script': 'metadb/dataarggroup_form.js',
        'attributes': [
            {'name': 'specificparameters-url',
             'value': reverse_lazy('metadb:specificparameter-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-dataarggroup-delete-form',
        'title': _('Confirm data arguments group delete'),
        'text': _('Are you sure you want to delete the data arguments group'),
        'submit_name': _('Delete data arguments group'),
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
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Data variable label'), 'field': 'label'},
        {'type': 'head_text', 'caption': _('Units'), 'field': 'units.unitsi18n.name'},
        {'type': 'head_text', 'caption': _('Data variable description'), 'field': 'description'},
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


class OptionsOverrideViewSet(BaseViewSet):
    """
    Returns overriding option values for processors in groupds
    """
    queryset = OptionsOverride.objects.all()
    serializer_class = OptionsOverrideSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:optionsoverride-list'
    action_url = 'metadb:optionsoverride-detail'

    table_headers = [
#        {'type': 'head_none', 'caption': _('Group id'),
#         'field': 'arguments_group_has_processor.arguments_group.id'},
#        {'type': 'head_text', 'caption': _('Group name'),
#         'field': 'arguments_group_has_processor.arguments_group.name'},
#        {'type': 'head_text', 'caption': _('Group description'),
#         'field': 'arguments_group_has_processor.arguments_group.description'},
#        {'type': 'head_text', 'caption': _('Processor'),
#         'field': 'arguments_group_has_processor.processor.processori18n.name'},
#        {'type': 'head_text', 'caption': _('Overriding option'),
#         'field': 'combination.string'},
        ('head_text', _('Group id')),
        ('head_select', _('Group name')),
        ('head_text', _('Group description')),
        ('head_select', _('Processor name')),
        ('head_text', _('Overriding option')),
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-optionsoverride-form',
        'title': _("Create a new options override"),
        'submit_name': _("Create options override"),
        'script': 'metadb/optionsoverride_form.js',
        'attributes': [
            {'name': 'argumentsgroups-url',
             'value': reverse_lazy('metadb:argumentsgroup-list')},
            {'name': 'processors-url',
             'value': reverse_lazy('metadb:processor-list')},
            {'name': 'combinations-url',
             'value': reverse_lazy('metadb:combination-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-optionsoverride-form',
        'title': _("Update options override"),
        'submit_name': _("Update options override"),
        'script': 'metadb/optionsoverride_form.js',
        'attributes': [
            {'name': 'argumentsgroups-url',
             'value': reverse_lazy('metadb:argumentsgroup-list')},
            {'name': 'processors-url',
             'value': reverse_lazy('metadb:processor-list')},
            {'name': 'combinations-url',
             'value': reverse_lazy('metadb:combination-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-optionsoverride-delete-form',
        'title': _('Confirm options override delete'),
        'text': _('Are you sure you want to delete the options override'),
        'submit_name': _('Delete options override'),
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
#        {'type': 'head_text', 'caption': _('GUI element name'), 'field': 'gui_element.name'},
#        {'type': 'head_text', 'caption': _('GUI element caption'), 'field': 'gui_element.guielementi18n.caption'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-option-form',
        'title': _("Create a new option"),
        'submit_name': _("Create option"),
#        'script': 'metadb/option_form.js',
#        'attributes': [
#            {'name': 'gui-element-url',
#             'value': reverse_lazy('metadb:guielement-list')},
#        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-option-form',
        'title': _("Update option"),
        'submit_name': _("Update option"),
#        'script': 'metadb/option_form.js',
#        'attributes': [
#            {'name': 'gui-element-url',
#             'value': reverse_lazy('metadb:guielement-list')},
#        ],
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


class ProcArgumentsGroupViewSet(BaseViewSet):
    """
    Returns processors arguments groups info
    """
    queryset = ArgumentsGroup.objects.filter(argument_type__label='processor').order_by('name')
    serializer_class = ProcArgumentsGroupSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:procargumentsgroup-list'
    action_url = 'metadb:procargumentsgroup-detail'

    table_headers = [
#        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
#        {'type': 'head_text', 'caption': _('Name'), 'field': 'name'},
#        {'type': 'head_text', 'caption': _('Description'), 'field': 'description'},
#        {'type': 'head_select', 'caption': _('Argument type'), 'field': 'argument_type.label'},
#        {'type': 'head_select', 'caption': _('Processor'), 'field': 'processor',
#                                                           'subfield': 'processor.processori18n.name'},
#        {'type': 'head_select', 'caption': _('Specific parameter'), 'field': 'specific_parameter',
#                                                                    'subfield': 'string'},
        ('head_none', 'Id'),
        ('head_text', _('Group name')),
        ('head_text', _('Group description')),
        ('head_none', _('Processor name')),
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-procarggroup-form',
        'title': _("Create a new processors arguments group"),
        'submit_name': _("Create arguments group"),
        'script': 'metadb/procarggroup_form.js',
        'attributes': [
            {'name': 'processors-url',
             'value': reverse_lazy('metadb:processor-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-procarggroup-form',
        'title': _("Update processors arguments group"),
        'submit_name': _("Update arguments group"),
        'script': 'metadb/procarggroup_form.js',
        'attributes': [
            {'name': 'processors-url',
             'value': reverse_lazy('metadb:processor-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-procarggroup-delete-form',
        'title': _('Confirm processors arguments group delete'),
        'text': _('Are you sure you want to delete the processors arguments group'),
        'submit_name': _('Delete arguments group'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class ProcessorViewSet(BaseViewSet):
    """
    Returns processors
    """
    queryset = Processor.objects.all()
    serializer_class = ProcessorSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    template_name = 'metadb/includes/processor_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:processor-list'
    action_url = 'metadb:processor-detail'

    table_headers = [
        ('head_none', _('Processor id')),
        ('head_select', _('Is visible')),
        ('head_text', _('Processor name')),
        ('head_text', _('Processor description')),
        ('head_text', _('Processor reference')),
        ('head_select', _('Conveyor label')),
        ('head_select', _('Settings')),
        ('head_select', _('Time period types')),
        ('head_none', _('Arguments selected by user')),
        ('head_select', _('Arguments')),
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-processor-form',
        'title': _("Create a new processor"),
        'submit_name': _("Create processor"),
        'script': 'metadb/processor_form.js',
        'attributes': [
            {'name': 'conveyors-url',
             'value': reverse_lazy('metadb:conveyor-list')},
            {'name': 'settings-url',
             'value': reverse_lazy('metadb:setting-list')},
            {'name': 'timeperiodtypes-url',
             'value': reverse_lazy('metadb:timeperiodtype-list')},
            {'name': 'argumentsgroups-url',
             'value': reverse_lazy('metadb:argumentsgroup-list')},
            {'name': 'fullconveyors-url',
             'value': reverse_lazy('metadb:fullconveyor-list')},
            {'name': 'fullargumentsgroups-url',
             'value': reverse_lazy('metadb:fullargumentsgroup-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-processor-form',
        'title': _("Update processor"),
        'submit_name': _("Update processor"),
        'script': 'metadb/processor_form.js',
        'attributes': [
            {'name': 'conveyors-url',
             'value': reverse_lazy('metadb:conveyor-list')},
            {'name': 'settings-url',
             'value': reverse_lazy('metadb:setting-list')},
            {'name': 'timeperiodtypes-url',
             'value': reverse_lazy('metadb:timeperiodtype-list')},
            {'name': 'argumentsgroups-url',
             'value': reverse_lazy('metadb:argumentsgroup-list')},
            {'name': 'fullconveyors-url',
             'value': reverse_lazy('metadb:fullconveyor-list')},
            {'name': 'fullargumentsgroups-url',
             'value': reverse_lazy('metadb:fullargumentsgroup-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-processor-delete-form',
        'title': _('Confirm processor delete'),
        'text': _('Are you sure you want to delete the processor'),
        'submit_name': _('Delete processor'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    def __init__(self, *args, **kwargs):
        self.queryset = self.queryset.filter(
            language__code=get_language()).order_by('processori18n__name')


class ProcessorFullViewSet(BaseViewSet):
    """
    Returns full processors info
    """
    queryset = Processor.objects.all()
    serializer_class = ProcessorFullSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:fullprocessor-list'
    action_url = 'metadb:fullprocessor-detail'

    table_headers = [
        ('head_none', _('Processor id')),
        ('head_select', _('Is visible')),
        ('head_text', _('Processor name')),
        ('head_text', _('Processor description')),
        ('head_text', _('Processor reference')),
        ('head_select', _('Conveyor label')),
        ('head_select', _('Settings')),
        ('head_select', _('Time period types')),
        ('head_none', _('Arguments selected by user')),
        ('head_select', _('Arguments')),
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-processor-form',
        'title': _("Create a new processor"),
        'submit_name': _("Create processor"),
        'script': 'metadb/processor_form.js',
        'attributes': [
            {'name': 'accmodes-url',
             'value': reverse_lazy('metadb:accumulationmode-list')}
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-processor-form',
        'title': _("Update processor"),
        'submit_name': _("Update processor"),
        'script': 'metadb/processor_form.js',
        'attributes': [
            {'name': 'accmodes-url',
             'value': reverse_lazy('metadb:accumulationmode-list')}
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-processor-delete-form',
        'title': _('Confirm processor delete'),
        'text': _('Are you sure you want to delete the processor'),
        'submit_name': _('Delete processor'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    def __init__(self, *args, **kwargs):
        self.queryset = self.queryset.filter(
            language__code=get_language()).order_by('processori18n__name')


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
             'value': reverse_lazy('metadb:guielement-list')},
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
             'value': reverse_lazy('metadb:guielement-list')},
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


class SettingViewSet(BaseViewSet):
    """
    Returns settings
    """
    queryset = Setting.objects.order_by('label')
    serializer_class = SettingSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options_noblank.html'
    list_url = 'metadb:setting-list'
    action_url = 'metadb:setting-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Label'), 'field': 'label'},
        {'type': 'head_text', 'caption': _('GUI Element'), 'field': 'gui_element.name'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-setting-form',
        'title': _("Create a new setting"),
        'submit_name': _("Create setting"),
        'script': 'metadb/setting_form.js',
        'attributes': [
            {'name': 'guielements-url',
             'value': reverse_lazy('metadb:guielement-list')}
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-setting-form',
        'title': _("Update setting"),
        'submit_name': _("Update setting"),
        'script': 'metadb/setting_form.js',
        'attributes': [
            {'name': 'guielements-url',
             'value': reverse_lazy('metadb:guielement-list')}
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-setting-delete-form',
        'title': _('Confirm setting delete'),
        'text': _('Are you sure you want to delete the setting'),
        'submit_name': _('Delete setting'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class SettingFullViewSet(BaseViewSet):
    """
    Returns full settings
    """
    queryset = Setting.objects.order_by('label')
    serializer_class = SettingFullSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:fullsetting-list'
    action_url = 'metadb:fullsetting-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Label'), 'field': 'label'},
        {'type': 'head_text', 'caption': _('GUI Element'), 'field': 'gui_element.name'},
        {'type': 'head_text', 'caption': _('Option label'), 'field': 'combinations',
                                                            'subfield': 'combination.string'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-settingfull-form',
        'title': _("Create a new setting"),
        'submit_name': _("Create setting"),
        'script': 'metadb/settingfull_form.js',
        'attributes': [
            {'name': 'guielements-url',
             'value': reverse_lazy('metadb:guielement-list')},
            {'name': 'combinations-url',
             'value': reverse_lazy('metadb:combination-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-settingfull-form',
        'title': _("Update setting"),
        'submit_name': _("Update setting"),
        'script': 'metadb/settingfull_form.js',
        'attributes': [
            {'name': 'guielements-url',
             'value': reverse_lazy('metadb:guielement-list')},
            {'name': 'combinations-url',
             'value': reverse_lazy('metadb:combination-list')},
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-settingfull-delete-form',
        'title': _('Confirm setting delete'),
        'text': _('Are you sure you want to delete the setting'),
        'submit_name': _('Delete setting'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }


class SettingHasCombinationViewSet(BaseViewSet):
    """
    Returns links beyween settings and option-value combination
    """
    queryset = SettingHasCombination.objects.all()
    serializer_class = SettingHasCombinationSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:settinghascombination-list'
    action_url = 'metadb:settinghascombination-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Name'), 'field': 'name'},
        {'type': 'head_select', 'caption': _('Settings'), 'field': 'setting'},
        {'type': 'head_select', 'caption': _('Option-value combinations'), 'field': 'combination'},
        {'type': 'head_text', 'caption': _('Index'), 'field': 'index'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-settinghascombination-form',
        'title': _("Create a new link setting - combination"),
        'submit_name': _("Create link"),
        'script': 'metadb/settinghascombination_form.js',
        'attributes': [
            {'name': 'settings-url',
             'value': reverse_lazy('metadb:setting-list')},
            {'name': 'combinations-url',
             'value': reverse_lazy('metadb:combination-list')}
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-settinghascombination-form',
        'title': _("Update the linksetting - combination"),
        'submit_name': _("Update link"),
        'script': 'metadb/settinghascombination_form.js',
        'attributes': [
            {'name': 'settings-url',
             'value': reverse_lazy('metadb:setting-list')},
            {'name': 'combinations-url',
             'value': reverse_lazy('metadb:combination-list')}
        ],
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-settinghascombination-delete-form',
        'title': _('Confirm setting - combination link delete'),
        'text': _('Are you sure you want to delete the link setting - combination'),
        'submit_name': _('Delete link'),
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


class TimePeriodTypeViewSet(BaseViewSet):
    """
    Returns time period types
    """
    queryset = TimePeriodType.objects.all()
    serializer_class = TimePeriodTypeSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options_noblank.html'
    list_url = 'metadb:timeperiodtype-list'
    action_url = 'metadb:timeperiodtype-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
        {'type': 'head_text', 'caption': _('Name of constant'), 'field': 'const_name'},
        {'type': 'head_text', 'caption': _('Time period type name'), 'field': 'timeperiodtypei18n.name'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-timeperiodtype-form',
        'title': _("Create a new time period type"),
        'submit_name': _("Create time period type"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-timeperiodtype-form',
        'title': _("Update time period type"),
        'submit_name': _("Update time period type"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-timeperiodtype-delete-form',
        'title': _('Confirm time period type'),
        'text': _('Are you sure you want to delete the time period type'),
        'submit_name': _('Delete time period type'),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    def __init__(self, *args, **kwargs):
        self.queryset = self.queryset.filter(
            language__code=get_language()).order_by('timeperiodtypei18n__name')


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
        ('head_select', _('Condition option-value combination')),
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
            {'name': 'combinations-url',
             'value': reverse_lazy('metadb:combination-list')},
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
            {'name': 'combinations-url',
             'value': reverse_lazy('metadb:combination-list')},
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
            vcc = vertex.condition_combination
            data.append({'id': vertex.id,
                         'computing_module': {'name': vertex.computing_module.name},
                         'condition_option': {'label': vcc.option.label if vcc else None},
                         'condition_value': {'label': vcc.option_value.label if vcc else None},
                        })

        result = {'data': data}
        response = JsonResponse(result)
        return response

    def __init__(self, *args, **kwargs):
        self.queryset = self.queryset.order_by('computing_module__name')
