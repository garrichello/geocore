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
            ('head_text', _('Scenario subpath')),
            ('head_text', _('Resolution subpath')),
            ('head_text', _('Time step subpath')),
            ('head_none', _('File name pattern')),
            ('head_none', _('Scale')),
            ('head_none', _('Offset')),
        ]

        app_prfx = 'metadb:'
        choices = [
            {'title': 'Accumulation mode', 'api_url': app_prfx+'accmodes_api',
             'create_url': app_prfx+'accmode_create', 
             'update_url': app_prfx+'accmode_update', 'delete_url': app_prfx+'accmode_delete'},

            {'title': 'Data kinds', 'api_url': app_prfx+'datakinds_api',
             'create_url': app_prfx+'datakind_create', 
             'update_url': app_prfx+'datakind_update', 'delete_url': app_prfx+'datakind_delete'},

            {'title': 'Files', 'api_url': app_prfx+'files_api',
             'create_url': app_prfx+'file_create', 
             'update_url': app_prfx+'file_update', 'delete_url': app_prfx+'file_delete'},

            {'title': 'File types', 'api_url': app_prfx+'filetypes_api',
             'create_url': app_prfx+'filetype_create', 
             'update_url': app_prfx+'filetype_update', 'delete_url': app_prfx+'filetype_delete'},

            {'title': 'GUI elements', 'api_url': app_prfx+'gui_elements_api',
             'create_url': app_prfx+'gui_element_create', 
             'update_url': app_prfx+'gui_element_update', 'delete_url': app_prfx+'gui_element_delete'},

            {'title': 'Languages', 'api_url': app_prfx+'languages_api',
             'create_url': app_prfx+'language_create', 
             'update_url': app_prfx+'language_update', 'delete_url': app_prfx+'language_delete'},

            {'title': 'Levels', 'api_url': app_prfx+'levels_api',
             'create_url': app_prfx+'level_create', 
             'update_url': app_prfx+'level_update', 'delete_url': app_prfx+'level_delete'},

            {'title': 'Levels groups', 'api_url': app_prfx+'levels_groups_api',
             'create_url': app_prfx+'levels_group_create', 
             'update_url': app_prfx+'levels_group_update', 'delete_url': app_prfx+'levels_group_delete'},

            {'title': 'Levels variables', 'api_url': app_prfx+'levels_variables_api',
             'create_url': app_prfx+'levels_variable_create', 
             'update_url': app_prfx+'levels_variable_update', 'delete_url': app_prfx+'levels_variable_delete'},

            {'title': 'Organizations', 'api_url': app_prfx+'organizations_api',
             'create_url': app_prfx+'organization_create', 
             'update_url': app_prfx+'organization_update', 'delete_url': app_prfx+'organization_delete'},

            {'title': 'Parameters', 'api_url': app_prfx+'parameters_api',
             'create_url': app_prfx+'parameter_create', 
             'update_url': app_prfx+'parameter_update', 'delete_url': app_prfx+'parameter_delete'},

            {'title': 'Properties', 'api_url': app_prfx+'properties_api',
             'create_url': app_prfx+'property_create', 
             'update_url': app_prfx+'property_update', 'delete_url': app_prfx+'property_delete'},

            {'title': 'Property values', 'api_url': app_prfx+'property_values_api',
             'create_url': app_prfx+'property_value_create', 
             'update_url': app_prfx+'property_value_update', 'delete_url': app_prfx+'property_value_delete'},

            {'title': 'Resolutions', 'api_url': app_prfx+'resolutions_api',
             'create_url': app_prfx+'resolution_create', 
             'update_url': app_prfx+'resolution_update', 'delete_url': app_prfx+'resolution_delete'},

            {'title': 'Root diresctories', 'api_url': app_prfx+'root_dirs_api',
             'create_url': app_prfx+'root_dir_create', 
             'update_url': app_prfx+'root_dir_update', 'delete_url': app_prfx+'root_dir_delete'},

            {'title': 'Scenarios', 'api_url': app_prfx+'scenarios_api',
             'create_url': app_prfx+'scenario_create', 
             'update_url': app_prfx+'scenario_update', 'delete_url': app_prfx+'scenario_delete'},

            {'title': 'Time steps', 'api_url': app_prfx+'time_steps_api',
             'create_url': app_prfx+'time_step_create', 
             'update_url': app_prfx+'time_step_update', 'delete_url': app_prfx+'time_step_delete'},

            {'title': 'Units', 'api_url': app_prfx+'units_api',
             'create_url': app_prfx+'unit_create', 
             'update_url': app_prfx+'unit_update', 'delete_url': app_prfx+'unit_delete'},

            {'title': 'Variables', 'api_url': app_prfx+'variables_api',
             'create_url': app_prfx+'variable_create', 
             'update_url': app_prfx+'variable_update', 'delete_url': app_prfx+'variable_delete'},
        ]

        ctx = {
            'collection_headers': collection_headers,
            'dataset_headers': dataset_headers,
            'specpar_headers': specpar_headers,
            'data_headers': data_headers,
            'choices': choices,
        }
        return render(request, 'metadb/main_view.html', context=ctx)
