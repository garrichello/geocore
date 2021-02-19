from django.urls import include, path
from rest_framework import routers

from .views import MainView

from .apiviews import *

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
router.register('conveyors', ConveyorViewSet)
router.register('computingmodules', ComputingModuleViewSet)
router.register('options', OptionViewSet)
router.register('optionvalues', OptionValueViewSet)
router.register('vertices', VertexViewSet)
router.register('datavariables', DataVariableViewSet)
router.register('edges', EdgeViewSet)


app_name = 'metadb'
urlpatterns = [
    path('', MainView.as_view(), name='main_view'),
    path('', include(router.urls)),
]
