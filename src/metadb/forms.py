from django.forms import ModelForm, ModelChoiceField, CharField, Textarea, DateInput
from django.utils.html import escape
from django.utils.translation import get_language, gettext_lazy as _

from .models import Collection, CollectionI18N, OrganizationI18N
from .models import Dataset, Scenario, Resolution, DataKind, FileType
from .models import Data, SpecificParameter, ParameterI18N, TimeStepI18N, LevelsGroup, LevelI18N, UnitsI18N

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


class DataForm(ModelForm):

    empty_label = '*'

    class Meta:
        model = Data
        fields = ['levels_variable', 'variable', 'property', 'property_value', 'root_dir', 'file', 'scale', 'offset']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['collection'] = ModelChoiceField(queryset=Collection.objects.all())
        self.fields['collection'].empty_label = self.empty_label
        self.fields['collection'].label = _('Collection label')
        self.fields['resolution'] = ModelChoiceField(queryset=Resolution.objects.none())
        self.fields['resolution'].empty_label = self.empty_label
        self.fields['resolution'].label = _('Horizontal resolution')
        self.fields['scenario'] = ModelChoiceField(queryset=Scenario.objects.none())
        self.fields['scenario'].empty_label = self.empty_label
        self.fields['scenario'].label = _('Scenario')

        qset = ParameterI18N.objects.filter(language__code=get_language())
        self.fields['parameteri18n'] = ModelChoiceField(queryset=qset)
        self.fields['parameteri18n'].empty_label = self.empty_label
        self.fields['parameteri18n'].label = _('Parameter')
        self.fields['time_stepi18n'] = ModelChoiceField(queryset=Resolution.objects.none())
        self.fields['time_stepi18n'].empty_label = self.empty_label
        self.fields['time_stepi18n'].label = _('Time step')
        self.fields['levels_group'] = ModelChoiceField(queryset=Scenario.objects.none())
        self.fields['levels_group'].empty_label = self.empty_label
        self.fields['levels_namesi18n'] = CharField(widget=Textarea(attrs={'rows': 3}), disabled=True)
        self.fields['levels_namesi18n'].label = _('Levels names')
        self.fields['levels_group'].empty_label = self.empty_label
        self.fields['levels_variable'].empty_label = self.empty_label

        self.fields['variable'].empty_label = self.empty_label
        qset = UnitsI18N.objects.filter(language__code=get_language())
        self.fields['unitsi18n'] = ModelChoiceField(queryset=qset)
        self.fields['unitsi18n'].empty_label = '*'
        self.fields['unitsi18n'].label = _('Units')

        self.fields['property'].empty_label = self.empty_label
        self.fields['property_value'].empty_label = self.empty_label

        self.fields['root_dir'].empty_label = self.empty_label
        self.fields['file'].empty_label = self.empty_label
        self.fields['scale'].initial = 1
        self.fields['offset'].initial = 0

        self.order_fields(['collection', 'resolution', 'scenario', 'parameteri18n', 
                          'time_stepi18n', 'levels_group', 'levels_namesi18n', 
                          'levels_variable', 'variable', 'unitsi18n'])



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


