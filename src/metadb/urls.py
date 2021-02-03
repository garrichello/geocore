from django.urls import include, path
from rest_framework import routers

from .views import MainView

from .form_loads import *

from .apiviews import *
from .conveyor_views import (ConveyorCreateView, ConveyorDeleteView,
                               ConveyorUpdateView)

router = routers.DefaultRouter()
router.register('collections', CollectionViewSet)
router.register('organizations', OrganizationViewSet)
router.register('datasets', DatasetViewSet)
router.register('scenarios', ScenarioViewSet)
router.register('resolutions', ResolutionViewSet)
router.register('datakinds', DataKindViewSet)
router.register('filetypes', FileTypeViewSet)
router.register('specificparameters', SpecificParameterViewSet)
router.register('accumulationmodes', AccumulationModeViewSet)
router.register('parameters', ParameterViewSet)
router.register('units', UnitsViewSet)
router.register('levelsgroups', LevelsGroupViewSet)
router.register('levels', LevelViewSet)
router.register('timesteps', TimeStepViewSet)
router.register('data', DataViewSet)
router.register('properties', PropertyViewSet)
router.register('propertyvalues', PropertyValueViewSet)
router.register('variables', VariableViewSet)
router.register('files', FileViewSet)
router.register('levelsvariables', LevelsVariableViewSet, basename='levelsvariable')
router.register('rootdirs', RootDirViewSet)
router.register('guielements', GuiElementViewSet)
router.register('languages', LanguageViewSet)

app_name = 'metadb'
urlpatterns = [
    path('', MainView.as_view(), name='main_view'),
    path('', include(router.urls)),

    path('conveyors/create/', ConveyorCreateView.as_view(), name='conveyor_create'),
    path('conveyors/', ConveyorApiListView.as_view(), name='conveyor_api'),
    path('conveyors/<int:pk>/update/', ConveyorUpdateView.as_view(), name='conveyor_update'),
    path('conveyors/<int:pk>/delete/', ConveyorDeleteView.as_view(), name='conveyor_delete'),
]
