from django.urls import include, path
from rest_framework import routers

from .views import MainView

from .simple_views import *

from .form_loads import *

from .apiviews import *
from .collection_views import (CollectionCreateView, CollectionDeleteView,
                               CollectionUpdateView)
from .conveyor_views import (ConveyorCreateView, ConveyorDeleteView,
                               ConveyorUpdateView)
from .dataset_views import (DatasetCreateView, DatasetDeleteView,
                            DatasetUpdateView)
from .specpar_views import (SpecificParameterCreateView, SpecificParameterDeleteView,
                            SpecificParameterUpdateView)
from .data_views import (DataCreateView, DataDeleteView, DataUpdateView)
from .organization_views import (OrganizationCreateView, OrganizationUpdateView,
                                 OrganizationDeleteView)
from .unit_views import (UnitCreateView, UnitUpdateView, UnitDeleteView)
from .guielement_views import (GuiElementCreateView, GuiElementUpdateView,
                               GuiElementDeleteView)
from .parameter_views import (ParameterCreateView, ParameterUpdateView,
                              ParameterDeleteView)
from .timestep_views import (TimeStepCreateView, TimeStepUpdateView,
                             TimeStepDeleteView)
from .levelsgroup_views import (LevelsGroupCreateView, LevelsGroupUpdateView,
                                LevelsGroupDeleteView)
from .level_views import (LevelCreateView, LevelUpdateView,
                                LevelDeleteView)

router = routers.DefaultRouter()
router.register('collections', CollectionViewSet)
router.register('organizations', OrganizationViewSet)

app_name = 'metadb'
urlpatterns = [
    path('', MainView.as_view(), name='main_view'),
    path('', include(router.urls)),

    # Form elements content loaders

    path('collections/form/load-organizations/', load_organizations, name='form_load_organizations'),
    path('datasets/form/load-collections/', load_collections, name='form_load_collections'),
    path('datasets/form/load-resolutions/', load_resolutions, name='form_load_resolutions'),
    path('datasets/form/load-scenarios/', load_scenarios, name='form_load_scenarios'),
    path('datasets/form/load-datakinds/', load_datakinds, name='form_load_datakinds'),
    path('datasets/form/load-filetypes/', load_filetypes, name='form_load_filetypes'),
    path('specpars/form/load-parameters/', load_parameters, name='form_load_parameters'),
    path('specpars/form/load-timesteps/', load_timesteps, name='form_load_timesteps'),
    path('specpars/form/load-lvsgroups/', load_lvsgroups, name='form_load_lvsgroups'),
    path('specpars/form/load-lvsnames/', load_lvsgroup_lvsnames, name='sp_form_load_lvsgroup_lvsnames'),
    path('specpars/form/load-levels/', load_levels, name='form_load_levels'),
    path('specpars/form/load-accmodes/', load_accmodes, name='form_load_accmodes'),
    path('data/form/load-resolutions/', load_dataset_resolutions, name='form_load_dataset_resolutions'),
    path('data/form/load-scenarios/', load_dataset_scenarios, name='form_load_dataset_scenarios'),
    path('data/form/load-timesteps/', load_parameter_timesteps, name='form_load_parameter_timesteps'),
    path('data/form/load-lvsgroups/', load_parameter_lvsgroups, name='form_load_parameter_lvsgroups'),
    path('data/form/load-lvsnames/', load_lvsgroup_lvsnames, name='form_load_lvsgroup_lvsnames'),
    path('data/form/load-lvsvars/', load_lvsvars, name='form_load_lvsvars'),
    path('data/form/load-variables/', load_variables, name='form_load_variables'),
    path('data/form/load-units/', load_units, name='form_load_units'),
    path('data/form/load-properties/', load_properties, name='form_load_properties'),
    path('data/form/load-propvals/', load_propvals, name='form_load_propvals'),
    path('data/form/load-rootdirs/', load_rootdirs, name='form_load_rootdirs'),
    path('data/form/load-files/', load_files, name='form_load_files'),
    path('data/form/load-guielements/', load_guielements, name='form_load_guielements'),


    # CRUDs

    path('accmodes/create/', AccumulationModeCreateView.as_view(), name='accmode_create'),
    path('accmodes/api/', AccumulationModeApiListView.as_view(), name='accmodes_api'),
    path('accmodes/<int:pk>/update/', AccumulationModeUpdateView.as_view(), name='accmode_update'),
    path('accmodes/<int:pk>/delete/', AccumulationModeDeleteView.as_view(), name='accmode_delete'),

#    path('argumentsgroups/create/', ArgumentsGroupCreateView.as_view(), name='argsgroup_create'),
#    path('argumentsgroups/<int:pk>/update/', ArgumentsGroupUpdateView.as_view(), name='argsgroup_update'),
#    path('argumentsgroups/<int:pk>/delete/', ArgumentsGroupDeleteView.as_view(), name='argsgroup_delete'),

#    path('argumenttypes/create/', ArgumentTypeCreateView.as_view(), name='argtype_create'),
#    path('argumenttypes/<int:pk>/update/', ArgumentTypeUpdateView.as_view(), name='argtype_update'),
#    path('argumenttypes/<int:pk>/delete/', ArgumentTypeDeleteView.as_view(), name='argtype_delete'),

#    path('collection/create/', CollectionCreateView.as_view(), name='collection_create'),
#    path('collections/api/', CollectionApiListView.as_view(), name='collections_api'),
    path('collection/<int:pk>/update/', CollectionUpdateView.as_view(), name='collection_update'),
    path('collection/<int:pk>/delete/', CollectionDeleteView.as_view(), name='collection_delete'),

#    path('computingmodules/create/', ComputingModuleCreateView.as_view(), name='computing_module_create'),
#    path('computingmodules/<int:pk>/update/', ComputingModuleUpdateView.as_view(), name='computing_module_update'),
#    path('computingmodules/<int:pk>/delete/', ComputingModuleDeleteView.as_view(), name='computing_module_delete'),

    path('conveyors/create/', ConveyorCreateView.as_view(), name='conveyor_create'),
    path('conveyors/', ConveyorApiListView.as_view(), name='conveyor_api'),
    path('conveyors/<int:pk>/update/', ConveyorUpdateView.as_view(), name='conveyor_update'),
    path('conveyors/<int:pk>/delete/', ConveyorDeleteView.as_view(), name='conveyor_delete'),

    path('data/create/', DataCreateView.as_view(), name='data_create'),
    path('data/api/', DataApiListView.as_view(), name='data_api'),
    path('data/<int:pk>/update/', DataUpdateView.as_view(), name='data_update'),
    path('data/<int:pk>/delete/', DataDeleteView.as_view(), name='data_delete'),

    path('datakinds/create/', DataKindCreateView.as_view(), name='datakind_create'),
    path('datakinds/api/', DataKindApiListView.as_view(), name='datakinds_api'),
    path('datakinds/<int:pk>/update/', DataKindUpdateView.as_view(), name='datakind_update'),
    path('datakinds/<int:pk>/delete/', DataKindDeleteView.as_view(), name='datakind_delete'),

    path('datasets/create/', DatasetCreateView.as_view(), name='dataset_create'),
    path('datasets/api/', DatasetApiListView.as_view(), name='datasets_api'),
    path('datasets/<int:pk>/update/', DatasetUpdateView.as_view(), name='dataset_update'),
    path('datasets/<int:pk>/delete/', DatasetDeleteView.as_view(), name='dataset_delete'),

#    path('datavars/create/', DataVariableCreateView.as_view(), name='data_variable_create'),
#    path('datavars/<int:pk>/update/', DataVariableUpdateView.as_view(), name='data_variable_update'),
#    path('datavars/<int:pk>/delete/', DataVariableDeleteView.as_view(), name='data_variable_delete'),

#    path('edges/create/', EdgeCreateView.as_view(), name='edge_create'),
#    path('edges/<int:pk>/update/', EdgeUpdateView.as_view(), name='edge_update'),
#    path('edges/<int:pk>/delete/', EdgeDeleteView.as_view(), name='edge_delete'),

    path('files/create/', FileCreateView.as_view(), name='file_create'),
    path('files/api/', FileApiListView.as_view(), name='files_api'),
    path('files/<int:pk>/update/', FileUpdateView.as_view(), name='file_update'),
    path('files/<int:pk>/delete/', FileDeleteView.as_view(), name='file_delete'),

    path('filetypes/create/', FileTypeCreateView.as_view(), name='filetype_create'),
    path('filetypes/api/', FileTypeApiListView.as_view(), name='filetypes_api'),
    path('filetypes/<int:pk>/update/', FileTypeUpdateView.as_view(), name='filetype_update'),
    path('filetypes/<int:pk>/delete/', FileTypeDeleteView.as_view(), name='filetype_delete'),

    path('guielements/create/', GuiElementCreateView.as_view(), name='gui_element_create'),
    path('guielements/api/', GuiElementApiListView.as_view(), name='gui_elements_api'),
    path('guielements/<int:pk>/update/', GuiElementUpdateView.as_view(), name='gui_element_update'),
    path('guielements/<int:pk>/delete/', GuiElementDeleteView.as_view(), name='gui_element_delete'),

    path('languages/create/', LanguageCreateView.as_view(), name='language_create'),
    path('languages/api/', LanguageApiListView.as_view(), name='languages_api'),
    path('languages/<int:pk>/update/', LanguageUpdateView.as_view(), name='language_update'),
    path('languages/<int:pk>/delete/', LanguageDeleteView.as_view(), name='language_delete'),

    path('levels/create/', LevelCreateView.as_view(), name='level_create'),
    path('levels/api/', LevelApiListView.as_view(), name='levels_api'),
    path('levels/<int:pk>/update/', LevelUpdateView.as_view(), name='level_update'),
    path('levels/<int:pk>/delete/', LevelDeleteView.as_view(), name='level_delete'),

    path('levelsgroups/create/', LevelsGroupCreateView.as_view(), name='levels_group_create'),
    path('levelsgroups/api/', LevelsGroupApiListView.as_view(), name='levels_groups_api'),
    path('levelsgroups/<int:pk>/update/', LevelsGroupUpdateView.as_view(), name='levels_group_update'),
    path('levelsgroups/<int:pk>/delete/', LevelsGroupDeleteView.as_view(), name='levels_group_delete'),

    path('levelsvariables/create/', LevelsVariableCreateView.as_view(), name='levels_variable_create'),
    path('levelsvariables/api/', LevelsVariableApiListView.as_view(), name='levels_variables_api'),
    path('levelsvariables/<int:pk>/update/', LevelsVariableUpdateView.as_view(), name='levels_variable_update'),
    path('levelsvariables/<int:pk>/delete/', LevelsVariableDeleteView.as_view(), name='levels_variable_delete'),

    path('organization/create/', OrganizationCreateView.as_view(), name='organization_create'),
#    path('organizations/api/', OrganizationApiListView.as_view(), name='organizations_api'),
    path('organization/<int:pk>/update/', OrganizationUpdateView.as_view(), name='organization_update'),
    path('organization/<int:pk>/delete/', OrganizationDeleteView.as_view(), name='organization_delete'),

#    path('options/create/', OptionCreateView.as_view(), name='option_create'),
#    path('options/<int:pk>/update/', OptionUpdateView.as_view(), name='option_update'),
#    path('options/<int:pk>/delete/', OptionDeleteView.as_view(), name='option_delete'),

#    path('optionsovers/create/', OptionsOverrideCreateView.as_view(), name='options_overs_create'),
#    path('optionsovers/<int:pk>/update/', OptionsOverrideUpdateView.as_view(), name='options_overs_update'),
#    path('optionsovers/<int:pk>/delete/', OptionsOverrideDeleteView.as_view(), name='options_overs_delete'),

#    path('optionvalues/create/', OptionValueCreateView.as_view(), name='option_value_create'),
#    path('optionvalues/<int:pk>/update/', OptionValueUpdateView.as_view(), name='option_value_update'),
#    path('optionvalues/<int:pk>/delete/', OptionValueDeleteView.as_view(), name='option_value_delete'),

    path('parameters/create/', ParameterCreateView.as_view(), name='parameter_create'),
    path('parameters/api/', ParameterApiListView.as_view(), name='parameters_api'),
    path('parameters/<int:pk>/update/', ParameterUpdateView.as_view(), name='parameter_update'),
    path('parameters/<int:pk>/delete/', ParameterDeleteView.as_view(), name='parameter_delete'),

    path('properties/create/', PropertyCreateView.as_view(), name='property_create'),
    path('properties/api/', PropertyApiListView.as_view(), name='properties_api'),
    path('properties/<int:pk>/update/', PropertyUpdateView.as_view(), name='property_update'),
    path('properties/<int:pk>/delete/', PropertyDeleteView.as_view(), name='property_delete'),

#    path('processors/create/', ProcessorCreateView.as_view(), name='processor_create'),
#    path('processors/<int:pk>/update/', ProcessorUpdateView.as_view(), name='processor_update'),
#    path('processors/<int:pk>/delete/', ProcessorDeleteView.as_view(), name='processor_delete'),

#    path('processorshasargs/create/', ProcessorHasArgsCreateView.as_view(), name='processor_has_args_create'),
#    path('processorshasargs/<int:pk>/update/', ProcessorHasArgsUpdateView.as_view(), name='processor_has_args_update'),
#    path('processorshasargs/<int:pk>/delete/', ProcessorHasArgsDeleteView.as_view(), name='processor_has_args_delete'),

#    path('processorshasopts/create/', ProcessorHasOptsCreateView.as_view(), name='processor_has_opts_create'),
#    path('processorshasopts/<int:pk>/update/', ProcessorHasOptsUpdateView.as_view(), name='processor_has_opts_update'),
#    path('processorshasopts/<int:pk>/delete/', ProcessorHasOptsDeleteView.as_view(), name='processor_has_opts_delete'),

    path('propertyvalues/create/', PropertyValueCreateView.as_view(), name='property_value_create'),
    path('propertyvalues/api/', PropertyValueApiListView.as_view(), name='property_values_api'),
    path('propertyvalues/<int:pk>/update/', PropertyValueUpdateView.as_view(), name='property_value_update'),
    path('propertyvalues/<int:pk>/delete/', PropertyValueDeleteView.as_view(), name='property_value_delete'),

    path('resolutions/create/', ResolutionCreateView.as_view(), name='resolution_create'),
    path('resolutions/api/', ResolutionApiListView.as_view(), name='resolutions_api'),
    path('resolutions/<int:pk>/update/', ResolutionUpdateView.as_view(), name='resolution_update'),
    path('resolutions/<int:pk>/delete/', ResolutionDeleteView.as_view(), name='resolution_delete'),

    path('rootdirs/create/', RootDirCreateView.as_view(), name='root_dir_create'),
    path('rootdirs/api/', RootDirApiListView.as_view(), name='root_dirs_api'),
    path('rootdirs/<int:pk>/update/', RootDirUpdateView.as_view(), name='root_dir_update'),
    path('rootdirs/<int:pk>/delete/', RootDirDeleteView.as_view(), name='root_dir_delete'),

    path('scenarios/create/', ScenarioCreateView.as_view(), name='scenario_create'),
    path('scenarios/api/', ScenarioApiListView.as_view(), name='scenarios_api'),
    path('scenarios/<int:pk>/update/', ScenarioUpdateView.as_view(), name='scenario_update'),
    path('scenarios/<int:pk>/delete/', ScenarioDeleteView.as_view(), name='scenario_delete'),

    path('specpars/create/', SpecificParameterCreateView.as_view(), name='specpar_create'),
    path('specpars/api/', SpecificParameterApiListView.as_view(), name='specpars_api'),
    path('specpars/<int:pk>/update/', SpecificParameterUpdateView.as_view(), name='specpar_update'),
    path('specpars/<int:pk>/delete/', SpecificParameterDeleteView.as_view(), name='specpar_delete'),

#    path('tptypes/create/', TimePeriodTypeCreateView.as_view(), name='time_period_type_create'),
#    path('tptypes/<int:pk>/update/', TimePeriodTypeUpdateView.as_view(), name='time_period_type_update'),
#    path('tptypes/<int:pk>/delete/', TimePeriodTypeDeleteView.as_view(), name='time_period_type_delete'),

    path('timesteps/create/', TimeStepCreateView.as_view(), name='time_step_create'),
    path('timesteps/api/', TimeStepApiListView.as_view(), name='time_steps_api'),
    path('timesteps/<int:pk>/update/', TimeStepUpdateView.as_view(), name='time_step_update'),
    path('timesteps/<int:pk>/delete/', TimeStepDeleteView.as_view(), name='time_step_delete'),

    path('units/create/', UnitCreateView.as_view(), name='unit_create'),
    path('units/api/', UnitApiListView.as_view(), name='units_api'),
    path('units/<int:pk>/update/', UnitUpdateView.as_view(), name='unit_update'),
    path('units/<int:pk>/delete/', UnitDeleteView.as_view(), name='unit_delete'),

    path('variables/create/', VariableCreateView.as_view(), name='variable_create'),
    path('variables/api/', VariableApiListView.as_view(), name='variables_api'),
    path('variables/<int:pk>/update/', VariableUpdateView.as_view(), name='variable_update'),
    path('variables/<int:pk>/delete/', VariableDeleteView.as_view(), name='variable_delete'),

#    path('vertices/create/', VertexCreateView.as_view(), name='vertex_create'),
#    path('vertices/<int:pk>/update/', VertexUpdateView.as_view(), name='vertex_update'),
#    path('vertices/<int:pk>/delete/', VertexDeleteView.as_view(), name='vertex_delete'),


]
