from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from django.forms import (BooleanField, CharField, ModelChoiceField,
                          ModelForm, Textarea)

from .models import (Collection, Data, LevelI18N, LevelsGroup, ParameterI18N, Resolution, 
                     Scenario, TimeStepI18N, UnitsI18N)


def get_resolutions(collection_id):
    return Resolution.objects.filter(dataset__collection_id=collection_id).distinct()

def get_scenarios(collection_id, resolution_id):
    return Scenario.objects.filter(dataset__collection_id=collection_id, dataset__resolution_id=resolution_id)

def get_timesteps(parameter_id):
    return TimeStepI18N.objects.filter(
        language__code=get_language(), time_step__specificparameter__parameter_id=parameter_id).distinct()

def get_levelsgroups(parameter_id, time_step_id):
    return LevelsGroup.objects.filter(
        specificparameter__parameter_id=parameter_id, specificparameter__time_step_id=time_step_id)

def get_levels(lvsgroup_id):
    units = UnitsI18N.objects.filter(
        language__code=get_language(), 
        units__levelsgroup__id=lvsgroup_id).get().name
    levels = '; '.join(['{} [{}]'.format(level.name, units) for level in 
        LevelI18N.objects.filter(
            language__code=get_language(),
            level__levels_group__id=lvsgroup_id)])
    return levels


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
        self.fields['collection'].data_url = reverse('metadb:collection_create')
        # Horizontal resolution
        self.fields['resolution'] = ModelChoiceField(queryset=Resolution.objects.none())
        self.fields['resolution'].empty_label = self.empty_label
        self.fields['resolution'].label = _('Horizontal resolution')
        self.fields['resolution'].data_url = reverse('metadb:resolution_create')
        # Scenario
        self.fields['scenario'] = ModelChoiceField(queryset=Scenario.objects.none())
        self.fields['scenario'].empty_label = self.empty_label
        self.fields['scenario'].label = _('Scenario')
        self.fields['scenario'].data_url = reverse('metadb:scenario_create')
        # Parameter
        qset = ParameterI18N.objects.filter(language__code=get_language())
        self.fields['parameteri18n'] = ModelChoiceField(queryset=qset)
        self.fields['parameteri18n'].empty_label = self.empty_label
        self.fields['parameteri18n'].label = _('Parameter')
        #self.fields['parameteri18n'].data_url = reverse('metadb:parameter_create')
        # Time step
        self.fields['time_stepi18n'] = ModelChoiceField(queryset=TimeStepI18N.objects.none())
        self.fields['time_stepi18n'].empty_label = self.empty_label
        self.fields['time_stepi18n'].label = _('Time step')
        #self.fields['time_stepi18n'].data_url = reverse('metadb:timestep_create')
        # Levels group
        self.fields['levels_group'] = ModelChoiceField(queryset=LevelsGroup.objects.none())
        self.fields['levels_group'].empty_label = self.empty_label
        self.fields['levels_group'].label = _('Levels group')
        #self.fields['levels_group'].data_url = reverse('metadb:levelsgroup_create')
        # Levels names
        self.fields['levels_namesi18n'] = CharField(widget=Textarea(attrs={'rows': 3}), disabled=True)
        self.fields['levels_namesi18n'].label = _('Levels names')
        # Levels variable
        self.fields['use_lvsvar'] = BooleanField()
        self.fields['use_lvsvar'].label = _('Use levels variable')
        self.fields['use_lvsvar'].required = False
        self.fields['levels_variable'].empty_label = self.empty_label
        self.fields['levels_variable'].disabled = True
        self.fields['levels_variable'].initial = 1
        self.fields['levels_variable'].label = _('Levels variable')
        #self.fields['levels_variable'].data_url = reverse('metadb:variable_create')
        # Variable
        self.fields['variable'].empty_label = self.empty_label
        self.fields['variable'].label = _('Variable')
        #self.fields['variable'].data_url = reverse('metadb:variable_create')
        # Units
        qset = UnitsI18N.objects.filter(language__code=get_language())
        self.fields['unitsi18n'] = ModelChoiceField(queryset=qset)
        self.fields['unitsi18n'].empty_label = '*'
        self.fields['unitsi18n'].label = _('Units')
        #self.fields['unitsi18n'].data_url = reverse('metadb:units_create')
        # Property
        self.fields['use_property'] = BooleanField()
        self.fields['use_property'].label = _('Use property')
        self.fields['use_property'].required = False
        self.fields['property'].empty_label = self.empty_label
        self.fields['property'].disabled = True
        self.fields['property'].initial = 1
        self.fields['property'].label = _('Property')
        #self.fields['property'].data_url = reverse('metadb:propery_create')
        # Property value
        self.fields['property_value'].empty_label = self.empty_label
        self.fields['property_value'].disabled = True
        self.fields['property_value'].initial = 1
        self.fields['property_value'].label = _('Property value')
        #self.fields['property_value'].data_url = reverse('metadb:properyvalue_create')
        # Root dir
        self.fields['root_dir'].empty_label = self.empty_label
        self.fields['root_dir'].label = _('Root diriectory')
        #self.fields['root_dir'].data_url = reverse('metadb:rootdir_create')
        # File
        self.fields['file'].empty_label = self.empty_label
        self.fields['file'].label = _('File name pattern')
        #self.fields['file'].data_url = reverse('metadb:file_create')
        # Scale
        self.fields['scale'].initial = 1
        self.fields['scale'].label = _('Scale')
        # Offset
        self.fields['offset'].initial = 0
        self.fields['offset'].label = _('Offset')

        self.order_fields(['collection', 'resolution', 'scenario', 'parameteri18n', 
                          'time_stepi18n', 'levels_group', 'levels_namesi18n', 
                          'use_lvsvar', 'levels_variable', 'variable', 'unitsi18n',
                          'levels_variable', 'variable', 'use_property', 'property', 'property_value'])        


    def fill_fields(self):
        # The following is needed for passing validation by the form.
        # Collection, resolution and scenario fields are connected.
        # User selects collection, then resolution, and finally scenario.
        
        # Get resolutions for a selected collection.
        if 'collection' in self.data:  # To Create a new record
            try:
                collection_id = self.data.get('collection')
                if collection_id:
                    self.fields['resolution'].queryset = get_resolutions(collection_id)
            except:
                pass
        elif self.instance.pk:  # To Update an existing record
            self.fields['resolution'].queryset = get_resolutions(self.instance.dataset.collection.id)

            self.fields['collection'].initial = self.instance.dataset.collection.id
            self.fields['resolution'].initial = self.instance.dataset.resolution.id

        # Get scenarios for a selected collection and a resolution.
        if 'collection' in self.data and 'resolution' in self.data:
            try:
                collection_id = self.data.get('collection')
                resolution_id = self.data.get('resolution')
                if collection_id and resolution_id:
                    self.fields['scenario'].queryset = get_scenarios(collection_id, resolution_id)
            except:
                pass
        elif self.instance.pk:
            self.fields['scenario'].queryset = get_scenarios(
                self.instance.dataset.collection.id, 
                self.instance.dataset.resolution.id)

            self.fields['scenario'].initial = self.instance.dataset.scenario.id

        # The following is needed for passing validation by the form.
        # Parameter, time step and levels group fields are connected.
        # User selects parameter, then time step, and finally levels group.

        # Get time steps for a selected parameter (localized name of a parameter).
        if 'parameteri18n' in self.data:  # To create a new record.
            try:
                parameteri18n_id = self.data.get('parameteri18n')
                parameter_id = ParameterI18N.objects.get(pk=parameteri18n_id).parameter_id
                if parameter_id:
                    self.fields['time_stepi18n'].queryset = get_timesteps(parameter_id)
            except:
                pass
        elif self.instance.pk:  # To update an existing record.
            self.fields['time_stepi18n'].queryset = get_timesteps(self.instance.specific_parameter.parameter.id)

            self.fields['parameteri18n'].initial = \
                self.instance.specific_parameter.parameter.parameteri18n_set.filter(
                    language__code=get_language()).get().id
            self.fields['time_stepi18n'].initial = \
                self.instance.specific_parameter.time_step.timestepi18n_set.filter(
                    language__code=get_language()).get().id

        # Get levels groups for a selected parameter and a time step.
        if 'parameteri18n' in self.data and 'time_stepi18n' in self.data:
            try:
                parameteri18n_id = self.data.get('parameteri18n')
                parameter_id = ParameterI18N.objects.get(pk=parameteri18n_id).parameter_id
                timestepi18n_id = self.data.get('time_stepi18n')
                time_step_id = TimeStepI18N.objects.get(pk=timestepi18n_id).time_step_id
                if parameter_id and time_step_id:
                    self.fields['levels_group'].queryset = get_levelsgroups(parameter_id, time_step_id)
            except:
                pass
        elif self.instance.pk:
            self.fields['levels_group'].queryset = get_levelsgroups(
                self.instance.specific_parameter.parameter.id,
                self.instance.specific_parameter.time_step.id)

            self.fields['levels_group'].initial = self.instance.specific_parameter.levels_group.id

        # Fill the Levels names text field based on the Levels group field
        if 'levels_group' in self.data:  # When Create data record
            try:
                lvsgroup_id = self.data.get('levels_group')
                if lvsgroup_id:
                    self.fields['levels_namesi18n'].initial = get_levels(lvsgroup_id)
            except:
                pass
        elif self.instance.pk:  # When Update data record
            self.fields['levels_namesi18n'].initial = get_levels(self.instance.specific_parameter.levels_group.id)

        # The following is needed for passing validation by the form.
        # Fill the Units field.
        if self.instance.pk:
            self.fields['unitsi18n'].queryset = UnitsI18N.objects.filter(
                language__code=get_language()
            )
            self.fields['unitsi18n'].initial = self.instance.units.unitsi18n_set.filter(
                language__code=get_language()
            ).get().id

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_fields()

        self.fill_fields()
