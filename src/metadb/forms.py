from django.forms import ModelForm, ModelChoiceField, CharField, Textarea, DateInput
from django.utils.html import escape
from django.utils.translation import get_language, gettext_lazy as _

from .models import Collection, CollectionI18N, OrganizationI18N
from .models import Dataset, Scenario, Resolution, DataKind, FileType
from .models import Data, SpecificParameter, ParameterI18N, TimeStepI18N, LevelsGroup, LevelI18N, Level, UnitsI18N

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


class DataForm(ModelForm):

    empty_label = '*'

    class Meta:
        model = Data
        fields = ['levels_variable', 'variable', 'property', 'property_value', 'root_dir', 'file', 'scale', 'offset']

    def set_fields(self):
        # Collection label
        self.fields['collection'] = ModelChoiceField(queryset=Collection.objects.all())
        self.fields['collection'].empty_label = self.empty_label
        self.fields['collection'].label = _('Collection label')
        # Horizontal resolution
        self.fields['resolution'] = ModelChoiceField(queryset=Resolution.objects.none())
        self.fields['resolution'].empty_label = self.empty_label
        self.fields['resolution'].label = _('Horizontal resolution')
        # Scenario
        self.fields['scenario'] = ModelChoiceField(queryset=Scenario.objects.none())
        self.fields['scenario'].empty_label = self.empty_label
        self.fields['scenario'].label = _('Scenario')
        # Parameter
        qset = ParameterI18N.objects.filter(language__code=get_language())
        self.fields['parameteri18n'] = ModelChoiceField(queryset=qset)
        self.fields['parameteri18n'].empty_label = self.empty_label
        self.fields['parameteri18n'].label = _('Parameter')
        # Time step
        self.fields['time_stepi18n'] = ModelChoiceField(queryset=TimeStepI18N.objects.none())
        self.fields['time_stepi18n'].empty_label = self.empty_label
        self.fields['time_stepi18n'].label = _('Time step')
        # Levels group
        self.fields['levels_group'] = ModelChoiceField(queryset=LevelsGroup.objects.none())
        self.fields['levels_group'].empty_label = self.empty_label
        self.fields['levels_group'].empty_label = self.empty_label
        # Levels names
        self.fields['levels_namesi18n'] = CharField(widget=Textarea(attrs={'rows': 3}), disabled=True)
        self.fields['levels_namesi18n'].label = _('Levels names')
        # Levels variable
        self.fields['levels_variable'].empty_label = self.empty_label
        # Variable
        self.fields['variable'].empty_label = self.empty_label
        # Units
        qset = UnitsI18N.objects.filter(language__code=get_language())
        self.fields['unitsi18n'] = ModelChoiceField(queryset=qset)
        self.fields['unitsi18n'].empty_label = '*'
        self.fields['unitsi18n'].label = _('Units')
        # Property
        self.fields['property'].empty_label = self.empty_label
        # Property value
        self.fields['property_value'].empty_label = self.empty_label
        # Root dir
        self.fields['root_dir'].empty_label = self.empty_label
        # File
        self.fields['file'].empty_label = self.empty_label
        # Scale
        self.fields['scale'].initial = 1
        # Offset
        self.fields['offset'].initial = 0

        self.order_fields(['collection', 'resolution', 'scenario', 'parameteri18n', 
                          'time_stepi18n', 'levels_group', 'levels_namesi18n', 
                          'levels_variable', 'variable', 'unitsi18n'])        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_fields()

        if 'collection' in self.data:  # When Create data record
            try:
                collection_id = self.data.get('collection')
                if collection_id:
                    self.fields['resolution'].queryset = Resolution.objects.filter(id__in=
                        [dataset.resolution.id for dataset in Dataset.objects.filter(
                            collection_id=collection_id)])
            except:
                pass
        elif self.instance.pk:  # When Update data record
            self.fields['resolution'].queryset = self.instance.dataset.resolution

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
            self.fields['scenario'].queryset = self.instance.dataset.scenario

        if 'parameteri18n' in self.data:
            try:
                parameteri18n_id = self.data.get('parameteri18n')
                parameter_id = ParameterI18N.objects.get(pk=parameteri18n_id).parameter_id
                if parameter_id:
                    self.fields['time_stepi18n'].queryset = TimeStepI18N.objects.filter(
                        language__code=get_language(), time_step__in=
                            [sp.time_step for sp in SpecificParameter.objects.filter(
                                parameter_id=parameter_id)])
            except:
                pass
        elif self.instance.pk:
            self.fields['time_stepi18n'].queryset = \
                self.instance.specific_parameter.time_step.timestepi18n_set.filter(language=get_language())

        if 'parameteri18n' in self.data and 'time_stepi18n' in self.data:
            try:
                parameteri18n_id = self.data.get('parameteri18n')
                parameter_id = ParameterI18N.objects.get(pk=parameteri18n_id).parameter_id
                timestepi18n_id = self.data.get('time_stepi18n')
                time_step_id = TimeStepI18N.objects.get(pk=timestepi18n_id).time_step_id
                if parameter_id and time_step_id:
                    self.fields['levels_group'].queryset = LevelsGroup.objects.filter(id__in=
                        [sp.levels_group.id for sp in SpecificParameter.objects.filter(
                            parameter_id=parameter_id, time_step_id=time_step_id)])
            except:
                pass
        elif self.instance.pk:
            self.fields['levels_group'].queryset = \
                self.instance.specific_parameter.levels_group

        if 'levels_group' in self.data:  # When Create data record
            try:
                lvsgroup_id = self.data.get('levels_group')
                if lvsgroup_id:
                    units = UnitsI18N.objects.filter(language__code=get_language(), units_id=
                        LevelsGroup.objects.get(pk=lvsgroup_id).units_id).get().name
                    levels = '; '.join(['{} [{}]'.format(level.name, units) for level in LevelI18N.objects.filter(
                        language__code=get_language(), level__in=Level.objects.filter(
                            levels_group__id=lvsgroup_id))])
                    self.fields['levels_namesi18n'].initial = levels
            except:
                pass
        elif self.instance.pk:  # When Update data record
            self.fields['resolution'].queryset = self.instance.dataset.resolution


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


