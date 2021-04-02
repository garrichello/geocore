from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.renderers import *
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language

from .serializers_data import GuiElementRelatedField
from .serializers_conveyor import ( CombinationRelatedField, OptionValueSerializer,
                                    ConveyorRelatedField, CombinationRelatedField)
from .serializers_specparam import SpecificParameterRelatedField

from .models import *
from .serializers import ModifiedRelatedField


class ArgumentTypeSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:argumenttype-detail',
                                                   read_only=True)

    class Meta:
        model = ArgumentType
        fields = ['id', 'dataurl', 'label']

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
        return ArgumentType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.label = validated_data.get('label', instance.label)
        instance.save()
        return instance


class ArgumentTypeRelatedField(ModifiedRelatedField):
    serializer = ArgumentTypeSerializer
    model = ArgumentType


class ArgumentsGroupSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:argumentsgroup-detail',
                                                   read_only=True)
    fulldataurl = serializers.HyperlinkedIdentityField(view_name='metadb:fullargumentsgroup-detail',
                                                   read_only=True)
    qset = ArgumentType.objects.order_by('label')
    argument_type = ArgumentTypeRelatedField(queryset=qset)


    class Meta:
        model = ArgumentsGroup
        fields = ['id', 'dataurl', 'fulldataurl', 'name', 'description', 'argument_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Label
        self.fields['name'].label = _('Name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}
        # Description
        self.fields['description'].label = _('Description')
        self.fields['description'].style = {'template': 'metadb/custom_input.html'}
        # Argument type
        self.fields['argument_type'].label = _('Argument type')
        self.fields['argument_type'].style = {'template': 'metadb/custom_select.html'}
        self.fields['argument_type'].data_url = reverse('metadb:argumenttype-list')


    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
#        processors = validated_data.pop('processor')
#        specific_parameters = validated_data.pop('specific_parameter')
        instance = ArgumentsGroup.objects.create(**validated_data)
#        instance.processor.set(processors)
#        instance.specific_parameter.set(specific_parameters)
        return instance

    def update(self, instance, validated_data):
#        processors = validated_data.pop('processor')
#        specific_parameters = validated_data.pop('specific_parameter')
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.argument_type = validated_data.get('argument_type', instance.argument_type)
#        instance.processor.set(processors)
#        instance.specific_parameter.set(specific_parameters)
        instance.save()
        return instance


class ArgumentsGroupRelatedField(ModifiedRelatedField):
    serializer = ArgumentsGroupSerializer
    model = ArgumentsGroup


class TimePeriodTypeI18NSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimePeriodTypeI18N
        fields = ['id', 'name', 'name']

    def to_representation(self, instance):
        data = instance.filter(language__code=get_language()).get()
        return super().to_representation(data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Time period type name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}


class TimePeriodTypeSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:timeperiodtype-detail',
                                                   read_only=True)
    timeperiodtypei18n = TimePeriodTypeI18NSerializer(source='timeperiodtypei18n_set', label='')

    class Meta:
        model = TimePeriodType
        fields = ['id', 'dataurl', 'const_name', 'timeperiodtypei18n']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Name of constant
        self.fields['const_name'].label = _('Name on constant')
        self.fields['const_name'].style = {'template': 'metadb/custom_input.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        timeperiodtypei18n_data = validated_data.pop('timeperiodtypei18n_set')
        instance = TimePeriodType.objects.create(**validated_data)
        for db_lang in Language.objects.all():
            TimePeriodTypeI18N.objects.create(time_period_type=instance,
                                              language=db_lang,
                                              **timeperiodtypei18n_data)
        return instance

    def update(self, instance, validated_data):
        instance.const_name = validated_data.get('const_name', instance.const_name)
        timeperiodtypei18n = instance.timeperiodtypei18n_set.filter(language__code=get_language()).get()
        timeperiodtypei18n.name = validated_data['timeperiodtypei18n_set'].get('name', timeperiodtypei18n.name)
        timeperiodtypei18n.save()
        instance.save()
        return instance


class SettingSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:setting-detail',
                                                   read_only=True)
    fulldataurl = serializers.HyperlinkedIdentityField(view_name='metadb:fullsetting-detail',
                                                   read_only=True)
    qset = GuiElement.objects.order_by('name')
    gui_element = GuiElementRelatedField(queryset=qset)

    class Meta:
        model = Setting
        fields = ['id', 'dataurl', 'fulldataurl', 'label', 'gui_element']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Label
        self.fields['label'].label = _('Label')
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
        return Setting.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.label = validated_data.get('label', instance.label)
        instance.gui_element = validated_data.get('gui_element', instance.gui_element)
        instance.save()
        return instance


class SettingRelatedField(ModifiedRelatedField):
    serializer = SettingSerializer
    model = Setting


class SettingHasCombinationSerializer(serializers.HyperlinkedModelSerializer):
    qset = Combination.objects.all()
    combination = CombinationRelatedField(queryset=qset)
    class Meta:
        model = SettingHasCombination
        fields = ['id', 'index', 'combination']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Label
        self.fields['index'].label = _('Index')
        self.fields['index'].style = {'template': 'metadb/custom_input.html'}
        # Combination
        self.fields['combination'].data_url = reverse('metadb:combination-list')
        self.fields['combination'].label = _('Option-value combinations')
        self.fields['combination'].style = {'template': 'metadb/custom_select_multiple.html'}


class SettingHasCombinationRelatedField(ModifiedRelatedField):
    serializer = SettingHasCombinationSerializer
    model = SettingHasCombination


class SettingFullSerializer(SettingSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:fullsetting-detail',
                                                   read_only=True)
    qset = SettingHasCombination.objects.all()
    combinations = SettingHasCombinationRelatedField(queryset=qset, source='setting_combinations', many=True)

    class Meta:
        model = Setting
        fields = ['id', 'dataurl', 'label', 'gui_element', 'combinations']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Combinations
        self.fields['combinations'].data_url = reverse('metadb:combination-list')
        self.fields['combinations'].label = _('Option-value combinations')
        self.fields['combinations'].style = {'template': 'metadb/custom_select_multiple.html'}

    def create(self, validated_data):
        combinations = validated_data.pop('setting_combinations')
        instance = Setting.objects.create(**validated_data)
        for i, val in enumerate(combinations):
            shc = SettingHasCombination.objects.create(setting=instance,
                                                       combination=val.combination,
                                                       index=i)
            shc.save()
        return instance

    def update(self, instance, validated_data):
        combinations = validated_data.pop('setting_combinations')
        instance.label = validated_data.get('label', instance.label)
        instance.gui_element = validated_data.get('gui_element', instance.gui_element)
        SettingHasCombination.objects.filter(setting=instance).delete()
        for i, val in enumerate(combinations):
            shc = SettingHasCombination.objects.create(setting=instance,
                                                       combination=val.combination,
                                                       index=i)
            shc.save()
        instance.save()
        return instance


class SettingFullRelatedField(ModifiedRelatedField):
    serializer = SettingFullSerializer
    model = Setting


class TimePeriodTypeRelatedField(ModifiedRelatedField):

    def to_representation(self, value):
        data = TimePeriodTypeSerializer(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data
        if action == 'update':
            result = result.get('id', None)
        return result

    def to_internal_value(self, data):
        return TimePeriodType.objects.get(pk=data)


class ProcessorI18NSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProcessorI18N
        fields = ['id', 'name', 'description', 'reference']

    def to_representation(self, instance):
        data = instance.filter(language__code=get_language()).get()
        return super().to_representation(data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Processor name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}
        self.fields['description'].label = _('Processor short description')
        self.fields['description'].style = {'template': 'metadb/custom_input.html'}
        self.fields['reference'].label = _('Reference / URL')
        self.fields['reference'].style = {'template': 'metadb/custom_input.html'}


class OptionAndValuesRelatedField(ModifiedRelatedField):
    serializer = OptionValueSerializer
    model = OptionValue


class ProcessorHasArgumentsSerializer(serializers.HyperlinkedModelSerializer):
    qset = ArgumentsGroup.objects.all()
    arguments_group = ArgumentsGroupRelatedField(queryset=qset)
    class Meta:
        model = ProcessorHasArguments
        fields = ['id', 'argument_position', 'arguments_group']


class ProcessorHasArgumentsRelatedField(ModifiedRelatedField):
    serializer = ProcessorHasArgumentsSerializer
    model = ProcessorHasArguments


class ProcessorLightSerializer(serializers.HyperlinkedModelSerializer):
    processori18n = ProcessorI18NSerializer(source='processori18n_set', label='')

    class Meta:
        model = Processor
        fields = ['id', 'processori18n']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result


class ProcessorLightRelatedField(ModifiedRelatedField):
    serializer = ProcessorLightSerializer
    model = Processor


class ProcessorSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:processor-detail',
                                                   read_only=True)
    fulldataurl = serializers.HyperlinkedIdentityField(view_name='metadb:fullprocessor-detail',
                                                   read_only=True)
    processori18n = ProcessorI18NSerializer(source='processori18n_set', label='')
    qset = Conveyor.objects.order_by('label')
    conveyor = ConveyorRelatedField(queryset=qset)
    arguments = ProcessorHasArgumentsRelatedField(many=True, source='processor_arguments',
                                                  read_only=True)
    qset = Setting.objects.order_by('label')
    settings = SettingRelatedField(queryset=qset, many=True)
    qset = TimePeriodType.objects.order_by('timeperiodtypei18n__name')
    time_period_types = TimePeriodTypeRelatedField(queryset=qset, many=True)

    class Meta:
        model = Processor
        fields = ['id', 'dataurl', 'fulldataurl', 'is_visible', 'processori18n', 'conveyor',
                  'settings', 'time_period_types', 'arguments_selected_by_user', 'arguments']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Is visible
        self.fields['is_visible'].label = _('Visible')
        self.fields['is_visible'].style = {'template': 'metadb/custom_checkbox.html'}
        self.fields['is_visible'].initial = True
        # Conveyor
        self.fields['conveyor'].data_url = reverse('metadb:conveyor-list')
        self.fields['conveyor'].label = _('Conveyor label')
        self.fields['conveyor'].style = {'template': 'metadb/custom_select.html'}
        self.fields['conveyor'].allow_blank = True
        # Setting
        self.fields['settings'].data_url = reverse('metadb:setting-list')
        self.fields['settings'].label = _('Settings')
        self.fields['settings'].style = {'template': 'metadb/custom_select_multiple.html'}
        # Time period type
        self.fields['time_period_types'].data_url = reverse('metadb:timeperiodtype-list')
        self.fields['time_period_types'].label = _('Time period type')
        self.fields['time_period_types'].style = {'template': 'metadb/custom_select_multiple.html'}
        # Number of arguments given by a user
        self.fields['arguments_selected_by_user'].label = _('Number of arguments given by user')
        self.fields['arguments_selected_by_user'].style = {'template': 'metadb/custom_input.html'}
        # Arguments
        self.fields['arguments'].data_url = reverse('metadb:argumentsgroup-list')
        self.fields['arguments'].label = _('Arguments')
        self.fields['arguments'].style = {'template': 'metadb/custom_select_multiple.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def to_internal_value(self, data):
        result = super().to_internal_value(data)
        # Add arguments groups to the result since these data are generated client-side
        result['arguments_groups'] = {}
        for key in data.keys():
            if 'arguments_group' in key:
                idx = key.split('_')[-1]  # Get index of the group
                result['arguments_groups'][idx] = list(
                    ArgumentsGroup.objects.filter(pk__in=data.getlist(key)))
        return result

    def create(self, validated_data):
        arguments_groups = validated_data.pop('arguments_groups')
        settings_data = validated_data.pop('settings')
        time_period_types = validated_data.pop('time_period_types')
        processori18n_data = validated_data.pop('processori18n_set')

        instance = Processor.objects.create(**validated_data)

        for db_lang in Language.objects.all():
            ProcessorI18N.objects.create(processor=instance,
                                         language=db_lang,
                                         **processori18n_data)
        instance.time_period_types.set(time_period_types)
        instance.settings.set(settings_data)
        for argument_position, arguments_group_set in arguments_groups.items():
            for arguments_group in arguments_group_set:
                ProcessorHasArguments.objects.create(processor=instance,
                                                     arguments_group=arguments_group,
                                                     argument_position=argument_position)
        return instance

    def update(self, instance, validated_data):
        arguments_groups = validated_data.pop('arguments_groups')
        settings_data = validated_data.pop('settings')
        time_period_types = validated_data.pop('time_period_types')
        processori18n_data = validated_data.pop('processori18n_set')

        instance.is_visible = validated_data.get('is_visible', instance.is_visible)
        instance.conveyor = validated_data.get('conveyor', instance.conveyor)
        instance.arguments_selected_by_user = validated_data.get('arguments_selected_by_user',
                                                                 instance.arguments_selected_by_user)

        processori18n = instance.processori18n_set.filter(language__code=get_language()).get()
        processori18n.name = processori18n_data.get('name', processori18n.name)
        processori18n.description = processori18n_data.get('description', processori18n.description)
        processori18n.reference = processori18n_data.get('reference', processori18n.reference)
        processori18n.save()

        instance.time_period_types.set(time_period_types)
        instance.settings.set(settings_data)
        ProcessorHasArguments.objects.filter(processor=instance).delete()
        for argument_position, arguments_group_set in arguments_groups.items():
            for arguments_group in arguments_group_set:
                ProcessorHasArguments.objects.create(processor=instance,
                                                     arguments_group=arguments_group,
                                                     argument_position=argument_position)


        instance.save()
        return instance


class ProcessorRelatedField(ModifiedRelatedField):
    serializer = ProcessorSerializer
    model = Processor


class ArgumentsGroupHasProcessorSerializer(serializers.HyperlinkedModelSerializer):
    qset = ArgumentsGroup.objects.all()
    arguments_group = ArgumentsGroupRelatedField(queryset=qset)
    qset = Processor.objects.all()
    processor = ProcessorRelatedField(queryset=qset)

    class Meta:
        model = ArgumentsGroupHasProcessor
        fields = ['id', 'arguments_group', 'processor']


class ArgumentsGroupHasProcessorRelatedField(ModifiedRelatedField):
    serializer = ArgumentsGroupHasProcessorSerializer
    model = ArgumentsGroupHasProcessor


class ArgumentsGroupHasProcessorFullSerializer(serializers.HyperlinkedModelSerializer):
    qset = Processor.objects.all()
    processor = ProcessorRelatedField(queryset=qset)
    qset = Combination.objects.all()
    override_combination = CombinationRelatedField(queryset=qset, many=True)

    class Meta:
        model = ArgumentsGroupHasProcessor
        fields = ['id', 'processor', 'override_combination']


class ArgumentsGroupHasProcessorFullRelatedField(ModifiedRelatedField):
    serializer = ArgumentsGroupHasProcessorFullSerializer
    model = ArgumentsGroupHasProcessor


class ArgumentsGroupFullSerializer(ArgumentsGroupSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:fullargumentsgroup-detail',
                                                   read_only=True)
    qset = ArgumentsGroupHasProcessor.objects.all() #order_by('processori18n__name')
    processor = ArgumentsGroupHasProcessorFullRelatedField(queryset=qset, many=True, source='argumentgroup_processors')
    qset = SpecificParameter.objects.all()
    specific_parameter = SpecificParameterRelatedField(queryset=qset, many=True)

    class Meta:
        model = ArgumentsGroup
        fields = ['id', 'dataurl', 'name', 'description', 'argument_type', 'processor', 'specific_parameter']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Processor
        self.fields['processor'].label = _('Processor')
        self.fields['processor'].style = {'template': 'metadb/custom_select_multiple.html'}
        self.fields['processor'].data_url = reverse('metadb:processor-list')
        # Specific parameter
        self.fields['specific_parameter'].label = _('Specific parameter')
        self.fields['specific_parameter'].style = {'template': 'metadb/custom_select_multiple.html'}
        self.fields['specific_parameter'].data_url = reverse('metadb:specificparameter-list')


class ArgumentsGroupFullRelatedField(ModifiedRelatedField):
    serializer = ArgumentsGroupFullSerializer
    model = ArgumentsGroup


class ProcessorHasArgumentsFullSerializer(serializers.HyperlinkedModelSerializer):
    qset = ArgumentsGroup.objects.all()
    arguments_group = ArgumentsGroupFullRelatedField(queryset=qset)
    class Meta:
        model = ProcessorHasArguments
        fields = ['id', 'argument_position', 'arguments_group']


class ProcessorHasArgumentsFullRelatedField(ModifiedRelatedField):
    serializer = ProcessorHasArgumentsFullSerializer
    model = ProcessorHasArguments


class ProcessorFullSerializer(ProcessorSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:fullprocessor-detail',
                                                   read_only=True)
    qset = ProcessorHasArguments.objects.order_by('argument_position')
    arguments = ProcessorHasArgumentsFullRelatedField(queryset=qset, many=True, source='processor_arguments')
    qset = Setting.objects.order_by('label')
    settings = SettingFullRelatedField(queryset=qset, many=True)
    qset = TimePeriodType.objects.order_by('timeperiodtypei18n__name')

    class Meta:
        model = Processor
        fields = ['id', 'dataurl', 'is_visible', 'processori18n', 'conveyor',
                  'settings', 'time_period_types', 'arguments_selected_by_user', 'arguments']


class OptionsOverrideSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:optionsoverride-detail',
                                                   read_only=True)

#    qset = ArgumentsGroupHasProcessor.objects.all()
#    arguments_group_has_processor = ArgumentsGroupHasProcessorRelatedField(queryset=qset)
    qset = ArgumentsGroup.objects.filter(argument_type__label='processor')
    arguments_group = ArgumentsGroupRelatedField(queryset=qset, source='arguments_group_has_processor.arguments_group')
    qset = Processor.objects.order_by('processori18n__name')
    processor = ProcessorLightRelatedField(queryset=qset, source='arguments_group_has_processor.processor')
    qset = Combination.objects.order_by('option__label')
    combination = CombinationRelatedField(queryset=qset)

    class Meta:
        model = OptionsOverride
        fields = ['id', 'dataurl', 'arguments_group', 'processor', 'combination']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Arguments group
        self.fields['arguments_group'].label = _('Arguments group')
        self.fields['arguments_group'].style = {'template': 'metadb/custom_select.html'}
        self.fields['arguments_group'].data_url = reverse('metadb:argumentsgroup-list')
        # Processor
        self.fields['processor'].label = _('Processor')
        self.fields['processor'].style = {'template': 'metadb/custom_select.html'}
        self.fields['processor'].data_url = reverse('metadb:processor-list')
        # Combination
        self.fields['combination'].label = _('Overriding combination')
        self.fields['combination'].style = {'template': 'metadb/custom_select.html'}
        self.fields['combination'].data_url = reverse('metadb:combination-list')

    def create(self, validated_data):
        aghp_val = validated_data.pop('arguments_group_has_processor')
        aghp_instance = ArgumentsGroupHasProcessor.objects.create(
            arguments_group=aghp_val['arguments_group'],
            processor=aghp_val['processor'])
        instance = OptionsOverride.objects.create(
            arguments_group_has_processor = aghp_instance,
            **validated_data)
        return instance

    def update(self, instance, validated_data):
        specific_parameters = validated_data.pop('specific_parameter')
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.argument_type = validated_data.get('argument_type', instance.argument_type)
        instance.specific_parameter.set(specific_parameters)
        instance.save()
        return instance


class DataArgumentsGroupSerializer(ArgumentsGroupSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:dataargumentsgroup-detail',
                                                   read_only=True)
    argument_type = ArgumentTypeRelatedField(read_only=True)
    qset = SpecificParameter.objects.all()
    specific_parameter = SpecificParameterRelatedField(queryset=qset, many=True)

    class Meta:
        model = ArgumentsGroup
        fields = ['id', 'dataurl', 'name', 'description', 'argument_type', 'specific_parameter']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Specific parameter
        self.fields['specific_parameter'].label = _('Specific parameter')
        self.fields['specific_parameter'].style = {'template': 'metadb/custom_select_multiple.html'}
        self.fields['specific_parameter'].data_url = reverse('metadb:specificparameter-list')

    def create(self, validated_data):
        specific_parameters = validated_data.pop('specific_parameter')
        validated_data['argument_type_id'] = ArgumentType.objects.filter(label='data').get().id
        instance = ArgumentsGroup.objects.create(**validated_data)
        instance.specific_parameter.set(specific_parameters)
        return instance

    def update(self, instance, validated_data):
        specific_parameters = validated_data.pop('specific_parameter')
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.argument_type = validated_data.get('argument_type', instance.argument_type)
        instance.specific_parameter.set(specific_parameters)
        instance.save()
        return instance


class DataArgumentsGroupRelatedField(ModifiedRelatedField):
    serializer = DataArgumentsGroupSerializer
    model = ArgumentsGroup


class ProcArgumentsGroupSerializer(ArgumentsGroupSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:procargumentsgroup-detail',
                                                   read_only=True)
    argument_type = ArgumentTypeRelatedField(read_only=True)
    qset = ArgumentsGroupHasProcessor.objects.all() #order_by('processori18n__name')
    processor = ArgumentsGroupHasProcessorFullRelatedField(queryset=qset, many=True, source='argumentgroup_processors')

    class Meta:
        model = ArgumentsGroup
        fields = ['id', 'dataurl', 'name', 'description', 'argument_type', 'processor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Processor
        self.fields['processor'].label = _('Processor')
        self.fields['processor'].style = {'template': 'metadb/custom_select_multiple.html'}
        self.fields['processor'].data_url = reverse('metadb:processor-list')


class ProcArgumentsGroupRelatedField(ModifiedRelatedField):
    serializer = ProcArgumentsGroupSerializer
    model = ArgumentsGroup
