from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.renderers import *
from django.utils.translation import gettext_lazy as _

from .models import *
from .serializers import ModifiedRelatedField


class AccumulationModeSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:accumulationmode-detail',
                                                   read_only=True)
    class Meta:
        model = AccumulationMode
        fields = ['id', 'dataurl', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Accumulation mode')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return AccumulationMode.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class AccumulationModeRelatedField(ModifiedRelatedField):
    serializer = AccumulationModeSerializer
    model = AccumulationMode
    data_field = 'name'


class ParameterI18NSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParameterI18N
        fields = ['id', 'name']

    def to_representation(self, instance):
        data = instance.filter(language__code=get_language()).get()
        return super().to_representation(data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Parameter name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}


class ParameterSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:parameter-detail',
                                                   read_only=True)
    qset = AccumulationMode.objects.order_by('name')
    accumulation_mode = AccumulationModeRelatedField(queryset=qset)
    parameteri18n = ParameterI18NSerializer(source='parameteri18n_set', label='')

    class Meta:
        model = Parameter
        fields = ['id', 'dataurl', 'is_visible', 'accumulation_mode', 'parameteri18n']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Is visible
        self.fields['is_visible'].label = _('Visible')
        self.fields['is_visible'].style = {'template': 'metadb/custom_checkbox.html'}
        self.fields['is_visible'].initial = True
        # Accumulation mode
        self.fields['accumulation_mode'].data_url = reverse('metadb:accumulationmode-list')
        self.fields['accumulation_mode'].label = _('Accumulation mode')
        self.fields['accumulation_mode'].style = {'template': 'metadb/custom_select.html'}
        self.fields['accumulation_mode'].allow_blank = True

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        parameteri18n_data = validated_data.pop('parameteri18n_set')
        parameter = Parameter.objects.create(**validated_data)
        for db_lang in Language.objects.all():
            ParameterI18N.objects.create(parameter=parameter,
                                          language=db_lang,
                                          **parameteri18n_data)

        return parameter

    def update(self, instance, validated_data):
        instance.is_visible = validated_data.get('is_visible', instance.is_visible)
        instance.accumulation_mode = validated_data.get('accumulation_mode', instance.accumulation_mode)
        parameteri18n = instance.parameteri18n_set.filter(language__code=get_language()).get()
        parameteri18n.name = validated_data['parameteri18n_set'].get('name', parameteri18n.name)
        parameteri18n.save()
        instance.save()

        return instance


class ParameterRelatedField(ModifiedRelatedField):
    serializer = ParameterSerializer
    model = Parameter


class UnitsI18NSerializer(serializers.ModelSerializer):

    class Meta:
        model = UnitsI18N
        fields = ['id', 'name']

    def to_representation(self, instance):
        data = instance.filter(language__code=get_language()).get()
        return super().to_representation(data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Measurement unit name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}


class UnitsSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:organization-detail',
                                                   read_only=True)
    unitsi18n = UnitsI18NSerializer(source='unitsi18n_set', label='')

    class Meta:
        model = Units
        fields = ['id', 'dataurl', 'unitsi18n']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        unitsi18n_data = validated_data.pop('unitsi18n_set')
        units = Units.objects.create(**validated_data)
        for db_lang in Language.objects.all():
            UnitsI18N.objects.create(units=units,
                                     language=db_lang,
                                     **unitsi18n_data)

        return units

    def update(self, instance, validated_data):
        unitsi18n = instance.unitsi18n_set.filter(language__code=get_language()).get()
        unitsi18n.name = validated_data['unitsi18n_set'].get('name', unitsi18n.name)
        unitsi18n.save()
        instance.save()

        return instance


class UnitsRelatedField(ModifiedRelatedField):
    serializer = UnitsSerializer
    model = Units


class LevelI18NSerializer(serializers.ModelSerializer):

    class Meta:
        model = LevelI18N
        fields = ['id', 'name']

    def to_representation(self, instance):
        data = instance.filter(language__code=get_language()).get()
        return super().to_representation(data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Level name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}


class LevelSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:level-detail',
                                                   read_only=True)
    leveli18n = LevelI18NSerializer(source='leveli18n_set', label='')

    class Meta:
        model = Level
        fields = ['id', 'dataurl', 'label', 'leveli18n']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['label'].label = _('Level label')
        self.fields['label'].style = {'template': 'metadb/custom_input.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        leveli18n_data = validated_data.pop('leveli18n_set')
        level = Level.objects.create(**validated_data)
        for db_lang in Language.objects.all():
            LevelI18N.objects.create(level=level,
                                     language=db_lang,
                                     **leveli18n_data)

        return level

    def update(self, instance, validated_data):
        leveli18n = instance.leveli18n_set.filter(language__code=get_language()).get()
        leveli18n.name = validated_data['leveli18n_set'].get('name', leveli18n.name)
        leveli18n.save()
        instance.label = validated_data.get('label', instance.label)
        instance.save()

        return instance


class LevelRelatedField(ModifiedRelatedField):
    serializer = LevelSerializer
    model = Level


class LevelsGroupSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:levelsgroup-detail',
                                                   read_only=True)
    qset = Units.objects.order_by('unitsi18n__name')
    units = UnitsRelatedField(queryset=qset)
    qset = Level.objects.order_by('leveli18n__name')
    levels = LevelRelatedField(queryset=qset, many=True, source='level')

    class Meta:
        model = LevelsGroup
        fields = ['id', 'dataurl', 'description', 'units', 'levels']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Description
        self.fields['description'].label = _('Description')
        self.fields['description'].style = {'template': 'metadb/custom_input.html'}
        # Units
        self.fields['units'].data_url = reverse('metadb:units-list')
        self.fields['units'].label = _('Measurement units')
        self.fields['units'].style = {'template': 'metadb/custom_select.html'}
        self.fields['units'].allow_blank = True
        # Level
        self.fields['levels'].data_url = reverse('metadb:level-list')
        self.fields['levels'].label = _('Levels')
        self.fields['levels'].style = {'template': 'metadb/custom_select_multiple.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        levelslist = validated_data.pop('level')
        levelsgroup = LevelsGroup.objects.create(**validated_data)
        levelsgroup.level.set(levelslist)
        return levelsgroup

    def update(self, instance, validated_data):
        instance.units = validated_data.get('units', instance.units)
        instance.description = validated_data.get('description', instance.description)
        levelslist = validated_data.get('level', instance.level)
        instance.level.set(levelslist)
        instance.save()

        return instance


class LevelsGroupRelatedField(ModifiedRelatedField):
    serializer = LevelsGroupSerializer
    model = LevelsGroup


class TimeStepI18NSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeStepI18N
        fields = ['id', 'name']

    def to_representation(self, instance):
        data = instance.filter(language__code=get_language()).get()
        return super().to_representation(data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Time step name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}


class TimeStepSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:timestep-detail',
                                                   read_only=True)
    timestepi18n = TimeStepI18NSerializer(source='timestepi18n_set', label='')

    class Meta:
        model = TimeStep
        fields = ['id', 'dataurl', 'label', 'subpath2', 'timestepi18n']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['label'].label = _('Time step label')
        self.fields['label'].style = {'template': 'metadb/custom_input.html'}
        self.fields['subpath2'].label = _('Time step subpath')
        self.fields['subpath2'].style = {'template': 'metadb/custom_input.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        timestepi18n_data = validated_data.pop('timestepi18n_set')
        timestep = TimeStep.objects.create(**validated_data)
        for db_lang in Language.objects.all():
            TimeStepI18N.objects.create(time_step=timestep,
                                        language=db_lang,
                                        **timestepi18n_data)

        return timestep

    def update(self, instance, validated_data):
        timestepi18n = instance.timestepi18n_set.filter(language__code=get_language()).get()
        timestepi18n.name = validated_data['timestepi18n_set'].get('name', timestepi18n.name)
        timestepi18n.save()
        instance.save()

        return instance


class TimeStepRelatedField(ModifiedRelatedField):
    serializer = TimeStepSerializer
    model = TimeStep


class SpecificParameterSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:specificparameter-detail',
                                                   read_only=True)
    qset = Parameter.objects.order_by('parameteri18n__name')
    parameter = ParameterRelatedField(queryset=qset)
    qset = LevelsGroup.objects.all()
    levels_group = LevelsGroupRelatedField(queryset=qset)
    qset = TimeStep.objects.all()
    time_step = TimeStepRelatedField(queryset=qset)

    class Meta:
        model = SpecificParameter
        fields = ['id', 'dataurl', 'parameter', 'time_step', 'levels_group']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Parameter
        self.fields['parameter'].data_url = reverse('metadb:parameter-list')
        self.fields['parameter'].label = _('Meteorological parameter')
        self.fields['parameter'].style = {'template': 'metadb/custom_select.html'}
        self.fields['parameter'].allow_blank = True
        # Levels group
        self.fields['levels_group'].data_url = reverse('metadb:levelsgroup-list')
        self.fields['levels_group'].label = _('Levels group')
        self.fields['levels_group'].style = {'template': 'metadb/custom_select.html'}
        self.fields['levels_group'].allow_blank = True
        # Time step
        self.fields['time_step'].data_url = reverse('metadb:timestep-list')
        self.fields['time_step'].label = _('Time step')
        self.fields['time_step'].style = {'template': 'metadb/custom_select.html'}
        self.fields['time_step'].allow_blank = True


    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return SpecificParameter.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.parameter = validated_data.get('parameter', instance.parameter)
        instance.levels_group = validated_data.get('levels_group', instance.levels_group)
        instance.time_step = validated_data.get('time_step', instance.time_step)
        instance.save()

        return instance

class SpecificParameterRelatedField(ModifiedRelatedField):
    serializer = SpecificParameterSerializer
    model = SpecificParameter
