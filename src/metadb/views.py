from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View

class MainView(View):

    def get(self, request):

        app_prfx = 'metadb:'
        choices = [
            {'title': _('Accumulation mode'), 'api_url': app_prfx+'accumulationmode-list',
                'create_api_url': app_prfx+'accumulationmode-detail'},
            {'title': _('Argument type'), 'api_url': app_prfx+'argumenttype-list',
                'create_api_url': app_prfx+'argumenttype-detail'},
            {'title': _('Combination'), 'api_url': app_prfx+'combination-list',
                'create_api_url': app_prfx+'combination-detail'},
            {'title': _('Computing module'), 'api_url': app_prfx+'computingmodule-list',
                'create_api_url': app_prfx+'computingmodule-detail'},
            {'title': _('Data kind'), 'api_url': app_prfx+'datakind-list',
                'create_api_url': app_prfx+'datakind-detail'},
            {'title': _('Data variable'), 'api_url': app_prfx+'datavariable-list',
                'create_api_url': app_prfx+'datavariable-detail'},
            {'title': _('File'), 'api_url': app_prfx+'file-list',
                'create_api_url': app_prfx+'file-detail'},
            {'title': _('File type'), 'api_url': app_prfx+'filetype-list',
                'create_api_url': app_prfx+'filetype-detail'},
            {'title': _('GUI element'), 'api_url': app_prfx+'guielement-list',
                'create_api_url': app_prfx+'guielement-detail'},
            {'title': _('Language'), 'api_url': app_prfx+'language-list',
                'create_api_url': app_prfx+'language-detail'},
            {'title': _('Level'), 'api_url': app_prfx+'level-list',
                'create_api_url': app_prfx+'level-detail'},
            {'title': _('Levels group'), 'api_url': app_prfx+'levelsgroup-list',
                'create_api_url': app_prfx+'levelsgroup-detail'},
            {'title': _('Levels variable'), 'api_url': app_prfx+'levelsvariable-list',
                'create_api_url': app_prfx+'levelsvariable-detail'},
            {'title': _('Option'), 'api_url': app_prfx+'option-list',
                'create_api_url': app_prfx+'option-detail'},
            {'title': _('Option value'), 'api_url': app_prfx+'optionvalue-list',
                'create_api_url': app_prfx+'optionvalue-detail'},
            {'title': _('Organization'), 'api_url': app_prfx+'organization-list',
                'create_api_url': app_prfx+'organization-detail'},
            {'title': _('Meteorological parameter'), 'api_url': app_prfx+'parameter-list',
                'create_api_url': app_prfx+'parameter-detail'},
            {'title': _('Property'), 'api_url': app_prfx+'property-list',
                'create_api_url': app_prfx+'property-detail'},
            {'title': _('Property value'), 'api_url': app_prfx+'propertyvalue-list',
                'create_api_url': app_prfx+'propertyvalue-detail'},
            {'title': _('Resolution'), 'api_url': app_prfx+'resolution-list',
                'create_api_url': app_prfx+'resolution-detail'},
            {'title': _('Root directory'), 'api_url': app_prfx+'rootdir-list',
                'create_api_url': app_prfx+'rootdir-detail'},
            {'title': _('Scenario'), 'api_url': app_prfx+'scenario-list',
                'create_api_url': app_prfx+'scenario-detail'},
#            {'title': _('Setting'), 'api_url': app_prfx+'fullsetting-list',
#                'create_api_url': app_prfx+'fullsetting-detail'},
            {'title': _('Time step'), 'api_url': app_prfx+'timestep-list',
                'create_api_url': app_prfx+'timestep-detail'},
            {'title': _('Measurement unit'), 'api_url': app_prfx+'units-list',
                'create_api_url': app_prfx+'units-detail'},
            {'title': _('Time period type'), 'api_url': app_prfx+'timeperiodtype-list',
                'create_api_url': app_prfx+'timeperiodtype-detail'},
            {'title': _('Variable'), 'api_url': app_prfx+'variable-list',
                'create_api_url': app_prfx+'variable-detail'},
        ]

        tabs = [
            { 'name': "collection", 'label': _("Collection"),
              'list_url': 'metadb:collection-list', 'detail_url': 'metadb:collection-detail' },
            { 'name': "dataset", 'label': _("Dataset"),
              'list_url': 'metadb:dataset-list', 'detail_url': 'metadb:dataset-detail' },
            { 'name': "specpar", 'label': _("Parameter"),
              'list_url': 'metadb:specificparameter-list', 'detail_url': 'metadb:specificparameter-detail' },
            { 'name': "data", 'label': _("Data"),
              'list_url': 'metadb:data-list', 'detail_url': 'metadb:data-detail' },
            { 'name': "conveyor", 'label': _("Conveyor"),
              'list_url': 'metadb:conveyor-list', 'detail_url': 'metadb:conveyor-detail' },
            { 'name': "dataarggroup", 'label': _("Data-arguments"),
              'list_url': 'metadb:dataargumentsgroup-list', 'detail_url': 'metadb:dataargumentsgroup-detail' },
            { 'name': "procarggroup", 'label': _("Processors-arguments"),
              'list_url': 'metadb:argumentsgrouphasprocessor-list', 'detail_url': 'metadb:argumentsgrouphasprocessor-detail' },
            { 'name': "setting", 'label': _("Setting"),
              'list_url': 'metadb:fullsetting-list', 'detail_url': 'metadb:fullsetting-detail' },
            { 'name': "processor", 'label': _("Processor"),
              'list_url': 'metadb:processor-list', 'detail_url': 'metadb:processor-detail' },
            { 'name': "other", 'label': _("Other") },
        ]

        ctx = {
            'choices': choices, 'tabs': tabs,
        }
        return render(request, 'metadb/main_view.html', context=ctx)
