from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View

class MainView(View):

    def get(self, request):

        app_prfx = 'metadb:'
        choices = [
            {'title': _('Accumulation mode'), 'api_url': app_prfx+'accumulationmode-list'},
            {'title': _('Data kind'), 'api_url': app_prfx+'datakind-list'},
            {'title': _('File'), 'api_url': app_prfx+'file-list'},
            {'title': _('File type'), 'api_url': app_prfx+'filetype-list'},
            {'title': _('GUI element'), 'api_url': app_prfx+'guielement-list'},
            {'title': _('Language'), 'api_url': app_prfx+'language-list'},
            {'title': _('Level'), 'api_url': app_prfx+'level-list'},
            {'title': _('Levels group'), 'api_url': app_prfx+'levelsgroup-list'},
            {'title': _('Levels variable'), 'api_url': app_prfx+'variable-list'},
            {'title': _('Organization'), 'api_url': app_prfx+'organization-list'},
            {'title': _('Meteorological parameter'), 'api_url': app_prfx+'parameter-list'},
            {'title': _('Property'), 'api_url': app_prfx+'property-list'},
            {'title': _('Property value'), 'api_url': app_prfx+'propertyvalue-list'},
            {'title': _('Resolution'), 'api_url': app_prfx+'resolution-list'},
            {'title': _('Root directory'), 'api_url': app_prfx+'rootdir-list'},
            {'title': _('Scenario'), 'api_url': app_prfx+'scenario-list'},
            {'title': _('Time step'), 'api_url': app_prfx+'timestep-list'},
            {'title': _('Measurement unit'), 'api_url': app_prfx+'units-list'},
            {'title': _('Variable'), 'api_url': app_prfx+'variable-list'},
        ]

        ctx = {
            'choices': choices,
        }
        return render(request, 'metadb/main_view.html', context=ctx)
