from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View

class MainView(View):

    def get(self, request):

        app_prfx = 'metadb:'
        choices = [
            {'title': _('Accumulation mode'), 'api_url': app_prfx+'accumulationmode-list',
                'create_api_url': app_prfx+'accumulationmode-detail'},
            {'title': _('Data kind'), 'api_url': app_prfx+'datakind-list',
                'create_api_url': app_prfx+'datakind-detail'},
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
            {'title': _('Time step'), 'api_url': app_prfx+'timestep-list',
                'create_api_url': app_prfx+'timestep-detail'},
            {'title': _('Measurement unit'), 'api_url': app_prfx+'units-list',
                'create_api_url': app_prfx+'units-detail'},
            {'title': _('Variable'), 'api_url': app_prfx+'variable-list',
                'create_api_url': app_prfx+'variable-detail'},
        ]

        ctx = {
            'choices': choices,
        }
        return render(request, 'metadb/main_view.html', context=ctx)
