from django.urls import path

from .views import MainView

from .apiviews import (CollectionApiListView, DatasetApiListView, DataApiListView,
                       CollectionApiView, SpecificParameterApiListView)
from .collection_views import (CollectionCreateView, CollectionDeleteView,
                               CollectionUpdateView)
from .dataset_views import (DatasetCreateView, DatasetDeleteView,
                            DatasetUpdateView)
from .specpar_views import (SpecificParameterCreateView, SpecificParameterDeleteView,
                            SpecificParameterUpdateView)
from .data_views import (DataCreateView, DataDeleteView, DataUpdateView)

from .organization_views import (OrganizationCreateView, OrganizationUpdateView,
                                 OrganizationDeleteView)

from .resolution_views import (ResolutionCreateView, ResolutionUpdateView,
                               ResolutionDeleteView)

from .scenario_views import (ScenarioCreateView, ScenarioUpdateView,
                               ScenarioDeleteView)

from .datakind_views import (DataKindCreateView, DataKindUpdateView,
                               DataKindDeleteView)

from .filetype_views import (FileTypeCreateView, FileTypeUpdateView,
                               FileTypeDeleteView)

from .levelsvariable_views import (LevelsVariableCreateView, LevelsVariableUpdateView,
                                   LevelsVariableDeleteView)

from .variable_views import (VariableCreateView, VariableUpdateView,
                             VariableDeleteView)

from .unit_views import (UnitCreateView, UnitUpdateView, UnitDeleteView)

from .property_views import (PropertyCreateView, PropertyUpdateView,
                             PropertyDeleteView)

from .guielement_views import (GuiElementCreateView, GuiElementUpdateView,
                               GuiElementDeleteView)

from .propertyvalue_views import (PropertyValueCreateView, PropertyValueUpdateView,
                                  PropertyValueDeleteView)

from .rootdir_views import (RootDirCreateView, RootDirUpdateView,
                            RootDirDeleteView)

from .file_views import (FileCreateView, FileUpdateView, FileDeleteView)


from .parameter_views import (ParameterCreateView, ParameterUpdateView,
                              ParameterDeleteView)


from .timestep_views import (TimeStepCreateView, TimeStepUpdateView,
                             TimeStepDeleteView)

from .levelsgroup_views import (LevelsGroupCreateView, LevelsGroupUpdateView,
                                LevelsGroupDeleteView)

from .level_views import (LevelCreateView, LevelUpdateView,
                                LevelDeleteView)

from .form_loads import (load_organizations, load_collections, load_resolutions,
                         load_scenarios, load_datakinds, load_filetypes,
                         load_dataset_resolutions, load_dataset_scenarios,
                         load_parameter_lvsgroups, load_lvsgroup_lvsnames,
                         load_parameter_timesteps, load_lvsvars, load_variables,
                         load_units, load_properties, load_propvals,
                         load_rootdirs, load_files, load_guielements,
                         load_parameters, load_timesteps, load_lvsgroups, load_levels)

app_name = 'metadb'
urlpatterns = [
    path('', MainView.as_view(), name='main_view'),
    path('collections/create/', CollectionCreateView.as_view(), name='collection_create'),
    path('collections/<int:pk>/update/', CollectionUpdateView.as_view(), name='collection_update'),
    path('collections/<int:pk>/delete/', CollectionDeleteView.as_view(), name='collection_delete'),
    path('collections/api/', CollectionApiListView.as_view(), name='collections_api'),
    path('collections/<int:pk>/api/', CollectionApiView.as_view(), name='collection_api'),
    path('collections/form/load-organizations/', load_organizations, name='form_load_organizations'),

    path('datasets/create/', DatasetCreateView.as_view(), name='dataset_create'),
    path('datasets/<int:pk>/update/', DatasetUpdateView.as_view(), name='dataset_update'),
    path('datasets/<int:pk>/delete/', DatasetDeleteView.as_view(), name='dataset_delete'),
    path('datasets/api/', DatasetApiListView.as_view(), name='datasets_api'),
    path('datasets/form/load-collections/', load_collections, name='form_load_collections'),
    path('datasets/form/load-resolutions/', load_resolutions, name='form_load_resolutions'),
    path('datasets/form/load-scenarios/', load_scenarios, name='form_load_scenarios'),
    path('datasets/form/load-datakinds/', load_datakinds, name='form_load_datakinds'),
    path('datasets/form/load-filetypes/', load_filetypes, name='form_load_filetypes'),

    path('specpars/create/', SpecificParameterCreateView.as_view(), name='specpar_create'),
    path('specpars/<int:pk>/update/', SpecificParameterUpdateView.as_view(), name='specpar_update'),
    path('specpars/<int:pk>/delete/', SpecificParameterDeleteView.as_view(), name='specpar_delete'),
    path('specpars/api/', SpecificParameterApiListView.as_view(), name='specpars_api'),
    path('specpars/form/load-parameters/', load_parameters, name='form_load_parameters'),
    path('specpars/form/load-timesteps/', load_timesteps, name='form_load_timesteps'),
    path('specpars/form/load-lvsgroups/', load_lvsgroups, name='form_load_lvsgroups'),
    path('specpars/form/load-lvsnames/', load_lvsgroup_lvsnames, name='sp_form_load_lvsgroup_lvsnames'),
    path('specpars/form/load-levels/', load_levels, name='form_load_levels'),

    path('data/create/', DataCreateView.as_view(), name='data_create'),
    path('data/<int:pk>/update/', DataUpdateView.as_view(), name='data_update'),
    path('data/<int:pk>/delete/', DataDeleteView.as_view(), name='data_delete'),
    path('data/api/', DataApiListView.as_view(), name='data_api'),

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

    path('organizations/create/', OrganizationCreateView.as_view(), name='organization_create'),
    path('organizations/<int:pk>/update/', OrganizationUpdateView.as_view(), name='organization_update'),
    path('organizations/<int:pk>/delete/', OrganizationDeleteView.as_view(), name='organization_delete'),

    path('resolutions/create/', ResolutionCreateView.as_view(), name='resolution_create'),
    path('resolutions/<int:pk>/update/', ResolutionUpdateView.as_view(), name='resolution_update'),
    path('resolutions/<int:pk>/delete/', ResolutionDeleteView.as_view(), name='resolution_delete'),

    path('scenarios/create/', ScenarioCreateView.as_view(), name='scenario_create'),
    path('scenarios/<int:pk>/update/', ScenarioUpdateView.as_view(), name='scenario_update'),
    path('scenarios/<int:pk>/delete/', ScenarioDeleteView.as_view(), name='scenario_delete'),

    path('datakinds/create/', DataKindCreateView.as_view(), name='datakind_create'),
    path('datakinds/<int:pk>/update/', DataKindUpdateView.as_view(), name='datakind_update'),
    path('datakinds/<int:pk>/delete/', DataKindDeleteView.as_view(), name='datakind_delete'),

    path('filetypes/create/', FileTypeCreateView.as_view(), name='filetype_create'),
    path('filetypes/<int:pk>/update/', FileTypeUpdateView.as_view(), name='filetype_update'),
    path('filetypes/<int:pk>/delete/', FileTypeDeleteView.as_view(), name='filetype_delete'),

    path('levelsvariables/create/', LevelsVariableCreateView.as_view(), name='levels_variable_create'),
    path('levelsvariables/<int:pk>/update/', LevelsVariableUpdateView.as_view(), name='levels_variable_update'),
    path('levelsvariables/<int:pk>/delete/', LevelsVariableDeleteView.as_view(), name='levels_variable_delete'),

    path('variables/create/', VariableCreateView.as_view(), name='variable_create'),
    path('variables/<int:pk>/update/', VariableUpdateView.as_view(), name='variable_update'),
    path('variables/<int:pk>/delete/', VariableDeleteView.as_view(), name='variable_delete'),

    path('units/create/', UnitCreateView.as_view(), name='unit_create'),
    path('units/<int:pk>/update/', UnitUpdateView.as_view(), name='unit_update'),
    path('units/<int:pk>/delete/', UnitDeleteView.as_view(), name='unit_delete'),

    path('properties/create/', PropertyCreateView.as_view(), name='property_create'),
    path('properties/<int:pk>/update/', PropertyUpdateView.as_view(), name='property_update'),
    path('properties/<int:pk>/delete/', PropertyDeleteView.as_view(), name='property_delete'),

    path('guielements/create/', GuiElementCreateView.as_view(), name='gui_element_create'),
    path('guielements/<int:pk>/update/', GuiElementUpdateView.as_view(), name='gui_element_update'),
    path('guielements/<int:pk>/delete/', GuiElementDeleteView.as_view(), name='gui_element_delete'),

    path('propertyvalues/create/', PropertyValueCreateView.as_view(), name='property_value_create'),
    path('propertyvalues/<int:pk>/update/', PropertyValueUpdateView.as_view(), name='property_value_update'),
    path('propertyvalues/<int:pk>/delete/', PropertyValueDeleteView.as_view(), name='property_value_delete'),

    path('rootdirs/create/', RootDirCreateView.as_view(), name='root_dir_create'),
    path('rootdirs/<int:pk>/update/', RootDirUpdateView.as_view(), name='root_dir_update'),
    path('rootdirs/<int:pk>/delete/', RootDirDeleteView.as_view(), name='root_dir_delete'),

    path('filenames/create/', FileCreateView.as_view(), name='file_create'),
    path('filenames/<int:pk>/update/', FileUpdateView.as_view(), name='file_update'),
    path('filenames/<int:pk>/delete/', FileDeleteView.as_view(), name='file_delete'),

    path('parameters/create/', ParameterCreateView.as_view(), name='parameter_create'),
    path('parameters/<int:pk>/update/', ParameterUpdateView.as_view(), name='parameter_update'),
    path('parameters/<int:pk>/delete/', ParameterDeleteView.as_view(), name='parameter_delete'),

    path('timesteps/create/', TimeStepCreateView.as_view(), name='time_step_create'),
    path('timesteps/<int:pk>/update/', TimeStepUpdateView.as_view(), name='time_step_update'),
    path('timesteps/<int:pk>/delete/', TimeStepDeleteView.as_view(), name='time_step_delete'),

    path('levelsgroups/create/', LevelsGroupCreateView.as_view(), name='levels_group_create'),
    path('levelsgroups/<int:pk>/update/', LevelsGroupUpdateView.as_view(), name='levels_group_update'),
    path('levelsgroups/<int:pk>/delete/', LevelsGroupDeleteView.as_view(), name='levels_group_delete'),

    path('levels/create/', LevelCreateView.as_view(), name='level_create'),
    path('levels/<int:pk>/update/', LevelUpdateView.as_view(), name='level_update'),
    path('levels/<int:pk>/delete/', LevelDeleteView.as_view(), name='level_delete'),

]
