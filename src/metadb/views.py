from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View

class MainView(View):

    def get(self, request):

        # Datatable Collection headers
        collection_headers = [
            ('head_none', 'Id'),
            ('head_select', _('Collection label')),
            ('head_select', _('Collection name')),
            ('head_text', _('Collection description')),
            ('head_select', _('Organization')),
            ('head_text', _('Organization URL')),
            ('head_text', _('Collection URL'))
        ]

        # Datatable Dataset headers
        dataset_headers = [
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

        # Datatable Specific parameter headers
        specpar_headers = [
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

        # Datatable Data headers
        data_headers = [
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
            ('head_none', _('File name pattern')),
            ('head_none', _('Scale')),
            ('head_none', _('Offset')),
        ]

        ctx = {
            'collection_headers': collection_headers,
            'dataset_headers': dataset_headers,
            'specpar_headers': specpar_headers,
            'data_headers': data_headers,
        }
        return render(request, 'metadb/main_view.html', context=ctx)
