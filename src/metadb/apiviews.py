from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import *
from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed
from django.utils.translation import get_language, gettext_lazy as _
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse

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
        action = request.META.get('HTTP_ACTION')
        serializer = self.get_serializer(self.get_queryset(), many=True)
        ctx = {'data': serializer.data}

        if action == 'options_list' or request.GET.get('format') == 'html':
            result = render(request, self.options_template_name, ctx)
        else:
            if isinstance(request.accepted_renderer, JSONRenderer):
                ctx['headers'] = self.table_headers
            result = Response(ctx)

        return result

    def retrieve(self, request, pk=None):
        action = request.META.get('HTTP_ACTION')
        if action == 'create':
            instance = None
        elif action == 'update' or action == 'delete' or pk is not None:
            instance = self.get_queryset().filter(pk=pk).first()
        else:
            raise MethodNotAllowed(action, detail='Unknown action')
        serializer = self.get_serializer(instance)

        if isinstance(request.accepted_renderer, BrowsableAPIRenderer) or action == 'json':
            response = Response({'data': serializer.data})
        else:
            if action == 'create':
                ctx = self.ctx_create
                ctx['action'] = reverse(self.list_url)
            elif action == 'update':
                ctx = self.ctx_update
                ctx['action'] = reverse(self.action_url, kwargs={'pk': pk})
            elif action == 'delete':
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


class ConveyorApiListView(APIView):
    """
    Returns conveyors
    """
    def get(self, request):
        language = get_language()

        edges = Edge.objects.all()
        data = {'data': []}
        for edge in edges:
            data['data'].append(
                {
                    'conveyor_id': edge.conveyor.id,
                    'edge_id': edge.id,
                    'from_vertex_id': edge.from_vertex.id,
                    'from_module': edge.from_vertex.computing_module.name,
                    'from_option': edge.from_vertex.condition_option.label,
                    'from_option_value': edge.from_vertex.condition_value.label,
                    'from_output': edge.from_output,
                    'to_vertex_id': edge.to_vertex.id,
                    'to_module': edge.to_vertex.computing_module.name,
                    'to_option': edge.to_vertex.condition_option.label,
                    'to_option_value': edge.to_vertex.condition_value.label,
                    'to_input': edge.to_input,
                    'data_label': edge.data_variable.label,
                    'data_description': edge.data_variable.description,
                    'units': edge.data_variable.units.unitsi18n_set.filter(language__code=language).get().name,
                }
            )
        data['headers'] = [
            ('head_select', _('Conveyor id')),
            ('head_none', _('Edge id')),
            ('head_none', _('Source vertex id')),
            ('head_none', _('Source module')),
            ('head_none', _('Source condition option')),
            ('head_none', _('Source condition value')),
            ('head_none', _('Source module output')),
            ('head_none', _('Target vertex id')),
            ('head_none', _('Target module')),
            ('head_none', _('Target condition option')),
            ('head_none', _('Target condition value')),
            ('head_none', _('Target module input')),
            ('head_none', _('Data label')),
            ('head_none', _('Data description')),
            ('head_none', _('Data units')),
        ]

        return Response(data)


class ConveyorViewSet(BaseViewSet):
    """
    Returns conveyors
    """
    queryset = Conveyor.objects.all()
    serializer_class = ConveyorSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
    list_url = 'metadb:conveyor-list'
    action_url = 'metadb:conveyor-detail'

    table_headers = [
        {'type': 'head_none', 'caption': _('Id'), 'field': 'id'},
    ]

    ctx_create = {
        'method': 'POST',
        'form_class': 'js-conveyor-form',
        'title': _("Create a new conveyor"),
        'submit_name': _("Create conveyor"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_update = {
        'method': 'PUT',
        'form_class': 'js-conveyor-form',
        'title': _("Update conveyor"),
        'submit_name': _("Update conveyor"),
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
        action = request.META.get('HTTP_ACTION')
        qset = self.get_queryset()
        parameter_id = request.GET.get('parameterId')
        time_step_id = request.GET.get('timestepId')
        if parameter_id and time_step_id:
            qset = qset.filter(specificparameter__parameter_id=parameter_id,
                               specificparameter__time_step_id=time_step_id)
        serializer = self.get_serializer(qset, many=True)
        ctx = {'data': serializer.data}

        if action == 'options_list' or request.GET.get('format') == 'html':
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
             'value': reverse_lazy('metadb:form_load_guielements')},
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
             'value': reverse_lazy('metadb:form_load_guielements')},
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
    queryset = OptionValue.objects.all()
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

    def __init__(self, *args, **kwargs):
        self.queryset = self.queryset.filter(
            language__code=get_language()).order_by('optionvaluei18n__name')




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
        ('head_select', _('Levels group units')),
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
        action = request.META.get('HTTP_ACTION')
        qset = self.get_queryset()
        parameter_id = request.GET.get('parameterId')
        if parameter_id:
            qset = qset.filter(specificparameter__parameter_id=parameter_id).distinct()
        serializer = self.get_serializer(qset, many=True)
        ctx = {'data': serializer.data}

        if action == 'options_list' or request.GET.get('format') == 'html':
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
        'submit_name': _("Update units"),
        'style': {'template_pack': 'rest_framework/vertical/'}
    }

    ctx_delete = {
        'method': 'DELETE',
        'form_class': 'js-unit-delete-form',
        'title': _('Confirm measurement unit delete'),
        'text': _('Are you sure you want to delete the unit'),
        'submit_name': _('Delete units'),
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
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    template_name = 'metadb/includes/rest_form.html'
    options_template_name = 'metadb/hr/dropdown_list_options.html'
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
            {'name': 'computingmodule-url',
             'value': reverse_lazy('metadb:computingmodule-list')},
            {'name': 'option-url',
             'value': reverse_lazy('metadb:option-list')},
            {'name': 'optionvalue-url',
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
            {'name': 'computingmodule-url',
             'value': reverse_lazy('metadb:computingmodule-list')},
            {'name': 'option-url',
             'value': reverse_lazy('metadb:option-list')},
            {'name': 'optionvalue-url',
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

