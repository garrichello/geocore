from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.renderers import *
from django.utils.translation import gettext_lazy as _

from .serializers_dataset import DatasetRelatedField
from .serializers_specparam import ( ParameterRelatedField, LevelsGroupRelatedField,
                                     TimeStepRelatedField, UnitsRelatedField)

from .models import *
from .serializers import ModifiedRelatedField


class GuiElementI18NSerializer(serializers.ModelSerializer):

    class Meta:
        model = GuiElementI18N
        fields = ['id', 'caption']

    def to_representation(self, instance):
        data = instance.filter(language__code=get_language()).get()
        return super().to_representation(data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['caption'].label = _('GUI element caption')
        self.fields['caption'].style = {'template': 'metadb/custom_input.html'}


class GuiElementSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:guielement-detail',
                                                   read_only=True)
    guielementi18n = GuiElementI18NSerializer(source='guielementi18n_set', label='')

    class Meta:
        model = GuiElement
        fields = ['id', 'dataurl', 'name', 'guielementi18n']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('GUI element name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        guielementi18n_data = validated_data.pop('guielementi18n_set')
        guielement = GuiElement.objects.create(**validated_data)
        for db_lang in Language.objects.all():
            GuiElementI18N.objects.create(gui_element=guielement,
                                          language=db_lang,
                                          **guielementi18n_data)

        return guielement

    def update(self, instance, validated_data):
        guielementi18n = instance.guielementi18n_set.filter(language__code=get_language()).get()
        guielementi18n.caption = validated_data['guielementi18n_set'].get('caption', guielementi18n.caption)
        guielementi18n.save()
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        return instance


class GuiElementRelatedField(ModifiedRelatedField):
    serializer = GuiElementSerializer
    model = GuiElement


class PropertySerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:property-detail',
                                                   read_only=True)
    qset = GuiElement.objects.order_by('name')
    gui_element = GuiElementRelatedField(queryset=qset)

    class Meta:
        model = Property
        fields = ['id', 'dataurl', 'label', 'gui_element']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Label
        self.fields['label'].label = _('Property label')
        self.fields['label'].style = {'template': 'metadb/custom_input.html'}
        # GUI element
        self.fields['gui_element'].data_url = reverse('metadb:guielement-list')
        self.fields['gui_element'].label = _('GUI element name')
        self.fields['gui_element'].style = {'template': 'metadb/custom_select.html'}
        self.fields['gui_element'].allow_blank = True

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return Property.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.label = validated_data.get('label', instance.label)
        instance.gui_element = validated_data.get('gui_element', instance.gui_element)
        instance.save()

        return instance


class PropertyRelatedField(ModifiedRelatedField):
    serializer = PropertySerializer
    model = Property


class PropertyValueSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:propertyvalue-detail',
                                                   read_only=True)
    class Meta:
        model = Property
        fields = ['id', 'dataurl', 'label']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Label
        self.fields['label'].label = _('Property value label')
        self.fields['label'].style = {'template': 'metadb/custom_input.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return Property.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.label = validated_data.get('label', instance.label)
        instance.save()

        return instance


class PropertyValueRelatedField(ModifiedRelatedField):
    serializer = PropertyValueSerializer
    model = PropertyValue


class VariableSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:variable-detail',
                                                   read_only=True)
    class Meta:
        model = Variable
        fields = ['id', 'dataurl', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Label
        self.fields['name'].label = _('Variable name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return Variable.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        return instance


class VariableRelatedField(ModifiedRelatedField):
    serializer = VariableSerializer
    model = Variable


class LevelsVariableSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:levelsvariable-detail',
                                                   read_only=True)
    class Meta:
        model = Variable
        fields = ['id', 'dataurl', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Label
        self.fields['name'].label = _('Levels variable name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return Variable.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        return instance


class LevelsVariableRelatedField(ModifiedRelatedField):
    serializer = VariableSerializer
    model = Variable


class FileSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:file-detail',
                                                   read_only=True)
    class Meta:
        model = File
        fields = ['id', 'dataurl', 'name_pattern']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Label
        self.fields['name_pattern'].label = _('File name pattern')
        self.fields['name_pattern'].style = {'template': 'metadb/custom_input.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return File.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name_pattern = validated_data.get('name_pattern', instance.name_pattern)
        instance.save()

        return instance


class FileRelatedField(ModifiedRelatedField):
    serializer = FileSerializer
    model = File


class RootDirSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:rootdir-detail',
                                                   read_only=True)
    class Meta:
        model = RootDir
        fields = ['id', 'dataurl', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Label
        self.fields['name'].label = _('Root directory name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return RootDir.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        return instance


class RootDirRelatedField(ModifiedRelatedField):
    serializer = RootDirSerializer
    model = RootDir


class DataSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:data-detail',
                                                   read_only=True)
    qset = Dataset.objects.all().order_by('description')
    dataset = DatasetRelatedField(queryset=qset)
#    qset = SpecificParameter.objects.all()
#    specific_parameter = SpecificParameterRelatedField(queryset=qset)
    qset = Parameter.objects.all().order_by('parameteri18n__name')
    parameter = ParameterRelatedField(queryset=qset, source='specific_parameter.parameter')
    qset = LevelsGroup.objects.all()
    levels_group = LevelsGroupRelatedField(queryset=qset, source='specific_parameter.levels_group')
    qset = TimeStep.objects.all().order_by('timestepi18n__name')
    time_step = TimeStepRelatedField(queryset=qset, source='specific_parameter.time_step')
    qset = Property.objects.all()
    property = PropertyRelatedField(queryset=qset)
    qset = PropertyValue.objects.all()
    property_value = PropertyValueRelatedField(queryset=qset)
    qset = Units.objects.order_by('unitsi18n__name')
    units = UnitsRelatedField(queryset=qset)
    qset = Variable.objects.all()
    variable = VariableRelatedField(queryset=qset)
    qset = File.objects.all()
    file = FileRelatedField(queryset=qset)
    qset = Variable.objects.all()
    levels_variable = VariableRelatedField(queryset=qset)
    qset = RootDir.objects.all()
    root_dir = RootDirRelatedField(queryset=qset)

    class Meta:
        model = Data
        fields = ['id', 'dataurl', 'dataset', 'parameter', 'time_step', 'levels_group',
                  'variable', 'units', 'levels_variable', 'property', 'property_value',
                  'file', 'root_dir', 'scale', 'offset']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dataset
        self.fields['dataset'].data_url = reverse('metadb:dataset-list')
        self.fields['dataset'].label = _('Dataset')
        self.fields['dataset'].style = {'template': 'metadb/custom_select.html'}
        self.fields['dataset'].allow_blank = True
        # Specific parameter
#        self.fields['specific_parameter'].data_url = reverse('metadb:specificparameter-list')
#        self.fields['specific_parameter'].label = _('Specific parameter')
#        self.fields['specific_parameter'].style = {'template': 'metadb/custom_select.html'}
#        self.fields['specific_parameter'].allow_blank = True
        # Parameter
        self.fields['parameter'].data_url = reverse('metadb:parameter-list')
        self.fields['parameter'].label = _('Meteorological parameter')
        self.fields['parameter'].style = {'template': 'metadb/custom_select.html'}
        self.fields['parameter'].allow_blank = True
        self.fields['parameter'].no_add_btn = True
        # Levels group
        self.fields['levels_group'].data_url = reverse('metadb:levelsgroup-list')
        self.fields['levels_group'].label = _('Levels group')
        self.fields['levels_group'].style = {'template': 'metadb/custom_select.html'}
        self.fields['levels_group'].allow_blank = True
        self.fields['levels_group'].no_add_btn = True
        # Time step
        self.fields['time_step'].data_url = reverse('metadb:timestep-list')
        self.fields['time_step'].label = _('Time step')
        self.fields['time_step'].style = {'template': 'metadb/custom_select.html'}
        self.fields['time_step'].allow_blank = True
        self.fields['time_step'].no_add_btn = True
        # Property
        self.fields['property'].data_url = reverse('metadb:property-list')
        self.fields['property'].label = _('Property')
        self.fields['property'].style = {'template': 'metadb/custom_select.html'}
        self.fields['property'].allow_blank = True
        # Property value
        self.fields['property_value'].data_url = reverse('metadb:propertyvalue-list')
        self.fields['property_value'].label = _('Property value')
        self.fields['property_value'].style = {'template': 'metadb/custom_select.html'}
        self.fields['property_value'].allow_blank = True
        # Units
        self.fields['units'].data_url = reverse('metadb:units-list')
        self.fields['units'].label = _('Units')
        self.fields['units'].style = {'template': 'metadb/custom_select.html'}
        self.fields['units'].allow_blank = True
        # Variable
        self.fields['variable'].data_url = reverse('metadb:variable-list')
        self.fields['variable'].label = _('Variable')
        self.fields['variable'].style = {'template': 'metadb/custom_select.html'}
        self.fields['variable'].allow_blank = True
        # File
        self.fields['file'].data_url = reverse('metadb:file-list')
        self.fields['file'].label = _('File name pattern')
        self.fields['file'].style = {'template': 'metadb/custom_select.html'}
        self.fields['file'].allow_blank = True
        # Levels variable
        self.fields['levels_variable'].data_url = reverse('metadb:levelsvariable-list')
        self.fields['levels_variable'].label = _('Levels variable')
        self.fields['levels_variable'].style = {'template': 'metadb/custom_select.html'}
        self.fields['levels_variable'].allow_blank = True
        # Root directory
        self.fields['root_dir'].data_url = reverse('metadb:rootdir-list')
        self.fields['root_dir'].label = _('Root directory')
        self.fields['root_dir'].style = {'template': 'metadb/custom_select.html'}
        self.fields['root_dir'].allow_blank = True
        # Scale
        self.fields['scale'].label = _('Scale coefficient')
        self.fields['scale'].style = {'template': 'metadb/custom_input.html'}
        self.fields['scale'].initial = 1.0
        # Offset
        self.fields['offset'].label = _('Offset coefficient')
        self.fields['offset'].style = {'template': 'metadb/custom_input.html'}
        self.fields['offset'].initial = 0.0

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        specific_parameter_data = validated_data.pop('specific_parameter')
        specific_parameter = SpecificParameter.objects.filter(
            parameter=specific_parameter_data['parameter'],
            time_step=specific_parameter_data['time_step'],
            levels_group=specific_parameter_data['levels_group']
        ).get()
        data = Data.objects.create(**validated_data, specific_parameter = specific_parameter)
        return data

    def update(self, instance, validated_data):
        instance.dataset = validated_data.get('dataset', instance.dataset)
        specific_parameter_data = validated_data.get('specific_parameter')
        specific_parameter = SpecificParameter.objects.filter(
            parameter=specific_parameter_data['parameter'],
            time_step=specific_parameter_data['time_step'],
            levels_group=specific_parameter_data['levels_group']
        ).get()
        instance.specific_parameter = specific_parameter
        instance.property = validated_data.get('property', instance.property)
        instance.property_value = validated_data.get('property_value', instance.property_value)
        instance.units = validated_data.get('units', instance.units)
        instance.variable = validated_data.get('variable', instance.variable)
        instance.file = validated_data.get('file', instance.file)
        instance.levels_variable = validated_data.get('levels_variable', instance.levels_variable)
        instance.root_dir = validated_data.get('root_dir', instance.root_dir)
        instance.scale = validated_data.get('scale', instance.scale)
        instance.offset = validated_data.get('offset', instance.offset)
        instance.save()
        return instance