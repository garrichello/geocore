from django.urls import path, include

from . import views, apiviews

app_name = 'metadb'
urlpatterns = [
    path('', views.MainView.as_view(), name='main_view'),
    path('collections/create/', views.CollectionCreateView.as_view(), name='collection_create'),
    path('collections/<int:pk>/update/', views.CollectionUpdateView.as_view(), name='collection_update'),
    path('collections/<int:pk>/delete/', views.CollectionDeleteView.as_view(), name='collection_delete'),
    path('collections/api/', apiviews.CollectionApiListView.as_view(), name='collections_api'),
    path('collections/<int:pk>/api/', apiviews.CollectionApiView.as_view(), name='collection_api'),

    path('datasets/create/', views.DatasetCreateView.as_view(), name='dataset_create'),
    path('datasets/<int:pk>/update/', views.DatasetUpdateView.as_view(), name='dataset_update'),
    path('datasets/<int:pk>/delete/', views.DatasetDeleteView.as_view(), name='dataset_delete'),
    path('datasets/api/', apiviews.DatasetApiListView.as_view(), name='datasets_api'),

    path('data/create/', views.DataCreateView.as_view(), name='data_create'),
    path('data/<int:pk>/update/', views.DataUpdateView.as_view(), name='data_update'),
    path('data/<int:pk>/delete/', views.DataDeleteView.as_view(), name='data_delete'),
    path('data/api/', apiviews.DataApiListView.as_view(), name='data_api'),

    path('data/api/load-resolutions/', views.load_dataset_resolutions, name='api_load_resolutions'),
    path('data/api/load-scenarios/', views.load_dataset_scenarios, name='api_load_scenarios'),
]