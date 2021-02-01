from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View

class MainView(View):

    def get(self, request):

        app_prfx = 'metadb:'
        choices = [
            {'title': _('Accumulation mode'), 'api_url': app_prfx+'accumulationmode-list'},

            {'title': _('Data kind'), 'api_url': app_prfx+'datakind-list'},

            {'title': _('File'), 'api_url': app_prfx+'files_api',
             'create_url': app_prfx+'file_create',
             'update_url': app_prfx+'file_update', 'delete_url': app_prfx+'file_delete'},

            {'title': _('File type'), 'api_url': app_prfx+'filetype-list'},

            {'title': _('GUI element'), 'api_url': app_prfx+'gui_elements_api',
             'create_url': app_prfx+'gui_element_create',
             'update_url': app_prfx+'gui_element_update', 'delete_url': app_prfx+'gui_element_delete'},

            {'title': _('Language'), 'api_url': app_prfx+'languages_api',
             'create_url': app_prfx+'language_create',
             'update_url': app_prfx+'language_update', 'delete_url': app_prfx+'language_delete'},

            {'title': _('Level'), 'api_url': app_prfx+'level-list'},

            {'title': _('Levels group'), 'api_url': app_prfx+'levelsgroup-list'},

            {'title': _('Levels variable'), 'api_url': app_prfx+'levels_variables_api',
             'create_url': app_prfx+'levels_variable_create',
             'update_url': app_prfx+'levels_variable_update', 'delete_url': app_prfx+'levels_variable_delete'},

            {'title': _('Organization'), 'api_url': app_prfx+'organization-list'},

            {'title': _('Meteorological parameter'), 'api_url': app_prfx+'parameter-list'},

            {'title': _('Property'), 'api_url': app_prfx+'properties_api',
             'create_url': app_prfx+'property_create',
             'update_url': app_prfx+'property_update', 'delete_url': app_prfx+'property_delete'},

            {'title': _('Property value'), 'api_url': app_prfx+'property_values_api',
             'create_url': app_prfx+'property_value_create',
             'update_url': app_prfx+'property_value_update', 'delete_url': app_prfx+'property_value_delete'},

            {'title': _('Resolution'), 'api_url': app_prfx+'resolution-list'},

            {'title': _('Root directory'), 'api_url': app_prfx+'root_dirs_api',
             'create_url': app_prfx+'root_dir_create',
             'update_url': app_prfx+'root_dir_update', 'delete_url': app_prfx+'root_dir_delete'},

            {'title': _('Scenario'), 'api_url': app_prfx+'scenario-list'},

            {'title': _('Time step'), 'api_url': app_prfx+'timestep-list'},

            {'title': _('Measurement unit'), 'api_url': app_prfx+'units-list'},

            {'title': _('Variable'), 'api_url': app_prfx+'variables_api',
             'create_url': app_prfx+'variable_create',
             'update_url': app_prfx+'variable_update', 'delete_url': app_prfx+'variable_delete'},
        ]

        ctx = {
            'choices': choices,
        }
        return render(request, 'metadb/main_view.html', context=ctx)
