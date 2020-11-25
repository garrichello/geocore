from django.urls import include, path

from .views import MainView

from .apiviews import (CollectionApiListView, DatasetApiListView, DataApiListView, 
                       CollectionApiView)
from .collection_views import (CollectionCreateView, CollectionDeleteView,
                               CollectionUpdateView)
from .dataset_views import (DatasetCreateView, DatasetDeleteView,
                            DatasetUpdateView)
from .data_views import (DataCreateView, DataDeleteView, DataUpdateView,
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

    path('datasets/create/', DatasetCreateView.as_view(), name='dataset_create'),
    path('datasets/<int:pk>/update/', DatasetUpdateView.as_view(), name='dataset_update'),
    path('datasets/<int:pk>/delete/', DatasetDeleteView.as_view(), name='dataset_delete'),
    path('datasets/api/', DatasetApiListView.as_view(), name='datasets_api'),

    path('data/create/', DataCreateView.as_view(), name='data_create'),
    path('data/<int:pk>/update/', DataUpdateView.as_view(), name='data_update'),
    path('data/<int:pk>/delete/', DataDeleteView.as_view(), name='data_delete'),
    path('data/api/', DataApiListView.as_view(), name='data_api'),

    path('data/form/load-resolutions/', load_dataset_resolutions, name='form_load_resolutions'),
    path('data/form/load-scenarios/', load_dataset_scenarios, name='form_load_scenarios'),
    path('data/form/load-timesteps/', load_parameter_timesteps, name='form_load_timesteps'),
    path('data/form/load-lvsgroups/', load_parameter_lvsgroups, name='form_load_lvsgroups'),
    path('data/form/load-lvsnames/', load_parameter_lvsnames, name='form_load_lvsnames'),
]
