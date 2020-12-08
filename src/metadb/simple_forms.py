from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
from django.urls import reverse

from .models import ( DataKind, FileType, Organization,
    OrganizationI18N, Resolution, Scenario, Variable,
    UnitsI18N, Property, PropertyValue, RootDir, File, 
    GuiElement, GuiElementI18N, Parameter, ParameterI18N )


class DataKindForm(ModelForm):

    class Meta:
        model = DataKind
        fields = ['name']
        labels = {
            'name': _('Data kind name'),
        }


class FileTypeForm(ModelForm):

    class Meta:
        model = FileType
        fields = ['name']
        labels = {
            'name': _('File type name'),
        }


class OrganizationForm(ModelForm):

    class Meta:
        model = Organization
        fields = ['url']
        labels = {
            'url': _('Organization URL'),
        }


class OrganizationI18NForm(ModelForm):

    class Meta:
        model = OrganizationI18N
        fields = ['name']
        labels = {
            'name': _('Organization name'),
        }


class ResolutionForm(ModelForm):

    class Meta:
        model = Resolution
        fields = ['name', 'subpath1']
        labels = {
            'name': _('Resolution name'),
            'subpath1': _('Resolution subpath'),
        }


class ScenarioForm(ModelForm):

    class Meta:
        model = Scenario
        fields = ['name', 'subpath0']
        labels = {
            'name': _('Scenario name'),
            'subpath0': _('Scenario subpath'),
        }


class LevelsVariableForm(ModelForm):

    class Meta:
        model = Variable
        fields = ['name']
        labels = {
            'name': _('Levels variable name'),
        }


class VariableForm(ModelForm):

    class Meta:
        model = Variable
        fields = ['name']
        labels = {
            'name': _('Variable name'),
        }


class UnitsI18NForm(ModelForm):

    class Meta:
        model = UnitsI18N
        fields = ['name']
        labels = {
            'name': _('Measurement unit name'),
        }


class PropertyForm(ModelForm):
    empty_label = '*'

    class Meta:
        model = Property
        fields = ['label', 'gui_element']
        labels = {
            'label': _('Property label'),
            'gui_element': _('GUI element'),
        }

    def __init__(self, *args, **kwargs):
        super(PropertyForm, self).__init__(*args, **kwargs)

        self.fields['gui_element'].empty_label = self.empty_label
        self.fields['gui_element'].data_url = reverse('metadb:gui_element_create')


class PropertyValueForm(ModelForm):

    class Meta:
        model = PropertyValue
        fields = ['label']
        labels = {
            'label': _('Property value'),
        }


class RootDirForm(ModelForm):

    class Meta:
        model = RootDir
        fields = ['name']
        labels = {
            'name': _('Root directory'),
        }


class FileForm(ModelForm):

    class Meta:
        model = File
        fields = ['name_pattern']
        labels = {
            'name_pattern': _('File name pattern'),
        }


class GuiElementForm(ModelForm):

    class Meta:
        model = GuiElement
        fields = ['name']
        labels = {
            'name': _('GUI element name'),
        }


class GuiElementI18NForm(ModelForm):

    class Meta:
        model = GuiElementI18N
        fields = ['caption']
        labels = {
            'caption': _('GUI element caption'),
        }
