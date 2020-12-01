from django.urls import include, path

from .views import MainView

from .apiviews import (CollectionApiListView, DatasetApiListView, DataApiListView, 
                       CollectionApiView)
from .collection_views import (CollectionCreateView, CollectionDeleteView,
                               CollectionUpdateView)
from .dataset_views import (DatasetCreateView, DatasetDeleteView,
                            DatasetUpdateView)
from .data_views import (DataCreateView, DataDeleteView, DataUpdateView)

from .organization_views import (OrganizationCreateView, OrganizationUpdateView,
                                 OrganizationDeleteView)

from .resolution_views import (ResolutionCreateView, ResolutionUpdateView,
                               ResolutionDeleteView)

from .scenario_views import (ScenarioCreateView, ScenarioUpdateView,
                               ScenarioDeleteView)

from .form_loads import (load_organizations, load_collections, load_resolutions,
                         load_scenarios, load_datakinds, load_filetypes, 
                         load_dataset_resolutions, load_dataset_scenarios,
                         load_parameter_lvsgroups, load_parameter_lvsnames,
                         load_parameter_timesteps)

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

    path('data/create/', DataCreateView.as_view(), name='data_create'),
    path('data/<int:pk>/update/', DataUpdateView.as_view(), name='data_update'),
    path('data/<int:pk>/delete/', DataDeleteView.as_view(), name='data_delete'),
    path('data/api/', DataApiListView.as_view(), name='data_api'),

    path('data/form/load-resolutions/', load_dataset_resolutions, name='form_load_dataset_resolutions'),
    path('data/form/load-scenarios/', load_dataset_scenarios, name='form_load_dataset_scenarios'),
    path('data/form/load-timesteps/', load_parameter_timesteps, name='form_load_parameter_timesteps'),
    path('data/form/load-lvsgroups/', load_parameter_lvsgroups, name='form_load_parameter_lvsgroups'),
    path('data/form/load-lvsnames/', load_parameter_lvsnames, name='form_load_parameter_lvsnames'),

    path('organizations/create/', OrganizationCreateView.as_view(), name='organization_create'),
    path('organizations/<int:pk>/update/', OrganizationUpdateView.as_view(), name='organization_update'),
    path('organizations/<int:pk>/delete/', OrganizationDeleteView.as_view(), name='organization_delete'),

    path('resolutions/create/', ResolutionCreateView.as_view(), name='resolution_create'),
    path('resolutions/<int:pk>/update/', ResolutionUpdateView.as_view(), name='resolution_update'),
    path('resolutions/<int:pk>/delete/', ResolutionDeleteView.as_view(), name='resolution_delete'),

    path('scenarios/create/', ScenarioCreateView.as_view(), name='scenario_create'),
    path('scenarios/<int:pk>/update/', ScenarioUpdateView.as_view(), name='scenario_update'),
    path('scenarios/<int:pk>/delete/', ScenarioDeleteView.as_view(), name='scenario_delete'),

]
