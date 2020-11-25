from django.urls import path, include

from . import views, col_views, ds_views, data_views, apiviews

app_name = 'metadb'
urlpatterns = [
    path('', views.MainView.as_view(), name='main_view'),
    path('collections/create/', col_views.CollectionCreateView.as_view(), name='collection_create'),
    path('collections/<int:pk>/update/', col_views.CollectionUpdateView.as_view(), name='collection_update'),
    path('collections/<int:pk>/delete/', col_views.CollectionDeleteView.as_view(), name='collection_delete'),
    path('collections/api/', apiviews.CollectionApiListView.as_view(), name='collections_api'),
    path('collections/<int:pk>/api/', apiviews.CollectionApiView.as_view(), name='collection_api'),

    path('datasets/create/', ds_views.DatasetCreateView.as_view(), name='dataset_create'),
    path('datasets/<int:pk>/update/', ds_views.DatasetUpdateView.as_view(), name='dataset_update'),
    path('datasets/<int:pk>/delete/', ds_views.DatasetDeleteView.as_view(), name='dataset_delete'),
    path('datasets/api/', apiviews.DatasetApiListView.as_view(), name='datasets_api'),

    path('data/create/', data_views.DataCreateView.as_view(), name='data_create'),
    path('data/<int:pk>/update/', data_views.DataUpdateView.as_view(), name='data_update'),
    path('data/<int:pk>/delete/', data_views.DataDeleteView.as_view(), name='data_delete'),
    path('data/api/', apiviews.DataApiListView.as_view(), name='data_api'),

    path('data/form/load-resolutions/', data_views.load_dataset_resolutions, name='form_load_resolutions'),
    path('data/form/load-scenarios/', data_views.load_dataset_scenarios, name='form_load_scenarios'),
    path('data/form/load-timesteps/', data_views.load_parameter_timesteps, name='form_load_timesteps'),
    path('data/form/load-lvsgroups/', data_views.load_parameter_lvsgroups, name='form_load_lvsgroups'),
    path('data/form/load-lvsnames/', data_views.load_parameter_lvsnames, name='form_load_lvsnames'),
]
