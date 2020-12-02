from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm

from .models import (DataKind, FileType, Organization, 
    OrganizationI18N, Resolution, Scenario )


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
