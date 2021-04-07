from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.renderers import *
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language

from .serializers_specparam import UnitsRelatedField

from .models import *
from .serializers import ModifiedRelatedField


class ConveyorSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:conveyor-detail',
                                                   read_only=True)
    fulldataurl = serializers.HyperlinkedIdentityField(view_name='metadb:fullconveyor-detail',
                                                   read_only=True)
    class Meta:
        model = Conveyor
        fields = ['id', 'dataurl', 'fulldataurl', 'label']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Label
        self.fields['label'].label = _('Label')
        self.fields['label'].style = {'template': 'metadb/custom_input.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return Conveyor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.label = validated_data.get('label', instance.label)
        instance.save()

        return instance


class ConveyorRelatedField(ModifiedRelatedField):
    serializer = ConveyorSerializer
    model = Conveyor


class ComputingModuleSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:computingmodule-detail',
                                                   read_only=True)
    class Meta:
        model = ComputingModule
        fields = ['id', 'dataurl', 'name', 'number_of_inputs', 'number_of_outputs', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Name
        self.fields['name'].label = _('Computing module name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}
        # Number of inputs
        self.fields['number_of_inputs'].label = _('Number of inputs')
        self.fields['number_of_inputs'].style = {'template': 'metadb/custom_input.html'}
        # Number of outputs
        self.fields['number_of_outputs'].label = _('Number of outputs')
        self.fields['number_of_outputs'].style = {'template': 'metadb/custom_input.html'}
        # Description
        self.fields['description'].label = _('Description')
        self.fields['description'].style = {'template': 'metadb/custom_textarea.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return ComputingModule.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class ComputingModuleRelatedField(ModifiedRelatedField):
    serializer = ComputingModuleSerializer
    model = ComputingModule


class OptionSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:option-detail',
                                                   read_only=True)

    class Meta:
        model = Option
        fields = ['id', 'dataurl', 'label']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Label
        self.fields['label'].label = _('Option label')
        self.fields['label'].style = {'template': 'metadb/custom_input.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return Option.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.label = validated_data.get('label', instance.label)
        instance.save()
        return instance


class OptionRelatedField(ModifiedRelatedField):
    serializer = OptionSerializer
    model = Option


class OptionValueI18NSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionValueI18N
        fields = ['id', 'name']

    def to_representation(self, instance):
        data = instance.filter(language__code=get_language()).get()
        return super().to_representation(data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Option value name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}


class OptionValueSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:optionvalue-detail',
                                                   read_only=True)
    optionvaluei18n = OptionValueI18NSerializer(source='optionvaluei18n_set', label='')

    class Meta:
        model = OptionValue
        fields = ['id', 'dataurl', 'label', 'optionvaluei18n']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['label'].label = _('Option value label')
        self.fields['label'].style = {'template': 'metadb/custom_input.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        optionvaluei18n_data = validated_data.pop('optionvaluei18n_set')
        optionvalue = OptionValue.objects.create(**validated_data)
        for db_lang in Language.objects.all():
            OptionValueI18N.objects.create(option_value=optionvalue,
                                           language=db_lang,
                                           **optionvaluei18n_data)

        return optionvalue

    def update(self, instance, validated_data):
        optionvaluei18n = instance.optionvaluei18n_set.filter(language__code=get_language()).get()
        optionvaluei18n.name = validated_data['optionvaluei18n_set'].get('name', optionvaluei18n.name)
        optionvaluei18n.save()
        instance.label = validated_data.get('label', instance.label)
        instance.save()
        return instance


class OptionValueRelatedField(ModifiedRelatedField):
    serializer = OptionValueSerializer
    model = OptionValue


class ConditionCombinationSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:combination-detail',
                                                   read_only=True)
    qset = Option.objects.order_by('label')
    option = OptionRelatedField(queryset=qset)
    qset = OptionValue.objects.order_by('label')
    option_value = OptionValueRelatedField(queryset=qset)
    string = serializers.SerializerMethodField()

    class Meta:
        model = Combination
        fields = ['id', 'dataurl', 'string', 'option', 'option_value']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_string(self, obj):
        return obj.__str__()


class ConditionCombinationRelatedField(ModifiedRelatedField):
    serializer = ConditionCombinationSerializer
    model = Combination


class CombinationSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:combination-detail',
                                                   read_only=True)

    qset = Option.objects.order_by('label')
    option = OptionRelatedField(queryset=qset)
    qset = OptionValue.objects.order_by('label')
    option_value = OptionValueRelatedField(queryset=qset)
    qset = Combination.objects.all()
    condition = ConditionCombinationRelatedField(queryset=qset)
    string = serializers.SerializerMethodField()

    class Meta:
        model = Combination
        fields = ['id', 'dataurl', 'string', 'option', 'option_value', 'condition']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['option'].data_url = reverse('metadb:option-list')
        self.fields['option'].label = _('Option')
        self.fields['option'].style = {'template': 'metadb/custom_select.html'}
        self.fields['option'].allow_blank = False
        self.fields['option_value'].data_url = reverse('metadb:optionvalue-list')
        self.fields['option_value'].label = _('Value')
        self.fields['option_value'].style = {'template': 'metadb/custom_select.html'}
        self.fields['option_value'].allow_blank = False
        self.fields['condition'].data_url = reverse('metadb:combination-list')
        self.fields['condition'].label = _('Condition combination')
        self.fields['condition'].style = {'template': 'metadb/custom_select.html'}
        self.fields['condition'].allow_blank = False
        self.fields['condition'].no_add_btn = True
        self.fields['string'].hidden = True
        self.fields['string'].label = 'string'

    def get_string(self, obj):
        return obj.__str__()

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return Combination.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.option = validated_data.get('option', instance.option)
        instance.option_value = validated_data.get('option_value', instance.option_value)
        instance.condition = validated_data.get('condition', instance.condition)
        instance.save()
        return instance


class CombinationRelatedField(ModifiedRelatedField):
    serializer = CombinationSerializer
    model = Combination


class VertexSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:vertex-detail',
                                                   read_only=True)
    qset = ComputingModule.objects.order_by('name')
    computing_module = ComputingModuleRelatedField(queryset=qset)
    qset = Combination.objects.order_by('option__label')
    condition_combination = CombinationRelatedField(queryset=qset)

    class Meta:
        model = Vertex
        fields = ['id', 'dataurl', 'computing_module', 'condition_combination']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Computing module
        self.fields['computing_module'].data_url = reverse('metadb:computingmodule-list')
        self.fields['computing_module'].label = _('Computing module')
        self.fields['computing_module'].style = {'template': 'metadb/custom_select.html'}
        self.fields['computing_module'].allow_blank = True
        # Condition combination
        self.fields['condition_combination'].data_url = reverse('metadb:combination-list')
        self.fields['condition_combination'].label = _('Condition combination')
        self.fields['condition_combination'].style = {'template': 'metadb/custom_select.html'}
        self.fields['condition_combination'].allow_blank = False

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return Vertex.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.computing_module = validated_data.get('computing_module', instance.computing_module)
        instance.condition_option = validated_data.get('condition_option', instance.condition_option)
        instance.condition_value = validated_data.get('condition_value', instance.condition_value)
        instance.save()

        return instance


class VertexRelatedField(ModifiedRelatedField):
    serializer = VertexSerializer
    model = Vertex


class DataVariableSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:datavariable-detail',
                                                   read_only=True)
    qset = Units.objects.order_by('unitsi18n__name')
    units = UnitsRelatedField(queryset=qset)

    class Meta:
        model = DataVariable
        fields = ['id', 'dataurl', 'label', 'description', 'units']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Label
        self.fields['label'].label = _('Label')
        self.fields['label'].style = {'template': 'metadb/custom_input.html'}
        # Description
        self.fields['description'].label = _('Description')
        self.fields['description'].style = {'template': 'metadb/custom_input.html'}
        # Units
        self.fields['units'].data_url = reverse('metadb:units-list')
        self.fields['units'].label = _('Measurement unit')
        self.fields['units'].style = {'template': 'metadb/custom_select.html'}
        self.fields['units'].allow_blank = True

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return DataVariable.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.label = validated_data.get('label', instance.label)
        instance.description = validated_data.get('description', instance.description)
        instance.units = validated_data.get('units', instance.units)
        instance.save()
        return instance


class DataVariableRelatedField(ModifiedRelatedField):
    serializer = DataVariableSerializer
    model = DataVariable


class EdgeSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:edge-detail',
                                                   read_only=True)
    qset = Conveyor.objects.order_by('label')
    conveyor = ConveyorRelatedField(queryset=qset)
    qset = Vertex.objects.order_by('computing_module__name')
    from_vertex = VertexRelatedField(queryset=qset)
    qset = Vertex.objects.order_by('computing_module__name')
    to_vertex = VertexRelatedField(queryset=qset)
    qset = DataVariable.objects.order_by('label')
    data_variable = DataVariableRelatedField(queryset=qset)

    class Meta:
        model = Edge
        fields = ['id', 'dataurl', 'conveyor', 'from_vertex', 'from_output', 'to_vertex',
                  'to_input', 'data_variable']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Conveyor
        self.fields['conveyor'].data_url = reverse('metadb:conveyor-list')
        self.fields['conveyor'].label = _('Conveyor')
        self.fields['conveyor'].style = {'template': 'metadb/custom_select.html'}
        self.fields['conveyor'].allow_blank = True
        self.fields['conveyor'].no_add_btn = True
        # From vertex
        self.fields['from_vertex'].data_url = reverse('metadb:vertex-list')
        self.fields['from_vertex'].label = _('Source vertex')
        self.fields['from_vertex'].style = {'template': 'metadb/custom_select.html'}
        self.fields['from_vertex'].allow_blank = True
        # From output
        self.fields['from_output'].label = _('Source output')
        self.fields['from_output'].style = {'template': 'metadb/custom_input.html'}
        # To vertex
        self.fields['to_vertex'].data_url = reverse('metadb:vertex-list')
        self.fields['to_vertex'].label = _('Target vertex')
        self.fields['to_vertex'].style = {'template': 'metadb/custom_select.html'}
        self.fields['to_vertex'].allow_blank = True
        # To input
        self.fields['to_input'].label = _('Target input')
        self.fields['to_input'].style = {'template': 'metadb/custom_input.html'}
        # Data variable
        self.fields['data_variable'].data_url = reverse('metadb:datavariable-list')
        self.fields['data_variable'].label = _('Data variable')
        self.fields['data_variable'].style = {'template': 'metadb/custom_select.html'}
        self.fields['data_variable'].allow_blank = True

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


class EdgeRelatedField(ModifiedRelatedField):
    serializer = EdgeSerializer
    model = Edge


class ConveyorFullSerializer(ConveyorSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:fullconveyor-detail',
                                                   read_only=True)
    edges = EdgeRelatedField(many=True, read_only=True, source='edge_set')

    class Meta:
        model = Conveyor
        fields = ['id', 'dataurl', 'label', 'edges']