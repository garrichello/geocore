from django.forms import ModelForm, ModelChoiceField, CharField, Textarea, DateInput
from django.utils.html import escape
from django.utils.translation import get_language, gettext_lazy as _

from .models import Collection, CollectionI18N, OrganizationI18N
from .models import Dataset, Scenario, Resolution, DataKind, FileType
from .models import Data, SpecificParameter

class CollectionForm(ModelForm):

    class Meta:
        model = Collection
        fields = ['label', 'url']
        labels = {
            'label': _('Collection label'),
            'url': _('Collection URL'),
        }

    def __init__(self, *args, **kwargs):
        orgi18n_pk = kwargs.pop('orgi18n_pk', None)
        super(CollectionForm, self).__init__(*args, **kwargs)

        qset = OrganizationI18N.objects.filter(language__code=get_language())
        self.fields['organizationi18n'] = ModelChoiceField(queryset=qset, initial=orgi18n_pk)
        self.fields['organizationi18n'].label = _('Organization')


class CollectionI18NForm(ModelForm):

    class Meta:
        model = CollectionI18N
        fields = ['name', 'description']
        labels = {
            'name': _('Collection name'),
            'description': _('Collection description'),
        }
        widgets = {
            'description': Textarea(attrs={'rows': 3}),
        }


class DatasetForm(ModelForm):

    class Meta:
        model = Dataset
        fields = '__all__'

        widgets = {
            'description': Textarea(attrs={'rows': 3}),
        }


class DatasetShortForm(ModelForm):

    class Meta:
        model = Dataset
        fields = ['collection', 'resolution', 'scenario']
        labels = {
            'collection': _('Collection label'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['collection'].empty_label = '*'
        self.fields['resolution'].empty_label = '*'
        self.fields['resolution'].queryset = Resolution.objects.none()
        self.fields['scenario'].empty_label = '*'
        self.fields['scenario'].queryset = Scenario.objects.none()

        if 'collection' in self.data:
            try:
                collection_id = self.data.get('collection')
                if collection_id:
                    self.fields['resolution'].queryset = Resolution.objects.filter(id__in=
                        [dataset.resolution.id for dataset in Dataset.objects.filter(
                            collection_id=collection_id)])
            except:
                pass
        elif self.instance.pk:
            self.fields['resolution'].queryset = Resolution.objects.filter(id__in=
                        [dataset.resolution.id for dataset in Dataset.objects.filter(collection=
                        self.instance.collection)])

        if 'collection' in self.data and 'resolution' in self.data:
            try:
                collection_id = self.data.get('collection')
                resolution_id = self.data.get('resolution')
                if collection_id and resolution_id:
                    self.fields['scenario'].queryset = Scenario.objects.filter(id__in=
                        [dataset.scenario.id for dataset in Dataset.objects.filter(
                            collection_id=collection_id, resolution_id=resolution_id)])
            except:
                pass
        elif self.instance.pk:
            self.fields['scenario'].queryset = Scenario.objects.filter(id__in=
                        [dataset.scenario.id for dataset in Dataset.objects.filter(
                            collection=self.instance.collection, resolution=self.instance.resolution)])


class SpecificParameterForm(ModelForm):

    class Meta:
        model = SpecificParameter
        fields = ['parameter', 'time_step', 'levels_group']


class DataForm(ModelForm):

    class Meta:
        model = Data
        fields = ['variable', 'file', 'levels_variable', 'root_dir', 'scale', 'offset']


class ScenarioForm(ModelForm):

    class Meta:
        model = Scenario
        fields = '__all__'


class ResolutionForm(ModelForm):

    class Meta:
        model = Resolution
        fields = '__all__'


class DataKindForm(ModelForm):

    class Meta:
        model = DataKind
        fields = '__all__'


class FileTypeForm(ModelForm):

    class Meta:
        model = FileType
        fields = '__all__'


