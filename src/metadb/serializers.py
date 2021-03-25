from collections import OrderedDict

from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.renderers import *
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language

from .models import *


class ModifiedRelatedField(serializers.RelatedField):
    serializer = lambda value, context: None
    model = None
    data_field = None
    # Below code is copied from rest_framework.serializers.RelatedField
    # because we need to override the keys in the return value
    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            # Ensure that field.choices returns something sensible
            # even when accessed with a read-only field.
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([
            (
                # This is the only line that differs
                # from the RelatedField's implementation
                item.pk,
                self.display_value(item)
            )
            for item in queryset
        ])

    def get_serializer(self):
        return self.serializer

    def get_model(self):
        return self.model

    def to_representation(self, value):
        data = self.get_serializer()(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data[self.data_field] if self.data_field else data
        if action == 'update':
            result = result.get('id', None)
        return result

    def to_internal_value(self, data):
        return self.get_model().objects.get(pk=data)


class OrganizationI18NSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationI18N
        fields = ['id', 'name']

    def to_representation(self, instance):
        data = instance.filter(language__code=get_language()).get()
        return super().to_representation(data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Organization name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    organizationi18n = OrganizationI18NSerializer(source='organizationi18n_set', label='')
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:organization-detail',
                                                   read_only=True)
    class Meta:
        model = Organization
        fields = ['id', 'dataurl', 'organizationi18n', 'url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['url'].label = _('Organization URL')
        self.fields['url'].style = {'template': 'metadb/custom_input.html'}


    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        organizationi18n_data = validated_data.pop('organizationi18n_set')
        organization = Organization.objects.create(**validated_data)
        for db_lang in Language.objects.all():
            OrganizationI18N.objects.create(organization=organization,
                                            language=db_lang,
                                            **organizationi18n_data)

        return organization

    def update(self, instance, validated_data):
        instance.url = validated_data.get('url', instance.url)
        organizationi18n = instance.organizationi18n_set.filter(language__code=get_language()).get()
        organizationi18n.name = validated_data['organizationi18n_set'].get('name', organizationi18n.name)
        organizationi18n.save()
        instance.save()

        return instance


class OrganizationRelatedField(ModifiedRelatedField):
    serializer = OrganizationSerializer
    model = Organization


class CollectionI18NSerializer(serializers.ModelSerializer):

    class Meta:
        model = CollectionI18N
        fields = ['id', 'name', 'description']

    def to_representation(self, instance):
        data = instance.filter(language__code=get_language()).get()
        return super().to_representation(data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Collection name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}
        self.fields['description'].label = _('Collection description')
        self.fields['description'].style = {'template': 'metadb/custom_textarea.html', 'rows': 3}


class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    collectioni18n = CollectionI18NSerializer(source='collectioni18n_set', label='')
    qset = Organization.objects.order_by('organizationi18n__name')
    organization = OrganizationRelatedField(queryset=qset)
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:collection-detail',
                                                   read_only=True)
    class Meta:
        model = Collection
        fields = ['id', 'dataurl', 'label', 'url', 'collectioni18n', 'organization']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['label'].label = _('Collection label')
        self.fields['label'].style = {'template': 'metadb/custom_input.html'}
        self.fields['url'].label = _('Collection URL')
        self.fields['url'].style = {'template': 'metadb/custom_input.html'}
        self.fields['organization'].label = _('Organization')
        self.fields['organization'].data_url = reverse('metadb:organization-list')
        self.fields['organization'].style = {'template': 'metadb/custom_select.html'}
        self.fields['organization'].allow_blank = True

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        collectioni18n_data = validated_data.pop('collectioni18n_set')
        collection = Collection.objects.create(**validated_data)
        for db_lang in Language.objects.all():
            CollectionI18N.objects.create(collection=collection,
                                          language=db_lang,
                                          **collectioni18n_data)

        return collection

    def update(self, instance, validated_data):
        instance.label = validated_data.get('label', instance.label)
        instance.url = validated_data.get('url', instance.url)
        collectioni18n = instance.collectioni18n_set.filter(language__code=get_language()).get()
        collectioni18n.name = validated_data['collectioni18n_set'].get('name', collectioni18n.name)
        collectioni18n.description = validated_data['collectioni18n_set'].get('description', collectioni18n.description)
        collectioni18n.save()
        instance.organization = validated_data.get('organization', instance.organization)
        instance.save()

        return instance


class CollectionRelatedField(ModifiedRelatedField):
    serializer = CollectionSerializer
    model = Collection
    data_field = 'label'


class ScenarioSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:scenario-detail',
                                                   read_only=True)
    class Meta:
        model = Scenario
        fields = ['id', 'dataurl', 'name', 'subpath0']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Scenario name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}
        self.fields['subpath0'].label = _('Scenario subpath')
        self.fields['subpath0'].style = {'template': 'metadb/custom_input.html'}


    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return Scenario.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.subpath0 = validated_data.get('subpath0', instance.subpath0)
        instance.save()
        return instance


class ScenarioRelatedField(ModifiedRelatedField):
    serializer = ScenarioSerializer
    model = Scenario


class ResolutionSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:resolution-detail',
                                                   read_only=True)
    class Meta:
        model = Resolution
        fields = ['id', 'dataurl', 'name', 'subpath1']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Resolution name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}
        self.fields['subpath1'].label = _('Resolution subpath')
        self.fields['subpath1'].style = {'template': 'metadb/custom_input.html'}


    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return Resolution.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.subpath1 = validated_data.get('subpath1', instance.subpath1)
        instance.save()
        return instance


class ResolutionRelatedField(ModifiedRelatedField):
    serializer = ResolutionSerializer
    model = Resolution


class DataKindSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:datakind-detail',
                                                   read_only=True)
    class Meta:
        model = DataKind
        fields = ['id', 'dataurl', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Data kind name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}


    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return DataKind.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class DataKindRelatedField(ModifiedRelatedField):
    serializer = DataKindSerializer
    model = DataKind
    data_field = 'name'


class FileTypeSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:filetype-detail',
                                                   read_only=True)
    class Meta:
        model = FileType
        fields = ['id', 'dataurl', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('File type name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}


    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return FileType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class FileTypeRelatedField(ModifiedRelatedField):
    serializer = FileTypeSerializer
    model = FileType
    data_field = 'name'


class DatasetSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:dataset-detail',
                                                   read_only=True)
    qset = Collection.objects.order_by('label')
    collection_label = CollectionRelatedField(queryset=qset, source='collection')
    qset = Scenario.objects.order_by('name')
    scenario = ScenarioRelatedField(queryset=qset)
    qset = Resolution.objects.order_by('name')
    resolution = ResolutionRelatedField(queryset=qset)
    qset = DataKind.objects.order_by('name')
    data_kind_name = DataKindRelatedField(queryset=qset, source='data_kind')
    qset = FileType.objects.order_by('name')
    file_type_name = FileTypeRelatedField(queryset=qset, source='file_type')
    class Meta:
        model = Dataset
        fields = ['id', 'dataurl', 'is_visible', 'collection_label', 'resolution',
                  'scenario', 'data_kind_name', 'file_type_name', 'time_start',
                  'time_end', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Is visible
        self.fields['is_visible'].label = _('Visible')
        self.fields['is_visible'].style = {'template': 'metadb/custom_checkbox.html'}
        self.fields['is_visible'].initial = True
        # Collection label
        self.fields['collection_label'].data_url = reverse('metadb:collection-list')
        self.fields['collection_label'].label = _('Collection label')
        self.fields['collection_label'].style = {'template': 'metadb/custom_select.html'}
        self.fields['collection_label'].allow_blank = True
        # Horizontal resolution
        self.fields['resolution'].data_url = reverse('metadb:resolution-list')
        self.fields['resolution'].label = _('Horizontal resolution')
        self.fields['resolution'].style = {'template': 'metadb/custom_select.html'}
        self.fields['resolution'].allow_blank = True
        # Scenario
        self.fields['scenario'].data_url = reverse('metadb:scenario-list')
        self.fields['scenario'].label = _('Scenario')
        self.fields['scenario'].style = {'template': 'metadb/custom_select.html'}
        self.fields['scenario'].allow_blank = True
        # Data kind
        self.fields['data_kind_name'].data_url = reverse('metadb:datakind-list')
        self.fields['data_kind_name'].label = _('Data kind')
        self.fields['data_kind_name'].style = {'template': 'metadb/custom_select.html'}
        self.fields['data_kind_name'].allow_blank = True
        # File type
        self.fields['file_type_name'].data_url = reverse('metadb:filetype-list')
        self.fields['file_type_name'].label = _('File type')
        self.fields['file_type_name'].style = {'template': 'metadb/custom_select.html'}
        self.fields['file_type_name'].allow_blank = True
        # Time start
        self.fields['time_start'].label = _('Start date')
        self.fields['time_start'].style = {'template': 'metadb/custom_input.html'}
        # Time end
        self.fields['time_end'].label = _('End date')
        self.fields['time_end'].style = {'template': 'metadb/custom_input.html'}
        # Description
        self.fields['description'].label = _('Description')
        self.fields['description'].style = {'template': 'metadb/custom_textarea.html', 'rows': 3}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return Dataset.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.is_visible = validated_data.get('is_visible', instance.is_visible)
        instance.collection = validated_data.get('collection', instance.collection)
        instance.resolution = validated_data.get('resolution', instance.resolution)
        instance.scenario = validated_data.get('scenario', instance.scenario)
        instance.data_kind = validated_data.get('data_kind', instance.data_kind)
        instance.file_type = validated_data.get('file_type', instance.file_type)
        instance.time_start = validated_data.get('time_start', instance.time_start)
        instance.time_end = validated_data.get('time_end', instance.time_end)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        return instance


class DatasetRelatedField(ModifiedRelatedField):
    serializer = DatasetSerializer
    model = Dataset


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


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:language-detail',
                                                   read_only=True)
    class Meta:
        model = Language
        fields = ['id', 'dataurl', 'name', 'code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Name
        self.fields['name'].label = _('Language name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}
        # Code
        self.fields['code'].label = _('Language code')
        self.fields['code'].style = {'template': 'metadb/custom_input.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return Language.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.code = validated_data.get('code', instance.code)
        instance.save()
        return instance


class LanguageRelatedField(ModifiedRelatedField):
    serializer = LanguageSerializer
    model = Language


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
        fields = ['id', 'dataurl', 'name', 'number_of_inputs', 'number_of_outputs']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Name
        self.fields['name'].label = _('Computing module name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}
        # Number of inputs
        self.fields['number_of_inputs'].label = _('Number of inputa')
        self.fields['number_of_inputs'].style = {'template': 'metadb/custom_input.html'}
        # Number of outputs
        self.fields['number_of_outputs'].label = _('Number of outputa')
        self.fields['number_of_outputs'].style = {'template': 'metadb/custom_input.html'}

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

    class Meta:
        model = Combination
        fields = ['id', 'dataurl', 'option', 'option_value']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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

    class Meta:
        model = Combination
        fields = ['id', 'dataurl', 'option', 'option_value', 'condition']

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
        processors = validated_data.pop('processor')
        specific_parameters = validated_data.pop('specific_parameter')
        instance = ArgumentsGroup.objects.create(**validated_data)
        instance.processor.set(processors)
        instance.specific_parameter.set(specific_parameters)
        return instance

    def update(self, instance, validated_data):
        processors = validated_data.pop('processor')
        specific_parameters = validated_data.pop('specific_parameter')
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.argument_type = validated_data.get('argument_type', instance.argument_type)
        instance.processor.set(processors)
        instance.specific_parameter.set(specific_parameters)
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
        fields = ['index', 'combination']

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

    def create(self, validated_data):
        raise ValueError('Not implemented yet')
        parameteri18n_data = validated_data.pop('parameteri18n_set')
        parameter = Parameter.objects.create(**validated_data)
        for db_lang in Language.objects.all():
            ParameterI18N.objects.create(parameter=parameter,
                                          language=db_lang,
                                          **parameteri18n_data)

        return parameter

    def update(self, instance, validated_data):
        raise ValueError('Not implemented yet')
        instance.is_visible = validated_data.get('is_visible', instance.is_visible)
        instance.accumulation_mode = validated_data.get('accumulation_mode', instance.accumulation_mode)
        parameteri18n = instance.parameteri18n_set.filter(language__code=get_language()).get()
        parameteri18n.name = validated_data['parameteri18n_set'].get('name', parameteri18n.name)
        parameteri18n.save()
        instance.save()
        return instance


class ProcessorRelatedField(ModifiedRelatedField):
    serializer = ProcessorSerializer
    model = Processor


class ArgumentsGroupHasProcessorSerializer(serializers.HyperlinkedModelSerializer):
    qset = Processor.objects.all()
    processor = ProcessorRelatedField(queryset=qset)
    qset = Combination.objects.all()
    override_combination = CombinationRelatedField(queryset=qset, many=True)

    class Meta:
        model = ArgumentsGroupHasProcessor
        fields = ['id', 'processor', 'override_combination']


class ArgumentsGroupHasProcessorRelatedField(ModifiedRelatedField):
    serializer = ArgumentsGroupHasProcessorSerializer
    model = ArgumentsGroupHasProcessor


class ArgumentsGroupFullSerializer(ArgumentsGroupSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:fullargumentsgroup-detail',
                                                   read_only=True)
    qset = ArgumentsGroupHasProcessor.objects.all()
    processors = ArgumentsGroupHasProcessorRelatedField(queryset=qset, many=True, source='argumentgroup_processors')
    qset = SpecificParameter.objects.all()
    specific_parameter = SpecificParameterRelatedField(queryset=qset, many=True)

    class Meta:
        model = ArgumentsGroup
        fields = ['id', 'dataurl', 'name', 'description', 'argument_type', 'processors', 'specific_parameter']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Processor
        self.fields['processors'].label = _('Processor')
        self.fields['processors'].style = {'template': 'metadb/custom_select_multiple.html'}
        self.fields['processors'].data_url = reverse('metadb:processor-list')
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
